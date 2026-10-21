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
