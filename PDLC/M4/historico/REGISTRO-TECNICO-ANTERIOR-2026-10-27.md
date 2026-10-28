# Registro histórico — sem vigência

Conteúdo anterior da SPEC canônica, preservado apenas para rastreabilidade. Consulte ../SPEC_RunPass_MVP_v1.md para decisões atuais.

# SPEC — RunPass MVP — v1

**Estado:** DRAFT técnico para revisão. Produto: PRD v2 aprovado pelo usuário. Esta SPEC não tem aprovação técnica nem autoriza implantação.

## Problem Statement

Corredores precisam organizar experiências em provas, medalhas e avaliações e trocar essas informações com outros corredores. O beta validará adesão, repetição do registro, interação, disponibilidade e percepção de valor.

## Solution

Aplicativo Android/iPhone com catálogo por edição, conclusão autodeclarada, avaliação obrigatória, medalheiro, wishlist e feed de conquistas. Equipe RunPass opera um painel interno para catálogo e moderação. Sem site público para corredores.

## User Stories

1. Como usuário elegível que instalou o app pela loja oficial, quero ingressar no beta se houver vaga, para experimentar o produto dentro do limite aprovado.
2. Como interessado que encontra o beta lotado, quero entrar na lista de espera dentro do aplicativo, para manifestar interesse na próxima liberação.
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
| Framework da API | FastAPI aprovado pelo usuário para API Python em Lambda, com contrato OpenAPI e módulos de negócio separados. Integração e desempenho ainda a validar. |
| AWS | Direção inicial solicitada; arquitetura detalhada ainda proposta. |
| Região AWS | São Paulo (`sa-east-1`), definida pelo usuário na revisão técnica. Substitui a sugestão de Norte da Virgínia. |
| Infraestrutura como código | CloudFormation, definido pelo usuário. SAM não foi aprovado como complemento. |
| Ambientes | DEV e PROD em contas AWS distintas, com dados, imagens e configurações independentes. O beta será operado em PROD; não há terceiro ambiente BETA definido. |
| CI/CD | GitHub Actions aprovado para implantações automatizadas, com revisão das alterações do CloudFormation e aprovação manual antes de aplicar mudanças em PROD. |
| Promoção de versão | PROD receberá a mesma versão de código e artefatos validada em DEV, alterando apenas configurações de ambiente, com identificação de versão e procedimento de reversão. |
| Autenticação do pipeline | GitHub Actions com OIDC e credenciais temporárias AWS, com papéis e permissões separados para as contas DEV e PROD; sem chaves AWS permanentes no GitHub para esse fluxo. |
| Integração na main | Pull request, testes automatizados aprovados e revisão humana obrigatórios antes da integração. Aprovação de deploy em PROD permanece uma etapa separada. |
| Aplicativo | Flutter/Dart aprovado pelo usuário para Android e iPhone. |
| IDE | VS Code como proposta, sem vincular a arquitetura a uma IDE. Build iOS exige ambiente macOS/Xcode. |
| Dados | DynamoDB considerado como banco operacional principal por solicitação do usuário; modelagem e dimensionamento ainda sujeitos à revisão técnica. |
| Capacidade DynamoDB | Sob demanda aprovada como modo inicial, com acompanhamento do consumo antes de avaliar capacidade provisionada. |
| Arquitetura desenhada | API Gateway, Lambda modular, Cognito, DynamoDB, S3 e processamento assíncrono; proposta de referência, sem aprovação técnica integral. |

**Definições confirmadas:** Python apenas no backend e Flutter/Dart no aplicativo Android/iPhone. As demais escolhas de arquitetura permanecem propostas até revisão específica.

### Arquitetura proposta, não aprovada

- Backend Python em monólito modular, evitando microsserviços no MVP.
- API Python em FastAPI executada em Lambda, aprovada pelo usuário, com contrato OpenAPI, validação de entrada e módulos de negócio separados. Adaptador/empacotamento FastAPI–Lambda, ciclo de execução e desempenho ainda precisam de validação. Django/Fargate permanece alternativa histórica, não escolha atual. Com DynamoDB, não presumir integração direta com Django ORM/Admin.
- Arquitetura desenhada mais recente: API Gateway como entrada HTTPS/JWT e backend Python modular em Lambda. Validar latência, concorrência, limites e custos antes da aprovação. Módulos de negócio não implicam microsserviços independentes.
- Amazon Cognito como proposta de identidade; autorização de proprietário, bloqueios, suspensão e papel administrativo permanece no domínio, além de validar token.
- DynamoDB como fonte operacional principal nesta proposta, substituindo a referência inicial a PostgreSQL. Não incluir Aurora/PostgreSQL simultaneamente sem justificativa e revisão explícita.
- S3 privado para imagens; acesso temporário autorizado e sem exposição direta indiscriminada dos objetos. CloudWatch como proposta de logs/métricas, gestão de segredos e permissões mínimas por serviço.
- Painel interno consumindo as mesmas regras de domínio. Framework e hospedagem dependem da escolha de backend; acesso administrativo segregado e auditado.
- Painel administrativo consumirá a API FastAPI; tecnologia de interface e hospedagem ainda não definidas. A aprovação do framework não aprova automaticamente todos os demais serviços ou a SPEC integral.
- Pergunta técnica 23: usuário manteve a recomendação de avaliar Flutter Web para o painel administrativo interno, reutilizando Dart e consumindo a mesma API. Trata-se de candidato em avaliação, não escolha definitiva. Validar tabelas, formulários, upload, navegação, acessibilidade e autenticação MFA no navegador antes de fechar a tecnologia. Não introduz site público para corredores; hospedagem ainda a definir.
- Autenticação aprovada na revisão técnica: MFA obrigatório para administradores e moderadores acessarem o painel e suas operações protegidas; corredores mantêm e-mail e senha no MVP, sem exigência de MFA aprovada. Método do segundo fator, recuperação de acesso e separação/configuração dos clientes ou pools ainda serão detalhados. A proteção deve ser verificada também nas operações administrativas da API, não apenas na tela de login; não presumir que validar JWT comprova MFA por si só.
- Papéis aprovados na pergunta técnica 24: Administrador gerencia catálogo, solicitações e acessos; Moderador analisa denúncias e modera conteúdo, sem gerenciar permissões. Ambos exigem MFA. Aplicar autorização na API e no painel; detalhar matriz de ações, atribuição/revogação e auditoria sem presumir que Moderador possui operações exclusivas de Administrador. Acesso à moderação por Administrador deve constar explicitamente da matriz, não ser inferido por nome do papel.
- Região inicial definida: São Paulo (`sa-east-1`). Infraestrutura como código em CloudFormation; SAM continua sem aprovação específica. Não provisionar outra região por presumida economia.
- Ambientes definidos em contas AWS distintas: DEV para desenvolvimento e testes; PROD para os participantes do beta e operação do produto. Separar tabelas, buckets, identidades de aplicação, configurações, permissões e stacks; testes de DEV não devem acessar dados de PROD. IDs das contas e papéis de implantação serão definidos na preparação dos ambientes, sem criar contas ou recursos nesta revisão.
- Implantação automatizada via GitHub Actions, com revisão do plano de alterações do CloudFormation antes da aplicação e aprovação manual para PROD. Implementação do bloqueio, responsáveis autorizados, permissões do workflow e autenticação com as duas contas serão detalhados e verificados antes de habilitar o pipeline. Não presumir disponibilidade de um recurso específico de proteção de ambientes no plano GitHub utilizado.
- Promoção aprovada na pergunta técnica 20: construir e identificar a versão, validá-la em DEV e promover os mesmos artefatos para PROD sem reconstrução independente; somente configurações de ambiente podem variar. Preservar a identidade/integridade dos artefatos ao transferi-los entre contas. Revisar as alterações do CloudFormation e manter aprovação manual em PROD. Documentar reversão de código/configuração e compatibilidade das alterações de dados; reversão de código não desfaz automaticamente escritas ou exclusões.
- Autenticação do pipeline aprovada na pergunta técnica 21: OIDC do GitHub Actions para assumir papéis AWS e obter credenciais temporárias, separados por conta DEV/PROD e com menor privilégio. Não armazenar access keys permanentes no GitHub para o deploy. Restringir a confiança ao repositório autorizado e às referências/ambientes previstos, validar audience e subject e preservar a aprovação manual de PROD. Políticas, papéis de execução do CloudFormation e regras de branch/ambiente serão detalhados antes de habilitar o pipeline; não configurar confiança ampla para forks ou repositórios arbitrários.
- Política de integração aprovada na pergunta técnica 22: exigir pull request, testes automatizados aprovados e revisão humana antes de integrar alterações à main. Aprovar o PR não aprova automaticamente o deploy em PROD. Definir checks obrigatórios, revisores e proteção compatível com o plano e a visibilidade do repositório; não afirmar que as proteções já estão configuradas. Exceções de emergência não foram aprovadas e não devem ser presumidas.
- Sem valor de custo estimado aprovado: carga, armazenamento, alta disponibilidade e orçamento precisam ser definidos antes de provisionar. Calcular os preços e verificar disponibilidade dos componentes para `sa-east-1`.

### Armazenamento DynamoDB e padrões de acesso

- Pergunta técnica 39: participações, avaliações e medalhas podem compartilhar configuração de criptografia e papéis técnicos de acesso, com autorização de usuário/proprietário/função aplicada pela API. Aplicativo mobile não acessa diretamente as tabelas. Isso não unifica papéis de DEV/PROD nem concede permissões administrativas a todos os serviços; limitar cada executor às operações necessárias. Tipo e gestão da chave ainda serão detalhados, sem presumir chave KMS gerenciada pelo cliente ou requisito de criptografia por usuário.

- Pergunta técnica 37: participações, avaliações e medalhas permanecem sem expiração automática por TTL. Remoção ocorre pelos fluxos aprovados de exclusão do usuário ou ação administrativa prevista. Isso não impede ocultação, invalidação por moderação nem limpeza após exclusão de conta, e não equivale a política de retenção irrestrita de todos os dados pessoais. Eventos temporários, outbox e controles de processamento terão política própria ainda a definir. Em single-table, não atribuir atributo de expiração aos itens do histórico; eventual configuração TTL da tabela deve atuar apenas sobre os tipos de item expressamente elegíveis.

- Pergunta técnica 36: participações, avaliações e medalhas devem ser recuperadas em conjunto após incidente, preservando vínculos e consistência. Não há necessidade de restauração independente desses três grupos aprovada no MVP. Coordenar a recuperação das referências com as imagens correspondentes no S3. Essa decisão favorece agrupamento, mas não define sozinha chaves, tabelas nem mecanismo físico de restauração.

- Diretriz do usuário para single-table: considerar os dados que possuem relação. A proposta anterior de Core amplo e tabelas auxiliares não constitui divisão física aprovada. Avaliar participação, avaliação e medalha como agregado relacionado e outras relações conforme consultas, invariantes e requisitos operacionais; uma tabela pode conter múltiplas partições e itens, sem concentrar todos os dados em um item ou chave única.
- Relação de negócio é critério de agrupamento, mas não prova suficiente para colocar todas as entidades conectadas na mesma tabela. Recuperação conjunta de participação/avaliação/medalha confirmada na pergunta 36; confirmar Streams, TTL, criptografia e escopo IAM por agregado e recuperação dos demais grupos antes de fixar fronteiras. Produzir alternativas rastreáveis aos padrões de acesso, sem tabela por entidade como regra automática.

- Busca de corridas aprovada na revisão técnica: nome pelo início do título, combinado com cidade, período e distância. Informar essa restrição na interface. Busca aproximada e por qualquer trecho ficam para evolução. Normalização de maiúsculas/acentos, índices e combinações dos filtros precisam ser especificados e validados; não presumir que um único índice atende todas as combinações nem recorrer a varreduras globais como solução padrão.

- Modo inicial de capacidade aprovado: sob demanda, com acompanhamento de leituras, escritas, throttling e custos. Avaliar capacidade provisionada posteriormente com medições reais. Não significa custo fixo, orçamento ilimitado nem dispensa de modelar índices, transações e distribuição das chaves; limites operacionais e alarmes ainda serão especificados.

- Modelar chaves, índices e projeções a partir das consultas aprovadas, antes da implementação. Número de tabelas, chaves e índices ainda não foi decidido; não presumir single-table obrigatório.
- Mapear pelo menos: perfil por username; histórico/medalhas por usuário; catálogo por cidade/data/distância/nome; avaliações por edição e distância; feed público e de seguidos; wishlist; avisos; solicitações e denúncias por estado.
- Consultas críticas não devem depender de varreduras globais como estratégia principal. Busca combinada do catálogo e ordenação do feed precisam de prova técnica, estimativa de leitura/escrita e paginação.
- Usar identidade determinística e escrita condicional para participação única por usuário/edição, curtidas únicas e reserva de username. Verificar unicidade no armazenamento principal, não por consulta prévia a índice eventualmente consistente.
- Concluir participação, avaliação, medalha e registro de evento/outbox em transação, respeitando limites do DynamoDB. Imagens continuam no S3; sua validação antecede a conclusão e não faz parte da transação do banco.
- Índices globais podem ter atraso de atualização. Definir onde leitura fortemente consistente é necessária e revalidar permissões/visibilidade na fonte antes de expor dados sensíveis, mesmo se a projeção do feed estiver atrasada.
- RunScore terá atualização assíncrona, aprovada pelo usuário: salvar a avaliação imediatamente e atualizar o agregado com meta de até 10 segundos em condições normais após confirmação de criação, edição, exclusão ou invalidação da avaliação (pergunta técnica 32). Atualização idempotente de soma/contagem ou projeção reconstruível, sem duplicar contribuições. Medir do commit da alteração até o agregado atualizado estar disponível para consulta. Condições de carga e critério estatístico ainda serão especificados e testados; não é garantia de limite absoluto em incidentes. Monitorar atraso e falhas, com recuperação/reprocessamento; ultrapassar a meta não deve perder a avaliação nem reaplicar sua contribuição.
- Avaliar distribuição de chaves, concentração de acesso em provas populares e índices de feed; capacidade automática não elimina hot keys nem modelagem inadequada.
- Prever exportação/reprocessamento para analytics, recuperação e evolução de projeções, sem usar varreduras de produção para cada relatório.

### Eventos, imagens e evolução

- Pergunta técnica 40: eventos temporários e controles de processamento terão retenção própria, separada do histórico de conquistas. Não apagar itens enquanto houver processamento, retentativa ou recuperação pendente. Prazos, estados elegíveis à expiração e conciliação com backups/replay ainda serão definidos com base em recuperação e custos. Não usar TTL como agendador de execução nem como garantia de exclusão imediata. Retenção diferente por tipo de item não exige automaticamente tabela separada; decidir fronteiras com base no conjunto de requisitos operacionais.

- Pergunta técnica 38: emissão de eventos de criação, alteração e exclusão do histórico aprovada para atualizar RunScore e demais projeções. Eventos com payload mínimo, identificador único e versão do agregado para idempotência e controle de ordem. Não incluir nascimento, credenciais ou outros dados privados desnecessários. A aprovação não autoriza projetar dados ocultos como públicos nem duplicar contribuições do RunScore por eventos de participação e avaliação relativos à mesma mudança; definir contratos e consumidores explícitos.

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

- Versionamento de imagem oficial aprovado: medalhas já registradas preservam a versão da imagem de catálogo vinculada no cadastro. Substituir a imagem oficial afeta novas vinculações, sem reescrever o histórico automaticamente. Correção retroativa exige ação administrativa explícita e auditada, ainda sem contrato específico aprovado. Usar referência/versionamento imutável do conteúdo, evitando substituir bytes sob uma mesma referência e alterar medalhas antigas por efeito indireto de cache/URL. Não eliminar versões ainda referenciadas; fotos próprias continuam separadas. Essa preservação de imagem é distinta da retenção de 60 dias dos eventos de avaliação e de 7 dias dos pontos de recuperação.

- Imagem oficial da medalha: Administrador autorizado com MFA pode substituir a referência do catálogo da edição/distância, sem alterar fotos próprias enviadas pelos corredores. Identificar a origem (catálogo ou usuário) e preservar autorização/validação da imagem. Alteração administrativa deve ter controle de versão e auditoria e não pode apagar objeto ainda referenciado. Efeito sobre medalhas já registradas que usam imagem de catálogo (acompanhar a atual ou preservar versão histórica) ainda requer definição específica; não atualizar fotos próprias nem remapear todas as medalhas por inferência.

- Organizadores no MVP: cadastros de referência mantidos pela equipe RunPass, aprovados pelo usuário, sem login, papel operacional ou portal próprio. Edições podem referenciar organizerId; nome exibido é informação do cadastro, não comprovação de vínculo comercial. Administração por Administrador com MFA, versão esperada e auditoria. Alterações não devem apagar referências de edições e participações existentes. Campos adicionais, deduplicação e eventual arquivamento ainda serão detalhados; não coletar dados de contato pessoais por inferência.

- Encerramento de denúncia aprovado: registrar decisão (procedente, improcedente ou sem elementos suficientes) e motivo obrigatórios, restritos à operação autorizada. Ação por Moderador com MFA e auditoria, sem publicar justificativa interna ou identidade do denunciante. Resolver denúncia não executa automaticamente remoção/suspensão; vincular eventual ação de moderação executada por referência, preservando rastreabilidade. Versionar a transição para impedir encerramentos concorrentes conflitantes e tornar retentativas idempotentes.

- Compartilhamento aprovado: gerar cards no aplicativo Flutter, sem serviço adicional de renderização/armazenamento de cards no backend. Incluir marca RunPass e apenas dados autorizados pela visibilidade atual; tempo oculto implica pace oculto, e colocação segue sua configuração. Evitar usar valores privados de cache em novos cards; revalidar os dados e preferências antes de gerar quando necessário. Compartilhar via mecanismos nativos suportados pelo dispositivo. Imagens exportadas não podem ser revogadas retroativamente pelo RunPass. A decisão não elimina a necessidade de API de leitura autorizada, acesso temporário às imagens nem configuração dos links para app/loja.

- Desbloqueio aprovado pelo usuário: interações anteriores preservadas podem voltar a ser exibidas se ainda autorizadas, sem recriar automaticamente relações de seguir removidas. Exclusões, ocultações, suspensão, moderação e bloqueio na direção oposta continuam válidos. Remover um bloqueio não concede acesso geral nem restaura conteúdo removido; reavaliar autorização na leitura e nas novas interações. Não foi definida exclusão automática do seguimento ao bloquear; manter essa política separada.
- Política de seguimento no bloqueio aprovada posteriormente: remover as relações de seguir nos dois sentidos quando o bloqueio for confirmado. Impedir novos vínculos enquanto houver bloqueio em qualquer direção. Não apagar curtidas/comentários anteriores: continuam ocultos entre os envolvidos. Desbloquear não recria seguimentos; cada pessoa pode seguir novamente se autorizada. Atualizar prioridade do feed e contagens consistentemente, com retentativas idempotentes e proteção contra concorrência entre seguir e bloquear. Esta definição resolve a pendência de remoção de seguimento indicada acima.

- Edição de comentário social aprovada pelo usuário: PATCH /comments/{id} pelo autor, com texto e versão esperada; retornar indicação de editado e data da alteração, mantendo createdAt original. Revalidar proprietário, post e acesso atual; preservar moderação/ocultação. Retentativa não duplica a alteração. O histórico informacional de avaliações não abrange automaticamente comentários sociais.

- Definição adicional do usuário: ao substituir a avaliação por PUT, omitir o comentário remove o comentário anterior da representação atual, condicionado à preservação do histórico de eventos em camada informacional no data lake. Não perder silenciosamente o evento de alteração. Comentário anterior não permanece visível pela API operacional após sua remoção.
- Data lake informacional passa a ser requisito do histórico de alterações das avaliações; amplia o escopo anterior que deixava analytics para evolução. Isso não aprova dashboards B2B, busca avançada ou integrações externas. Extensão do histórico a outros domínios ainda não definida.
- Conteúdo histórico aprovado pelo usuário: preservar valores anteriores e novos das notas e do comentário necessários à auditoria, com acesso restrito e política explícita de retenção e exclusão. Registrar avaliação/participação de referência, ação, versão, data e correlação para rastreabilidade. Distinguir campo ausente, comentário removido e novo valor. Isso não aprova retenção indefinida, exposição pública de versões antigas ou cópia de dados privados de cadastro. Duração de retenção e papéis de acesso ainda não definidos.
- Retenção do histórico de avaliações no data lake aprovada para o beta: 60 dias, com revisão do prazo antes do encerramento da fase. Não confundir com janela de recuperação operacional de 7 dias nem aplicar esse prazo aos registros ativos de conquistas. Proposta de implementação: contar a idade por evento, desde sua ocorrência, sem renovar pela entrega/reprocessamento; âncora de contagem e execução do descarte devem ser confirmadas no desenho da política. Uma revisão futura não autoriza extensão silenciosa nem apaga automaticamente todo o lake no fim do beta. Pedidos de exclusão e demais obrigações de privacidade precisam de tratamento específico; não usar os 60 dias para dispensá-los. Papéis de acesso e mecanismo de descarte ainda a definir.
- Consulta do histórico informacional aprovada exclusivamente para Administradores autorizados da equipe RunPass, sem acesso para corredores ou Moderadores por padrão. Não conceder acesso automático a todo usuário com papel Administrador: autorização específica e menor privilégio, com MFA e auditoria das consultas. Permissões técnicas de gravação e descarte dos serviços são distintas do acesso humano de consulta; não autorizar edição arbitrária do histórico. Mecanismo de consulta, controles IAM e atendimento de solicitações de privacidade ainda serão detalhados.
- Armazenamento informacional aprovado: S3 privado, separado por DEV/PROD nas respectivas contas, com entrega assíncrona. Persistir o evento durável junto à alteração operacional para reenvio em caso de falha de entrega ao lake; não depender apenas da retenção do stream. Usar identificador de evento para evitar duplicação lógica e confirmar a entrega persistida antes de marcar o evento como entregue. Falha na entrega não pode apagar o evento pendente; outbox e lake têm finalidades/retenções distintas.
- Marco de retenção confirmado pelo usuário: 60 dias desde a ocorrência original de cada evento. Reenvio, cópia ou reprocessamento não reiniciam o prazo; preservar occurredAt original e calcular a expiração a partir dele. Objetos entregues com atraso não recebem novos 60 dias por sua criação no S3. O descarte deve considerar versões e cópias e usar o prazo de negócio, não presumir que lifecycle baseado apenas na idade do objeto atende a essa regra. Tratamento de evento ainda pendente ao ultrapassar 60 dias precisa ser explicitado na política, sem apagar silenciosamente evento não entregue nem prorrogar o histórico indefinidamente.
- Isolar os objetos do lake das imagens públicas/autorizadas do produto, sem conceder acesso pelo fluxo de URLs de medalhas. Prefixos, formato, particionamento, consulta, reconciliação, proteção e descarte de objetos/versionamentos ainda serão especificados. Não foi aprovado tornar a escrita operacional dependente da disponibilidade síncrona do S3 nem instalar serviços analíticos adicionais automaticamente. Incluir armazenamento, requisições, workers e auditoria do lake na próxima revisão do orçamento; os subtotais anteriores não incluem explicitamente essa ampliação.
- Proposta para revisão: gravar evento durável junto à alteração operacional e entregá-lo de forma assíncrona e idempotente em área S3 privada, segregada por DEV/PROD, com versão do evento, referência da avaliação, momento, ação e correlação. Não confundir histórico informacional com outbox temporária ou backup. Persistência de comentário anterior/completo exige política explícita de conteúdo, minimização, acesso, retenção e exclusão, inclusive após apagar a conta; não assumir retenção indefinida ou inclusão de dados pessoais em todos os eventos.
- Reconciliar entrega ao lake, replay, falhas e restauração para não perder histórico nem duplicar eventos. Serviços de catálogo/consulta, formato/particionamento, prazo de entrega e custos ainda serão especificados; não implantar Glue/Athena/Firehose por inferência. Data lake não autoriza restaurar comentário removido na exibição pública nem manter dados pessoais contra a política de exclusão.

- Expansão OpenAPI aprovada pelo usuário: PATCH /participations/{id} altera parcialmente dados da corrida; PUT /participations/{id}/review substitui a avaliação completa exigindo as oito notas. O PATCH não aceita notas nem comentário da avaliação. Contrato atualizado para 0.2.0-draft; nomes/unidades dos campos, controle de versão e semântica de limpeza do comentário no PUT são propostas técnicas para revisão, sem implementação executada. Correção de avaliação invalidada continua sujeita à revisão humana.

- Contrato HTTP orientado a recursos e comandos de concluir, revisar, arquivar, moderar e ocultar. Identidade vem do token, nunca apenas de identificador enviado pelo cliente.
- Leituras devem aplicar projeção pública: não devolver resultado oculto e apenas esconder na tela. Mesmo controle em perfil, medalheiro, feed, cards e acesso às imagens.
- Conclusão verifica edição, unicidade, oito notas e imagem válida; gravar participação, avaliação e medalha em transação. Retentativas não criam cópias: comando idempotente.
- Upload iniciado com autorização, validado no servidor por tamanho, tipo real e imagem decodificável. Só imagem concluída e pertencente ao usuário pode satisfazer o requisito. Limites exatos e remoção de metadados devem ser especificados antes de implementar uploads.
- Pergunta técnica 26: aprovados JPEG e PNG para fotos de medalhas, arquivo original de até 10 MB e otimização para a meta de até 1 MB. Validar tamanho e formato real no servidor, além de extensão/MIME declarados; limites de dimensões/pixels e política de metadados ainda serão detalhados. Compatibilidade HEIC deve ser resolvida por conversão no aplicativo ou suporte no processamento antes do lançamento em iPhone; mecanismo ainda não escolhido. Não rejeitar silenciosamente fotos compatíveis do dispositivo nem presumir que HEIC já é aceito pelo backend. Validar o fluxo em dispositivos reais e sua compatibilidade com a meta de 5 segundos após upload.
- Pergunta técnica 27: remover metadados de localização GPS antes de disponibilizar fotos a outros usuários, preservando a orientação visual correta. Aplicar o tratamento no processamento confiável do servidor, mesmo que o aplicativo já o faça. Imagens otimizadas, miniaturas e demais derivados disponibilizados não devem conter localização GPS. Não servir o original ainda não tratado a terceiros. Essa remoção não elimina localização eventualmente visível no próprio conteúdo da foto; testar metadados e orientação nos formatos suportados.
- Validação da foto em near real time, definida pelo usuário: confirmar sucesso ou informar falha no próprio fluxo após o upload, sem aprovação silenciosa nem espera indefinida. A participação só pode ser concluída quando a validação obrigatória tiver sucesso; em falha, preservar rascunho e oferecer correção/reenvio. Verificação de formato/conteúdo de arquivo não equivale a comprovação de autenticidade da medalha nem moderação visual por IA.
- Contrato de processamento da imagem: pendente, válida ou falha, com motivo compreensível. Meta aprovada pelo usuário: retorno da validação em até 5 segundos após o término do upload, em condições normais, sujeito à validação nos testes de desempenho. O tempo de transferência do arquivo não integra essa meta. Condições de carga e critério estatístico de medição ainda serão especificados; a meta não é garantia de latência máxima em qualquer situação.
- Implementação pode usar requisição de finalização com resposta imediata quando possível ou acompanhamento curto de estado; mecanismo e limite de espera operacional ainda serão definidos. Ultrapassar a meta não transforma a imagem em válida nem equivale automaticamente a arquivo inválido. Timeout não significa sucesso; impedir conclusão/publicação enquanto pendente e oferecer recuperação ou retentativa segura. Otimização/miniaturas podem ser desacopladas somente se a imagem validada necessária à conclusão já estiver disponível.
- Rascunhos não contribuem para RunScore, medalheiro público nem métricas de conclusão.
- RunScore usa somente avaliações válidas; calcular com precisão e arredondar na exibição. Sem notas, mostrar ausência de avaliação, não nota zero.
- Invalidar avaliação mantém histórico e publicação, mas remove notas públicas e do agregado; correção só retorna após revisão humana.
- Editar a edição atualiza referências e agregados de ambas; conflito de unicidade não sobrescreve cadastro existente. Exclusão da participação remove os vínculos aprovados.
- Exclusão aprovada na revisão técnica: após confirmar a operação, retirar imediatamente a participação e sua publicação da exibição e impedir novas interações. Limpeza física das imagens próprias e dos dados vinculados pode ocorrer em segundo plano, com idempotência, retentativas e monitoramento. Leituras devem conferir o estado de exclusão na fonte, mesmo quando índices/projeções ainda estiverem atrasados. Atualização do RunScore segue a regra assíncrona aprovada.
- Limpeza não deve apagar imagens oficiais do catálogo nem objetos compartilhados ainda referenciados. URLs temporárias já emitidas e cópias exportadas têm limitações de revogação, a tratar na política de acesso/expiração. Prazo máximo de limpeza, retenção de backups e exclusão de dados pessoais precisam de detalhamento; não afirmar remoção física imediata de todas as cópias.
- Arquivamento aprovado nas perguntas técnicas 33–34: impedir novos registros de participação, conclusão de rascunhos e transferência de participação para a edição arquivada. Preservar rascunhos e participações de origem sem alterações parciais e informar o motivo do bloqueio ao usuário. Manter consulta ao histórico e edição/exclusão das participações já existentes, respeitando proprietário, unicidade, avaliação e visibilidade. Validar o estado da edição no servidor, inclusive diante de operações concorrentes com o arquivamento. Edição antiga não é automaticamente arquivada apenas por sua data.
- Ordenação do feed aprovada pelo usuário: primeiro publicações de autores que o usuário segue, depois as demais; mais recentes primeiro em cada grupo. Exibir apenas publicações visíveis e autorizadas, respeitando ocultações, exclusões, bloqueios, suspensão e moderação. Aplicar paginação com desempate estável; cursor e estratégia de consulta/projeção ainda serão detalhados para DynamoDB. Não alterar a data de publicação apenas por editar a participação nem exibir a mesma publicação novamente na transição entre grupos. Política para inserções e mudanças de seguimento durante a navegação será especificada e testada.
- Bloqueio preserva registros anteriores, ocultando-os entre envolvidos, e impede novas interações. Não prometer proteção sobre cópias exportadas.
- Avisos e feedback não dependem de push. Emissão de avisos após transações deve tolerar retentativa e evitar duplicação.
- Links abrem no app ou na loja; validar configuração de domínio e associação das plataformas sem criar site público completo.
- Solicitação aprovada ou vinculada não conclui participação automaticamente: corredor revisa e conclui.

### Beta, observabilidade e feedback

- Pergunta técnica 30: idade mínima de 18 anos completos durante o beta, confirmada pelo usuário, com possibilidade de redefinição em evolução futura mediante revisão de requisitos. Não admitir menores na fase atual por antecipação dessa evolução.
- Pergunta técnica 31: confirmação por autodeclaração com preenchimento da data de nascimento. Validar no servidor data válida, não futura e idade mínima de 18 anos completos na admissão, sem considerar apenas o ano de nascimento. Definir referência de calendário/fuso e testar limites de aniversário e datas bissextas. Data de nascimento é informação privada de cadastro: não expor em perfil, publicações, cards ou respostas públicas, nem incluir desnecessariamente em logs e analytics. Não exigir documento por inferência e não apresentar autodeclaração como verificação documental. Retenção, correção e descarte desse dado serão tratados na política de privacidade/exclusão antes do beta.

- Pergunta técnica 28: distribuição definida pelo usuário diretamente pelas lojas oficiais de aplicativos, tanto no beta quanto na produção futura, para evitar dependência de links de convite percebidos como suspeitos. Não usar download externo ou convite individual por link como fluxo obrigatório de instalação. Publicação, aprovação e modalidades disponíveis em cada loja ainda devem ser verificadas antes de prometer distribuição pública do beta.
- Pergunta técnica 29: liberar cadastro e admissão para os primeiros 1.000 usuários elegíveis e, atingido o limite, oferecer lista de espera dentro do app. Substitui o beta por convite; não exigir link ou código de convite. Manter elegibilidade etária e início dos 60 dias com os primeiros 50 admitidos. Lista de espera não conta como admissão nem no denominador de ativação e não libera acesso automaticamente. Exclusões não reabrem vagas por padrão. Coleta mínima, confirmação ao interessado, deduplicação e comunicação de novas liberações ainda serão detalhadas; não introduzir push por inferência.

- Retenção de pontos de recuperação operacional de PROD definida pelo usuário: 7 dias durante o beta, a revisar ao final dessa fase antes de estabelecer a política posterior. Esta definição substitui a sugestão de 35 dias; não configura prazo de exclusão de dados ativos, logs ou dados pessoais. Especificar mecanismos compatíveis para DynamoDB e imagens S3 e validar recuperação coerente com RPO/RTO. Nenhum backup foi criado ou configurado nesta revisão.
- Alertas críticos de operação serão destinados à equipe RunPass por e-mail, canal inicial aprovado pelo usuário. Configurar o endereço de grupo antes do beta, fora dos documentos versionados. Cobertura de atendimento, confirmação do recebimento e eventual escalonamento ainda precisam ser definidos; responsável principal/substituto não foi nomeado. Essa definição é de alertas operacionais e não introduz push ou notificações de produto por e-mail. Mecanismo de envio ainda a especificar e testar.

- Recuperação de PROD: RPO de até 5 minutos e RTO de até 4 horas aprovados pelo usuário, respectivamente metas de perda máxima de dados e tempo de restabelecimento em incidentes que exijam recuperação. Validar por cenário a viabilidade técnica, custo e cobertura dos mecanismos antes da implantação; não representam garantias já implementadas nem frequência esperada de perda. Banco, imagens e demais dependências precisam ser recuperados de forma coerente. Definir o marco de início da medição do RTO, critérios para considerar o serviço restabelecido, responsáveis e procedimento, e comprovar as metas por testes de restauração. Não presumir recuperação de toda a região ou de todos os tipos de incidente sem projeto específico. RTO não é franquia de indisponibilidade nem substitui a meta de disponibilidade de 99,5%; verificar separadamente a compatibilidade dessas metas na revisão operacional.

- Cenário esperado de uso para orçamento, aprovado pelo usuário: 300 usuários por dia, duas sessões por usuário/dia, totalizando 600 sessões/dia ou 18.000 sessões em um mês de referência de 30 dias. Não representa usuários simultâneos nem altera a definição de ativação do beta. Imagens por sessão aprovadas abaixo; chamadas por sessão são hipótese técnica de dimensionamento.
- Premissas consolidadas no documento complementar PREMISSAS-USO-RunPass-MVP.md, com cenários econômico, esperado e pico, separação DEV/PROD e fórmulas de armazenamento, tráfego, API, Lambda e DynamoDB. Hipóteses adicionais são parâmetros de simulação, não limites funcionais ou orçamento aprovado.
- Premissa de imagens por sessão aprovada: 30 carregamentos, utilizando miniaturas no feed e imagem maior ao abrir detalhes. Com 18.000 sessões/mês, considerar 540.000 carregamentos de imagens/mês, antes de deduplicação e cache. Isso não representa imagens únicas armazenadas nem implica transferir 1 MB em cada carregamento. Tamanho das miniaturas, proporção de detalhes e eficiência de cache serão hipóteses explícitas da estimativa; não exigem nova aprovação para cada cenário de simulação.

- Premissas de orçamento confirmadas pelo usuário: 20 medalhas por usuário e até 1 MB por foto própria otimizada. No cenário de 1.000 usuários e 20.000 fotos próprias distintas, considerar aproximadamente 20 GB decimais antes de miniaturas, versões e metadados. Não é limite funcional de medalhas nem definição final do tamanho aceito no upload original. Imagens do catálogo podem ser compartilhadas por referência; quantidade real de uploads, derivados, versões e tráfego ainda precisam ser estimados.
- Orçamento mensal de DEV e PROD ainda não definido: produzir estimativa após revisão técnica, com premissas de carga e cenários econômico, esperado e pico. Nenhum teto de gastos foi aprovado.

- Contabilizar admitidos únicos em transação para não ultrapassar 1.000 em admissões concorrentes. Registrar marco de entrada do 50º; fim em 60 dias. Contagem não reinicia por exclusão.
- Ativação >=50% dos admitidos reais, incluindo os primeiros 50; repetição >=30% dos ativados em outra edição; interação >=30% dos ativados com like/comentário em conquista alheia.
- Definir em revisão técnica como correções e exclusões afetam o relatório histórico, sem duplicar ativação por recriação. Eventos de comportamento não devem expor resultados ocultos ou texto pessoal desnecessário.
- Logs estruturados com correlação, latência, erros e operações administrativas; nunca credenciais. Monitorar jornadas, não apenas disponibilidade de infraestrutura.
- Metas herdadas: inicial <3 s, média API crítica <500 ms, disponibilidade 99,5%; medições exigem perfil de dispositivo/rede, endpoints e janela definidos. Não garantir esses números antes de testar.
- Feedback voluntário: facilidade após primeiro registro (1–5 e texto opcional), botão problema/sugestão/elogio, pesquisa aos 30 dias, fechamento aos 60 e pergunta após sete dias sem registro. Consolidar semanalmente.
- Preparar exclusão de conta e dados com política de retenção, tratamento de terceiros, backups e métricas; política ainda não aprovada e não pode ser inventada pela implementação.
- Exclusão de conta aprovada na pergunta técnica 25: após confirmação da solicitação, bloquear o acesso e ocultar imediatamente o perfil e o conteúdo do usuário, realizando a limpeza dos dados em segundo plano. Aplicar o bloqueio nas operações da API, inclusive com tokens anteriormente emitidos, e não apenas encerrar a sessão no aplicativo. Processamento idempotente, com retentativas e acompanhamento de conclusão. Prazo de limpeza, tratamento de conteúdo de terceiros, dados agregados, registros sujeitos a retenção e backups serão definidos na política de exclusão; não afirmar apagamento físico imediato de todas as cópias. Restauração de backup não deve reativar contas nem republicar conteúdo excluído sem reaplicar os registros de exclusão pertinentes.

## Testing Decisions

**Condição de liberação do beta aprovada na pergunta técnica 35:** executar e documentar testes das jornadas essenciais em Android e iPhone, teste de carga, verificação de segurança e um teste de restauração antes de liberar o beta em PROD. Registrar versão/artefatos, ambiente, cenários, critérios de aceite, resultados e achados. Não confundir aprovação desta exigência com testes já executados. Definir o tratamento de achados e registrar a decisão humana de liberação, sem inventar limiares ou aceitar falhas silenciosamente. Restauração deve verificar coerência entre dados e imagens e as metas RPO/RTO nos cenários cobertos; não restaurar destrutivamente sobre dados reais dos participantes para testar.

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
3. Arquitetura, orçamento em São Paulo (`sa-east-1`), stack do painel e responsável técnico. Região e CloudFormation já definidos; templates e estratégia de stacks ainda a detalhar.
4. Retenção/exclusão, verificação etária, limites de upload e lista de espera com admissão concorrente dentro do teto.
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

Revisão de cobertura em 27/10/2026: COBERTURA-PRD-OPENAPI-RunPass.md mapeia jornadas representadas/parciais e requisitos fora do contrato. OpenAPI atualizado para 0.6.1-draft, 49 caminhos/62 operações: referências da imagem oficial da medalha, versão da edição e alinhamento do envelope de auditoria. Validação semântica OpenAPI 3.0.3 com openapi-spec-validator 0.7.2: zero erros; 12 exemplos de schemas aprovados. Evidência com hash em VALIDACAO-OPENAPI-RunPass.json e script/requirements reproduzíveis. O resultado supera as pendências anteriores de validação semântica, mas não representa execução da API, cobertura integral do PRD ou aprovação técnica.

Bloco operacional consolidado em OpenAPI 0.6.0-draft: 49 caminhos e 62 operações. Acrescentados status/admissão/lista de espera, exclusão da própria conta, denúncias, feedback, revisão de solicitações, manutenção/arquivamento de edições, moderação, papéis e consulta restrita ao histórico. REVISAO-OPENAPI-OPERACAO.md registra controles e lacunas. Verificados JSON, referências internas, operationIds, parâmetros, marcações administrativas e 14 exemplos positivos/negativos. Não equivale a validação semântica integral, API implementada ou autorização de provisionamento.

Fluxos de bootstrap autenticados antes de admissão não devem exigir vaga prévia; cadastro/validação de e-mail e emissão de tokens são fluxos do provedor Cognito. Operações administrativas não consomem vaga de corredor por inferência; separar métricas das contas técnicas. Extensões do contrato que descrevem MFA/papéis/admissão precisam de implementação explícita, não são mecanismos de segurança executáveis por si só.

Expansão social: OpenAPI 0.5.0-draft com 34 caminhos e 45 operações, incluindo feed/posts, seguir/bloquear, curtidas/comentários, wishlist e avisos internos. REVISAO-OPENAPI-SOCIAL.md registra comportamento aprovado preservado e propostas/lacunas. Checadas referências, operationIds, parâmetros de caminho, respostas 204 e dez exemplos positivos/negativos de schemas. Ainda não é contrato completo ou validação semântica integral; nenhuma rota foi implantada.

Expansão de catálogo/perfis: OpenAPI 0.4.0-draft com 21 caminhos e 26 operações, incluindo edições, avaliações públicas atuais, perfil próprio/público e solicitações de inclusão/correção/reenvio. Complemento REVISAO-OPENAPI-CATALOGO-PERFIS.md registra escopo e lacunas. Solicitações não são catálogo público; respostas de perfil não incluem nascimento/e-mail; rascunhos de prova ausente aceitam distância em quilômetros até a vinculação à edição. Campos, limites e estados detalhados permanecem propostas técnicas.

Atualização de 27/10/2026: OpenAPI 0.3.0-draft ampliado para 9 rotas e 12 operações, incluindo criação de rascunho, consulta/listagem, exclusão e status da limpeza. Validado JSON, referências internas, unicidade dos operationIds e correspondência dos parâmetros de caminho; validação semântica OpenAPI ainda pendente. Limites de página, nomes/unidades e detalhes de concorrência são propostas técnicas, não novas decisões funcionais aprovadas.

DATA-LAKE-AVALIACOES-RunPass-v1.md detalha proposta de entrega e descarte; EVENTO-AUDITORIA-AVALIACAO.schema.json descreve evento antes/depois. Retenção de 60 dias desde ocorrência é requisito aprovado; periodicidade do descarte, formato e tratamento de eventos pendentes além do prazo ainda são propostas/lacunas. ORCAMENTO-RunPass-preliminar.md e seu script foram atualizados com linhas de entrega/armazenamento do lake e exclusões explícitas, usando as tarifas públicas já coletadas, sem nova consulta de preços ou implantação.

Artefatos complementares preparados nesta consolidação, todos DRAFT:

- MODELO-DYNAMODB-RunPass-v1.md: proposta parcial do agregado relacionado participação/avaliação/medalha, índices candidatos, acesso e lacunas dos demais domínios. Não é esquema integral aprovado.
- API-RunPass-v1.openapi.json: contrato inicial parcial de conclusão de participação e upload/finalização/status, com validação sintática JSON realizada. Validação semântica OpenAPI e geração de clientes ainda pendentes.
- ORCAMENTO-RunPass-preliminar.md: simulação de sensibilidade em São Paulo; subtotal e reserva separados, com exclusões explícitas. Valores não aprovados como teto nem promessa de custo final.
- AWS-PRECOS-SA-EAST-1.json, ORCAMENTO-RunPass-simulacao.json e calcular_orcamento_runpass.py: evidência de tarifas públicas e cálculo reproduzível. Executar script a partir da pasta que contém esses arquivos. Não descontar gratuidades por inferência.

Documento complementar FECHAMENTO-TECNICO-RunPass-MVP.md preparado com matriz de acesso, contratos HTTP/eventos e critérios de teste propostos. Não define tabelas ou índices finais antes de confirmar configurações operacionais por agregado; não substitui validação de desempenho, orçamento nem aprovação técnica.

Rodada de decisões técnicas: 35 perguntas respondidas; o número foi estimativa de acompanhamento, não limite imposto pelo usuário. Não iniciar nova sequência automaticamente para detalhes resolvíveis por análise técnica. Ainda faltam modelagem DynamoDB e padrões de acesso com chaves/índices, contratos da API/eventos, recuperação da outbox, validação do painel Flutter Web, autenticação MFA detalhada, retenção/exclusão, orçamento e critérios mensuráveis dos testes. Consolidar propostas revisáveis para fechar essas lacunas antes da aprovação técnica integral. Nenhuma implementação, provisionamento ou teste de liberação foi executado por registrar estas decisões.

Atualização da rodada: 40 perguntas técnicas respondidas. Recuperação conjunta, ausência de TTL no histórico, eventos e configuração comum de criptografia/acesso do agregado participação/avaliação/medalha foram confirmados; retenção dos itens operacionais terá política própria. Nenhuma pergunta dessa sequência permanece aguardando resposta. Próximo trabalho: produzir proposta física de dados rastreável aos padrões de acesso, identificar os parâmetros dos demais agregados ainda desconhecidos e consolidar contratos, custos e critérios de teste para revisão, sem tratar a SPEC integral como aprovada.

Revisar as propostas e validar riscos com prova técnica quando necessário; aprovar a especificação e então produzir implementation-slices. Não criar tickets como prontos para execução enquanto escolhas essenciais permanecerem abertas.

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