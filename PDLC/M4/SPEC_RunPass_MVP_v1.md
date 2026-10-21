# SPEC — RunPass MVP — v1

**Estado:** DRAFT técnico para revisão. Produto: PRD v2 aprovado pelo usuário. Esta SPEC não tem aprovação técnica nem autoriza implantação.

## Problem Statement

Corredores precisam organizar experiências em provas, medalhas e avaliações e trocar essas informações com outros corredores. O beta validará adesão, repetição do registro, interação, disponibilidade e percepção de valor.

## Solution

Aplicativo Android/iPhone com catálogo por edição, conclusão autodeclarada, avaliação obrigatória, medalheiro, wishlist e feed de conquistas. Equipe RunPass opera um painel interno para catálogo e moderação. Sem site público para corredores.

## User Stories

1. Como convidado, quero ingressar no beta, para experimentar o produto dentro do limite aprovado.
2. Como corredor, quero cadastrar e validar meu e-mail e recuperar minha senha, para acessar minha conta.
3. Como corredor, quero escolher nome e username, para ser encontrado por conhecidos.
4. Como corredor, quero incluir foto, cidade e bio opcionalmente, para personalizar meu perfil.
5. Como corredor, quero buscar edições por nome, cidade, data e distância, para encontrar minhas corridas.
6. Como corredor, quero consultar dados e avaliações de uma edição, para conhecer a experiência de outros.
7. Como corredor, quero filtrar reviews por distância, para consultar experiências relevantes.
8. Como corredor, quero declarar que concluí uma edição, para registrar minha conquista sem comprovante obrigatório.
9. Como corredor, quero informar resultado opcional, para manter meu histórico esportivo.
10. Como corredor, quero preencher os oito critérios, para avaliar a experiência.
11. Como corredor, quero comentar opcionalmente a avaliação, para contextualizar as notas.
12. Como corredor, quero receber a medalha com imagem oficial, para organizar minha coleção.
13. Como corredor, quero enviar foto quando faltar imagem da medalha, para concluir o cadastro.
14. Como corredor, quero salvar rascunho de uma prova ausente, para não perder os dados.
15. Como corredor, quero solicitar uma edição informando nome, data, cidade e distância, para registrá-la após revisão.
16. Como corredor, quero consultar a decisão e corrigir uma solicitação recusada, para reenviá-la.
17. Como corredor, quero revisar a vinculação a uma edição existente, para concluir o registro correto.
18. Como corredor, quero editar meus dados e notas, para corrigir erros sem duplicar a participação.
19. Como corredor, quero excluir minha participação, para remover seus vínculos e publicação.
20. Como corredor, quero ocultar tempo e colocação por participação, para controlar sua exposição.
21. Como corredor, quero ocultar uma publicação antes ou depois de concluí-la, para controlar o feed.
22. Como corredor, quero salvar edições futuras e ocultar minha wishlist, para organizar meus interesses.
23. Como corredor, quero buscar e seguir conhecidos, para priorizar suas conquistas no feed.
24. Como corredor, quero ver publicações de outras pessoas, para descobrir experiências além dos meus contatos.
25. Como corredor, quero curtir e comentar conquistas, para interagir com outros participantes.
26. Como corredor, quero compartilhar cards e links, para divulgar minhas conquistas.
27. Como corredor, quero receber avisos dentro do aplicativo, para acompanhar revisões e interações.
28. Como corredor, quero denunciar e bloquear usuários, para controlar interações indesejadas.
29. Como corredor, quero corrigir uma avaliação invalidada, para submetê-la novamente à revisão.
30. Como corredor, quero excluir minha conta e solicitar exclusão de dados, para encerrar meu uso.
31. Como administrador, quero aprovar, recusar e vincular solicitações duplicadas, para manter o catálogo consistente.
32. Como administrador, quero manter edições, distâncias e imagens de medalhas, para apoiar os registros.
33. Como administrador, quero arquivar edições com participações, para preservar o histórico.
34. Como moderador, quero ocultar comentários, invalidar notas e suspender contas com motivo, para executar a política de conteúdo.
35. Como operador, quero limitar o beta a 1.000 admitidos e acompanhar os 60 dias desde os primeiros 50, para respeitar o experimento.
36. Como operador, quero medir ativação sobre admitidos reais, repetição e interação sobre ativados, para avaliar as metas.
37. Como operador, quero medir falhas e disponibilidade, para identificar impedimentos ao uso.
38. Como participante, quero enviar feedback voluntário, para relatar problemas e sugestões.
39. Como equipe RunPass, quero consolidar feedbacks semanalmente, para priorizar correções.

## Implementation Decisions

### Estado das escolhas

| Item | Situação |
| --- | --- |
| Python | Confirmado pelo usuário apenas no backend. Não há exigência de Python na interface mobile. |
| AWS | Direção inicial solicitada; arquitetura detalhada ainda proposta. |
| Aplicativo | Flutter/Dart aprovado pelo usuário para Android e iPhone. |
| IDE | VS Code como proposta, sem vincular a arquitetura a uma IDE. Build iOS exige ambiente macOS/Xcode. |
| Dados | DynamoDB considerado como banco operacional principal por solicitação do usuário; modelagem e dimensionamento ainda sujeitos à revisão técnica. |
| Arquitetura desenhada | API Gateway, Lambda modular, Cognito, DynamoDB, S3 e processamento assíncrono; proposta de referência, sem aprovação técnica integral. |

**Definições confirmadas:** Python apenas no backend e Flutter/Dart no aplicativo Android/iPhone. As demais escolhas de arquitetura permanecem propostas até revisão específica.

### Arquitetura proposta, não aprovada

- Backend Python em monólito modular, evitando microsserviços no MVP.
- API HTTP com contrato OpenAPI e validação de entrada. Framework Python ainda em revisão; FastAPI é candidato. Django/Fargate foi alternativa anterior, não escolha aprovada. Com DynamoDB, não presumir integração direta com Django ORM/Admin.
- Arquitetura desenhada mais recente: API Gateway como entrada HTTPS/JWT e backend Python modular em Lambda. Validar latência, concorrência, limites e custos antes da aprovação. Módulos de negócio não implicam microsserviços independentes.
- Amazon Cognito como proposta de identidade; autorização de proprietário, bloqueios, suspensão e papel administrativo permanece no domínio, além de validar token.
- DynamoDB como fonte operacional principal nesta proposta, substituindo a referência inicial a PostgreSQL. Não incluir Aurora/PostgreSQL simultaneamente sem justificativa e revisão explícita.
- S3 privado para imagens; acesso temporário autorizado e sem exposição direta indiscriminada dos objetos. CloudWatch como proposta de logs/métricas, gestão de segredos e permissões mínimas por serviço.
- Painel interno consumindo as mesmas regras de domínio. Framework e hospedagem dependem da escolha de backend; acesso administrativo segregado e auditado.
- Sem valor de custo estimado aprovado: região, carga, armazenamento, conexões, alta disponibilidade e orçamento precisam ser definidos antes de provisionar.

### Armazenamento DynamoDB e padrões de acesso

- Modelar chaves, índices e projeções a partir das consultas aprovadas, antes da implementação. Número de tabelas, chaves e índices ainda não foi decidido; não presumir single-table obrigatório.
- Mapear pelo menos: perfil por username; histórico/medalhas por usuário; catálogo por cidade/data/distância/nome; avaliações por edição e distância; feed público e de seguidos; wishlist; avisos; solicitações e denúncias por estado.
- Consultas críticas não devem depender de varreduras globais como estratégia principal. Busca combinada do catálogo e ordenação do feed precisam de prova técnica, estimativa de leitura/escrita e paginação.
- Usar identidade determinística e escrita condicional para participação única por usuário/edição, curtidas únicas e reserva de username. Verificar unicidade no armazenamento principal, não por consulta prévia a índice eventualmente consistente.
- Concluir participação, avaliação, medalha e registro de evento/outbox em transação, respeitando limites do DynamoDB. Imagens continuam no S3; sua validação antecede a conclusão e não faz parte da transação do banco.
- Índices globais podem ter atraso de atualização. Definir onde leitura fortemente consistente é necessária e revalidar permissões/visibilidade na fonte antes de expor dados sensíveis, mesmo se a projeção do feed estiver atrasada.
- RunScore exige atualização idempotente de soma/contagem ou projeção reconstruível; tratar edição, exclusão e invalidação sem duplicar contribuições. Escolha entre consistência imediata e atualização assíncrona do agregado permanece em revisão.
- Avaliar distribuição de chaves, concentração de acesso em provas populares e índices de feed; capacidade automática não elimina hot keys nem modelagem inadequada.
- Prever exportação/reprocessamento para analytics, recuperação e evolução de projeções, sem usar varreduras de produção para cada relatório.

### Eventos, imagens e evolução

- Fluxo proposto: transação grava evento de domínio na outbox; DynamoDB Streams aciona Lambda publicadora; esta encaminha eventos para SQS; workers Python/Lambda executam efeitos secundários. Filtrar registros de outbox para evitar que toda alteração seja tratada como evento de negócio ou gere ciclos.
- Retentativas podem duplicar entregas: identificador de evento e consumidores idempotentes são necessários. Configurar fila de erro, alarmes, reprocessamento e tratamento de falhas no publicador e nos workers.
- Avaliar prazo de retenção dos streams e estratégia de reconciliação da outbox para indisponibilidade prolongada; não depender apenas de retentativa indefinida.
- Tarefas assíncronas candidatas: processamento/validação de imagens, avisos internos e projeções analíticas. Não tornar assíncrona uma validação necessária para concluir a participação sem definir estado intermediário.
- Upload autorizado do aplicativo para S3 privado, com confirmação/validação pelo backend e acesso temporário à imagem. URLs previamente emitidas não são revogadas automaticamente por ocultar o post; definir expiração e comportamento de cache coerentes com privacidade.
- Evolução prevista, fora do MVP: EventBridge para múltiplos consumidores, OpenSearch para busca avançada, analytics separado e integrações externas. São possibilidades, não serviços já aprovados para provisionamento.
- Serviços podem ser extraídos quando carga, disponibilidade ou organização da equipe justificarem. Manter fronteiras entre módulos e contratos de eventos para reduzir acoplamento; extração futura não será automática.

### Diagrama da proposta

O diagrama RunPass-Arquitetura-MVP-DynamoDB-v1.png acompanha esta SPEC como referência visual para revisão. É uma imagem ilustrativa; as regras escritas prevalecem.

Ressalvas de leitura: login ocorre no Cognito, aplicativo e painel chamam API Gateway; DynamoDB alimenta Streams, embora essa seta esteja implícita na imagem. A menção a “inscrições” no cartão de catálogo não autoriza gestão/venda de inscrições. O painel atende apenas à equipe RunPass, não a organizadores. Sem site público nem push.

### Módulos e modelo de dados propostos

Identidade/perfil, catálogo, solicitações, participações, avaliações/RunScore, imagens/medalheiro, social, moderação, avisos, beta/feedback e administração.

Entidades principais:

- Usuário: referência de identidade, nome, username único, campos opcionais, status, admissão no beta e preferências de wishlist.
- Prova e Edição: identidade própria, data/local, organizador, status e distâncias oferecidas.
- Imagem de medalha do catálogo: associada à edição e, quando necessário, à distância.
- Solicitação: solicitante, dados mínimos, status, motivo e edição vinculada.
- Participação: usuário, edição ou solicitação enquanto rascunho, distância, resultado opcional, status e visibilidade de resultados. Unicidade por usuário/edição.
- Avaliação: participação única, oito notas inteiras 1–5, comentário opcional e estado de moderação.
- Medalha: participação única, referência da imagem oficial ou upload do proprietário.
- Publicação: participação única, estado de visibilidade e datas; curtidas únicas por usuário/publicação e comentários associados.
- Seguimento, bloqueio, wishlist, denúncia, aviso, feedback, auditoria administrativa e registro do beta.

### Operações e invariantes

- Contrato HTTP orientado a recursos e comandos de concluir, revisar, arquivar, moderar e ocultar. Identidade vem do token, nunca apenas de identificador enviado pelo cliente.
- Leituras devem aplicar projeção pública: não devolver resultado oculto e apenas esconder na tela. Mesmo controle em perfil, medalheiro, feed, cards e acesso às imagens.
- Conclusão verifica edição, unicidade, oito notas e imagem válida; gravar participação, avaliação e medalha em transação. Retentativas não criam cópias: comando idempotente.
- Upload iniciado com autorização, validado no servidor por tamanho, tipo real e imagem decodificável. Só imagem concluída e pertencente ao usuário pode satisfazer o requisito. Limites exatos e remoção de metadados devem ser especificados antes de implementar uploads.
- Rascunhos não contribuem para RunScore, medalheiro público nem métricas de conclusão.
- RunScore usa somente avaliações válidas; calcular com precisão e arredondar na exibição. Sem notas, mostrar ausência de avaliação, não nota zero.
- Invalidar avaliação mantém histórico e publicação, mas remove notas públicas e do agregado; correção só retorna após revisão humana.
- Editar a edição atualiza referências e agregados de ambas; conflito de unicidade não sobrescreve cadastro existente. Exclusão da participação remove os vínculos aprovados.
- Arquivar edição impede novas inclusões como proposta operacional; quais correções continuam permitidas precisa ser validado antes de implementar essa operação.
- Feed consulta publicações visíveis, exclui conteúdo bloqueado/suspenso e prioriza autores seguidos. Ordem proposta: seguidos primeiro, depois demais, com recência e desempate estável dentro dos grupos; paginação por cursor. Confirmar a regra detalhada na revisão técnica.
- Bloqueio preserva registros anteriores, ocultando-os entre envolvidos, e impede novas interações. Não prometer proteção sobre cópias exportadas.
- Avisos e feedback não dependem de push. Emissão de avisos após transações deve tolerar retentativa e evitar duplicação.
- Links abrem no app ou na loja; validar configuração de domínio e associação das plataformas sem criar site público completo.
- Solicitação aprovada ou vinculada não conclui participação automaticamente: corredor revisa e conclui.

### Beta, observabilidade e feedback

- Contabilizar admitidos únicos em transação para não ultrapassar 1.000 em admissões concorrentes. Registrar marco de entrada do 50º; fim em 60 dias. Contagem não reinicia por exclusão.
- Ativação >=50% dos admitidos reais, incluindo os primeiros 50; repetição >=30% dos ativados em outra edição; interação >=30% dos ativados com like/comentário em conquista alheia.
- Definir em revisão técnica como correções e exclusões afetam o relatório histórico, sem duplicar ativação por recriação. Eventos de comportamento não devem expor resultados ocultos ou texto pessoal desnecessário.
- Logs estruturados com correlação, latência, erros e operações administrativas; nunca credenciais. Monitorar jornadas, não apenas disponibilidade de infraestrutura.
- Metas herdadas: inicial <3 s, média API crítica <500 ms, disponibilidade 99,5%; medições exigem perfil de dispositivo/rede, endpoints e janela definidos. Não garantir esses números antes de testar.
- Feedback voluntário: facilidade após primeiro registro (1–5 e texto opcional), botão problema/sugestão/elogio, pesquisa aos 30 dias, fechamento aos 60 e pergunta após sete dias sem registro. Consolidar semanalmente.
- Preparar exclusão de conta e dados com política de retenção, tratamento de terceiros, backups e métricas; política ainda não aprovada e não pode ser inventada pela implementação.

## Testing Decisions

**Abordagem aprovada pelo usuário:** usar o contrato da API como principal fronteira de testes do domínio, verificando entradas e saídas com persistência real em ambiente de teste isolado. Complementar com testes ponta a ponta das jornadas essenciais Android/iPhone para validar UI, imagens, links e visibilidade. A aprovação dessa abordagem não equivale à aprovação integral da arquitetura ou a testes já executados.

Não foi encontrado aplicativo implementado no diretório inspecionado; não há padrões anteriores de testes identificados. Não inventar cobertura existente.

- Bons testes verificam comportamento observável, autorização e efeitos persistidos, sem depender de nomes internos, chaves físicas específicas ou composição das classes.
- Cenários: conclusão válida; notas incompletas; ausência de imagem; duplicidade concorrente; rascunho; solicitação recusada/reenvio; correção de edição; exclusão e recálculo; moderação; bloqueio; perfil público sem e-mail; resultado oculto ausente da resposta; feed com prioridade de seguidos; convite e teto concorrente do beta.
- Testes de imagem comprovam acesso autorizado e ausência de referência utilizável a objeto de outro usuário.
- Cenários mobile: cadastro, descoberta, rascunho, upload, conclusão, ocultação antes/depois de publicar e retorno de links compartilhados.
- Testes de contrato de identidade/armazenamento em ambiente AWS separado; não usar recursos de produção.
- Testes de carga e disponibilidade usam critérios mensuráveis e volume simultâneo aprovado; 1.000 convidados não significa 1.000 usuários simultâneos.
- Segurança inclui acesso de outro usuário, administrativo indevido, bloqueios, suspensão e downloads privados.
- Verificar recuperação de banco e limpeza de dados em ambiente de teste antes do beta.
- Para DynamoDB: validar escritas condicionais e transações concorrentes, atraso de índices, atualização de RunScore, eventos duplicados/fora de ordem, reprocessamento da outbox e ocultação de dados apesar de projeções atrasadas. Testar comportamento real em ambiente AWS isolado, além de testes locais.

## Out of Scope

Site para corredores, tracking GPS, treino, chat privado, stories, vídeos, feed de fotos livres, clubes/grupos, marcos extras, rankings, monetização, pagamentos, importação de contatos, push e integrações esportivas/IA. Não provisionar AWS, criar contas ou publicar aplicativos durante a redação desta SPEC.

## Further Notes

### Revisão necessária

1. Planejar ambiente e build mobile com Flutter/Dart aprovado; Python confirmado exclusivamente no backend.
2. Detalhamento dos cenários de teste; fronteira principal pela API e complemento por jornadas essenciais no aplicativo já aprovados pelo usuário.
3. Arquitetura, orçamento/região, stack do painel e responsável técnico.
4. Retenção/exclusão, verificação etária, limites de upload e acesso por convite.
5. Critérios de medição e políticas operacionais não resolvidas no PRD.
6. Modelo DynamoDB, índices e consultas de catálogo/feed; consistência do RunScore, capacidade e custo sob carga.
7. Contratos dos eventos, recuperação de falhas, outbox/Streams/SQS e política de acesso/cache das imagens.

Este documento sintetiza o contexto sem repetir o grill-me. Propostas técnicas não são decisões aprovadas. O processo corporativo da SKILL-PDLC ainda não tem adaptação formal registrada; não declarar reunião Teams ou unanimidade inexistentes.

### Publicação da skill

Rastreador e vocabulário de triagem não configurados. A to-spec orienta executar `/setup-matt-pocock-skills` nessa situação. Esta é uma versão local revisável, não uma issue publicada nem marcada `ready-for-agent`. Não publicar em serviço externo sem destino identificado e autorização aplicável.

### Referências técnicas consultadas

- Flutter e linguagens: https://docs.flutter.dev/resources/faq
- Ambiente multiplataforma e iOS: https://docs.flutter.dev/platform-integration
- JWT/Cognito em HTTP API: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-jwt-authorizer.html
- Modelagem DynamoDB: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-relational-modeling.html
- Transações DynamoDB: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transaction-apis.html
- Índices e consistência: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/SecondaryIndexes.html
- Entrega SQS: https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/standard-queues-at-least-once-delivery.html

### Próximas entregas

Revisar as propostas e validar riscos com prova técnica quando necessário; aprovar a especificação e então produzir implementation-slices. Não criar tickets como prontos para execução enquanto escolhas essenciais permanecerem abertas.
