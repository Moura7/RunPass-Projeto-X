# S09 — Integração DEV e aceite da primeira entrega

Data: 01/11/2026. Estado: **preparação local**. Nenhum recurso foi provisionado.

## Gate de entrada

| Pré-condição | Estado | Evidência necessária antes do deploy |
| --- | --- | --- |
| S02–S08 disponíveis | Parcial | S02–S04, S06–S07 em revisão; S05 e S08 ainda têm pendências de dispositivo/objetos/mobile |
| Orçamento completo e teto autorizado | Bloqueado | orçamento atual é simulação parcial, sem teto; incluir itens excluídos e preços vigentes |
| Conta AWS DEV isolada | Não registrada | ID da conta, região `sa-east-1`, responsável e substituto |
| GitHub OIDC | Não configurado | organização/repositório/branch protegida e role DEV de privilégio mínimo |
| Alertas operacionais | Não configurado | tópico, destinatário fora do Git e teste de recebimento/escalonamento |
| Autorização de provisionamento | Não concedida | aprovação explícita após orçamento e revisão do change set |

Enquanto qualquer item obrigatório estiver bloqueado, comandos de criação de stack, upload de artefato ou deploy não devem ser executados.

## Infraestrutura candidata preparada

`infra/identity.template.json` mantém Cognito separado para corredores e operadores, com TOTP obrigatório para operadores. `infra/data.template.yaml` acrescenta:

- seis tabelas DynamoDB on-demand com chaves `PK/SK`, criptografia e proteção de deleção em PROD;
- PITR nos dados ativos e ausência deliberada de PITR no ErasureControl;
- buckets privados/versionados separados para medalhas e auditoria;
- lifecycle complementar para temporários e auditoria, sem substituir remoção ativa;
- duas filas standard e respectivas DLQs, retenção de um dia, visibility de 60 segundos e redrive após cinco recepções;
- tópico de alertas e alarmes para mensagens visíveis nas DLQs.

`make infra-check` valida ambos os templates em `sa-east-1`. Os templates não contêm nomes globais fixos, destinatários, IDs de conta, credenciais ou dados reais.

## Ainda necessário antes da integração

1. Empacotar FastAPI/workers para Lambda e declarar API Gateway, funções, logs e IAM mínimo por finalidade.
2. Declarar policies dos buckets/filas e separar acesso de fotos, auditoria, limpeza e recuperação.
3. Fechar estratégia de segredos/chaves, assinatura de artefatos e OIDC sem chaves permanentes.
4. Gerar change set somente leitura, estimativa atualizada e revisão humana; aplicar apenas após autorização.
5. Executar jornada em DEV: autenticação → catálogo → rascunho → imagem → conclusão → avaliação/medalha → edição/exclusão.
6. Medir imagem em cinco segundos e RunScore em dez segundos; executar carga, DLQ/replay, alarmes, permissões negativas e exclusões.
7. Ensaiar restore com tráfego fechado, incremento de `dispatchEpoch` e reaplicação dos controles de exclusão antes da promoção.
8. Executar Android e iPhone reais. Simulador e adaptadores locais não contam como evidência dos serviços AWS.

## Evidências a capturar

Registrar IDs de execução e timestamps, não tokens ou payloads pessoais: change set revisado, versão do artefato, outputs das stacks, testes por serviço, métricas p50/p95/p99, mensagens DLQ/replay, recebimento de alarme, relatório de restore, limpeza e custo observado. Diferenciar claramente falha, não executado e aprovado.

S09 não autoriza PROD, beta ou lojas. Promoção exige aprovação própria e usa os mesmos artefatos validados em DEV.
