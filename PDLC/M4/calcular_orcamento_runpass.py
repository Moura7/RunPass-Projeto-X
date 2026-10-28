"""Simulação de sensibilidade; não é orçamento final do esquema DynamoDB."""
import json
from pathlib import Path

prices = json.loads(Path('AWS-PRECOS-SA-EAST-1.json').read_text(encoding='utf-8'))

def rate(service, usage, details=False, **attributes):
    rows = prices[service]['detailRows' if details else 'rows']
    candidates = [r for r in rows if r.get('usage', r.get('attributes', {}).get('usagetype')) == usage and r['begin'] == '0'
                  and all(r.get('attributes', {}).get(k) == v for k, v in attributes.items())]
    if len(candidates) != 1:
        raise ValueError((service, usage, len(candidates)))
    return float(candidates[0]['USD'])

rates = {
    'api': rate('AmazonApiGateway', 'SAE1-ApiGatewayHttpRequest', True),
    'lambda_request': rate('AWSLambda', 'SAE1-Request', True),
    'lambda_duration': rate('AWSLambda', 'SAE1-Lambda-GB-Second'),
    'ddb_read': rate('AmazonDynamoDB', 'SAE1-ReadRequestUnits'),
    'ddb_write': rate('AmazonDynamoDB', 'SAE1-WriteRequestUnits'),
    'ddb_pitr': rate('AmazonDynamoDB', 'SAE1-TimedPITRStorage-ByteHrs'),
    's3_storage': rate('AmazonS3', 'SAE1-TimedStorage-ByteHrs', True),
    's3_get': rate('AmazonS3', 'SAE1-Requests-Tier2', True),
    's3_put': rate('AmazonS3', 'SAE1-Requests-Tier1', True),
    'transfer': rate('AWSDataTransfer', 'SAE1-DataTransfer-Out-Bytes', transferType='AWS Outbound'),
    'sqs': rate('AWSQueueService', 'SAE1-Requests-Tier1'),
    'logs': rate('AmazonCloudWatch', 'SAE1-DataProcessing-Bytes', True),
    'cognito_lite': rate('AmazonCognito', 'SAE1-CognitoLiteMAU', True),
}
# Storage: usar tarifa além da faixa gratuita, sem descontar elegibilidade.
rates['ddb_storage'] = next(float(r['USD']) for r in prices['AmazonDynamoDB']['rows']
                            if r['usage'] == 'SAE1-TimedStorage-ByteHrs' and float(r['USD']) > 0)

scenarios = {
    'DEV': dict(calls=60000, images=20000, storage=2, transfer=5, uploads=500, logs=1, mau=10, ddb_gb=1),
    'Econômico': dict(calls=66000, images=45000, storage=5.5, transfer=8.55, uploads=2500, logs=1, mau=1000, ddb_gb=2),
    'Esperado': dict(calls=594000, images=378000, storage=11, transfer=71.82, uploads=5000, logs=3, mau=1000, ddb_gb=2),
    'Pico': dict(calls=4950000, images=2700000, storage=22, transfer=513, uploads=10000, logs=10, mau=1000, ddb_gb=2),
}
out = {}
lake_assumptions = {'event_bytes': 4096, 'retention_days': 60, 'events_per_write': 1, 'note': 'Upper sensitivity: one audit event per write; review fraction and bytes not measured.'}
for name, s in scenarios.items():
    events = s['calls'] * .2
    # Hipóteses novas: 4 RRUs por chamada HTTP em média; 2,4 WRUs por
    # chamada HTTP após transações/índices. Não medidos, não derivados do esquema.
    rru, wru = s['calls'] * 4, s['calls'] * 2.4
    # Publicador + worker, sem lote, 5% de repetição; 256 MB/100 ms por entrega.
    deliveries = events * 1.05 * 2
    # Imagem: worker 1 GB/1 s, hipótese adicional conservada separadamente.
    invocations = s['calls'] + deliveries + s['uploads']
    duration = s['calls'] * .5 * .3 + deliveries * .25 * .1 + s['uploads']
    cost = {
        'API HTTP': s['calls'] * rates['api'],
        'Lambda HTTP e workers': invocations * rates['lambda_request'] + duration * rates['lambda_duration'],
        'DynamoDB consumo (sensibilidade)': rru * rates['ddb_read'] + wru * rates['ddb_write'],
        'DynamoDB estoque e PITR': s['ddb_gb'] * (rates['ddb_storage'] + rates['ddb_pitr']),
        'S3 estoque e requisições': s['storage'] * rates['s3_storage'] + s['images'] * rates['s3_get'] + s['uploads'] * 2 * rates['s3_put'],
        'Transferência de imagens': s['transfer'] * rates['transfer'],
        'SQS (3 operações/evento e 5% adicional)': events * 3 * 1.05 * rates['sqs'],
        'Logs (ingestão)': s['logs'] * rates['logs'],
        'Cognito Lite bruto (plano não aprovado)': s['mau'] * rates['cognito_lite'],
    }
    audit_events = events
    audit_deliveries = audit_events * 1.05
    lake_gb = audit_events * lake_assumptions['event_bytes'] * 2 / 1e9
    lake_cost = {
        'Lake S3 estoque e PUT': lake_gb * rates['s3_storage'] + audit_deliveries * rates['s3_put'],
        'Lake fila e worker de entrega': audit_deliveries * (3 * rates['sqs'] + rates['lambda_request'] + .25 * .1 * rates['lambda_duration']),
    }
    cost.update(lake_cost)
    out[name] = {'inputs': s, 'lake': {'events_per_month': audit_events, 'steady_state_gb': lake_gb, 'delivery_cost': sum(lake_cost.values())}, 'cost': cost, 'subtotal': sum(cost.values())}

Path('ORCAMENTO-RunPass-simulacao.json').write_text(json.dumps({'rates': rates, 'lake_assumptions': lake_assumptions, 'scenarios': out}, indent=2, ensure_ascii=False), encoding='utf8')
lines = ['# RunPass — Estimativa preliminar de custos', '',
    '**Estado:** simulação de sensibilidade, sem teto aprovado. Preços públicos consultados em 26/10/2026, São Paulo. USD, mês de 30 dias. Não é orçamento final nem benchmark.', '',
    '## Premissas e cobertura', '',
    'Base: documento de premissas de uso. Valores brutos sem gratuidades/créditos. Cognito Lite é hipótese de preço, não plano escolhido. Estoque no fim do período usado como envelope conservador de mês cheio; não confundir com média de crescimento do beta.', '',
    'As RRUs/WRUs abaixo são sensibilidade agregada (4 RRUs e 2,4 WRUs por chamada), NÃO cálculo definitivo do esquema. Tamanho dos itens, índices e acessos ainda precisam de validação; o calculador da skill DynamoDB deve ser aplicado ao modelo completo após essa revisão. Esta simulação não o substitui.', '',
    'Workers: evento em 20% das chamadas; publicador e consumidor sem lotes, 5% de entregas adicionais, 256 MB/100 ms. Validação de foto 1 GB/1 s e duas escritas S3 por upload. São hipóteses novas, não medições. Polling vazio e reconciliador ainda não modelados.', '',
    '## Linhas mensais estimadas', '',
    '| Componente | DEV | PROD econômico | PROD esperado | PROD pico |', '| --- | ---: | ---: | ---: | ---: |']
lines[2:2] = [
    'Atualizado em 27/10/2026 com tarifas coletadas em 26/10/2026, sem nova consulta. Lake incluido como sensibilidade: evento de 4 KB por chamada de escrita (20% das chamadas), objeto individual, retencao de 60 dias, 5% de reenvios, fila e worker adicional de 256 MB/100 ms. Fracao real de avaliacoes e tamanho dos comentarios nao medidos. Estoque de 60 dias em regime cheio, nao crescimento real do beta.',
    'As novas linhas incluem entrega, PUT e estoque. Nao incluem integralmente escrita adicional de outbox/ledger, reconciliacao, limpeza, consultas administrativas, auditoria e versoes; subtotal continua parcial. Nao sao autorizacao de gastos ou custo final do lake.', '']
names = list(out)
for component in out['DEV']['cost']:
    lines.append('| ' + component + ' | ' + ' | '.join(f"US$ {out[n]['cost'][component]:.2f}" for n in names) + ' |')
lines.append('| **Subtotal modelado** | ' + ' | '.join(f"**US$ {out[n]['subtotal']:.2f}**" for n in names) + ' |')
lines += ['', '## DEV + PROD e reserva provisória', '', '| Cenário | Subtotal somado | Com reserva provisória de US$ 25/mês | Com reserva e 30% de contingência |', '| --- | ---: | ---: | ---: |']
for n in names[1:]:
    total = out['DEV']['subtotal'] + out[n]['subtotal']
    lines.append(f'| {n} | US$ {total:.2f} | US$ {total+25:.2f} | US$ {(total+25)*1.3:.2f} |')
lines += ['', 'A reserva de US$ 25 e a contingência de 30% são envelopes propostos para planejamento, não preços oficiais, garantia de suficiência ou orçamento aprovado.', '',
    '## Exclusões e riscos de subestimação', '',
    'Não precificados individualmente: armazenamento/consulta de logs, métricas e alarmes, auditoria, segredos/KMS, DNS/domínio, hospedagem do painel, artefatos, minutos do GitHub Actions, contas das lojas, comunicação por e-mail, restauração, S3 versionado/temporários, tráfego de respostas da API e de outros objetos, testes de carga, impostos e câmbio. A reserva não comprova sua cobertura. Serviços como NAT, WAF ou CDN só entram se adotados e exigem recálculo.', '',
    'PITR não é precificado proporcionalmente a 7/35: usar tarifa de armazenamento correspondente, sem presumir economia linear de retenção. Custos de restauração não incluídos. Unidades de armazenamento/tráfego precisam ser alinhadas às convenções de medição de cada serviço no orçamento final.', '',
    'Não somar os três cenários. Para os 60 dias, não duplicar estoque de imagens; recalcular crescimento e admissão por mês. O cenário de pico representa mês inteiro com uso intenso, não apenas um instante.', '',
    '## Evidência e reprodução', '',
    'Preços filtrados preservados em AWS-PRECOS-SA-EAST-1.json, com URL e data de publicação do catálogo. Script calcular_orcamento_runpass.py gera relatório e JSON. Nenhuma credencial, Cost Explorer, recurso AWS ou cobrança foi acessado/criado.', '',
    'Endpoints: https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/{service}/current/sa-east-1/index.json ; serviços AWSLambda, AmazonApiGateway, AmazonDynamoDB, AmazonS3, AWSQueueService, AmazonCloudWatch, AmazonCognito e AWSDataTransfer.', '',
    'Próximo passo: revisar atributos e acessos, modelar linhas excluídas e comparar com consumo medido em DEV antes de fixar teto ou configurar PROD.']
Path('ORCAMENTO-RunPass-preliminar.md').write_text('\n'.join(lines)+'\n', encoding='utf8')
for n in names:
    print(n, round(out[n]['subtotal'], 2))
