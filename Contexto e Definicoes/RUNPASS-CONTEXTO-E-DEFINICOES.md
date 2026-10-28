# RunPass — Contexto, decisões e retomada

Registro consolidado da descoberta de produto. Atualizado em 20/10/2026 após as 20 perguntas finais.

## Estado da iniciativa

- Entrevista encerrada: as 20 perguntas adicionais foram respondidas. Não abrir novas rodadas de perguntas sem solicitação do usuário.
- Método: entrevista grill-me, uma pergunta por vez, em conjunto com a SKILL-PDLC.
- Existe um PRD inicial. As decisões abaixo foram confirmadas na conversa, mas ainda não foram incorporadas ao PRD original.
- Este documento registra decisões de produto; não representa aprovação formal de gates do PDLC. Não há evidência registrada de aprovação de M0–M3.
- Não houve implementação do produto nesta sessão.

## Fontes e localização

- PRD inicial: `C:\Users\rmfig\OneDrive\Documentos\Produto X - RedeSocial\PRD_RunPass_MVP.md`.
- PDLC: `C:\Users\rmfig\OneDrive\Documentos\Produto X - RedeSocial\SKILL-PDLC.md`.
- Grill-me: `C:\Users\rmfig\OneDrive\Documentos\Produto X - RedeSocial\Grill-me-codex`.
- Este registro foi salvo no workspace atual, `Pipeline de Dados - Camada Bronze`, que é diferente da pasta dos documentos do produto.
- A leitura das skills não equivale à sua instalação. A tentativa anterior de instalar via npx falhou porque o comando não estava disponível.

## Propósito e plataformas

- RunPass será uma rede social para praticantes de corridas de rua.
- A proposta central é cadastrar corridas concluídas e medalhas, avaliar experiências e trocar essas informações com outros corredores.
- Aplicativo compatível com Android e iPhone.
- Um site também está sendo considerado; seu papel e escopo ainda não foram definidos.
- As primeiras interações devem ocorrer principalmente entre corredores que já se conhecem.
- Deve existir uma área própria para descobrir corridas disponíveis.

## Base funcional do PRD

O item 3 do PRD define como objetivo validar o interesse em manter um histórico social de experiências em provas. A jornada contempla criar conta e perfil, encontrar corrida, registrar participação e resultado, avaliar, adicionar medalha, consultar histórico, salvar provas futuras e compartilhar conquistas.

O PRD continua sendo uma base inicial. Propostas nele contidas que não foram discutidas não devem ser tratadas como decisões confirmadas nesta entrevista.

## Decisões confirmadas

### Catálogo e descoberta

- A equipe RunPass será responsável pelo cadastro e pela atualização das provas no MVP.
- Integrações automáticas com IA ficam para o futuro.
- Não será obrigatório ter 500 provas antes de lançar o beta.
- O catálogo inicial deve cobrir as principais corridas de São Paulo capital.
- A cobertura histórica inicial será de dois anos.
- Provas mais antigas também poderão ser cadastradas pelos usuários e submetidas à revisão da equipe RunPass.
- Qualquer prova cadastrada por usuário precisa ser aprovada antes de aparecer no catálogo público.
- Para provas ausentes, o usuário poderá iniciar o cadastro e salvar sua participação como rascunho enquanto aguarda a revisão.
- A participação vinculada permanecerá como rascunho até a aprovação da prova.
- A lista objetiva das principais corridas e as datas exatas da janela de dois anos ainda não foram definidas.

### Participação e edição da prova

- Só serão registradas participações em provas concluídas no MVP.
- A conclusão será declarada pelo próprio corredor, sem comprovante obrigatório.
- O tempo será opcional.
- Cada corredor poderá ter apenas uma participação por edição.
- Uma nova participação deverá corresponder a outra edição, no mesmo ano ou em outro.
- O usuário poderá editar completamente e excluir seus próprios registros, inclusive corrigir a edição da prova selecionada.
- A exclusão da participação removerá a avaliação e a medalha vinculadas e recalculará o RunScore.

### Medalheiro

- A medalha será adicionada automaticamente durante o registro de conclusão.
- Será utilizada a imagem da medalha disponível no catálogo.
- Se a imagem não estiver disponível, o usuário poderá carregar uma foto da medalha.
- A foto enviada ficará vinculada apenas ao registro do usuário e não alterará automaticamente o catálogo público.

### Avaliações e RunScore

- A avaliação será obrigatória para concluir o registro da participação.
- Os oito critérios são obrigatórios, cada um com nota de 1 a 5 estrelas:
  1. Organização.
  2. Percurso.
  3. Kit.
  4. Medalha.
  5. Hidratação.
  6. Estrutura.
  7. Segurança.
  8. Custo-benefício.
- Haverá uma caixa de texto para comentário opcional na avaliação.
- Cada edição terá suas próprias avaliações e seu próprio RunScore; notas de edições distintas não serão misturadas.
- Cada edição terá um RunScore geral, com avaliações filtráveis pela distância registrada.
- A nota de cada avaliação será a média simples dos oito critérios.
- O RunScore será a média simples das avaliações da edição, com o mesmo peso para todos os critérios e corredores.
- O resultado será exibido com uma casa decimal.
- O usuário poderá editar a avaliação após publicá-la; as novas notas substituirão as anteriores no cálculo.
- A edição ou exclusão dos registros deverá manter o RunScore consistente.

### Feed e interações sociais

- O feed deve existir no MVP, inicialmente focado em conclusões de corridas e fotos das medalhas.
- Um feed de fotos livres dos usuários não será prioridade.
- Curtidas e comentários serão permitidos.
- O feed incluirá publicações de participantes das mesmas edições que o usuário concluiu ou marcou como “Quero correr”.
- Publicações dos usuários seguidos terão prioridade.
- O feed também exibirá todas as conquistas dos usuários seguidos, independentemente de terem provas em comum.
- A ordem exata e a regra de priorização ainda não foram detalhadas.
- A geração automática de uma única publicação por conclusão foi recomendada, mas não recebeu confirmação explícita; permanece em aberto.

### Perfil e visibilidade

- Os perfis serão públicos.
- A exposição deve se limitar a informações voltadas às corridas e conquistas, preservando dados sensíveis e de cadastro.
- O usuário poderá ocultar o tempo e a colocação.
- O conjunto exato de campos públicos ainda precisa ser confirmado.
- Ainda não foi definido se a ocultação será configurada por participação ou globalmente.
- Aplicar a ocultação também ao feed e aos cards foi uma recomendação, ainda sem resposta explícita.
- O pace pode revelar o tempo em conjunto com a distância; o tratamento dessa informação ainda precisa ser discutido.

## Termos utilizados

- **Corrida/prova:** evento esportivo listado no catálogo.
- **Edição:** ocorrência específica de uma prova; pode haver mais de uma no mesmo ano. É a unidade de participação e consolidação das avaliações.
- **Participação:** registro de uma prova concluída, declarado pelo corredor, limitado a um por corredor e edição.
- **Rascunho:** participação ainda não publicada, incluindo a vinculada a uma prova aguardando aprovação.
- **RunScore:** nota consolidada da edição, calculada a partir das avaliações dos participantes.
- **Quero correr:** indicação de interesse em uma edição futura, usada também para selecionar conteúdo do feed.

## Ajustes necessários no PRD original

- Promover feed, acompanhamento de corredores, curtidas e comentários para o escopo do MVP conforme as decisões acima. No original, parte dessas funções estava em P1/P2.
- Substituir a meta obrigatória de 500 provas por cobertura das principais corridas de São Paulo capital, com dois anos de histórico.
- Incluir cadastro de provas por usuários, revisão administrativa e rascunhos de participação.
- Especificar conclusão autodeclarada, tempo opcional e limite de uma participação por edição.
- Detalhar medalha automática e foto alternativa restrita ao usuário.
- Tornar explícitas a obrigatoriedade dos oito critérios e a opcionalidade do comentário.
- Formalizar o cálculo, a separação por edição e os filtros por distância do RunScore.
- Incluir edição e exclusão dos próprios registros e seus efeitos nos dados derivados.
- Definir visibilidade dos resultados e regras do feed.
- Rever métricas e critérios de sucesso à luz do escopo social confirmado; as metas originais ainda não foram revalidadas.

## Decisões finais — rodada limitada a 20 perguntas

Esta seção atualiza e prevalece sobre os pontos anteriormente em aberto neste registro.

1. A visibilidade de tempo e colocação será configurada por participação, com aplicação também ao feed e aos cards compartilhados.
2. Ocultar o tempo também ocultará o pace em todas essas superfícies.
3. Publicar a conquista no feed será uma escolha do usuário. Corrida e medalha permanecerão no perfil mesmo sem publicação.
4. Editar a participação atualizará o post existente, preservando curtidas e comentários e sem gerar nova publicação. Excluir a participação removerá o post e suas interações.
5. Enquanto o usuário não seguir corredores nem tiver provas registradas ou salvas, o feed mostrará conquistas recentes de corridas de São Paulo capital.
6. Será possível encontrar corredores por nome ou username e compartilhar o link do perfil. Importação de contatos fica fora do MVP.
7. O site fica fora do MVP. Sua implantação será avaliada após comprovar o valor do produto; o lançamento será em Android e iPhone.
8. Links compartilhados de perfis e conquistas abrirão no aplicativo. Quem não tiver o app será direcionado à loja correspondente, sem páginas web públicas de conteúdo nesta fase.
9. Solicitações de provas terão nome, data, cidade e distância obrigatórios; link oficial e imagem opcionais.
10. A equipe poderá vincular uma solicitação duplicada à edição existente, preservando os dados preenchidos e avisando o usuário. A participação seguirá como rascunho para revisão e conclusão pelo corredor.
11. Em caso de recusa, o usuário poderá consultar o motivo, corrigir e reenviar a solicitação, preservando o rascunho.
12. Haverá avisos dentro do aplicativo sobre revisão de provas, novos seguidores, curtidas e comentários. Notificações push ficam para evolução futura.
13. Será possível bloquear corredores, impedindo seguir, curtir e comentar e ocultando o conteúdo entre ambos dentro do aplicativo.
14. A equipe RunPass analisará denúncias com revisão humana, podendo remover conteúdo e suspender contas, com registro do motivo.
15. O beta terá 1.000 corredores, substituindo a meta inicial de 100.
16. Antes de liberar o beta, o catálogo deverá cobrir ao menos 90% das provas citadas por um grupo inicial de convidados, no recorte de São Paulo capital e dois anos de histórico.
17. O beta será avaliado durante 60 dias a partir da entrada dos 1.000 corredores. Metas: 50% registrarem uma participação completa e 30% dos ativados registrarem uma segunda prova. Ativado significa ter uma participação completa. Com 500 ativados, a meta de repetição corresponde a 150 corredores; o denominador é o total real de ativados.
18. Para validar o uso social, 30% dos ativados deverão curtir ou comentar uma conquista de outro corredor no período. Contar usuários únicos, desconsiderando interações próprias.
19. Conquistas extras por marcos, rankings, clubes e monetização ficam fora do MVP. O foco permanece em provas, medalhas, avaliações, descoberta e interação social.
20. O beta será gratuito, restrito a convidados e destinado a maiores de 18 anos.

## Próximo passo e limites

### Grill-me técnico — infraestrutura e região

- Imagem oficial: usuário aprovou preservar a versão vinculada no cadastro de medalhas existentes; troca do catálogo vale para novas vinculações. Correção retroativa precisa de ação administrativa explícita/auditada. Referências devem preservar conteúdo, sem sobrescrita indireta; fotos próprias mantidas. Resolve pendência anterior do efeito em medalhas antigas.

- Imagem de medalha: Administrador autorizado pode substituir a oficial no catálogo sem alterar fotos próprias dos corredores. Origens devem permanecer distintas. Efeito em registros antigos que usam imagem oficial ainda não decidido; controles de versão/auditoria e arquivos referenciados devem ser preservados.

- Organizadores: cadastros de referência mantidos pela equipe RunPass, sem login/portal no MVP, aprovado pelo usuário. Operações administrativas com MFA e auditoria; preservar referências das edições, sem introduzir contatos pessoais ou acesso B2B automaticamente.

- Denúncias: decisão e motivo obrigatórios no encerramento, aprovados pelo usuário, com resultados procedente/improcedente/sem elementos suficientes e acesso restrito à operação. Contrato de resolução por Moderador com MFA; eventual remoção/suspensão é ação separada e rastreável.

- Cards de compartilhamento gerados no aplicativo Flutter, aprovado pelo usuário, com marca e dados respeitando visibilidade atual. Sem serviço adicional de renderização/armazenamento no backend; cópias exportadas não são revogáveis. Leitura autorizada, imagens e links app/loja continuam sujeitos à implementação/testes.

- Usuário aprovou remover relações de seguir nos dois sentidos ao bloquear. Curtidas/comentários anteriores permanecem preservados e ocultos entre os envolvidos. Desbloqueio não recria seguimentos; novos vínculos dependem de ação de cada usuário e autorização atual. Resolve a pendência anterior da política de follow no bloqueio.

- Desbloqueio aprovado: reexibir interações anteriores preservadas que ainda sejam autorizadas, sem recriar relações de seguir removidas. Exclusão/ocultação/moderação/suspensão e bloqueio oposto prevalecem. Não foi definida remoção automática de seguimento no ato de bloquear.

- Usuário aprovou edição do comentário social pelo autor, com indicação de editado e data original preservada. PATCH /comments/{id} adicionado ao OpenAPI 0.6.2-draft. Não estende automaticamente o histórico de avaliações no lake aos comentários sociais.

- Revisão semântica/cobertura: OpenAPI 0.6.1-draft validado sem erros de OpenAPI 3.0.3 e com 12 exemplos de schemas; evidência/hash em VALIDACAO-OPENAPI-RunPass.json. Correções de referências de medalhas/versão da edição e envelope aplicadas. Matriz COBERTURA-PRD-OPENAPI-RunPass.md documenta lacunas de comentário, desbloqueio, cards, administração, métricas e exclusão. Não equivale a aprovação integral ou testes da API; sem deploy, commit ou push.

- Expansão operacional OpenAPI 0.6.0-draft: 49 caminhos/62 operações. Inclui beta/espera, exclusão de conta, denúncias/feedback, administração/moderação e histórico restrito. Complemento REVISAO-OPENAPI-OPERACAO.md registra propostas e lacunas. Referências/estrutura e 14 exemplos checados; não há implementação, validação integral, deploy, commit ou push.

- OpenAPI 0.5.0-draft: social, feed, relações, wishlist e avisos incluídos; 34 caminhos/45 operações. Complemento REVISAO-OPENAPI-SOCIAL.md lista lacunas de desbloqueio, edição de comentário social, limites, retenção de avisos e plano de consulta. Verificações estruturais e dez exemplos realizadas; sem deploy, commit ou push.

- OpenAPI 0.4.0-draft: catálogo, perfis e solicitações de provas acrescentados, total de 21 caminhos e 26 operações. Complemento de revisão documenta detalhes ainda propostos. Não há implantação ou aprovação automática de limites/campos; contratos sociais, administrativos e de admissão ainda pendentes.

- Consolidação de 27/10/2026: OpenAPI ampliado para 9 rotas/12 operações; documento de entrega/descarte do lake e JSON Schema do evento preparados; orçamento atualizado com ingestão e S3 do lake como sensibilidade, sem custo integral garantido. Arquivos salvos em PDLC/M4. Contratos de demais domínios e aprovação técnica integral continuam pendentes; sem provisionamento, commit ou push.

- Retenção do lake: 60 dias contados da ocorrência original de cada evento, sem reinício por reenvio/reprocessamento, aprovado. Corrige a pendência anterior de âncora da contagem. Considerar atraso de entrega, versões/cópias e evitar descarte por simples idade do objeto S3 que renove indevidamente a retenção.

- Data lake: S3 privado por DEV/PROD aprovado, com entrega assíncrona e preservação do evento junto à alteração operacional para reenvio após falhas. Isolar do acesso às imagens do produto. Formato/consulta/particionamento/descarte ainda a especificar e custos a acrescentar ao orçamento; nenhum recurso foi criado.

- Acesso ao histórico informacional no data lake aprovado somente para Administradores autorizados da equipe RunPass, sem acesso a corredores ou Moderadores por padrão. Autorização específica, MFA e auditoria de consultas; mecanismos técnicos ainda a definir.

- Retenção de 60 dias do histórico informacional de avaliações no data lake aprovada durante o beta, com revisão antes do encerramento. Separada dos 7 dias de recuperação operacional e dos registros ativos sem TTL. Contagem por ocorrência do evento é proposta; acesso, descarte e pedidos de exclusão ainda precisam de detalhamento.

- Histórico de avaliações: usuário aprovou preservar valores anteriores/novos das notas e do comentário necessários à auditoria no data lake, com acesso restrito e política explícita de retenção/exclusão. Não há prazo ou papéis autorizados aprovados; não presumir retenção indefinida nem distribuir comentário antigo em eventos de todos os consumidores.

- Revisão OpenAPI: omitir comentário no PUT remove o anterior da avaliação atual, condicionado à camada informacional com histórico de eventos no data lake. Requisito de histórico de avaliações amplia escopo anterior; dashboards e analytics avançado não foram aprovados. Retenção, campos antigos/completos, acesso, exclusão de dados pessoais, prazo de entrega e custos pendentes. S3 privado é proposta, sem provisionamento.

- Expansão do contrato: usuário aprovou PATCH /participations/{id} para dados da corrida e PUT /participations/{id}/review para substituir a avaliação completa com oito notas obrigatórias. OpenAPI parcial atualizado para 0.2.0-draft. Detalhes de campos e semântica de omissão do comentário ainda são propostas técnicas.

- Consolidação após a pergunta 40: produzidos modelo DynamoDB parcial do histórico, OpenAPI parcial dos fluxos de conclusão/upload e orçamento preliminar por cenários com preços públicos de São Paulo, memória de cálculo e exclusões. Salvos em PDLC/M4. Sem aprovação integral, deploy, benchmark ou push. Modelo dos demais domínios e retenção operacional ainda requerem fechamento.

- Pergunta técnica 40: retenção própria de eventos temporários e controles aprovada, separada do histórico, sem exclusão enquanto houver processamento ou recuperação pendente. Prazos e critérios de expiração ainda a definir; tabela separada não é consequência automática.
- Retomada atual: 40 perguntas técnicas respondidas, sem pergunta pendente na sequência. Preparar modelo físico de dados, contratos e orçamento para revisão; SPEC integral ainda DRAFT. Aprovações registradas não representam provisionamento, testes executados nem publicação dessas alterações no GitHub.

- Pergunta técnica 39: configuração comum de criptografia/papéis técnicos para participações, avaliações e medalhas aprovada, com autorização por usuário/função na API e sem acesso direto do aplicativo às tabelas. Separação DEV/PROD preservada; chave concreta e permissões mínimas por executor ainda a detalhar.

- Pergunta técnica 38: eventos de criação/alteração/exclusão do histórico aprovados para RunScore e projeções, com payload mínimo, identificador e versão para idempotência. Sem nascimento ou outros dados privados desnecessários. Contratos finais, consumidores e retenção ainda pendentes.

- Pergunta técnica 37: histórico de participações, avaliações e medalhas sem expiração automática por TTL. Exclusões e ações administrativas seguem fluxos aprovados; retenção dos itens temporários e dados pessoais tratada separadamente. Não preencher atributo TTL nos itens de histórico.

- Pergunta técnica 36: recuperação conjunta de participações, avaliações e medalhas aprovada; preservar vínculos e consistência, coordenando as imagens no S3. Não há requisito aprovado de restaurar um desses grupos isoladamente; mecanismo físico, chaves e tabelas ainda a definir. Esta decisão resolve a pendência anterior de recuperação conjunta.

- Diretriz de modelagem: usuário determinou que a visão single-table considere dados que possuem relação. Agrupar por relações de negócio e validar padrões de acesso/invariantes e requisitos operacionais. Não houve aprovação da quantidade de tabelas, de Core amplo, de tabela separada de outbox/feed nem de recuperação conjunta. Participação/avaliação/medalha são candidato a agregado relacionado, ainda sujeito à modelagem.

- Pergunta técnica 35: antes do beta em PROD, exigir testes das jornadas essenciais Android/iPhone, carga, segurança e restauração, com resultados documentados. Não há evidência de execução desses testes nem aprovação integral da SPEC. Próximo passo: consolidar decisões e produzir propostas técnicas para lacunas de modelagem, contratos, operação, orçamento e critérios de aceite, sem repetir perguntas já respondidas.

- Pergunta técnica 34: arquivamento bloqueia também conclusão de rascunhos e transferência para a edição arquivada. Preservar rascunho/participação de origem e informar o motivo; não aplicar alterações parciais. Resolve os casos pendentes da pergunta 33.

- Pergunta técnica 33: edição arquivada bloqueia novas participações, mantendo histórico e edição/exclusão dos registros existentes. Não confundir prova antiga com edição arquivada. Rascunhos preexistentes e troca para edição arquivada ainda precisam de regra explícita na especificação dos fluxos.

- Pergunta técnica 32: RunScore com meta de atualização em até 10 segundos em condições normais após criar, editar, excluir ou invalidar avaliação. Avaliação salva imediatamente; medir atraso desde a confirmação persistida até o agregado consultável. Monitorar e testar; não representa garantia em incidentes nem dispensa recuperação idempotente.

- Pergunta técnica 31: autodeclaração com data de nascimento aprovada para confirmar elegibilidade etária. Validar 18 anos completos no servidor; manter data privada, fora do perfil e demais superfícies públicas. Não exige documento nem equivale a verificação documental. Esta decisão resolve a pendência de método registrada na pergunta 30; detalhar retenção/correção/descarte antes do beta.

- Pergunta técnica 30: idade mínima de 18 anos completos no beta, passível de redefinição futura. Método de confirmação ainda não aprovado; não inferir aprovação de autodeclaração ou documentos. Atualizar os requisitos antes de qualquer mudança futura de público etário.

- Pergunta técnica 29: admissão dos primeiros 1.000 usuários elegíveis após instalação nas lojas oficiais aprovada, com lista de espera dentro do aplicativo ao atingir o teto. Substitui o acesso por convite. Lista de espera não conta como admitidos/ativados, não garante acesso automático e não reabre vagas por exclusões. Elegibilidade etária e janela de 60 dias desde os primeiros 50 permanecem.

- Pergunta técnica 28: usuário definiu instalação diretamente nas lojas oficiais durante o beta e na produção futura, sem depender de links de convite para download. Não aprovou convites individuais por e-mail. Fluxo de admissão dentro do app ainda precisa ser definido, preservando o teto de 1.000 até eventual revisão explícita; validar requisitos das lojas antes da distribuição.

- Pergunta técnica 27: remoção dos metadados GPS aprovada antes de disponibilizar fotos a outros usuários, mantendo orientação visual. Validar no processamento do servidor e nos derivados; não servir original não tratado a terceiros.

- Pergunta técnica 26: fotos de medalhas JPEG/PNG, original até 10 MB e otimização para a meta de até 1 MB aprovados. Compatibilidade HEIC a resolver antes do lançamento por conversão no app ou processamento, ainda sem mecanismo escolhido. Dimensões e metadados a detalhar; manter validação técnica no servidor e medir a meta de 5 segundos.

- Pergunta técnica 25: exclusão de conta confirmada bloqueia acesso e oculta perfil/conteúdo imediatamente; limpeza em segundo plano. Prazo, retenção, conteúdo de terceiros e backups ainda serão definidos. Validar bloqueio na API e evitar reativação indevida após restauração.

- Pergunta técnica 24: aprovados papéis distintos de Administrador (catálogo, solicitações e acessos) e Moderador (denúncias e moderação de conteúdo, sem gestão de permissões), ambos com MFA. Matriz de ações e mecanismos de atribuição/revogação ainda serão detalhados.

- Pergunta técnica 23: mantida a recomendação de avaliar Flutter Web para o painel interno; não houve aprovação definitiva da tecnologia. Validar tabelas, formulários e acessibilidade, além de integração/autenticação, antes da escolha. Site público continua fora do MVP.

- Pergunta técnica 22: integração na main exige pull request, testes automatizados aprovados e revisão humana. Aprovação de deploy em PROD continua separada. Proteções, checks e revisores ainda serão configurados; não houve alteração remota no GitHub nesta decisão.

- Pergunta técnica 21: OIDC e credenciais temporárias aprovados para GitHub Actions, com papéis/permissões separados nas contas DEV e PROD e sem chaves AWS permanentes para deploy no GitHub. Restringir confiança ao repositório e referências/ambientes autorizados; configuração ainda não executada.

- Pergunta técnica 20: promover para PROD a mesma versão de código e artefatos validada em DEV, sem reconstrução independente, variando apenas configurações de ambiente. Identificar a versão e manter aprovação manual e procedimento de reversão, incluindo análise de compatibilidade dos dados.
- Rodada técnica sem limite fixo de perguntas, conforme correção do usuário. Apresentar numeração com total estimado, atualmente 20/~30–35; não confundir com a rodada anterior de produto limitada a 20 perguntas.

- Pergunta técnica 19: busca de corridas pelo início do título, combinada com cidade, período e distância, com restrição explícita na interface. Busca aproximada e por qualquer trecho ficam para evolução. Definição incorporada ao PRD e à SPEC; modelagem dos índices ainda pendente de validação.

- Pergunta técnica 18: feed com autores seguidos primeiro e demais depois, mais recentes primeiro dentro de cada grupo, com paginação e respeito a ocultações, bloqueios e moderação. Estratégia DynamoDB, cursor e estabilidade entre páginas ainda a detalhar; regra de ordenação aprovada.

- Pergunta técnica 17: excluir participação deve retirá-la imediatamente da exibição e impedir novas interações; limpeza física de dados vinculados e imagens próprias em segundo plano, idempotente e monitorada. Preservar imagens compartilhadas do catálogo; RunScore assíncrono. Prazo da limpeza e tratamento de backups/URLs previamente emitidas ainda a detalhar.

- Pergunta técnica 16: capacidade sob demanda aprovada como modo inicial do DynamoDB, com monitoramento de consumo e custos; capacidade provisionada será avaliada com medições reais. Modelagem, alarmes e limites operacionais continuam pendentes de detalhamento.

- Pergunta técnica 14: equipe RunPass receberá os alertas críticos de operação; cobertura e escalonamento ainda a definir, sem principal/substituto nomeado.
- Pergunta técnica 15: e-mail aprovado como canal inicial dos alertas críticos, com endereço de grupo configurado antes do beta e fora dos documentos versionados. Mecanismo de envio e teste de recebimento ainda pendentes. Não altera o escopo das notificações de produto.

- Pergunta técnica 13: manter pontos de recuperação operacional de PROD por 7 dias durante o beta e revisar ao final da fase. Substitui a recomendação de 35 dias; não define retenção de dados ativos, logs nem descarte de dados pessoais. Configuração e testes ainda pendentes.

- Pergunta técnica 11: RPO de até 5 minutos aprovado para PROD, como meta de recuperação sujeita à validação técnica, de custos e testes por cenário. Recuperar banco e imagens coerentemente; não representa garantia implementada.
- Pergunta técnica 12: RTO de até 4 horas aprovado para PROD. Definir procedimento, responsáveis, início da medição e critérios de restabelecimento e validar por testes. Não substitui a meta de disponibilidade nem comprova recuperação regional.

- Pergunta técnica 10: MFA obrigatório aprovado para administradores e moderadores; corredores com e-mail e senha no MVP. Método, recuperação e configuração de identidade ainda a definir. Proteção também nas operações administrativas, sem depender apenas da interface do painel.

- Pergunta técnica 9: validação de foto em near real time, com confirmação ou falha no próprio fluxo. Meta de até 5 segundos após o término do upload aprovada pelo usuário, em condições normais e sujeita aos testes de desempenho; não inclui transferência do arquivo. Conclusão depende de imagem válida; falhas preservam rascunho e permitem reenvio. Mecanismo, condições de medição e limite de espera operacional ainda a definir; timeout não autoriza concluir. Não foi aprovada verificação de autenticidade da medalha por IA.

- Pergunta técnica 8: atualização assíncrona do RunScore aprovada. Avaliação salva imediatamente; agregado pode levar alguns segundos para refletir alterações, com retentativas e idempotência. Prazo máximo e critérios de recuperação ainda serão especificados e testados.

- Pergunta técnica 7: FastAPI aprovado pelo usuário para a API Python em Lambda, contrato OpenAPI e módulos de negócio separados. Validar integração/empacotamento e desempenho antes de implementar. Painel interno consumirá a API, com tecnologia de interface ainda pendente.

- Premissa de orçamento aprovada: 30 imagens carregadas por sessão, miniaturas no feed e imagens maiores nos detalhes; 540.000 carregamentos/mês no cenário de 18.000 sessões. Cache, tamanho das miniaturas e proporção de detalhes ainda serão hipóteses explícitas de cálculo, não novas funcionalidades aprovadas.

- Cenário esperado de orçamento aprovado: 300 usuários por dia, com duas sessões cada (600 sessões/dia; 18.000 em 30 dias). Não é simultaneidade nem redefine a ativação. Chamadas de API e imagens por sessão permanecem premissas a estimar.

- Orçamento a estimar após revisão técnica; sem teto mensal aprovado. Premissas confirmadas: 20 medalhas por usuário e até 1 MB por foto própria otimizada. Cenário com 1.000 usuários e 20.000 fotos próprias distintas: aproximadamente 20 GB decimais, sem miniaturas e versões. Não define limite funcional de medalhas nem limite de upload original. Reutilização de imagens do catálogo, quantidade de uploads e tráfego ainda precisam ser estimados.

- GitHub Actions aprovado para implantações automatizadas, com revisão das alterações do CloudFormation e aprovação manual antes de aplicar em PROD. Pipeline e bloqueios ainda não implementados; detalhar responsáveis, autenticação e mecanismo de aprovação compatível com o repositório.

- Ambientes confirmados pelo usuário: DEV e PROD em contas AWS distintas, com dados, imagens e configurações independentes. Beta operado em PROD, sem ambiente BETA adicional definido. IDs e papéis de implantação ainda serão configurados; nenhuma conta ou infraestrutura criada nesta revisão.

- CloudFormation escolhido pelo usuário para infraestrutura como código. SAM não foi aprovado automaticamente.
- São Paulo (`sa-east-1`) definida explicitamente como região AWS inicial. Essa decisão substitui a recomendação de Norte da Virgínia motivada por custo.
- Custos, disponibilidade dos serviços e desempenho devem ser avaliados em São Paulo. A escolha de região não representa aprovação integral da arquitetura nem autorização de provisionamento.

### Consolidação da proposta de arquitetura na SPEC

- SPEC atualizada para a proposta com DynamoDB como fonte operacional principal, sem PostgreSQL/Aurora no desenho atual.
- Componentes propostos: Flutter/Dart, Cognito, API Gateway, backend Python modular em Lambda, S3 privado, CloudWatch, IAM e gestão de segredos; outbox/Streams, publicador Lambda, SQS com fila de erro e workers idempotentes para efeitos assíncronos.
- Diagrama disponível em PDLC/M4/RunPass-Arquitetura-MVP-DynamoDB-v1.png. Referência visual, sem aprovação técnica integral; ressalvas registradas na SPEC.
- Referência inicial Django/Fargate/PostgreSQL preservada como alternativa histórica, não escolha atual aprovada. Framework do backend, modelagem DynamoDB, custos, região e dimensionamento ainda pendentes.
- EventBridge, OpenSearch, analytics avançado e integrações externas ficam como possibilidades de evolução, não implantação aprovada do MVP.

### Especificação técnica — linguagem

- Flutter/Dart aprovado explicitamente pelo usuário para o aplicativo Android/iPhone. Esta decisão substitui os registros anteriores que o classificavam como proposta não aprovada.

- Abordagem de testes aprovada pelo usuário: verificar regras principalmente pela API, com testes complementares das jornadas essenciais em Android/iPhone. Isso não representa aprovação integral da SPEC nem execução dos testes.

- O usuário confirmou: “Python apenas no backend”.
- Não existe exigência de Python na interface mobile; Flutter/Dart permanece proposta, sem aprovação automática.
- Primeira SPEC disponível em PDLC/M4/SPEC_RunPass_MVP_v1.md, em DRAFT técnico. Demais propostas de arquitetura e testes continuam sujeitas à revisão.

### Aprovação de todos os artefatos

- O usuário instruiu: “Coloque todos os artefatos como Aprovados”.
- Artefatos M0–M2, índice e controle documental aprovados pelo usuário, somando-se à aprovação já registrada do PRD v2 e dos registros de revisão/contexto.
- Referências históricas a conteúdo ainda em DRAFT ou aguardando aprovação estão superadas por esta decisão. Lacunas e detalhes técnicos permanecem identificados, sem atribuir evidências de reunião, unanimidade, aprovação técnica ou produção inexistentes.

### Aprovação do conteúdo do PRD v2

- O usuário respondeu “Aprovado” à solicitação explícita de aprovação do conteúdo consolidado do PRD v2, após a revisão final.
- Conteúdo de produto aprovado, incluindo as três últimas regras de perfil, foto da medalha e arquivamento.
- A aprovação não constitui liberação técnica, autorização de produção nem evidência de cumprimento formal de M0–M3.
- Próximo passo: verificar os artefatos e evidências exigidos pelo PDLC antes da passagem formal de fase; usar o conteúdo aprovado como referência para preparar a especificação sem alterar silenciosamente o escopo.

### Decisões da revisão final

Estas definições substituem propostas e pendências anteriores sobre os mesmos assuntos:

- Perfil: nome de exibição e username obrigatórios; foto do perfil, cidade e bio opcionais; e-mail privado.
- Medalha: se não houver imagem no catálogo, o usuário deverá enviar foto da medalha obrigatoriamente para concluir o cadastro da corrida. Sem imagem do catálogo ou foto enviada, a participação permanece rascunho. A foto continua vinculada apenas ao usuário.
- Edição com participações: arquivar para novas ações, preservando histórico e referências; não excluir em cascata os registros existentes.
- As três definições foram confirmadas pelo usuário; isso não constitui evidência de aprovação integral do PRD nem dos gates formais do PDLC.

### Fechamento complementar aprovado

Estas definições prevalecem sobre os relatos anteriores divergentes:

- Publicações começam visíveis; o usuário pode ocultá-las durante ou após publicar. Resultados informados seguem visibilidade inicial, com os controles por participação já definidos e pace oculto junto ao tempo. Dados privados de cadastro continuam privados.
- Wishlist pública por padrão, com opção de ocultar.
- Feed mostra publicações de outros usuários e prioriza, como ordenação, os corredores que o usuário passa a seguir. Corrige a menção anterior a “seguidores”.
- Duplicidade ao corrigir participação: orientar a editar o registro existente ou excluí-lo antes de adicionar novamente, sem sobrescrita automática.
- Bloqueio apenas oculta interações preexistentes entre os envolvidos, preservando registros.
- Usuário ativo na visão de adesão do beta: cadastro completo de ao menos uma competição concluída; equivale a ativado, sem exigir recorrência. Não ativo nessa visão significa ausência desse cadastro.
- Catálogo: montar lista de referência com os primeiros convidados, congelada antes da medição dos 90%, no recorte já aprovado. Tamanho da amostra não foi fixado.
- Feedback aprovado: facilidade após primeiro registro (1 a 5 e comentário opcional); botão contínuo para problema/sugestão/elogio; pesquisa de utilidade e dificuldades aos 30 dias; pesquisa final aos 60 dias sobre continuidade, valor e melhoria; pergunta opcional após 7 dias sem registro completo. Consolidação semanal pela equipe, priorizando bloqueios de uso. Sem novo limiar numérico de satisfação.

### Complemento aprovado — moderação e objetivo do beta

- Invalidação de notas: preservar participação, medalha e publicação; retirar as notas do RunScore e da exibição pública, avisar o usuário e permitir correção sujeita à revisão humana antes de restabelecer a avaliação. Ocultar apenas comentário não invalida notas. Exceção à avaliação válida em registro já concluído, sem dispensar as oito notas na conclusão inicial.
- Os 1.000 usuários são simultaneamente meta de recrutamento e limite máximo do beta de 60 dias, iniciado com os primeiros 50 usuários. Controlar o teto de admitidos no período; não liberar vagas automaticamente por exclusões.
- Foco: adesão, interações, disponibilidade durante o uso e feedbacks dos usuários. Registrar incidentes e consolidar feedbacks; não há novo limiar de satisfação aprovado.
- Denominador confirmado: total de usuários únicos efetivamente admitidos durante a janela do beta, incluindo os primeiros 50, até o encerramento dos 60 dias. Não usar a meta fixa de 1.000 nem contar convites sem adesão. Meta de ativação mantida em 50%; repetição e interação mantidas em 30% dos ativados.
- Visão de adesão: ativados e não ativados, conforme tenham ou não uma participação completa na janela. Não confundir com usuários ativos recorrentes ou inativos recentes; esses indicadores exigem janela e ações qualificadoras próprias, ainda não definidas.

### Atualização da revisão do PRD v2

As definições abaixo substituem regras anteriores conflitantes:

- Administração: painel interno mínimo restrito à equipe RunPass incluído no MVP. Site para usuários continua fora.
- Participação: estados rascunho/concluída separados da publicação no feed, publicada/não publicada.
- Moderação: distinguir ocultação do comentário de invalidação das notas. O efeito da invalidação sobre a participação e sua correção ainda requer especificação.
- Feed: permitir visualizar publicações de outros usuários, com destaque posterior aos seguidores. O usuário empregou “seguidores”; não equiparar automaticamente a “usuários seguidos”. Ordenação e momento desse destaque permanecem em aberto.
- Beta: 60 dias contados a partir da entrada dos primeiros 50 usuários; meta e teto de 1.000 convidados admitidos. Ativação calculada sobre o público efetivamente admitido, conforme complemento acima.
- Catálogo: cobertura calculada por edições distintas, com lista de referência e período congelados antes da avaliação; composição do grupo ainda pendente.
- PRD v2 criado e atualizado com essas definições. O PRD v1 permanece preservado.

- As 20 perguntas foram concluídas; não há pergunta pendente dessa rodada.
- Próximo trabalho: consolidar as decisões no PRD e revisar sua consistência, sem tratar o encerramento da entrevista como aprovação formal dos gates do PDLC.
- O PRD original ainda não foi alterado. Metas antigas incompatíveis com esta rodada deverão ser substituídas na consolidação.
- Detalhes ainda não decididos devem ser identificados como premissas ou pendências, sem ampliar silenciosamente o escopo nem afirmar aprovação.
- Permanecem detalhes de especificação, como lista das corridas e grupo usado para medir cobertura, ordenação exata do feed, campos públicos, prazos operacionais de revisão e tratamento de conflitos ao editar uma participação para uma edição já registrada.
- A viabilidade de redirecionamento de links para as lojas sem site de conteúdo deverá ser validada na especificação técnica.

## Parâmetros aprovados — imagens oficiais de medalhas

O usuário confirmou a reutilização dos parâmetros de fotos de medalhas para as imagens oficiais: JPEG/PNG, arquivo original de até 10 MB, otimização com meta de até 1 MB e meta de validação em até cinco segundos após o término do upload, em condições normais. A meta depende de testes de desempenho e não é garantia de prazo máximo. Enquanto pendente ou em falha, a imagem não pode substituir a vigente no catálogo. Validar formato real, tamanho e decodificação no servidor; preservar orientação e remover GPS dos derivados disponibilizados.

O detalhamento consta em UPLOAD-ADMINISTRATIVO-MEDALHAS-RunPass.md, em PDLC/M4. Esta confirmação aprova os parâmetros acima; não constitui aprovação integral da SPEC nem das rotas candidatas. Limites de pixels, expiração de sessões/arquivos não vinculados, retenção da auditoria e mecanismo de correção retroativa continuam a detalhar. Nenhum recurso foi provisionado.
## Contrato de upload administrativo — OpenAPI 0.7.0-draft

Incluídas POST /admin/medal-image-uploads, POST /admin/medal-image-uploads/{id}/finalize e GET /admin/medal-image-uploads/{id}. Operações exigem Administrador e MFA, sem vaga de corredor. Sessão vinculada a edição e distância opcional, envio PUT privado temporário, finalização idempotente e consulta de estado pending/valid/failed. Somente estado valid disponibiliza referência imutável para vinculação explícita pelo PATCH da edição, com versão esperada e auditoria. Verificar destino, ambiente e origem administrativa da referência no backend; uploads pessoais não podem ser promovidos por esse fluxo. A edição deve existir antes de iniciar a sessão de sua imagem oficial.

Schemas distinguem pendência, sucesso e falha, sem referência publicável nos estados pendente/falha. Limites aprovados de JPEG/PNG e 10 MB de original; otimização com meta de 1 MB e retorno em cinco segundos sujeitos a testes. Falha preserva imagem vigente e medalhas antigas. Prazo de expiração, limite de pixels, limpeza e retenção da auditoria continuam pendentes. Contrato validado estruturalmente; não comprova execução da API, autorização, MFA ou concorrência. A SPEC integral permanece em revisão.
## Proposta consolidada de retenção e exclusão

RETENCAO-E-EXCLUSAO-RunPass-MVP.md separa as regras aprovadas (histórico ativo sem TTL, lake de avaliações por 60 dias desde ocorrência, recuperação por sete dias no beta, bloqueio/ocultação imediatos da conta e preservação de imagens compartilhadas) de propostas operacionais ainda não aprovadas. Primeira proposta para decisão: limpeza dos sistemas ativos em até sete dias corridos, incluindo histórico identificável do titular no lake, preservando catálogo compartilhado. Exceções de denúncias/auditoria e controle de exclusões continuam a definir. Não declarar eliminação de todas as cópias em sete dias: backups têm janela própria. O documento não aprova prazos, não substitui revisão da política de dados e não altera a SPEC para aprovada.
## Exclusão de conta — decisão aprovada

O usuário aprovou bloquear acesso e ocultar perfil/conteúdo imediatamente ao aceitar a exclusão, com remoção dos dados pessoais dos sistemas ativos em até sete dias corridos desde a aceitação. O escopo inclui fotos próprias e histórico identificável de avaliações no data lake: a exclusão da conta prevalece sobre a retenção ordinária de 60 dias desse histórico. Preservar catálogo e imagens oficiais compartilhadas ainda referenciadas. A limpeza deve abranger projeções, índices e cópias intermediárias sob controle do RunPass, com processamento idempotente, retentativas e acompanhamento por destino.

Backups mantêm a janela própria de sete dias no beta; a aprovação não significa eliminação de todas as cópias em sete dias desde a solicitação. Reaplicar exclusões antes de liberar qualquer restauração. Tratamento de denúncias/evidências, auditoria e controle mínimo de exclusões continua pendente de definição específica, sem autorização para retenção indefinida. Os demais prazos propostos no documento de retenção não foram aprovados por esta decisão. Prazo de exclusão é requisito aprovado, ainda sem comprovação por implementação ou testes; a SPEC integral permanece em revisão.
## Retenção de denúncias e auditoria — prazos aprovados

O usuário aprovou a recomendação para o beta: denúncias em análise permanecem enquanto necessárias, com revisão semanal pela equipe RunPass; denúncias encerradas e evidências necessárias permanecem por até 60 dias desde o encerramento; auditoria administrativa mínima permanece por até 90 dias desde a ocorrência original da ação. Consulta, cópia, retentativa ou replay não renovam esses prazos. Denúncia aberta exige acompanhamento; o prazo máximo de resolução continua pendente, sem autorizar retenção indefinida sem revisão.

Acesso restrito por permissão e MFA, respeitando a separação entre Administração e Moderação. A retenção ordinária não estende o prazo aprovado para exclusão da conta: dados pessoais identificáveis continuam sujeitos à remoção em até sete dias corridos, incluindo os presentes nesses registros. Não presumir anonimização por troca de nome ou ID. Preservar registros independentes de terceiros somente sem reter indevidamente os dados do titular excluído; necessidade excepcional de retenção identificável exige política específica ainda não definida.

Essas janelas não se aplicam automaticamente a logs técnicos, feedbacks, lista de espera ou controles de exclusão/idempotência. Descarte físico em até 24 horas após expiração continua proposta não aprovada. O lake de alterações de avaliações mantém sua própria regra de 60 dias desde a ocorrência. Detalhamento: RETENCAO-DENUNCIAS-E-AUDITORIA-RunPass.md. Requisitos registrados, sem implementação ou testes de execução; SPEC integral em revisão.
## Proposta de retenção técnica preparada

RETENCAO-TECNICA-RunPass-MVP.md consolida propostas ainda não aprovadas para logs DEV/PROD (7/30 dias), URL de upload (15 minutos), temporários abandonados (limpeza em até 24 horas após expiração da sessão), imagens validadas nunca vinculadas (sete dias até elegibilidade), idempotência da API (sete dias) e payloads entregues a todos os destinos obrigatórios (sete dias após última confirmação). Propõe remoção em até 24 horas após expiração para conteúdos sujeitos a descarte, sem estender a promessa a backups. Preserva eventos de negócio pendentes e separa a exceção proposta de payload de auditoria de avaliação expirado. Ledger de consumidores e controle de exclusões dependem do horizonte de replay/recuperação e continuam pendentes. Nenhum prazo novo foi tratado como aprovado; permanece válida a exclusão de dados pessoais dos sistemas ativos em até sete dias.
## Retenção técnica — conjunto de prazos aprovado

O usuário aprovou o conjunto apresentado para o beta:
- Logs técnicos: sete dias em DEV e 30 dias em PROD, desde a ocorrência original, sem renovação por cópia/replay.
- URL assinada de upload: validade de 15 minutos desde emissão.
- Arquivo temporário abandonado: remoção em até 24 horas após expiração da sessão; não abrange arquivo publicado ou em processamento ativo. A janela operacional da sessão ainda será detalhada.
- Imagem validada nunca vinculada: elegível ao descarte após sete dias desde validação, com limpeza em até 24 horas depois e verificação de referências/concorrência.
- Registro de idempotência de comando da API: sete dias desde primeira aceitação durável; invariantes e versões continuam obrigatórias após a janela.
- Payload de evento entregue a todos os destinos obrigatórios: sete dias desde última confirmação obrigatória. O prazo não define a retenção do ledger dos consumidores.

Eventos de negócio pendentes continuam recuperáveis; não apagar trabalho pendente por regra genérica de limpeza. A retenção dos controles de deduplicação de consumidores e de exclusões depende da janela de replay/recuperação, ainda a definir. Os prazos ordinários não estendem os sete dias aprovados para exclusão de dados pessoais dos sistemas ativos. Logs devem minimizar conteúdo e permitir cumprimento dessa regra antes do beta.

Esta aprovação refere-se ao conjunto apresentado ao usuário. Não aprova por inferência o descarte físico em 24 horas de lake/denúncias/auditoria, a exceção para payload de auditoria ainda não entregue ao expirar, nem outros itens pendentes do documento. Backups mantêm janela própria de sete dias; não prometer remoção de todas as cópias pelos prazos de arquivos temporários. Requisitos registrados sem configuração de infraestrutura ou testes de execução; SPEC integral em revisão.
## Consolidação de aprovações anteriores — M4

Por instrução explícita do usuário, os requisitos suficientemente definidos no PRD, Grill-me e decisões posteriores foram classificados como aprovados em MATRIZ-APROVACOES-M4-RunPass.md. A matriz discrimina, nos oito blocos, o requisito aprovado, a escolha técnica ainda em avaliação e a comprovação pendente. Não é necessário reentrevistar requisitos confirmados. A aprovação não abrange automaticamente esquemas físicos, serviços candidatos, orçamento, testes não executados, SPEC integral, gates corporativos ou produção. Próximo trabalho: elaborar propostas consolidadas para as lacunas reais, usando a matriz como referência e evitando reabrir pendências históricas já resolvidas.
## Política de replay aprovada para o beta

O usuário aprovou reprocessar eventos concluídos por até sete dias, alinhados à janela de recuperação; preservar a recuperabilidade dos eventos pendentes até resolução, respeitando retenção/exclusão pessoal; reconstruir feed e RunScore mais antigos a partir dos dados operacionais vigentes; e restringir reprocessamento à operação interna controlada pela equipe RunPass. Não conservar eventos indefinidamente para reconstrução. Replay não recria conteúdo excluído nem renova retenção. O marco técnico proposto é a última confirmação dos destinos obrigatórios, coerente com o payload entregue; detalhar no contrato operacional.

EVENTOS-E-REPLAY-RunPass-MVP.md distingue a política aprovada dos mecanismos propostos. Ledger/deduplicação, margem para mensagens em trânsito, versões dos agregados, autorização operacional e reconstrução concorrente ainda serão projetados e validados. Não fixar automaticamente TTL de sete dias para todos os controles. A política não conclui o esquema físico DynamoDB nem aprova a SPEC integral; não houve implantação ou testes.
## SPEC v2 — revisão consolidada preparada para aprovação

Criados PDLC/M4/SPEC_RunPass_MVP_v2.md e REVISAO-APROVACAO-SPEC-RunPass-v2.md. A v1 permanece preservada. A revisão distingue requisitos já aprovados (A), nove propostas técnicas (P01–P09), seis grupos de bloqueios (B01–B06) e evidências exigidas antes da liberação (L). Propõe fronteiras físicas de dados, outbox/consumidores, identidade/MFA e critérios de aceite sem declarar mecanismos já implementados. Orçamento preservado como parcial, sem teto autorizado. Novas propostas não foram aprovadas automaticamente; a SPEC integral e o plano de slices continuam pendentes. Documento de fontes registra hashes dos artefatos técnicos consultados antes da consolidação. Não houve deploy, commit, push ou publicação.

## Aprovação prioritária e SPEC única

O usuário aprovou DynamoDB on-demand com agrupamento relacionado, outbox transacional/SQS e consumidores versionados/idempotentes, Cognito separado para corredores/operadores com MFA por aplicativo autenticador e autorização por função. Autorizado detalhamento e desenvolvimento incremental do fluxo autenticação → catálogo → rascunho → imagem → conclusão → avaliação e medalha. Referência única: SPEC_RunPass_MVP_v1.md, que recebeu o conteúdo consolidado; Não é mantida uma segunda SPEC ativa. Registro técnico anterior preservado em PDLC/M4/historico, sem vigência. Não exigir aprovação isolada de cada atributo nem nova rodada P01–P09; dependências técnicas devem ser fechadas antes da parte afetada. Não autoriza custo, deploy ou beta sem requisitos/evidências próprios.

## Plano da primeira entrega preparado

implementation-slices.md detalha S00–S09 para o fluxo aprovado: preparação local/contexto/harness, desenho de dados e contratos, identidade/admissão, catálogo, rascunho, imagem, conclusão/avaliação/medalha, consumidores/RunScore/histórico restrito, edição/exclusão e integração real em DEV. Cada slice tem dependências e critérios de aceite. S00 pode iniciar; os seguintes dependem das saídas anteriores. Provisionamento DEV depende de orçamento e autorização; release PROD/beta não é autorizado por esse plano. Não há implementação/testes de execução concluídos nem nova SPEC criada.