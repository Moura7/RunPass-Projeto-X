# RunPass — Fechamento técnico M4

**Estado:** DRAFT para revisão. Complementa a SPEC v1; não aprova arquitetura integral nem autoriza provisionamento. Base: PRD aprovado e 35 respostas técnicas. Propostas abaixo são identificadas como tais.

## 1. Decisões consolidadas

Flutter/Dart no app; Python/FastAPI em Lambda; AWS São Paulo; DynamoDB sob demanda; CloudFormation; DEV/PROD em contas distintas. GitHub Actions com OIDC, PR/testes/revisão humana, promoção dos mesmos artefatos e aprovação manual de PROD. Painel Flutter Web ainda candidato.

Imagem: JPEG/PNG até 10 MB original, otimização para meta de 1 MB, remoção de GPS, HEIC a validar; retorno de validação em até 5 s após upload em condições normais. RunScore assíncrono com meta de 10 s. Exclusão oculta imediatamente e limpa depois. MFA administrativo. RPO 5 min, RTO 4 h e pontos de recuperação por 7 dias no beta, sujeitos a ensaio e cobertura por cenário.

Instalação nas lojas oficiais; primeiros 1.000 elegíveis, lista de espera posterior; 18 anos completos por autodeclaração com nascimento privado. Beta de 60 dias desde os primeiros 50.

## 2. Premissas de carga e limites desta análise

Referência esperada: 18.000 sessões e 594.000 chamadas HTTP/mês incluindo reserva, aproximadamente 0,23 chamada/s na média de 30 dias. Teste de 20 req/s é patamar provisório, não volume observado. Cenários econômico/pico constam no documento de premissas. Não inferir uma chave de partição da média agregada.

As taxas por padrão abaixo não foram medidas; marcar RPS como desconhecido até instrumentação ou distribuição explícita do tráfego. Quantidades por página e tamanhos são hipóteses técnicas para prova de desenho, não limites aprovados do produto.

## 3. Matriz de padrões de acesso, antes do esquema

Pergunta técnica 39 respondida: criptografia e papéis técnicos compartilhados entre participação, avaliação e medalha, mantendo autorização na API e sem acesso direto do app às tabelas. Essa definição, junto da recuperação conjunta, ausência de TTL e eventos confirmados, fecha os parâmetros operacionais desse agregado; não determina automaticamente os requisitos dos demais domínios.

**Diretriz adicional do usuário:** single-table deve considerar dados relacionados. A sugestão de Core amplo, tabela operacional e projeção do feed é hipótese, não divisão aprovada. Participação/avaliação/medalha são candidato claro a agregado relacionado; outros agrupamentos exigem padrões de acesso e requisitos operacionais confirmados. Uma tabela não implica um único item ou partição. Relacionamento indireto entre todos os domínios não exige consolidá-los todos automaticamente. Recuperação conjunta continua sem confirmação específica.

| Prioridade / ID | Operação | RPS | Itens / tamanho proposto | Consistência | Autorização |
| --- | --- | --- | --- | --- | --- |
| 1 / A01 | Feed com seguidos primeiro e demais depois, recência por grupo | A medir; maior exposição esperada | Página 20; projeção 1–2 KB/item | Projeção eventual; revalidar estado e visibilidade atuais | Usuário autenticado, bloqueios bilaterais e autor |
| 2 / A02 | Perfil por ID ou username | A medir | 1 perfil, até 2 KB | Eventual em dados públicos; fonte atual para suspensão/privacidade | Projeção pública ou proprietário |
| 3 / A03 | Histórico e medalheiro de usuário | A medir | Página 20; 1–3 KB/item | Listagem eventual com filtros de autorização atuais | Público permitido ou proprietário |
| 4 / A04 | Catálogo por cidade/período/distância e início do título | A medir | Página 20; projeção 1–2 KB/item | Eventual | Autenticado; somente edições publicáveis |
| 5 / A05 | Detalhe de edição e RunScore | A medir | 1 edição e agregado, até 4 KB combinados como hipótese | Dados atuais para concluir; score eventual até meta de 10 s | Leitura autorizada; escrita administrativa |
| 6 / A06 | Avaliações de edição com filtro de distância | A medir | Página 20; 1–2 KB/item sem imagem binária | Eventual na listagem; validar moderação atual | Autenticado e conteúdo publicável |
| 7 / A07 | Concluir/editar participação | A medir | Conjunto limitado: participação, avaliação, medalha, evento e controle | Transação + versões condicionais | Proprietário, edição aberta, imagem válida |
| 8 / A08 | Excluir participação e consultar estado | A medir | Marcação + evento; filhos em páginas para limpeza | Estado de remoção imediato na fonte | Proprietário; workers com escopo mínimo |
| 9 / A09 | Curtir/comentar, seguir e bloquear | A medir | Escrita por relação, controle e evento quando necessário | Condicional; revalidar bloqueios/estado | Ator vem do token; alvo válido |
| 10 / A10 | Wishlist e avisos do próprio usuário | A medir | Página 20; até 1 KB/item como hipótese | Eventual; preferência privada consultada na fonte | Dono; wishlist pública apenas se permitida |
| 11 / A11 | Filas de solicitações e denúncias por estado | A medir | Página 20; 1–3 KB/item | Índice eventual; ação revalida versão atual | Administrador ou Moderador conforme matriz |
| 12 / A12 | Admitir usuário, reservar username, registrar espera | A medir; burst a testar | Poucos itens por operação | Transacional/condicional para teto e unicidade | Identidade confirmada e elegibilidade |
| 13 / A13 | Evento pendente, entrega e reprocessamento | A medir por mutação | Evento compacto, hipótese até 2 KB | Fonte durável; entrega duplicável | Publicador/worker autorizado |
| 14 / A14 | Exclusão de conta e enumeração dos seus dados | A medir; rara | Estado + job; enumeração paginada | Bloqueio imediato, limpeza eventual | Proprietário; executor específico |

O esquema deverá mostrar uma estratégia de chave/índice para cada entrada. Ainda não há esquema físico aprovado. Antes de definir tabelas: confirmar quais agregados compartilham recuperação, Streams, TTL, criptografia e isolamento IAM; requisitos ausentes não são defaults silenciosos.

## 4. Feed e catálogo: riscos que a modelagem precisa resolver

**Feed:** consultar cada seguido na abertura cresce com o número de relações; uma partição global de publicações pode concentrar carga. Comparar projeção por leitor e consulta agregada por autor, medindo amplificação de escrita/leitura. Não escolher fan-out completo sem medir seguidores e publicações. Cursor deve manter fase (seguidos/demais), recorte temporal e desempate estável; não repetir posts. Novos seguidores e posts podem exigir atualização do feed, sem promessa de snapshot perfeito não especificado.

**Catálogo:** ordenar por data e filtrar início do título não se resolve automaticamente com a mesma chave ordenadora. Construir matriz de combinações e provar que nenhuma varredura global é necessária. Filtros pós-leitura consomem capacidade sobre itens não retornados. Se houver explosão de índices ou custo excessivo, revisar desenho/escopo com Produto; não ativar OpenSearch silenciosamente.

**Privacidade:** índice atrasado não autoriza devolver conteúdo removido. Hidratar e revalidar perfil, publicação e bloqueios atuais antes da resposta; remover informações ocultas na API. Medir o custo adicional dessa verificação.

## 5. Contratos HTTP propostos

Rotas abaixo são contratos de API candidatos, não caminhos de arquivos. Modelos OpenAPI detalhados serão produzidos após revisão.

| Domínio | Operações propostas |
| --- | --- |
| Conta | POST /beta/admissions; POST /beta/waitlist; GET/PATCH /me; DELETE /me |
| Perfis | GET /profiles/{id}; GET /profiles?usernamePrefix=... |
| Catálogo | GET /editions; GET /editions/{id}; GET /editions/{id}/reviews |
| Solicitações | POST /edition-requests; GET /me/edition-requests; PATCH /edition-requests/{id}; POST /edition-requests/{id}/resubmit |
| Participações | POST /participations; GET/PATCH/DELETE /participations/{id}; POST /participations/{id}/complete |
| Imagens | POST /uploads; POST /uploads/{id}/finalize; GET /uploads/{id}/status |
| Social | GET /feed; PUT/DELETE /profiles/{id}/follow; PUT/DELETE /profiles/{id}/block; PUT/DELETE /posts/{id}/like; GET/POST /posts/{id}/comments |
| Visibilidade | PATCH /posts/{id}; PUT/DELETE /me/wishlist/{editionId}; GET /profiles/{id}/wishlist |
| Operação | GET /me/notices; POST /reports; POST /feedback; comandos administrativos separados de aprovação, recusa, arquivamento e moderação |

Requisitos transversais propostos:

- Token de acesso validado; não usar ID informado como identidade do ator. Dados públicos não significam cadastro aberto nem leitura anônima automaticamente.
- Idempotency-Key em comandos de criação/conclusão/admissão, vinculado a ator, operação e hash do corpo. Reuso com corpo diferente gera conflito; reenvio igual retorna resultado conhecido. Expiração desse registro ainda a definir.
- Controle de versão para alterações: conflito concorrente não sobrescreve silenciosamente.
- Erros consistentes: 400 entrada inválida; 401 autenticação; 403 acesso negado; 404 conforme política anti-enumeração; 409 duplicidade/versão/estado; 422 validação de domínio; 429 limitação; 503 indisponibilidade transitória. Fixar distinção 400/422 no OpenAPI antes de implementar.
- Não paginar apenas por offset. Cursor opaco e validado, limitado ao usuário e aos filtros; tamanho de página máximo a validar.
- DELETE confirma bloqueio de exibição e início do trabalho; resposta não significa que backups ou arquivos já foram apagados. Estado de limpeza consultável pelo proprietário quando aplicável.
- Imagem pendente retorna estado explícito; ultrapassar 5 s não é aprovação nem prova de arquivo inválido.

## 6. Eventos e RunScore: contrato proposto

Destino informacional confirmado: S3 privado segregado por DEV/PROD, ingestão assíncrona com evento persistido atomicamente à alteração operacional. Reenvio seguro e confirmação de entrega; destino separado do acesso às fotos de medalhas. Especificar formato, identificador/deduplicação, particionamento, consulta autorizada, retenção e reconciliação. Orçamento anterior precisa incorporar essa ampliação antes de ser tratado como abrangente.

Acesso humano ao histórico do data lake confirmado: somente Administradores autorizados da equipe RunPass, sem acesso padrão a corredores ou Moderadores. Detalhar autorização específica, MFA, auditoria e mecanismo de consulta. Serviços de ingestão/descarte não herdam permissão humana irrestrita; separar papéis técnicos e de consulta.

Conteúdo histórico confirmado: antes/depois de notas e comentário necessários à auditoria, com acesso restrito. Distinguir ausência/remoção de comentário no evento e correlacionar versões. A orientação anterior de payload mínimo continua aplicável: dados de auditoria não devem ser distribuídos indiscriminadamente a consumidores de feed/RunScore. Definir canal/contrato de auditoria protegido e tratamento de retenção e exclusão antes da implementação.

Ampliação confirmada pelo usuário na revisão do OpenAPI: omissão do comentário no PUT o remove da avaliação atual, com preservação do histórico de eventos em camada informacional no data lake. Histórico de alterações de avaliações entra no escopo; analytics avançado permanece futuro. Atualizar envelope e estratégia de entrega, separando evento operacional mínimo de eventual conteúdo histórico sensível; retenção, acesso e exclusão precisam ser definidos antes de armazenar comentários antigos. S3 privado como candidato, sem aprovação automática de ferramentas adicionais.

Pergunta técnica 40 respondida: retenção própria para eventos temporários e controles, sem apagar itens com processamento/recuperação pendente. Prazos ainda a definir. Não confundir retenção por tipo de item com obrigação de tabela separada; histórico de conquistas permanece sem TTL.

Pergunta técnica 38 respondida: eventos de criação, alteração e exclusão aprovados para histórico e projeções, com payload mínimo, identificador e versão. Envelope detalhado, nomes dos eventos, consumidores e política de retenção continuam propostas a revisar; nenhuma publicação de evento foi executada.

Envelope: eventId único, tipo, schemaVersion, aggregateId, aggregateVersion, occurredAt em UTC, correlationId e payload mínimo. Não transportar credenciais, nascimento completo ou fotos binárias. Dados de conta excluída exigem política de retenção e minimização.

Eventos candidatos: ParticipationCompleted, ParticipationUpdated, ParticipationDeleted, ReviewChanged, ReviewInvalidated, ReviewReapproved, ImageValidated, ImageRejected, EditionRequestReviewed, AccountDeletionRequested. Definir um único evento efetivo por mudança para não atualizar RunScore duas vezes por participação e review.

Transação grava mudança e evento de outbox. Streams serve de sinal de publicação, não de única cópia recuperável. Publicador manda para SQS e registra entrega; falha após envio pode duplicar mensagem. Reconciliador reencontra eventos não confirmados por acesso indexado, sem depender de histórico infinito do stream.

Proposta RunScore: manter contribuição por avaliação e versão processada. Worker compara nova contribuição válida com a anterior e aplica diferença na soma/contagem junto da atualização condicional da contribuição, em transação. Evento antigo/duplicado não altera o agregado. Mudança de edição exige retirar e adicionar às edições correspondentes consistentemente. Concentração de atualizações na mesma edição deverá ser medida; não fazer sharding antes de conhecer contenção.

Meta de 10 s é monitorada desde a alteração persistida até o score consultável. Alarmar atraso e fila de erros; reconstrução deve usar avaliações válidas e ser validada antes de substituir agregado ativo. Arquivo de payload, retenção e reprocessamento ainda requerem definição.

## 7. Critérios mensuráveis propostos para revisão

| Área | Evidência necessária |
| --- | --- |
| Integridade | Concorrência não produz dupla participação, dupla curtida ou mais de 1.000 admitidos. |
| Segurança | Matriz de proprietário/Admin/Moderador, MFA e bloqueios exercitada por testes negativos; dados ocultos ausentes das respostas. |
| Imagens | Formatos e limites aprovados, GPS removido e orientação preservada; pendência/falha não libera conclusão. |
| Latência | Proposta: p95 da validação <=5 s pós-upload e p95 da projeção RunScore <=10 s no perfil de carga acordado. Percentil ainda não aprovado. |
| Carga | Executar 20 req/s esperado e 100 req/s de estresse como hipóteses, medindo latência, erros, consumo e throttling; definir duração e limites aceitáveis antes do teste. |
| Recuperação | Ensaio de restauração com RPO <=5 min e RTO <=4 h nos cenários cobertos, reconciliando dados/imagens e exclusões. |
| Deploy | Mesmos artefatos DEV/PROD, sem chave permanente; aprovação de PROD e reversão demonstradas. |
| Mobile | Jornadas essenciais em dispositivos Android/iPhone, inclusive HEIC e links das lojas; registrar versões testadas. |

Disponibilidade de 99,5% precisa de fórmula e janela. Um RTO de 4 h pode exceder o orçamento mensal de indisponibilidade dependendo da ocorrência; RTO não representa permissão de ficar fora do ar por 4 h. Apresentar esse risco explicitamente antes do beta.

## 8. Recuperação e retenção: separação necessária

Marco de contagem do histórico no lake aprovado: ocorrência original do evento, sem renovação em reenvios/reprocessamentos. O prazo de criação do objeto S3 pode divergir desse marco; desenhar descarte por expiração de negócio, incluindo versões/cópias. Esta definição substitui a pendência anterior da âncora de retenção; tratamento de eventos atrasados além do prazo ainda requer política explícita.

Histórico de avaliações no data lake: retenção de 60 dias aprovada durante o beta, com revisão antes do encerramento; distinta dos 7 dias de recuperação e do histórico ativo sem TTL. Contagem por evento desde ocorrência é proposta técnica, ainda a formalizar junto do descarte e do atendimento à exclusão de dados pessoais. Não configurar retenção imutável ou extensão indefinida por inferência.

Pergunta técnica 37 respondida: participações, avaliações e medalhas sem TTL, preservadas até exclusão pelos fluxos aprovados. Não propagar essa regra a eventos, controles temporários ou todos os dados pessoais. Configuração TTL por tipo de item e política dos demais agregados ainda serão detalhadas.

Pergunta técnica 36 respondida: recuperação conjunta de participações, avaliações e medalhas aprovada. Reconciliar com imagens no S3, dados de edição e identidade necessários para o histórico. Não interpretar como restauração seletiva nativa de itens nem como escolha automática de tabela; procedimento físico e validação continuam pendentes. Essa decisão substitui a pendência de recuperação conjunta descrita anteriormente neste documento.

Pontos de recuperação por 7 dias não significam conservar dados pessoais por 7 dias nem garantem RPO/RTO automaticamente. Validar cobertura DynamoDB, S3, Cognito, configurações e trilhas de exclusão. Restauração do banco não restaura usuários Cognito nem objetos removidos. Restauração regional completa não foi aprovada. Escolher mecanismos apenas após inventário e estimativa.

## 9. Orçamento — entrega ainda pendente

O documento de premissas já permite iniciar orçamento; preços oficiais de São Paulo ainda precisam ser coletados e aplicados. Não existe total mensal calculado nem teto aprovado. Não apresentar volume lógico como unidades faturáveis DynamoDB. Separar DEV/PROD, armazenamento acumulado, mês de entrada e estabilizado, transferência, workers, logs, identidade e pipeline. Usar valores sem créditos, indicando elegibilidade de gratuidades separadamente.

## 10. Sequência de fechamento

Progresso de 27/10/2026: contratos de participação ampliados no OpenAPI e contrato JSON Schema de auditoria preparado. Fluxo do lake e descarte documentados no complemento DATA-LAKE-AVALIACOES-RunPass-v1.md; orçamento inclui sensibilidade de ingestão/S3. Catálogo, perfis, social e administração ainda não têm contratos completos; acesso ao lake, exceções de retenção e execução de testes permanecem pendentes. Não interpretar a ampliação como SPEC ou API integralmente concluída.

1. Confirmar parâmetros operacionais dos agregados antes de escolher tabelas.
2. Produzir esquema DynamoDB rastreável à matriz, OpenAPI e contratos versionados dos eventos.
3. Validar consultas de feed/catálogo, integridade e integração FastAPI–Lambda por prova técnica isolada, sem provisionar recursos sem autorização aplicável.
4. Calcular orçamento, resolver retenção e concretizar os critérios de aceite.
5. Revisar e aprovar tecnicamente a SPEC; só então marcar slices como prontos para implementação.

Não repetir as 35 perguntas nem tratar este pacote DRAFT como aprovação. A skill DynamoDB foi consultada em modo de desenho; não foram executados deploy, benchmark pago ou scripts de destruição.
