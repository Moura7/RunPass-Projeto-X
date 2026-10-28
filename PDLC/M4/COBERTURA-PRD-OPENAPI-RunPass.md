# RunPass — Cobertura PRD versus OpenAPI

**Data:** 27/10/2026. **Contrato:** 0.6.1-draft. Revisão documental, sem API implementada. Contrato semanticamente válido não significa produto completo, autorização segura ou desempenho comprovado.

## Matriz de cobertura

| Requisito | Contrato/local responsável | Situação |
| --- | --- | --- |
| Cadastro, e-mail, senha e recuperação | Provedor Cognito; bootstrap /beta | Externo ao FastAPI; integração ainda não testada |
| 18 anos e limite de 1.000 | POST /beta/admissions | Representado; idade/concorrência exigem código e teste |
| Lista de espera | /beta/waitlist, /me/waitlist | Representado; comunicação posterior pendente |
| Perfil e busca de conhecidos | /me, /profiles | Parcial: correspondência, limites e mudanças de username pendentes |
| Catálogo e filtros | /editions | Representado; plano de índices e combinações ainda a validar |
| Resultado e uma participação/edição | /participations, /complete, PATCH | Representado; autorização e unicidade não provadas pelo schema |
| Prova ausente e rascunho | /edition-requests e /participations | Representado; vinculação e concorrência ainda a testar |
| Oito notas obrigatórias | /complete, PUT /review | Representado e exemplos do schema verificados |
| Comentário opcional com remoção no PUT | ReplaceReview | Representado; evento durável ainda não implementado |
| RunScore por edição/distância | /editions/{id}, /reviews | Representado; agregado assíncrono/10 s não testado |
| Medalha automática e imagem oficial | Edition/Distance.medalImageReference e /complete | Referências acrescentadas; criação automática é regra de negócio |
| Foto própria e processamento | /uploads e status | Representado; HEIC, GPS e meta de 5 s exigem testes reais |
| Visibilidade de resultado | PATCH participação e projeções | Representado; ausência de dados ocultos depende de implementação |
| Feed e seguidores | /feed, /follow | Representado; consulta DynamoDB e estabilidade do cursor pendentes |
| Curtidas/comentários | /like e /comments | PATCH do próprio comentário acrescentado após aprovação, com indicação de editado e data original preservada; limites de texto ainda pendentes |
| Bloqueio | /block | Bloquear remove seguimentos nos dois sentidos; interações preservadas ficam ocultas. Desbloquear não recria vínculos, reexibindo apenas conteúdo ainda autorizado. Concorrência e projeções exigem implementação/testes |
| Wishlist pública/ocultável | /wishlist e /visibility | Representado; após data do evento ainda pendente |
| Avisos e feedback | /me/notices e /feedback | Parcial: conteúdo das pesquisas, retenção e limites pendentes |
| Catálogo administrativo | /admin/editions, /decision e /admin/organizers | Substituição de imagem oficial preserva versão em medalhas antigas e fotos próprias. Upload administrativo e ação explícita de correção retroativa ainda a detalhar |
| Moderação e papéis | /admin/moderation-actions, /roles e /admin/reports/{id}/resolution | Encerramento com decisão/motivo contratado; matriz detalhada, bootstrap e testes ainda pendentes |
| Histórico informacional | /admin/reviews/{id}/history e schema do evento | Representado; ingestão/expiração/exclusão ainda não implementadas |
| Exclusão da conta | DELETE /me | Parcial: prazo, recibo/acompanhamento após bloqueio e retenção precisam fechar |
| Cards e links compartilháveis | Aplicativo + configuração de links | Geração local no Flutter aprovada; não requer endpoint de renderização. Leituras autorizadas e links app/loja continuam necessários e ainda exigem testes |
| Analytics do beta | Instrumentação e consultas operacionais | Plano de eventos/relatório ainda incompleto; não exige necessariamente endpoint público |
| RPO/RTO, disponibilidade e deploy | Infraestrutura, testes e runbooks | Fora da validação OpenAPI; requisitos continuam sem comprovação |

Não foi atribuído percentual de cobertura: ter uma rota não comprova aceite do requisito.

## Correções feitas nesta revisão

- Referência opcional da imagem oficial da medalha em edição e distância, permitindo que a jornada obtenha a referência exigida ao concluir.
- Versão da edição na resposta, para suportar expectedVersion nas operações administrativas.
- Distância em quilômetros no PATCH de rascunho de prova ausente, antes de existir distanceId do catálogo.
- Envelope do histórico alinhado ao JSON Schema quanto aos campos obrigatórios e tipos de evento.
- Descrições de PATCH/PUT normalizadas nos pontos alterados, preservando semântica aprovada.

Campos acrescentados são concretizações técnicas DRAFT das jornadas aprovadas; não autorizam novos recursos AWS.

## Próximas ações recomendadas

1. Edição de comentário, bloqueio e desbloqueio confirmados; validar concorrência, prioridade do feed e contagens sem recriar seguimentos removidos.
2. Geração local de cards confirmada; detalhar acesso autorizado à imagem e testar visibilidade/compartilhamento e links nas duas plataformas.
3. Denúncias e organizadores de referência definidos; completar gestão de imagens e feedbacks, sem portal de organizadores.
4. Fechar exclusão/retenção e métricas, depois validar modelo DynamoDB contra todas as rotas.
5. Revisar o contrato consolidado, aprovar tecnicamente e só então gerar clientes/slices como prontos para implementação.

## Evidência reproduzível

Executar validar_openapi_runpass.py com openapi-spec-validator 0.7.2. VALIDACAO-OPENAPI-RunPass.json registra versão, hash do contrato e resultados. O ambiente isolado usado na revisão não deve ser publicado no repositório. Validação de contratos não faz chamadas AWS nem testa endpoints.

## Contrato de upload administrativo — OpenAPI 0.7.0-draft

Incluídas POST /admin/medal-image-uploads, POST /admin/medal-image-uploads/{id}/finalize e GET /admin/medal-image-uploads/{id}. Operações exigem Administrador e MFA, sem vaga de corredor. Sessão vinculada a edição e distância opcional, envio PUT privado temporário, finalização idempotente e consulta de estado pending/valid/failed. Somente estado valid disponibiliza referência imutável para vinculação explícita pelo PATCH da edição, com versão esperada e auditoria. Verificar destino, ambiente e origem administrativa da referência no backend; uploads pessoais não podem ser promovidos por esse fluxo. A edição deve existir antes de iniciar a sessão de sua imagem oficial.

Schemas distinguem pendência, sucesso e falha, sem referência publicável nos estados pendente/falha. Limites aprovados de JPEG/PNG e 10 MB de original; otimização com meta de 1 MB e retorno em cinco segundos sujeitos a testes. Falha preserva imagem vigente e medalhas antigas. Prazo de expiração, limite de pixels, limpeza e retenção da auditoria continuam pendentes. Contrato validado estruturalmente; não comprova execução da API, autorização, MFA ou concorrência. A SPEC integral permanece em revisão.