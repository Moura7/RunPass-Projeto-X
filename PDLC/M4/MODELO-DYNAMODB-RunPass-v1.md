# RunPass — Modelo DynamoDB v1

**Estado:** proposta física parcial para revisão, não infraestrutura implantada. Complementa a matriz A01–A14 do fechamento técnico. Não há quantidade final de tabelas aprovada.

## Critério de agrupamento

Imagem da medalha: o usuário confirmou preservação da versão oficial vinculada no cadastro. Item Medalha deve guardar referência imutável/versionada e origem, sem resolver sempre o ponteiro atual do catálogo. Novas vinculações usam a versão vigente; alterações retroativas são ações administrativas explícitas e auditadas, não migração automática. Preservar objetos referenciados independentemente da janela de eventos de avaliação.

Single-table considera dados relacionados que são lidos/escritos juntos. Participação, avaliação e medalha têm recuperação conjunta, sem TTL, capacidade sob demanda e acesso técnico/criptografia comuns, confirmados nas perguntas 36–39. São o primeiro agrupamento físico proposto.

Não inventar requisitos operacionais de perfil, catálogo, social e eventos para fixar suas tabelas. A configuração desses grupos ainda deve ser confirmada. A proposta ampla de Core com todos os domínios não está aprovada.

## Tabela candidata: RunHistory por ambiente

Chaves candidatas: `ownerKey` (partição), `recordKey` (ordenação). Nomes físicos e prefixes são proposta de implementação. DEV/PROD têm contas e tabelas distintas.

| Tipo | ownerKey | recordKey | Dados principais |
| --- | --- | --- | --- |
| Participação concluída | USER#userId | EDITION#editionId#PARTICIPATION | participationId, editionId, distance, result opcional, version, state, visibilidade, completedAt |
| Avaliação | USER#userId | EDITION#editionId#REVIEW | oito notas, comentário opcional, moderationState, reviewVersion |
| Medalha | USER#userId | EDITION#editionId#MEDAL | imageReference, imageOwner, validatedImageVersion |
| Rascunho sem edição | USER#userId | DRAFT#draftId | solicitação, dados parciais, estado/version |

As três chaves por usuário/edição dão identidade determinística. Conclusão cria o conjunto em transação com condições anti-duplicidade e validações de versão. Rascunho é removido/convertido na mesma operação quando couber. Reenvio usa chave de idempotência; não gerar novos itens após resposta perdida.

**Índices candidatos, sujeitos a prova:**

| Índice | Partição | Ordenação | Projeção | Padrão |
| --- | --- | --- | --- | --- |
| UserHistoryByCompletion | USER#userId | completedAt#participationId | IDs e campos mínimos para hidratação | A03: histórico em recência |
| ReviewsByEdition | EDITION#editionId | createdAt#reviewId | chaves, distância e resumo público mínimo | A06: avaliações da edição |
| ReviewsByEditionDistance | EDITION#editionId#DISTANCE#distanceId | createdAt#reviewId | chaves e resumo público mínimo | A06: filtro por distância |

Índices esparsos: atributos de índice apenas nos tipos elegíveis. Estado de exclusão/moderação atual é revalidado na fonte antes da resposta. Não projetar nascimento ou resultado privado. Decidir INCLUDE versus KEYS_ONLY com medição do custo de hidratação. Atributos e projeções dos GSIs não estão aprovados nem criados.

## Plano por padrão já coberto

| Padrão | Operação e condição | Consistência/custo |
| --- | --- | --- |
| A03 histórico | Query no UserHistoryByCompletion por usuário, ordem reversa; BatchGet dos itens fonte | Índice eventual; validar fonte e bloqueios. Custo depende das páginas e do tamanho real. |
| A06 reviews | Query em ReviewsByEdition ou ReviewsByEditionDistance com partição exata e cursor | Não varrer outras edições; validar moderação na fonte. |
| A07 conclusão | TransactWriteItems cria participação/review/medalha e evento, verificando fonte de edição e imagem | Escrita transacional, limites conferidos antes de implementar. S3 não participa da transação. |
| A07 edição | GetItem fonte + versão; TransactWriteItems com condição de versão e existência | Evita sobrescrita e criação acidental por UpdateItem. |
| A08 exclusão | Atualização condicional do estado + evento; limpeza paginada após bloqueio de leitura | Imediato na fonte; físico assíncrono. |
| A14 apagar conta | Bloqueio global do usuário; Query por ownerKey e limpeza paginada | Não depender de scan; respeitar política de retenção. |

Sem custo por operação definitivo: tamanhos dos itens e payloads precisam de revisão. RPS por padrão ainda não foi medido. Não converter uma página em uma única unidade faturável.

## Atributos e tamanhos — hipóteses visíveis, não aprovadas

| Entidade | Atributos | Tipo | Bytes propostos | Origem |
| --- | --- | --- | ---: | --- |
| Participação | Duas chaves | Strings | 160 | Estimativa, corrigível |
| Participação | IDs de usuário/edição/participação/distância | Strings | 160 | Estimativa |
| Participação | Estado, visibilidade e versão | Strings/números/booleanos | 100 | Estimativa |
| Participação | Resultado, timestamps e atributos dos índices | Mistos | 400 | Estimativa |
| Avaliação | Chaves/IDs/versão/estado/datas/índices | Mistos | 750 | Estimativa |
| Avaliação | Oito notas | Números e nomes | 160 | Estimativa |
| Avaliação | Comentário | String UTF-8 | Desconhecido | Limite e distribuição ainda não definidos |
| Medalha | Chaves e IDs | Strings | 300 | Estimativa |
| Medalha | Referência/versão da imagem e datas | Strings/números | 300 | Estimativa |

Somar nomes de atributos e estruturas reais ao medir; não usar estes envelopes como tamanho confirmado para precificar. Fotos são objetos S3 e não bytes do item DynamoDB.

## Configuração operacional

- Capacidade sob demanda. Sem replicas globais propostas para o MVP.
- PITR com janela de 7 dias para o beta, mecanismo a validar com recuperação RPO/RTO e região. Recuperação retorna tabela nova; promoção e reconciliação precisam de runbook. Não equivale a restauração seletiva nativa de um agregado.
- Itens do histórico sem atributo de expiração. TTL de outros tipos não pode remover histórico por engano.
- Criptografia e papéis comuns no agregado; chave concreta pendente. Mobile não recebe acesso direto à tabela.
- Eventos de domínio garantidos por outbox na transação. Co-localizar o item outbox na mesma tabela ou gravá-lo em outra na mesma transação continua hipótese condicionada à recuperação/retenção da outbox. Não finalizar a topologia antes dessa decisão.

## Demais padrões — desenho a concluir, sem prometer eficiência

| Domínio | Estratégia candidata | O que falta provar |
| --- | --- | --- |
| Perfil e username | Item por usuário + reserva condicional por username | Recuperação e dados privados, limites da busca de conhecidos |
| Catálogo | Entradas por cidade/período/distância e título normalizado | Prefixo e data usam ordenações diferentes; matriz de combinações e índices |
| Feed | Projeção por leitor ou consultas por autores com merge | Amplificação de escrita, número de seguidos e cursor entre grupos |
| Social | Relações direcionadas de follow/block e vínculo por post | Enumerar dados por usuário para exclusão e verificar bloqueio bilateral |
| Beta | Registro de admissão e contador transacional | Concorrência do 50º e 1.000º, identidade única e lista de espera |
| Outbox e controles | Itens duráveis por evento e fila de pendências consultável | Retenção, recuperação, índices de pendências e replay |

## Desvios e validação

Modelo parcial deliberado: não fixa tabelas dos agregados sem requisitos operacionais. Não executa calculador DynamoDB como estimativa final de um esquema ainda não aprovado. Não há benchmark, deploy ou custo pago autorizado nesta etapa.

Antes de executar: revisar atributos e tamanho do comentário; fechar configurações dos demais agregados; testar duplicidade, mudança de edição, exclusão, índices atrasados e concentração de reviews em uma mesma edição. Publicador/workers precisam de filtro de outbox, limite de retentativas, destino de falha e recuperação durável para interrupções além da retenção do stream.

## Política de replay aprovada para o beta

O usuário aprovou reprocessar eventos concluídos por até sete dias, alinhados à janela de recuperação; preservar a recuperabilidade dos eventos pendentes até resolução, respeitando retenção/exclusão pessoal; reconstruir feed e RunScore mais antigos a partir dos dados operacionais vigentes; e restringir reprocessamento à operação interna controlada pela equipe RunPass. Não conservar eventos indefinidamente para reconstrução. Replay não recria conteúdo excluído nem renova retenção. O marco técnico proposto é a última confirmação dos destinos obrigatórios, coerente com o payload entregue; detalhar no contrato operacional.

EVENTOS-E-REPLAY-RunPass-MVP.md distingue a política aprovada dos mecanismos propostos. Ledger/deduplicação, margem para mensagens em trânsito, versões dos agregados, autorização operacional e reconstrução concorrente ainda serão projetados e validados. Não fixar automaticamente TTL de sete dias para todos os controles. A política não conclui o esquema físico DynamoDB nem aprova a SPEC integral; não houve implantação ou testes.

## Aprovação prioritária e SPEC única

O usuário aprovou DynamoDB on-demand com agrupamento relacionado, outbox transacional/SQS e consumidores versionados/idempotentes, Cognito separado para corredores/operadores com MFA por aplicativo autenticador e autorização por função. Autorizado detalhamento e desenvolvimento incremental do fluxo autenticação → catálogo → rascunho → imagem → conclusão → avaliação e medalha. Referência única: SPEC_RunPass_MVP_v1.md, que recebeu o conteúdo consolidado; Não é mantida uma segunda SPEC ativa. Registro técnico anterior preservado em PDLC/M4/historico, sem vigência. Não exigir aprovação isolada de cada atributo nem nova rodada P01–P09; dependências técnicas devem ser fechadas antes da parte afetada. Não autoriza custo, deploy ou beta sem requisitos/evidências próprios.
