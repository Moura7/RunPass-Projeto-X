# RunPass — Revisão dos contratos de operação

**Estado:** OpenAPI 0.6.0-draft, propostas técnicas sem implementação.

## Novas operações

| Método | Rota | Controle principal |
| --- | --- | --- |
| GET | /beta/status | Identidade autenticada, mesmo sem admissão |
| POST | /beta/admissions | E-mail confirmado, autodeclaração/nascimento, teto transacional |
| POST | /beta/waitlist | Elegibilidade, consentimento explícito, sem admissão automática |
| GET, DELETE | /me/waitlist | Somente o interessado |
| DELETE | /me | Exclusão da própria conta, ocultação/bloqueio imediato |
| POST | /reports | Denúncia privada, sem remoção automática |
| POST | /feedback | Feedback voluntário |
| GET | /admin/edition-requests | Administrador e MFA |
| POST | /admin/edition-requests/{id}/decision | Administrador e MFA; decisão com versão |
| POST, PATCH | /admin/editions e /admin/editions/{id} | Administrador e MFA; catálogo |
| POST | /admin/editions/{id}/archive | Administrador e MFA; preservar histórico |
| GET | /admin/reports | Moderador e MFA |
| POST | /admin/moderation-actions | Moderador e MFA; motivo obrigatório |
| PUT | /admin/profiles/{id}/roles | Administrador especificamente autorizado e MFA |
| GET | /admin/reviews/{id}/history | Administrador, MFA e autorização específica de histórico |

## Evitar dependência circular no cadastro

Cognito cria/confirma identidade antes da admissão. Identidade autenticada ainda não admitida acessa apenas rotas de bootstrap previstas (status, admissão, lista de espera e exclusão da própria conta), não feed/catálogo por consequência automática. Admissão e limite são regras do backend. A criação da identidade não consome vaga; usuários em espera não integram ativação. Recuperação de senha e login são fluxos Cognito, não rotas fictícias do FastAPI.

Administrador/Moderador atuam por autorização operacional, sem exigir ocupação de vaga de corredor. O tratamento desses usuários nas métricas de participantes deve ser confirmado na implementação, evitando contaminar a coorte com contas técnicas.

## Segurança documentada versus aplicada

As extensões x-required-role, x-required-permission, x-requires-mfa e x-requires-beta-admission descrevem verificações obrigatórias do backend. OpenAPI não executa essas verificações. Um JWT válido não comprova MFA nem autorização específica sozinho. Não inventar scopes Cognito para substituir a matriz de permissões sem projetar emissão e revogação.

Administradores não herdam automaticamente moderação nem acesso ao lake. Gestão de papéis exige proteção contra autoelevação e perda de último administrador. Bootstrap, recuperação, revogação e atribuição cumulativa continuam pendentes.

## Exclusão de conta

DELETE retorna recibo de aceitação, não prova de limpeza física. Bloquear acesso à API mesmo com tokens emitidos anteriormente e ocultar conteúdo ao aceitar. Limpeza, data lake, backups e dados de terceiros seguem política específica ainda a fechar. Não manter endpoint comum de status acessível por token revogado só para facilitar polling; propor mecanismo de suporte/recibo seguro antes de implementá-lo.

## Detalhes pendentes e propostas

Versão da imagem oficial confirmada posteriormente: medalhas existentes preservam a versão vinculada; novos registros usam catálogo vigente. Corrigir retroativamente requer ação explícita e auditada, sem endpoint específico ainda definido. Não sobrescrever bytes referenciados por medalhas antigas nem confundir essa retenção com histórico de avaliações.

Substituição da imagem oficial da medalha aprovada por Administrador com MFA via edição do catálogo, preservando fotos próprias. Referência pode existir por edição e distância. Versão da edição e auditoria exigidas; impacto em medalhas antigas que usam imagem oficial e fluxo de upload administrativo ainda a especificar. Não apagar arquivos referenciados.

Organizadores definidos posteriormente como referências de catálogo sem login/portal. GET/POST /admin/organizers e GET/PATCH /admin/organizers/{id} para Administrador com MFA, sem exclusão em cascata. Campos mínimos de nome, ID e versão; contatos e dados pessoais adicionais não aprovados. Edições recebem organizerId opcional, sem exigir cadastro de organizador desconhecido para provas antigas.

Encerramento de denúncias definido posteriormente: POST /admin/reports/{id}/resolution exige Moderador com MFA, versão esperada, decisão (procedente/improcedente/sem elementos suficientes) e motivo; resposta administrativa restrita. Eventual ação de moderação é explícita e referenciada, não consequência automática. Decisão e motivo não são enviados nas projeções públicas.

- Encerramento dos 60 dias: comportamento de usuários existentes e novos cadastros após beta ainda não aprovado; não reabrir vagas automaticamente.
- Lista de espera: contato, exclusão e comunicação posterior precisam de minimização e política; não enviar push por inferência.
- Schemas administrativos ainda não abrangem todos os campos de organizador/imagens nem garantem um CRUD completo. Regras de alterações em distâncias com registros existentes exigem integridade referencial.
- Vocabulário de motivos, limites dos textos e combinações válidas de ação/objeto na moderação precisam de fechamento.
- Consulta do lake é proposta mediada, não escolha automática de Athena/Glue. Janela, custo, disponibilidade e auditoria devem ser medidos.
- Rota de papéis é proposta, não autorização para criar contas administrativas nesta etapa.
- Anonimização, descarte e tratamento de evento de auditoria entregue após expiração continuam pendências da política de dados.

## Verificações e próxima revisão

Validar referências, operationIds, parâmetros, erros e exemplos de admissão/decisão/moderação. Validação sintática não comprova identidade, MFA, concorrência ou conformidade de publicação nas lojas. O contrato cobre jornadas principais, mas ainda exige revisão de cobertura contra o PRD e validação semântica integral antes da aprovação técnica.

## Contrato de upload administrativo — OpenAPI 0.7.0-draft

Incluídas POST /admin/medal-image-uploads, POST /admin/medal-image-uploads/{id}/finalize e GET /admin/medal-image-uploads/{id}. Operações exigem Administrador e MFA, sem vaga de corredor. Sessão vinculada a edição e distância opcional, envio PUT privado temporário, finalização idempotente e consulta de estado pending/valid/failed. Somente estado valid disponibiliza referência imutável para vinculação explícita pelo PATCH da edição, com versão esperada e auditoria. Verificar destino, ambiente e origem administrativa da referência no backend; uploads pessoais não podem ser promovidos por esse fluxo. A edição deve existir antes de iniciar a sessão de sua imagem oficial.

Schemas distinguem pendência, sucesso e falha, sem referência publicável nos estados pendente/falha. Limites aprovados de JPEG/PNG e 10 MB de original; otimização com meta de 1 MB e retorno em cinco segundos sujeitos a testes. Falha preserva imagem vigente e medalhas antigas. Prazo de expiração, limite de pixels, limpeza e retenção da auditoria continuam pendentes. Contrato validado estruturalmente; não comprova execução da API, autorização, MFA ou concorrência. A SPEC integral permanece em revisão.
## Exclusão de conta — decisão aprovada

O usuário aprovou bloquear acesso e ocultar perfil/conteúdo imediatamente ao aceitar a exclusão, com remoção dos dados pessoais dos sistemas ativos em até sete dias corridos desde a aceitação. O escopo inclui fotos próprias e histórico identificável de avaliações no data lake: a exclusão da conta prevalece sobre a retenção ordinária de 60 dias desse histórico. Preservar catálogo e imagens oficiais compartilhadas ainda referenciadas. A limpeza deve abranger projeções, índices e cópias intermediárias sob controle do RunPass, com processamento idempotente, retentativas e acompanhamento por destino.

Backups mantêm a janela própria de sete dias no beta; a aprovação não significa eliminação de todas as cópias em sete dias desde a solicitação. Reaplicar exclusões antes de liberar qualquer restauração. Tratamento de denúncias/evidências, auditoria e controle mínimo de exclusões continua pendente de definição específica, sem autorização para retenção indefinida. Os demais prazos propostos no documento de retenção não foram aprovados por esta decisão. Prazo de exclusão é requisito aprovado, ainda sem comprovação por implementação ou testes; a SPEC integral permanece em revisão.
## Retenção de denúncias e auditoria — prazos aprovados

O usuário aprovou a recomendação para o beta: denúncias em análise permanecem enquanto necessárias, com revisão semanal pela equipe RunPass; denúncias encerradas e evidências necessárias permanecem por até 60 dias desde o encerramento; auditoria administrativa mínima permanece por até 90 dias desde a ocorrência original da ação. Consulta, cópia, retentativa ou replay não renovam esses prazos. Denúncia aberta exige acompanhamento; o prazo máximo de resolução continua pendente, sem autorizar retenção indefinida sem revisão.

Acesso restrito por permissão e MFA, respeitando a separação entre Administração e Moderação. A retenção ordinária não estende o prazo aprovado para exclusão da conta: dados pessoais identificáveis continuam sujeitos à remoção em até sete dias corridos, incluindo os presentes nesses registros. Não presumir anonimização por troca de nome ou ID. Preservar registros independentes de terceiros somente sem reter indevidamente os dados do titular excluído; necessidade excepcional de retenção identificável exige política específica ainda não definida.

Essas janelas não se aplicam automaticamente a logs técnicos, feedbacks, lista de espera ou controles de exclusão/idempotência. Descarte físico em até 24 horas após expiração continua proposta não aprovada. O lake de alterações de avaliações mantém sua própria regra de 60 dias desde a ocorrência. Detalhamento: RETENCAO-DENUNCIAS-E-AUDITORIA-RunPass.md. Requisitos registrados, sem implementação ou testes de execução; SPEC integral em revisão.