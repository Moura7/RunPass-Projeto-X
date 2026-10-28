# SPEC — RunPass MVP — referência única

Atualização: 27/10/2026. Estado: **direções prioritárias aprovadas pelo usuário; detalhamento e desenvolvimento incremental autorizados no escopo abaixo**.

Arquivo canônico: **SPEC_RunPass_MVP_v1.md**. Por decisão do usuário, existe uma única SPEC ativa. O conteúdo consolidado foi incorporado neste arquivo; a tentativa de v2 foi incorporada sem manter um segundo arquivo ativo. O registro anterior foi preservado em historico/REGISTRO-TECNICO-ANTERIOR-2026-10-27.md, sem vigência concorrente.

## Decisão de aprovação e primeira entrega

O usuário aprovou as três direções apresentadas e a manutenção de uma única SPEC:

1. **Dados:** DynamoDB sob demanda, agrupando participação, avaliação e medalha; separar os demais domínios conforme padrões de acesso e necessidades operacionais. Engenharia detalha tabelas, chaves, índices e transações sem exigir aprovação de cada atributo. A aprovação não fixa automaticamente as seis tabelas candidatas da seção 6.
2. **Eventos:** outbox persistida na mesma transação da alteração, entrega via SQS e consumidores protegidos por versões/idempotência; replay de sete dias e reconstrução de projeções antigas pelo estado atual, conforme política já aprovada.
3. **Identidade:** Cognito com separação entre corredores e operadores; MFA por aplicativo autenticador para administração, autorização na API e permissões por função.

Primeira entrega autorizada para detalhamento e desenvolvimento técnico: **autenticação → catálogo → rascunho → imagem → conclusão → avaliação e medalha**. Não autoriza provisionamento pago ou release. Detalhes locais e reversíveis de implementação podem prosseguir; orçamento autorizado é condição antes de criar recursos pagos.

Painel completo, feed, pós-beta e detalhes operacionais devem ser resolvidos antes das respectivas entregas. Segurança, restauração, desempenho e privacidade precisam de evidências antes do beta. Requisitos não implementados não voltam automaticamente à condição de não aprovados. Não criar nova SPEC para mera reorganização.

## 1. Problema e resultado esperado

Corredores precisam descobrir provas, registrar experiências concluídas, organizar medalhas e compartilhar avaliações e conquistas. O MVP deve validar adesão, repetição e interação com até mil corredores, sem exigir arquitetura de produção futura completa no primeiro lançamento.

Aplicativo Flutter/Dart para Android e iPhone, backend Python/FastAPI em Lambda, armazenamento operacional DynamoDB e operação inicial na AWS São Paulo. Não há site público para corredores no MVP. A equipe RunPass mantém catálogo e moderação por interface administrativa.

## 2. Estado das decisões e execução incremental

- **A — aprovado:** decisões anteriores e as três direções registradas acima.
- **P — proposta de detalhamento:** candidato técnico que Engenharia pode refinar no escopo aprovado. Alternativas com impacto real de produto, custo ou privacidade voltam à decisão do usuário.
- **B — dependência técnica:** resolver antes de implementar ou liberar a parte afetada; não bloqueia indiscriminadamente todo o projeto.
- **L — condição de liberação:** configuração, teste ou evidência necessária antes de PROD/beta.

As propostas P01–P09 e dependências B01–B06 abaixo foram preservadas para rastreabilidade. Não constituem uma nova rodada obrigatória de nove aprovações. As direções de DynamoDB on-demand, outbox/SQS e Cognito/MFA já estão aprovadas; quantidades físicas, parâmetros novos e escolhas além dessas direções não foram aprovados por inferência. A autorização de desenvolvimento não comprova testes nem libera produção.

## 3. Fontes e precedência

Base: PRD_RunPass_MVP_v2.md, decisões de Grill-me e confirmações posteriores, preservadas no registro histórico, MATRIZ-APROVACOES-M4-RunPass.md e documentos de retenção/eventos. Decisão explícita posterior prevalece sobre uma pendência histórica anterior.

O contrato API-RunPass-v1.openapi.json está em 0.7.0-draft, com 55 caminhos e 71 operações. Sua validação estrutural não comprova implementação. MODELO-DYNAMODB-RunPass-v1.md continua parcial; o desenho candidato desta revisão não o transforma em modelo físico homologado.

Referências complementares: EVENTOS-E-REPLAY-RunPass-MVP.md; DATA-LAKE-AVALIACOES-RunPass-v1.md; RETENCAO-E-EXCLUSAO-RunPass-MVP.md; RETENCAO-DENUNCIAS-E-AUDITORIA-RunPass.md; RETENCAO-TECNICA-RunPass-MVP.md; UPLOAD-ADMINISTRATIVO-MEDALHAS-RunPass.md; FECHAMENTO-TECNICO-RunPass-MVP.md; ORCAMENTO-RunPass-preliminar.md e respectiva simulação.

## 4. Requisitos de produto consolidados — A

### 4.1 Catálogo e solicitações

Catálogo por prova e edição, com distâncias próprias. Cobertura inicial das principais corridas de São Paulo capital, dois anos de histórico e provas futuras. Meta de cobertura de 90% usa a referência inicial documentada de provas, não mínimo arbitrário de edições.

Equipe RunPass gerencia catálogo; corredor solicita provas ausentes, com nome, data, cidade e distância. Duplicatas são vinculadas à edição existente após revisão humana. Rascunhos são preservados; solicitação aceita não conclui automaticamente a participação. Organizador é referência de catálogo, sem login ou portal B2B.

Arquivar edição impede novas conclusões e transferências para ela, preserva histórico e permite editar/excluir participações já concluídas. Alterações em distâncias não podem invalidar referências existentes silenciosamente.

### 4.2 Participação, avaliação e medalha

Uma participação por usuário/edição, somente de prova concluída por autodeclaração. Antes de concluir, pode manter rascunho. Conclusão exige oito notas de 1 a 5 e imagem de medalha disponível; comentário de avaliação é opcional.

Critérios: organização, percurso, kit, medalha, hidratação, estrutura, segurança e custo-benefício. RunScore é a média com pesos iguais, por edição, apresentado com uma casa decimal; avaliações podem ser filtradas por distância. Avaliação invalidada não contribui ao score; decisão de moderação não exclui automaticamente toda a conquista.

O proprietário pode editar ou excluir seu cadastro, respeitando unicidade e controle de versão. PUT da avaliação substitui as oito notas; omitir comentário remove o comentário atual e gera histórico restrito antes/depois. Alterar edição exige verificar duplicidade e ajustar contribuições/projeções.

Medalha é adicionada automaticamente na conclusão. Usa imagem oficial vigente ou foto própria obrigatória quando ela não existe. Foto própria não é promovida automaticamente ao catálogo. Cada medalha guarda a versão oficial vinculada; trocar a imagem do catálogo só afeta novos vínculos. Correção retroativa é ação separada, explícita e auditada.

### 4.3 Social e privacidade

Feed de conquistas e medalhas; sem feed genérico de fotos livres. Publicações de outros usuários são visíveis conforme autorização; usuários seguidos têm prioridade de ordenação, com recência dentro dos grupos. Curtidas, comentários, seguir, busca de perfis e wishlist integram o MVP.

Perfil público mostra dados de corrida/conquistas; e-mail e nascimento permanecem privados. Publicações e wishlist começam visíveis, podendo ser ocultadas. Tempo e colocação podem ser ocultados; ocultar tempo também oculta pace em todas as superfícies. API não devolve campos ocultos apenas porque o cliente os esconde.

Bloqueio oculta interações existentes e remove follows nos dois sentidos, sem apagar indiscriminadamente o histórico. Novas interações são impedidas enquanto existir bloqueio em qualquer direção. Desbloqueio não recria follows. Visibilidade e exclusões atuais prevalecem sobre índices/projeções atrasados.

### 4.4 Beta e feedback

Instalação nas lojas oficiais, como no produto futuro. Beta no ambiente PROD, até mil admitidos únicos, por 60 dias desde o 50º admitido. Admissão exige e-mail confirmado e idade mínima de 18 anos por autodeclaração/data de nascimento; não exigir documento por inferência. Exclusão não reabre vaga automaticamente. Excedentes podem entrar voluntariamente em lista de espera, sem acesso automático.

Ativo: pelo menos uma participação concluída com cadastro completo. Metas: ativação de 50% dos admitidos reais; repetição em outra edição de 30% dos ativados; interação social de 30% dos ativados. Cadastros de espera não integram denominadores. Contas técnicas não devem contaminar a coorte de corredores.

Feedback voluntário após primeiro registro, canal contínuo, pesquisa aos 30 dias e fechamento aos 60; revisão semanal. Resultados e privacidade devem respeitar correções/exclusões sem duplicar ativação por recriação.

## 5. Arquitetura e fronteiras

### 5.1 Decisões consolidadas — A

Python apenas no backend; Flutter/Dart mobile; FastAPI em Lambda; DynamoDB como direção de armazenamento; CloudFormation; região sa-east-1; DEV e PROD em contas distintas. Backend modular por domínio, sem exigir um microsserviço por módulo.

GitHub Actions com OIDC e papéis temporários separados por conta; pull request, testes e revisão humana antes de main. Promover os mesmos artefatos validados em DEV, com configuração por ambiente e aprovação manual separada de PROD.

### 5.2 Pacote proposto — P01

API Gateway HTTP como entrada; Cognito User Pools para identidade; Lambda para API, processamento e manutenção; DynamoDB on-demand (aprovado); S3 privado para arquivos; Streams como sinal e SQS com consumidores separados por finalidade; CloudWatch para observabilidade. Sem Aurora, OpenSearch, EventBridge geral, NAT ou CDN por padrão nesta linha de base. Adição posterior exige justificativa e atualização de custo.

Separar buckets/prefixos e papéis para originais temporários, imagens tratadas, histórico de avaliações e evidências. Acesso mobile sempre mediado pela autorização da API; não dar acesso direto às tabelas. Downloads por URLs temporárias autorizadas, com risco de validade residual explicitado.

O histórico de avaliações é uma camada informacional limitada, não plataforma analítica geral. Consulta administrativa mediada por índice de avaliação/período e objetos S3, sem introduzir Athena/Glue/Firehose automaticamente.

## 6. Dados: direção aprovada e desenho candidato — P02

A diretriz é agrupar dados relacionados e separar necessidades operacionais diferentes, sem impor single-table para toda a aplicação. Propõem-se seis fronteiras físicas por ambiente, revisáveis antes de CloudFormation. Nomes são ilustrativos, sem recursos criados.

| Tabela candidata | Conteúdo relacionado | Acesso principal e motivo |
| --- | --- | --- |
| IdentityAccess | Estado da conta, perfil, reserva de username, papéis, admissão/espera | Autorização atual, unicidade e teto transacional; dados privados segregados por tipo de item e IAM |
| RaceCatalog | Provas, edições, distâncias, organizadores e solicitações | Consultas de catálogo e revisão pela equipe; retenção independente do histórico do corredor |
| RunHistory | Participação, avaliação, medalha e rascunho | Agrupamento relacionado aprovado, recuperação conjunta e histórico sem TTL |
| Social | Publicação, comentário, like, follow/block, wishlist e avisos | Relações e enumeração por proprietário/alvo para privacidade e limpeza |
| Operations | Outbox, entregas, idempotência, jobs, sessões e referência de exclusão | Ciclos de vida técnicos explícitos; pendências recuperáveis, sem TTL genérico |
| Projections | Contribuição de avaliação, RunScore e feed materializado | Dados derivados reconstruíveis; controle de geração/versão separado da fonte |

Cada tabela usa PK/SK compostas; dados pessoais não entram em nomes de recursos ou chaves externas. Exemplo RunHistory: PK USER#id; SK EDITION#editionId#PARTICIPATION, REVIEW ou MEDAL. Rascunhos têm ID independente. Lookup por participationId aponta ao dono/edição. Não armazenar bytes de imagem no DynamoDB.

| Acesso | Estratégia candidata | Exigência antes de implementar |
| --- | --- | --- |
| Perfil exato e username único | Chave por usuário e reserva condicional de username | Definir normalização e busca por prefixo sem varredura global |
| Histórico/medalheiro | Partição do usuário e índice por data de conclusão | Paginação e verificação atual de visibilidade |
| Reviews por edição/distância | GSIs por edição e edição/distância, ordem temporal | Revalidar moderação, medir concentração e tamanho |
| Catálogo | Itens de índice explícitos por cidade/período e distância; índice de prefixos normalizados de título | Fixar combinações de filtro e medir leituras; não prometer busca arbitrária |
| Social e limpeza | Arestas por origem e índice inverso por alvo/proprietário | Enumerar referências para exclusão sem scan global |
| Admissão | Contador/registro de admitido em transação condicional | Concorrência no 50º/1.000º e não reabrir vagas por exclusão |
| Pendências e expiração | Índice por estado, shard e data; rechecagem na fonte | Leases e consulta paginada; índice atrasado não é fonte de autorização |
| Feed | Caixa de entrada por leitor com referências mínimas e ordenação em dois grupos | Prova de completude, mudança de follow e custo de fan-out |

Transações podem atravessar tabelas no mesmo ambiente/região, respeitando limites do serviço; isso não dá restauração conjunta automática. Restauração das fontes, controles e imagens exige runbook e reconciliação antes de reabrir tráfego.

**B01:** detalhar PK/SK/GSIs e itens de índice de catálogo/feed, consultas de cada combinação do OpenAPI, e a distribuição de carga. P02 é proposta de fronteiras, não prova de que todos os acessos estão resolvidos. Comparar fan-out do feed com alternativa de consultas limitadas antes de fixar a implementação. O usuário não precisa aprovar cada nome de atributo.

## 7. Integridade, transações e eventos

### 7.1 Invariantes — A

Não duplicar participação por usuário/edição, like por ator/publicação ou admissão. Versão esperada impede sobrescrita silenciosa. Ator vem da identidade autenticada. Conteúdo pendente, oculto, arquivado ou excluído não se torna publicável por uma projeção antiga.

### 7.2 Outbox/SQS aprovados e detalhamento — P03

Conclusão grava participação, review e medalha, conversão do rascunho quando aplicável, idempotência e outbox em transação com condições de unicidade, conta ativa e versão/estado da edição. Edição concorrente de catálogo deve provocar conflito/revalidação, não conclusão com dados inconsistentes.

Outbox durável em Operations na mesma transação da alteração de negócio. Streams apenas acorda publicador; reconciliador consulta pendências duráveis. Publicador encaminha por destino; falha após envio pode duplicar. Não declarar entrega aplicada apenas porque a fila aceitou.

Envelope: eventId, eventType, schemaVersion, aggregateId, aggregateVersion, occurredAt UTC, correlationId, payload mínimo. Payload de auditoria antes/depois fica separado do evento para score/feed. Nunca incluir nascimento, credenciais ou imagem binária.

Cada consumidor registra versão/contribuição com escrita condicional e, quando possível, na mesma transação do efeito. RunScore guarda contribuição válida por review: calcula diferença para somas/contagem anteriores e registra a versão aplicada. Evento antigo não reaplica contribuição; exclusão ou invalidação retira contribuição. Edição do destino corrige ambos os agregados. Reconstrução é isolada por geração e conciliada com mudanças concorrentes antes de promoção.

Replay de concluídos por até sete dias — A; propõe-se contar desde a última confirmação obrigatória, sem renovar por replay. Pendências permanecem recuperáveis, respeitando exclusões e expiração específica. Reconstruções mais antigas usam fontes atuais. Operação interna registra ator, motivo, seleção e resultado.

**B02:** fixar janela efetiva dos controles de deduplicação e exclusões após definir replay/restauração/transporte. Não assumir que TTL de sete dias cobre entregas em curso ou dados restaurados. Não impor retenção pessoal maior para simplificar controles. Após replay vencer, recusar execução histórica e orientar reconstrução; nunca recriar conteúdo excluído.

## 8. Identidade e autorização

### 8.1 Regras — A

Corredor: e-mail/senha; proprietário altera seus dados. Administrador gerencia catálogo/solicitações/acessos; Moderador atua em denúncias/conteúdo. Ambos exigem MFA. Administrador não recebe moderação ou consulta do lake automaticamente. Consulta do lake exige autorização específica e auditoria.

Conta excluída deve perder acesso à API mesmo com token emitido. Bloqueios são bilaterais na autorização de novas interações. Identidade autenticada sem admissão só acessa bootstrap e exclusão previstos no contrato. Operação administrativa não consome vaga de corredor.

### 8.2 Cognito/MFA aprovados e detalhamento — P04

Cognito segregado por ambiente e pools distintos para corredores e operadores; TOTP obrigatório no pool administrativo. Separar clients, audiences e papéis; API verifica issuer/audience/token e fluxo administrativo autenticado, além de papel/estado atual na fonte. Não inferir MFA de um JWT qualquer nem confiar em indicação enviada pelo frontend.

Bootstrap de operador por procedimento restrito de infraestrutura, sem cadastro público. Recuperação de MFA exige verificação e trilha operacional; não oferecer bypass por endpoint público. Propor ao menos dois operadores recuperáveis antes de PROD para evitar dependência de uma pessoa. Matriz de consulta de auditoria e replay usa permissões específicas.

**B03:** detalhar evidência confiável do fluxo MFA, recuperação, revogação e identidade dos responsáveis pelo bootstrap. Validar o plano Cognito escolhido e o custo, sem tratar a hipótese Lite do orçamento como aprovação. Política IAM e segredos não são criados por este documento.

## 9. Imagens e painel

### 9.1 Imagens — A

JPEG/PNG, original até 10 MB; meta de otimização até 1 MB. Servidor valida formato real, tamanho e decodificação, remove GPS e preserva orientação. Validação com meta de cinco segundos pós-upload; pendente não significa válida. Não servir original não tratado a terceiros.

Sessões administrativas vinculam edição/distância e ambiente. Upload não publica. Após prévia, PATCH versionado confirma referência administrativa validada, sem aceitar upload pessoal de terceiro. Versões anteriores referenciadas são preservadas. URL de upload: 15 minutos.

### 9.2 Propostas — P05

Converter HEIC no dispositivo para formato aceito antes do envio, com teste em iPhone real. Se conversão falhar, informar e preservar rascunho; não declarar suporte HEIC servidor. Limitar decodificação a 25 megapixels por imagem como proteção inicial proposta, com UX de redução local; validar fotos típicas antes de fixar. Downloads autorizados por URL de cinco minutos e sem cache público de conteúdo ocultável; validade residual deve constar no teste/experiência, sem promessa de revogação instantânea de URL já emitida.

Painel Flutter Web como proposta técnica, hospedagem estática privada na operação de administração ou pública apenas para o shell sem dados, com backend protegido. Escolher hospedagem após prova de login/MFA, formulários, uploads e acessibilidade; não acrescentar um site público de corredores.

**B04:** fechar hospedagem/painel, tratamento de filtros/limites e operação retroativa da imagem antes das respectivas entregas. Teste de HEIC, metadados, concorrência e preservação de versões é condição L, sem reaprovar formatos já aceitos.

## 10. Retenção e exclusão: referência consolidada

| Categoria | Estado/regra |
| --- | --- |
| Histórico ativo | A: sem TTL; exclusão pelos fluxos previstos |
| Conta excluída | A: bloqueio/ocultação imediatos; remover dados pessoais ativos em até sete dias, inclusive lake |
| Lake de avaliações | A: 60 dias desde ocorrência original, sem renovação por replay; exclusão de conta prevalece |
| Recuperação | A: sete dias no beta, independente dos dados ativos; reaplicar exclusões na restauração |
| Denúncia aberta | A: enquanto necessária, revisão semanal; não deixar sem acompanhamento indefinidamente |
| Denúncia encerrada/evidência necessária | A: até 60 dias do encerramento |
| Auditoria administrativa | A: até 90 dias da ação |
| Logs DEV/PROD | A: sete/30 dias; minimização e exclusão pessoal continuam obrigatórias |
| Idempotência de comando | A: sete dias desde primeira aceitação durável |
| Payload entregue | A: sete dias desde última confirmação obrigatória, não define ledger |
| Temporário abandonado | A: limpar até 24 horas após expiração da sessão, sem apagar trabalho ativo |
| Validada nunca vinculada | A: sete dias desde validação, limpar até 24 horas depois; checar referências |

**P06:** bloquear consulta de lake/denúncia/auditoria no vencimento e remover cópias operacionais elegíveis em até 24 horas depois. Auditoria de avaliação ainda pendente ao vencer deve ter payload pessoal descartado com registro mínimo de expiração/falha, sem falsa confirmação de entrega. Evento operacional de score continua independente.

**B05:** definir controle mínimo de exclusões e retenções restantes de rascunhos, espera, solicitações e feedbacks; política de nascimento; comprovar que logs e filas permitem cumprir exclusão pessoal. Não armazenar dados indefinidamente sob pretexto de pendência, backup ou auditoria. Backups não são prometidos como removidos em 24 horas; versões e cópias são inventariadas.

## 11. Contratos e testes

### 11.1 Contrato HTTP

OpenAPI 0.7.0-draft cobre conta/beta, perfis, catálogo, participação/review, uploads comuns e administrativos, social, wishlist, notices, solicitações, moderação e administração. PUT de review é substituição; PATCH é alteração parcial; DELETE aceita remoção e não afirma limpeza de todas as cópias. Cognito tem fluxo de login próprio, não endpoints fictícios no backend.

Erros, idempotência, versão, parâmetros e schemas existentes são a base de revisão. **P07:** aprovar a linha de base contratual condicionada a revisão por jornada; ajustes incompatíveis exigem versão/migração. Limites de texto e paginação devem ser fixados no contrato antes de gerar cliente definitivo. Não interpretar extensões x-required-role/x-requires-mfa como segurança executável.

### 11.2 Critérios mensuráveis propostos — P08

| Área | Proposta de aceite e evidência L |
| --- | --- |
| Integridade | Testes concorrentes sem participação/like/admissão duplicados; sem perda de outbox confirmada |
| Segurança | Testes negativos de proprietário, papéis, MFA, bloqueios e token anterior à exclusão; dados ocultos ausentes das respostas |
| Latência | p95 da validação de imagem até 5 s pós-upload; p95 RunScore até 10 s pós-commit, no cenário de carga acordado |
| API | Separar endpoint crítico de processamento assíncrono; medir média abaixo de 500 ms e p95 abaixo de 1 s para operações leves, sem contar transferência de arquivo |
| Carga | Patamar de 20 req/s por 30 min, mistura versionada de jornadas; estresse de 100 req/s por 10 min, com limitação controlada e sem corrupção/perda |
| Falhas | Menos de 1% de erros 5xx no ensaio esperado; respostas de validação deliberadamente inválidas fora dessa conta; identificar toda limitação 429 |
| Disponibilidade | Meta anterior de 99,5%; propor janela mensal por jornada sintética, contando indisponibilidade percebida inclusive manutenção planejada; RTO não é franquia de queda |
| Recuperação | Ensaio de RPO até 5 min e RTO até 4 h nos cenários cobertos, com exclusões reaplicadas, dados e imagens coerentes |
| Mobile | Jornadas essenciais em Android/iPhone reais, formatos de foto, privacidade e instalação pelas lojas; fixar modelos/versões testados |

P95, duração, mistura e limiares adicionais são propostas novas, não metas históricas aprovadas por inferência. Carga de mil inscritos não significa mil simultâneos. RTO depende de cenário e pode consumir mais que o orçamento mensal de disponibilidade; avaliar ambos separadamente.

## 12. Orçamento, operação e liberação

Premissas A: 20 medalhas/usuário, 300 usuários/dia, duas sessões/dia e 30 imagens/sessão. Estimativa existente é sensibilidade parcial baseada nas tarifas coletadas em 26/10/2026; não atualizada por esta consolidação.

Subtotal registrado: DEV US$ 3,07/mês e PROD esperado US$ 26,91/mês; soma modelada US$ 29,98/mês, antes das exclusões. Não é proposta de teto. Não usar US$ 29,98 como custo completo nem aplicar os valores automaticamente às seis tabelas candidatas ou à nova solução de identidade.

**B06:** recalcular por operações/tamanhos/índices, incluir outbox/ledger, jobs, S3 versões/limpeza, consulta/auditoria, logs completos, alarmes, identidade/painel, pipeline, tráfego API, lojas e demais exclusões; apresentar limite autorizado antes de provisionar. Não há orçamento aprovado.

Alertas críticos por e-mail à equipe RunPass — A. **L:** nomear principal/substituto e cobertura, testar recebimento/escalonamento, documentar falhas, replay, restore, rollback e exclusão. Endereço operacional fora do repositório. Antes de PROD: acessos, lojas, política de dados, testes essenciais, custo autorizado e aceite de release.

## 13. Encerramento do beta — proposta P09

Ao fim dos 60 dias, não apagar contas automaticamente nem ampliar vagas. Propor manter acesso dos admitidos e congelar novas admissões até revisão de resultados pela equipe RunPass; preservar lista de espera conforme política de retenção a fechar. Aprovar explicitamente a continuidade operacional e seu orçamento: a duração da avaliação não encerra custos nem obrigações por si só.

O aplicativo continua distribuído pelas lojas oficiais. Alteração de faixa etária, monetização, site público ou expansão de capacidade exige evolução específica; não faz parte desta proposta.

## 14. Plano de execução da primeira entrega

1. Detalhar apenas os acessos, chaves e transações de identidade, catálogo e histórico necessários ao fluxo inicial; adaptar o modelo DynamoDB existente. Fechar a deduplicação/versão e o controle de exclusões dos consumidores envolvidos. Feed completo não bloqueia essa modelagem inicial.
2. Atualizar os contratos existentes para esse fluxo, especificar autenticação/autorizações e preparar testes locais de unicidade, versão, imagem, transação/outbox e replay.
3. Preparar implementation-slices.md para a primeira entrega, com dependências e critérios de aceite. Organizar contexto/regras/harness antes da execução; não marcar uma dependência não resolvida como concluída.
4. Desenvolver e revisar por entrega. Antes de provisionar DEV, concluir orçamento aplicável e obter autorização de custo. Antes do beta, cumprir condições de liberação, fechar políticas necessárias e revisar resultados de testes.

**Aprovação registrada:** direções prioritárias e desenvolvimento incremental do fluxo inicial. **Pendente:** detalhamento dos pontos técnicos da entrega e aceite posterior dos resultados. Não é necessário reaprovar as mesmas direções; aprovação de todo o MVP e autorização de PROD não são presumidas.

## 15. Fora do MVP e pontos de extensão

Fora: rastreamento GPS/treinos, chat/stories, ranking competitivo, clubes, monetização, integrações esportivas, portal de organizadores, analytics avançado e site público para corredores. Notificações do produto inicialmente internas; push futuro. Compartilhamento usa cards gerados localmente com dados autorizados.

Evolução por contratos versionados, fronteiras de módulos e projeções reconstruíveis. Separar serviço, banco ou consumidor quando carga, isolamento ou operação justificarem; não prometer escalabilidade sem medir hot keys, fan-out, custo e limites.

## 16. Referências técnicas consultadas nesta revisão

- [DynamoDB: limites e transações](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Constraints.html): transações têm limites e não atravessam contas/regiões.
- [DynamoDB: TTL](https://docs.aws.amazon.com/us_en/amazondynamodb/latest/developerguide/TTL.html): expiração não representa descarte físico imediato; trabalhos com prazo precisam de desenho próprio.
- [Cognito: TOTP MFA](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-mfa-totp.html): base para a proposta de segundo fator; integração e recuperação precisam de validação.

Registro de aprovação: usuário respondeu **“Aprovado! vamos utilizar uma única SPEC”**, aprovando as três direções e a primeira entrega descritas no início. Não há aprovação de terceiros presumida. Identificação de responsáveis técnicos, aceite de implementação e liberação de PROD serão registrados separadamente. Esta decisão não cria evidência de reuniões ou gates corporativos não realizados.

## Plano da primeira entrega preparado

implementation-slices.md detalha S00–S09 para o fluxo aprovado: preparação local/contexto/harness, desenho de dados e contratos, identidade/admissão, catálogo, rascunho, imagem, conclusão/avaliação/medalha, consumidores/RunScore/histórico restrito, edição/exclusão e integração real em DEV. Cada slice tem dependências e critérios de aceite. S00 pode iniciar; os seguintes dependem das saídas anteriores. Provisionamento DEV depende de orçamento e autorização; release PROD/beta não é autorizado por esse plano. Não há implementação/testes de execução concluídos nem nova SPEC criada.