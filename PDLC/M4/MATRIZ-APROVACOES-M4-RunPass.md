# RunPass — Consolidação das aprovações de M4

Estado: classificação aprovada pelo usuário para os requisitos suficientemente definidos no PRD, Grill-me e decisões posteriores. Não aprova a SPEC integral nem comprova implementação, testes ou liberação de produção.

## Critério

A instrução do usuário autoriza aprovar os pontos suficientemente definidos nas decisões anteriores. Requisitos confirmados não precisam de nova entrevista. Detalhes físicos sem decisão, hipóteses e resultados ainda não medidos permanecem em avaliação. Cada bloco pode conter itens aprovados e pendentes.

Fontes: PRD_RunPass_MVP_v2.md; SPEC_RunPass_MVP_v1.md, incluindo registros das perguntas técnicas e atualizações posteriores; políticas de retenção; MODELO-DYNAMODB-RunPass-v1.md; API-RunPass-v1.openapi.json; orçamento preliminar. Este registro prevalece sobre pendências históricas já resolvidas, sem apagar a rastreabilidade.

## 1. Eventos e recuperação — aprovação parcial

APROVADO: eventos de criação/alteração/exclusão do histórico; persistência durável junto da alteração operacional; processamento assíncrono e idempotente; recuperação conjunta de participação/avaliação/medalha; preservação de pendências; meta RunScore de dez segundos em condições normais; RPO de cinco minutos, RTO de quatro horas e janela de recuperação de sete dias no beta. Retenção de payload integralmente entregue por sete dias e idempotência de comandos da API por sete dias, conforme confirmações posteriores.

AVALIAR: horizonte de replay, ledger/versões dos consumidores, armazenamento e recuperação da outbox, retentativas e falhas, marcos e cenários de recuperação e procedimento operacional. As metas aprovadas precisam de testes, não de nova aprovação dos mesmos números.

## 2. Retenção e privacidade — aprovação parcial

APROVADO: histórico ativo sem TTL; lake de alterações de avaliação por 60 dias desde ocorrência original; acesso restrito e auditado; bloqueio/ocultação imediatos e exclusão pessoal dos sistemas ativos em até sete dias, inclusive lake; preservação de imagens oficiais compartilhadas; reaplicação de exclusões na restauração. Denúncias abertas com revisão semanal, encerradas por até 60 dias e auditoria administrativa por até 90 dias. Logs DEV/PROD por sete/30 dias; URL de upload de 15 minutos; limpeza de temporários abandonados até 24 horas após expiração da sessão; imagem validada nunca vinculada elegível após sete dias, com limpeza até 24 horas depois.

AVALIAR: controle mínimo de exclusões, retenção de rascunhos/feedbacks/solicitações/lista de espera, tratamento da data de nascimento, expiração de leitura/cache, descarte físico de lake/denúncias/auditoria em até 24 horas e exceção de auditoria pendente além de 60 dias. Prazo de sessão operacional e mecanismo de limpeza ainda precisam ser projetados.

## 3. DynamoDB — aprovação parcial

APROVADO: adoção do DynamoDB como direção de armazenamento operacional; agrupar dados relacionados considerando acesso e requisitos operacionais; participação/avaliação/medalha com recuperação conjunta e possibilidade de configuração comum de criptografia/papéis técnicos; acesso por API, nunca diretamente pelo aplicativo; histórico sem expiração automática. Não se exige nova decisão de produto para cada nome de chave ou índice.

AVALIAR: proposta física completa, quantidade e fronteiras de tabelas, PK/SK/GSIs, transações, consultas de catálogo/feed e custos/distribuição de carga. A diretriz de dados relacionados não aprova uma única tabela para toda a aplicação. On-demand permanece proposta do modelo técnico a revisar com o desenho final.

## 4. Segurança e administração — aprovação parcial

APROVADO: e-mail/senha para corredores; MFA para Administrador e Moderador; separação de papéis; autorização de proprietário e bloqueios na API; dados privados fora dos perfis públicos; DEV/PROD em contas distintas; OIDC de GitHub Actions sem chaves permanentes; revisão humana/testes antes de main e aprovação manual de PROD.

AVALIAR: solução concreta de identidade e configuração, método/recuperação do MFA, bootstrap/revogação de administradores, matriz final de permissões, IAM e criptografia, acompanhamento seguro da exclusão e conformidade operacional da política de dados. Credencial ou recurso efetivamente configurado exige evidência própria.

## 5. Contratos e interfaces — aprovação funcional parcial

APROVADO: regras de participação única por edição, avaliação obrigatória de oito critérios, edição/exclusão próprias, comentários opcionais, medalha automática com imagem oficial ou foto própria obrigatória, feed com ordenação priorizando seguidos, privacidade/bloqueios e demais jornadas do PRD. Aplicativo Flutter/Dart Android/iPhone; Python/FastAPI em Lambda conforme decisão técnica registrada. Imagens JPEG/PNG de até 10 MB no original, meta de otimização de 1 MB e validação de cinco segundos; imagem oficial versionada, preservando vínculos antigos, e correção retroativa explícita/auditada. Upload administrativo com controle de permissão/MFA e publicação separada da transferência.

AVALIAR: aprovação integral do OpenAPI (estrutura validada não prova comportamento), limites de campos/pixels, HEIC no iPhone, contrato da correção retroativa, painel administrativo e hospedagem, consulta do lake, empacotamento e desempenho FastAPI–Lambda. Não confundir aprovação de requisito com homologação de todos os schemas, endpoints ou serviços candidatos.

## 6. Beta — execução inicial aprovada; encerramento pendente

APROVADO: distribuição pelas lojas oficiais; idade mínima de 18 anos por autodeclaração/data de nascimento; até mil admitidos, sem reabrir vagas automaticamente por exclusão; contagem de 60 dias iniciada nos primeiros 50; lista de espera; definição e denominadores de ativação/interação; coleta e revisão de feedbacks previstas no PRD.

AVALIAR: operação após o dia 60, novos ingressos/lista de espera e transição de política. Não é necessário reaprovar duração, tamanho ou início do beta.

## 7. Orçamento e aceite — premissas aprovadas; fechamento pendente

APROVADO: São Paulo, CloudFormation, ambientes separados, promoção dos mesmos artefatos; premissas confirmadas de 20 medalhas/usuário, 300 usuários/dia, duas sessões/dia e 30 imagens/sessão. Metas funcionais e de recuperação já confirmadas permanecem válidas. Alertas críticos por e-mail para equipe RunPass.

AVALIAR: estimativa completa com exclusões precificadas e limite autorizado; perfil e duração dos testes, percentis, erros/concorrência aceitáveis, fórmula de disponibilidade e critérios de liberação; cobertura de atendimento/escalonamento e responsáveis. Premissas de simulação adicionais não são limites funcionais aprovados.

## 8. SPEC e plano — aprovação final pendente

APROVADO: conteúdo de produto anteriormente confirmado e requisitos classificados acima; não reabrir por mera ausência de implementação.

AVALIAR: consolidar a SPEC sem contradições históricas, resolver ou delimitar pendências, apresentar riscos e aprovar tecnicamente o conjunto; produzir implementation-slices com dependências e critérios de aceite. Gates corporativos, testes concluídos e autorização de produção não são comprovados por este registro.

## Trabalho técnico que pode prosseguir sem nova entrevista

Produzir propostas de esquema, índices, contratos, IAM, infraestrutura como código, orçamento e testes com base nos requisitos aprovados; resolver detalhes rotineiros e apresentar o conjunto revisável. Só pedir decisão de produto quando houver escolha com impacto real de escopo, custo, privacidade ou comportamento. Nenhum deploy, cobrança, commit ou push é autorizado por esta classificação.

## Política de replay aprovada para o beta

O usuário aprovou reprocessar eventos concluídos por até sete dias, alinhados à janela de recuperação; preservar a recuperabilidade dos eventos pendentes até resolução, respeitando retenção/exclusão pessoal; reconstruir feed e RunScore mais antigos a partir dos dados operacionais vigentes; e restringir reprocessamento à operação interna controlada pela equipe RunPass. Não conservar eventos indefinidamente para reconstrução. Replay não recria conteúdo excluído nem renova retenção. O marco técnico proposto é a última confirmação dos destinos obrigatórios, coerente com o payload entregue; detalhar no contrato operacional.

EVENTOS-E-REPLAY-RunPass-MVP.md distingue a política aprovada dos mecanismos propostos. Ledger/deduplicação, margem para mensagens em trânsito, versões dos agregados, autorização operacional e reconstrução concorrente ainda serão projetados e validados. Não fixar automaticamente TTL de sete dias para todos os controles. A política não conclui o esquema físico DynamoDB nem aprova a SPEC integral; não houve implantação ou testes.

## Aprovação prioritária e SPEC única

O usuário aprovou DynamoDB on-demand com agrupamento relacionado, outbox transacional/SQS e consumidores versionados/idempotentes, Cognito separado para corredores/operadores com MFA por aplicativo autenticador e autorização por função. Autorizado detalhamento e desenvolvimento incremental do fluxo autenticação → catálogo → rascunho → imagem → conclusão → avaliação e medalha. Referência única: SPEC_RunPass_MVP_v1.md, que recebeu o conteúdo consolidado; Não é mantida uma segunda SPEC ativa. Registro técnico anterior preservado em PDLC/M4/historico, sem vigência. Não exigir aprovação isolada de cada atributo nem nova rodada P01–P09; dependências técnicas devem ser fechadas antes da parte afetada. Não autoriza custo, deploy ou beta sem requisitos/evidências próprios.
