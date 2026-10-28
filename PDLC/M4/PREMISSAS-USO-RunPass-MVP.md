# RunPass — Premissas de uso para dimensionamento e orçamento

**Data:** 26/10/2026. **Estado:** modelo de cálculo para revisão, não previsão garantida nem orçamento aprovado.

## 1. Base confirmada

- AWS São Paulo (`sa-east-1`); DEV e PROD em contas distintas.
- CloudFormation; GitHub Actions, revisão das mudanças e aprovação manual para PROD.
- Beta gratuito, até 1.000 admitidos únicos; 60 dias desde os primeiros 50.
- Cenário esperado: 300 usuários/dia, duas sessões/dia por usuário, 30 imagens/sessão.
- 20 medalhas por usuário como premissa de dimensionamento, não limite funcional.
- Até 1 MB por foto própria otimizada como premissa, não limite do upload original.
- Imagens oficiais podem ser reutilizadas por referência; medalhas registradas não equivalem automaticamente a novos objetos.
- Ativação de produto e usuários com acesso diário são indicadores diferentes.

## 2. Convenções e hipóteses novas

Mês de referência de 30 dias. GB e MB decimais. Cenários representam meses com diferentes intensidades de uso; não somar as três colunas. Econômico e pico são hipóteses técnicas, não decisões anteriores do usuário.

Para comparabilidade, os três cenários dimensionam capacidade de até 1.000 admitidos e 20.000 registros acumulados. Não presumir que todos entram no primeiro dia: isso é uma base conservadora para o mês cheio. Recrutamento real será medido.

## 3. Uso em PROD

| Variável | Econômico | Esperado | Pico / estresse |
| --- | ---: | ---: | ---: |
| Usuários com acesso por dia | 100 | 300 | 1.000 |
| Sessões por usuário/dia | 1 | 2 | 3 |
| Sessões/dia | 100 | 600 | 3.000 |
| Sessões/mês | 3.000 | 18.000 | 90.000 |
| Chamadas de API por sessão — hipótese | 20 | 30 | 50 |
| Chamadas interativas de API/mês | 60.000 | 540.000 | 4.500.000 |
| Imagens exibidas/sessão | 30 | 30 | 30 |
| Exibições de imagem/mês | 90.000 | 540.000 | 2.700.000 |
| Duração de sessão — hipótese | 5 min | 5 min | 5 min |
| Usuários simultâneos no teste — hipótese | 10 | 50 | 200 |
| Patamar de API para teste de pico — hipótese | 5 req/s | 20 req/s | 100 req/s |

Exibições não são necessariamente downloads: cache local reduz transferências. Sessões não são concorrência. Os patamares de teste são alvos independentes de validação, não taxas calculadas do total mensal, nem garantias de capacidade. O cenário de pico supõe uso intenso durante todo um mês para sensibilidade de custos; um pico curto terá outro perfil.

Reservar mais 10% sobre as chamadas interativas para retentativas e navegação auxiliar como hipótese: 66.000, 594.000 e 4.950.000 chamadas/mês. Chamadas administrativas, emissão/finalização de uploads, rotinas programadas e eventos precisam ser contabilizadas separadamente se não estiverem incluídas no fluxo medido, evitando dupla contagem.

## 4. Imagens: armazenamento e tráfego

Hipóteses comuns: imagem otimizada de 1 MB; uma miniatura de 100 KB por foto; 90% das exibições em miniatura e 10% em detalhe. Tamanho médio por exibição antes do cache: 0,9 × 0,1 MB + 0,1 × 1 MB = **0,19 MB**. Isso é cenário de cálculo, não especificação final de formatos.

| Variável | Econômico | Esperado | Pico / estresse |
| --- | ---: | ---: | ---: |
| Fotos próprias distintas acumuladas — hipótese | 5.000 | 10.000 | 20.000 |
| Imagens otimizadas acumuladas | 5 GB | 10 GB | 20 GB |
| Miniaturas acumuladas | 0,5 GB | 1 GB | 2 GB |
| Total acumulado base no S3 | 5,5 GB | 11 GB | 22 GB |
| Tráfego sem cache | 17,1 GB/mês | 102,6 GB/mês | 513 GB/mês |
| Acerto de cache local — hipótese | 50% | 30% | 0% |
| Downloads efetivos estimados | 45.000 | 378.000 | 2.700.000 |
| Tráfego após cache local | 8,55 GB/mês | 71,82 GB/mês | 513 GB/mês |

Cache local evita download. Cache em CDN apenas muda a origem da entrega; não elimina o tráfego até o usuário. CDN ainda não aprovada, portanto não embutir sua economia ou custo nesta base.

Somar à base S3: imagens oficiais do catálogo, fotos de perfil, cards se persistidos, arquivos temporários, versões não correntes e demais objetos. Exemplo de sensibilidade, não quantidade aprovada: 500 imagens oficiais × 1,1 MB = 0,55 GB adicionais.

O modelo não retém uploads originais indefinidamente. Definir limite de entrada e prazo de limpeza dos temporários antes de implementar; se originais forem mantidos, acrescentar seu volume explicitamente. Uma foto pode ser enviada por usuário e ainda falhar na validação: considerar retentativas e uploads abandonados.

Os valores são estoque acumulado ao fim do período, não novos uploads mensais obrigatórios nem média faturável de armazenamento. Para cada mês, calcular estoque inicial + crescimento e usar média temporal apropriada. Os 20.000 registros não devem ser multiplicados por dois só porque o beta dura 60 dias.

## 5. API e Lambda

Hipótese inicial para a função HTTP: 512 MB de memória e 300 ms de duração média faturável. Não é benchmark. As chamadas com validação de imagem devem usar perfil próprio.

| Indicador | Econômico | Esperado | Pico / estresse |
| --- | ---: | ---: | ---: |
| Invocações HTTP com reserva de 10% | 66.000 | 594.000 | 4.950.000 |
| GB-segundo HTTP (invocações × 0,5 GB × 0,3 s) | 9.900 | 89.100 | 742.500 |

Orçar workers e publicador separadamente, por invocações, lotes, memória e duração. Definir arquitetura de CPU e versão do runtime na implementação, sem inferir preço unitário. Limitar concorrência e monitorar throttling, mas não usar limites como substituto para orçamento.

## 6. DynamoDB

Capacidade sob demanda aprovada pelo usuário como modo inicial do DynamoDB. Estimar os custos nesse modo e acompanhar consumo antes de avaliar capacidade provisionada. Não converter uma chamada HTTP diretamente em uma unidade faturável.

Para obter uma primeira faixa de operações lógicas, supor 80% das chamadas interativas de leitura e 20% de escrita, com cinco itens lidos por chamada de leitura e três itens escritos por chamada de escrita:

| Operações lógicas antes de índices/transações | Econômico | Esperado | Pico / estresse |
| --- | ---: | ---: | ---: |
| Itens lidos/mês, sobre API com reserva | 264.000 | 2.376.000 | 19.800.000 |
| Itens escritos/mês, sobre API com reserva | 39.600 | 356.400 | 2.970.000 |

Esses números não são RRUs/WRUs. Calcular tamanho dos itens, consistência, leituras por página, escritas transacionais, atualizações de índices, projeções e tentativas adicionais. Feed com consultas por autor pode multiplicar operações; medir o plano de acesso antes de usar essa aproximação como orçamento final.

Para primeira sensibilidade de armazenamento, reservar **1 GB em DEV e 2 GB em PROD**, como envelope provisório, não medição. Substituir por inventário de itens e índices incluindo comentários, eventos, auditoria, avisos e outbox. Imagens ficam fora desse cálculo. Backups e recuperação têm linhas próprias.

## 7. Eventos e imagens em segundo plano

Hipótese de estoque: fotos próprias são enviadas uniformemente em 60 dias, gerando aproximadamente 2.500 / 5.000 / 10.000 uploads por mês. Caso haja carga inicial concentrada, simular o pico de ingestão separadamente.

Para efeitos assíncronos de negócio, hipótese de um evento por comando HTTP de escrita: aproximadamente 13.200 / 118.800 / 990.000 eventos por mês, antes de ajuste pelo mapeamento de eventos real. Nem toda escrita precisa de evento; essa aproximação não altera o domínio.

Publicador, SQS e workers devem considerar lotes, tamanho de mensagens, requisições de envio/recebimento/exclusão, polling e reprocessamento. Reservar 5% de entregas adicionais para sensibilidade, sem interpretar isso como taxa aceitável de erro. Não multiplicar eventos por usuários ou serviços sem consumidores definidos. Contabilizar validação de imagens uma única vez se já estiver incluída na contagem de eventos.

## 8. DEV e operação

| Item DEV | Hipótese de referência |
| --- | --- |
| Usuários de teste | Até 10, com dados sintéticos |
| API | 60.000 chamadas/mês |
| Lambda HTTP | 512 MB, 300 ms; 9.000 GB-segundo/mês |
| Objetos no S3 | 2 GB acumulados |
| Saída de imagens | 5 GB/mês |
| DynamoDB | Envelope de 1 GB; leituras/escritas medidas nos testes |
| Deploys | 20/mês em DEV e 4/mês em PROD, hipótese |
| Dados de PROD | Não copiar para DEV por padrão |

Testes de carga são adicionais, com duração e requisições explícitas; não incluí-los como tráfego permanente. Dev e Prod não têm necessariamente o mesmo consumo, apesar de usar templates equivalentes.

Hipóteses de logs para orçamento: 1 GB/mês em DEV e, em PROD, 1 / 3 / 10 GB/mês por cenário. Retenção proposta: sete dias em DEV e 30 em PROD, ainda não política aprovada. Dimensionar separadamente eventos de auditoria e segurança, consultas de logs, métricas customizadas e alarmes. Não registrar imagens, tokens ou dados pessoais desnecessários.

Cognito: estimar 10 usuários mensais autenticados em DEV e até 1.000 em PROD para todos os cenários. Usuários autenticados no mês, admitidos e ativados são contagens distintas; repetição diária não multiplica usuários únicos mensais. MFA, e-mail/SMS e plano contratado exigem decisão e preço próprios.

## 9. O que incluir na futura estimativa monetária

- API Gateway, Lambda HTTP e workers; DynamoDB dados/índices/leitura/escrita e backups.
- S3 armazenamento, requisições, transferência e temporários/versões.
- Cognito conforme plano e usuários mensais, eventuais custos de comunicação.
- SQS, mensageria e recuperação de falhas; CloudWatch, métricas e auditoria.
- Segredos e chaves gerenciadas, se usados; nomes e quantidade reais.
- Artefatos de implantação, GitHub Actions conforme plano/minutos, domínio e DNS se utilizados.
- Tributos, câmbio e contingência apresentados separadamente. Não descontar créditos ou gratuidades sem verificar elegibilidade.

Não incluir NAT Gateway, balanceador ou banco relacional sem que a arquitetura os adote. Não pressupor que recursos serverless eliminam custos de armazenamento, tráfego e observabilidade.

## 10. Pendências sem nova entrevista obrigatória

Validar estas hipóteses por medições e revisão: distribuição real das ações, tamanho dos itens, índices, algoritmo do feed, perfil de processamento, retenção, versões, cache e proporção de uploads próprios. Usar variações explícitas na estimativa até haver dados, sem apresentar hipóteses como aprovações do usuário.

Próxima entrega: orçamento mensal por serviço/ambiente/cenário com preços oficiais em São Paulo e memória de cálculo. Separar mês de entrada, mês estabilizado e total dos 60 dias, preservando a diferença entre estoque acumulado e consumo mensal. Este documento não estabelece teto nem autoriza provisionamento.
