# RunPass — Slices de implementação da primeira entrega

Data: 27/10/2026. Fonte única: SPEC_RunPass_MVP_v1.md. Escopo aprovado: autenticação → catálogo → rascunho → imagem → conclusão → avaliação e medalha.

Estado do plano: preparado a partir das direções aprovadas; não comprova implementação ou testes. Cada slice possui dependências e saída verificável. Nenhum slice é marcado como concluído. Propostas técnicas são resolvidas dentro dos slices de desenho; não exigem reaprovação de nomes de atributos. Escolhas que alterem produto, custo ou privacidade voltam ao usuário.

## Regras de execução

- Antes de codificar, concluir a preparação de contexto/regras e harness prevista em M4.1/M4.2, limitada à entrega.
- Trabalho local de desenho e testes pode começar sem criar recursos AWS. Provisionamento pago exige orçamento aplicável e autorização ainda pendentes.
- Usar API-RunPass-v1.openapi.json e MODELO-DYNAMODB-RunPass-v1.md, atualizando-os com a SPEC quando o desenho for fechado.
- Evidência de aceite: revisão da mudança, resultados dos testes pertinentes e limitações registradas. Não confundir teste local com integração real na AWS.
- Cada entrega deve respeitar exclusão/bloqueios e autorização; não publicar conteúdo sob justificativa de ser um slice inicial.

## Sequência e estado inicial

| ID | Resultado | Dependências | Estado |
| --- | --- | --- | --- |
| S00 | Contexto, estrutura e verificações locais | SPEC prioritária aprovada | Pronto para iniciar preparação |
| S01 | Desenho físico do fluxo inicial e contratos fechados | S00 | Aguardando desenho/revisão |
| S02 | Identidade, admissão e autorização | S01 | Aguardando dependências |
| S03 | Catálogo consultável e carga controlada | S01, S02 | Aguardando dependências |
| S04 | Participação em rascunho | S03 | Aguardando dependências |
| S05 | Upload e imagem validada | S02, S04 | Aguardando dependências |
| S06 | Conclusão atômica, avaliação e medalha | S04, S05 | Aguardando dependências |
| S07 | Entrega de eventos, RunScore e histórico restrito | S06 | Aguardando dependências |
| S08 | Edição, exclusão e proteção de dados | S06, S07 | Aguardando dependências |
| S09 | Integração real em DEV e aceite da entrega | S02–S08, orçamento/autorização | Bloqueado para provisionamento |

Não é uma decomposição de todo o MVP. Feed completo, interações sociais, wishlist, painel completo e pós-beta terão slices próprios depois; não foram removidos do escopo do produto.

## S00 — Preparação do contexto e execução local

Resultado: estrutura de backend/mobile/infra documentada, instruções AGENTS/RULES pertinentes e comandos reproduzíveis para validação, teste e análise estática.

Trabalho: inspecionar código existente antes de criar estrutura; fixar versões e dependências; configurar ambiente Python, projeto Flutter quando disponível e validação OpenAPI; definir dados sintéticos e isolamento de testes. Não criar segredos nem configurar credenciais permanentes.

Aceite: outra pessoa consegue executar as verificações locais documentadas; ausência de Flutter/Dart ou demais ferramentas fica explicitamente registrada. Checagens de contrato executáveis e teste mínimo relevante da lógica existente, sem testes artificiais que apenas copiem configuração. Não iniciar implementação sem contexto e comandos de verificação definidos.

## S01 — Modelo e contratos da entrega

Resultado: proposta física revisada para identidade/admissão, catálogo, participação/review/medalha, upload e operações/eventos envolvidos. Não é necessário modelar todo o feed para fechar este slice.

Trabalho: enumerar cada consulta/escrita, PK/SK, índices, projeções, unicidade, versões, recuperação e enumeração por titular. Escolher tabelas a partir dos requisitos; a proposta histórica de seis tabelas não é obrigação. Detalhar outbox transacional, contribuição versionada de RunScore, ledger, marco de replay e controle de exclusões. Definir quais dados são fonte e quais são projeção.

Fechar antes dos slices dependentes: normalização/uniquidade de username, filtros de catálogo suportados, limite de comentário/páginas/pixels, critérios de sessão de upload e proteção de chave após validação. Propor parâmetros técnicos e revisar impacto; não reduzir filtros do contrato silenciosamente. Definir provas de concorrência/ordem e política de retenção dos controles compatível com replay/restauração sem ampliar retenção pessoal por conveniência.

Aceite: matriz rota → consulta/transação → chave/índice; nenhum acesso crítico depende de scan global não justificado; transações enumeradas com condições e cenários de falha; contrato OpenAPI válido e coerente. Pendência que afete comportamento do slice seguinte impede marcá-lo como pronto. Não declarar eficiência ou custo medidos por desenho apenas.

## S02 — Identidade, elegibilidade e autorização

Resultado: aplicativo identifica o corredor e controla acesso conforme conta/admissão. Configuração declarativa de identidade separa corredores e operadores; integração real é verificada em S09.

Trabalho: abstrair identidade validada, autenticação e recuperação via Cognito; verificar issuer/audience/expiração e estado atual na API. Implementar admissão transacional, e-mail confirmado, data de nascimento privada, 18 anos completos, teto de mil e marco do 50º. Fluxos de status/espera/exclusão não exigem vaga prévia; demais rotas exigem admissão quando previsto. Separar MFA administrativo por autenticador e autorização por função, sem criar painel completo.

Aceite: tokens inválidos ou destinados a outro cliente negados; usuário não admitido não acessa catálogo protegido; concorrência não ultrapassa mil nem perde o marco inicial; nascimento não aparece em resposta pública/log; conta bloqueada não opera com token anterior. Documentar/bootstrap e recuperação de operadores antes de ativar administração. Testes locais de regras não substituem prova real de MFA em S09.

## S03 — Catálogo inicial consultável

Resultado: listar e detalhar edições/distâncias; estados e referências de imagens oficiais disponíveis para seleção no app.

Trabalho: consultas paginadas pelos filtros efetivamente definidos em S01; carga idempotente de catálogo sintético e importação controlada pela equipe. Não depender de painel completo para integração local. Upload administrativo só é exigido aqui se utilizado como caminho de carga; nesse caso cumprir autorização/MFA e contrato próprio.

Aceite: edição/distâncias corretas, filtros combinados previsíveis e cursor sem vazamento entre filtros; edição arquivada não aceita nova conclusão; dados de score não podem ser definidos pelo cliente. Catálogo real tem origem e revisão registradas; fixture não comprova cobertura das principais provas.

## S04 — Rascunho de participação

Resultado: corredor cria, consulta e altera rascunho de sua participação, sem publicar nem ativar conquistas.

Trabalho: persistir edição/distância e campos parciais, versões e autorização; integrar seleção de catálogo no aplicativo. Preservar rascunho em falhas e conflito; não ativar automaticamente solicitação de edição ausente. Solicitação completa é entrega posterior se não utilizada no primeiro fluxo.

Aceite: dados de outro usuário inacessíveis; edição/distância incompatível rejeitada; alteração concorrente não sobrescreve silenciosamente; rascunho não gera medalha pública, RunScore ou ativação. Repetir criação com a mesma chave respeita contrato idempotente.

## S05 — Upload e processamento da foto

Resultado: imagem própria passa de pendente para válida ou falha antes de poder concluir participação.

Trabalho: sessão privada, URL de upload de 15 minutos, finalização e consulta de estado; verificar dono/objeto real, JPEG/PNG até 10 MB, decodificação, GPS/orientação e otimização com meta de 1 MB. Integrar conversão HEIC no mobile conforme solução validada; original não tratado não é exposto. Limite de pixels e processamento definidos em S01.

Aceite: upload alheio, adulterado, expirado ou inválido não conclui corrida; timeout não aprova imagem; falha preserva rascunho; referência validada é protegida de sobrescrita pela URL ainda válida. Testes de metadados, orientação, tamanhos, retry e compatibilidade; meta de cinco segundos medida em S09, não presumida por mock.

Arquivos abandonados e imagens validadas nunca vinculadas seguem prazos aprovados, com rechecagem de vínculos. Não apagar imagem oficial compartilhada para limpar foto pessoal.

## S06 — Conclusão, avaliação e medalha

Resultado: fluxo vertical no aplicativo conclui a corrida e exibe participação, avaliação e medalha persistidas.

Trabalho: validar autodeclaração, edição/distância, oito notas e imagem oficial ou própria válida; transação grava itens relacionados, conversão do rascunho, idempotência e outbox. Guardar referência/versionamento da imagem oficial. Publicação respeita escolha de visibilidade e ocultação de resultado/pace.

Aceite: duas conclusões concorrentes geram apenas uma participação por usuário/edição; falha não deixa medalha ou review órfãos nem evento perdido; retry após resposta perdida não duplica efeitos. Sem nota obrigatória/imagem válida não conclui; uma edição distinta permite nova participação. Nova imagem oficial não muda medalha já registrada. Conferir jornada completa app → API → armazenamento local de teste.

## S07 — Consumidores, RunScore e auditoria de avaliação

Resultado: evento durável entrega efeitos derivados com recuperação; score usa contribuição vigente e histórico restrito recebe antes/depois necessário.

Trabalho: publicador/reconciliador, consumidores por finalidade, confirmação por destino, retentativas/falhas e replay controlado de até sete dias. Atualizar contribuição/score atomicamente quando possível; separar comentário histórico de consumidores operacionais. Ingestão S3 privada do histórico com expiração por ocorrência, acesso específico/MFA e auditoria. Meta de dez segundos para RunScore.

Aceite: duplicação, fora de ordem e falha entre escrita e confirmação não alteram score duas vezes; pendência reencontrável sem depender de uma única cópia de transporte; replay não renova prazos nem ressuscita dados excluídos. Payload concluído retido por sete dias desde última confirmação obrigatória; ledger segue desenho fechado em S01. Histórico vencido/excluído não é consultável. Política de payload de auditoria pendente após expiração deve estar resolvida antes de liberar esse caminho.

## S08 — Edição, exclusão e privacidade da entrega

Resultado: o usuário corrige/exclui seu cadastro e pode encerrar conta sem conteúdo permanecer acessível por índices atrasados.

Trabalho: alteração versionada de participação, PUT completo de review, exclusão própria, retirada/recomposição de score, ocultação de resultados e limpeza por titular. Omitir comentário no PUT remove o atual e grava histórico restrito. Troca de edição revalida unicidade e ajusta contribuições. Exclusão de conta bloqueia imediatamente e agenda limpeza por destino em até sete dias; proteger restore/replay com controle mínimo aprovado.

Aceite: conflito/duplicidade não sobrescreve outro cadastro; notas inválidas não substituem a review; exclusão não remove catálogo/imagens oficiais compartilhadas; projeções antigas não expõem conteúdo; tokens anteriores não dão acesso. Enumeração cobre atributos privados, fotos, filas e lake; execução parcial é retentada sem marcar conclusão prematura. Ensaio de restauração real ocorre em S09.

## S09 — Integração DEV, evidências e aceite da primeira entrega

Resultado: fluxo inicial demonstrado em DEV isolado, com relatório de limites e evidências dos serviços reais.

Pré-condições: orçamento aplicável completo e autorizado; acesso/configuração de conta DEV; responsáveis e recursos necessários definidos. Preparar CloudFormation e CI localmente antes disso é permitido; aplicar não é autorizado por este plano.

Trabalho: implantação por CloudFormation/GitHub Actions OIDC; integração real API Gateway/Cognito/Lambda/DynamoDB/S3/filas e monitoramento; testes Android/iPhone; carga no perfil aprovado; restore com RPO/RTO e reaplicação de exclusões; jobs de retenção, falhas/replay e permissões negativas. Promover mesmos artefatos somente após aprovação específica de PROD.

Aceite: relatório demonstra o fluxo, lista as evidências e compara com critérios acordados; registra limites, riscos e falhas sem declarar sucesso por ausência de medição. Testes de integração não acessam PROD. Aceite desta entrega não libera beta completo: feed/social, demais jornadas, políticas e requisitos de lançamento permanecem necessários.

## Fora desta primeira entrega

Feed completo, follow/block/comentários/likes, wishlist e avisos completos, painel administrativo integral, fila de solicitações/moderação completa e operação pós-beta. As regras desses módulos continuam aprovadas quando já definidas; não são implementadas implicitamente. Autorizações e privacidade relevantes ao fluxo inicial não podem ser adiadas com esses módulos.

## Acompanhamento

Atualizar estado por evidência: planejado → pronto (dependências resolvidas) → em execução → em revisão → aceito. Registrar por slice referência da mudança, verificações, resultados, decisão do revisor e pendências. Não há tickets externos publicados, código entregue, infraestrutura provisionada ou commit/push por criação deste plano.
