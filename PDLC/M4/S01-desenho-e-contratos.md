# S01 — Desenho e contratos da primeira entrega

Data: 28/10/2026. Estado: **aceito pelo usuário após revisão dos três blocos**. Desenvolvimento S01 autorizado pelo usuário após preparação S00. O aceite deste desenho não equivale à implementação dos mecanismos, ao aceite humano final nem à liberação de infraestrutura.

## Resultado e fontes

O modelo físico vigente da primeira entrega está em `MODELO-DYNAMODB-RunPass-v1.md`: tabelas, PK/SK, índices, fonte/projeção, matriz rota→acesso, transações, recuperação e enumeração por titular. O contrato correspondente é `API-RunPass-v1.openapi.json` 0.8.0-draft. A SPEC continua única em `SPEC_RunPass_MVP_v1.md`; este documento é evidência e fechamento do slice, não uma segunda SPEC.

Decisões já aprovadas continuam aprovadas. A única nova decisão de privacidade foi solicitada explicitamente e aprovada em 28/10: controle mínimo de exclusões por até 15 dias, segregado, pseudonimizado e acessível apenas à recuperação. Não guardar nome, e-mail, fotos ou avaliações nele. O prazo ordinário dos demais dados pessoais ativos continua sete dias. O mecanismo criptográfico e a comprovação operacional continuam a implementar.

## Decisões locais de engenharia

| Tema | Desenho escolhido | Evidência exigida no slice de código |
| --- | --- | --- |
| Username | ASCII letras/dígitos/underscore, 3–30 caracteres; minúsculas na representação e unicidade; entrada com espaço/acento é rejeitada, sem transliteração | Dois cadastros/trocas concorrentes, variação de caixa, reserva e liberação na mesma transação |
| Perfil inicial | PUT /me autenticado antes da admissão, displayName e username obrigatórios; GET próprio disponível sem vaga | Identidade validada, e-mail confirmado, sem autoatribuição de roles/admissão e sem recriação de excluído |
| Dados do perfil | displayName até 80, cidade 100, bio 500 caracteres; rejeitar nome apenas whitespace; bib até 40 e privado | Normalização, limites Unicode e respostas com allowlist |
| Comentário da avaliação | Até 2.000 caracteres Unicode; sem truncamento; oito notas inteiras 1–5 | Campo omitido no PUT remove atual, evento antes/depois durável; limites de item/evento em bytes |
| Página | limit 20 default, máximo 100; cursor autenticado 15 minutos, vinculado a ator/filtros/limite/ambiente; até 500 candidatos por resposta | Continuação de página vazia, limite durante hidratação, adulteração e mudanças concorrentes |
| Catálogo | Seis filtros existentes combináveis, consultas DATE/NAME e facets; sem Scan global, sem truncar conjunto | Coleção estável completa, prefixo com data, cidades homônimas, distância Decimal e geração parcial |
| História e review | Agrupamento por titular/participação; CLAIM usuário/edição independente; effectVersion para todo efeito de score | ID estável em troca de edição, rascunho versus conclusão, revisão e compensação antigas |
| Foto própria | JPEG/PNG, 10 MB aprovados; 25 megapixels de proteção inicial; sessão 15 min, finalize captura versão S3, processamento resolve até 15 min | Sobrescrita após finalize, orientação/GPS, decompression bomb, iPhone HEIC e retry |
| Download | Referência opaca, derivado privado e URL de cinco minutos | Dono/origem/ambiente, não servir original; medir validade residual após ocultação |
| Eventos | Outbox transacional, SQS com referência sem payload, confirmação por consumidor e versão na projeção | Duplicação, ordem invertida, falha entre efeito/confirmação e reconstrução com barreira |
| Recuperação | Replay até sete dias de allConfirmedAt; transporte de um dia; controle mínimo até 15 dias | Restore isolado, expurgos, epoch, mensagens antigas, descarte do controle no marco |

Esses parâmetros limitam recursos sem alterar as jornadas aprovadas; não comprovaram desempenho/compatibilidade. Mudanças com impacto real de produto, custo ou privacidade precisam de revisão; nenhuma ferramenta ou documentação significa recurso pago autorizado.

## Identidade e admissão: contrato para S02

Mobile chama Cognito para cadastro/confirmação/login/recuperação; não criar endpoints de senha fictícios na API RunPass. Bootstrap PUT /me só aceita access token válido do pool/client de corredores, e e-mail confirmado verificado em fonte Cognito confiável; acesso a esse estado privado não depende de claim inexistente no access token. Verificar assinatura com JWKS conhecido, algoritmo permitido, kid, issuer, expiração, token_use=access e client_id esperado (aud adicional se configurado), sem aceitar ID token no lugar. sub é identidade autenticada; ator nunca vem do corpo. Falha de verificação é 401, conta inelegível/sem admissão 403, estado não disponível 503 fechado, inexistência de recurso autorizado 404.

Pré-admissão permite apenas bootstrap/consulta própria, status, admissão, espera e exclusão conforme contrato. Perfil obrigatório antes de admissão; admissão exige e-mail confirmado, data válida, idade completa >=18 na data local São Paulo e autodeclaração. Não armazenar senha ou cópia de tokens nos itens de perfil/log. Dados privados de idade em item separado; após admissão não permitem alteração pelo PATCH público. Definir correção excepcional por suporte restrito antes de ativar esse procedimento; não acrescentar endpoint público por inferência.

Admissão usa contador CAS e condições de versão; perder disputa no 50º/1000º implica reler e tentar novamente com limite, sem ultrapassar teto. Horário do commit lógico vem do serviço confiável e é persistido na transição 49→50, não fornecido pelo cliente. Contas técnicas/operator não chamam admissão. Admissão já existente retorna resultado atual sem incrementar, ainda que CMD anterior tenha expirado. Janela encerrada recusa novas admissões; continuidade pós-beta não é aprovada aqui.

### Operadores e MFA

Pools e clients separados por ambiente/público; self-signup e federação desabilitados no pool operador; TOTP obrigatório. Não inferir cumprimento de MFA apenas de JWT válido ou de configuração do pool: a documentação Cognito descreve emissão inicial de tokens antes do fator adicional.

Protocolo escolhido para a primeira operação interna: ferramenta restrita de operação executa autenticação Cognito e observa a conclusão de SOFTWARE_TOKEN_MFA; só o componente confiável que recebe a resposta final pode gravar attestation em `OPERATOR#sub / SESSION#SHA256(accessToken)`, com issuer/client/auth_time/verifiedAt/expiresAt e sem token, senha ou segredo TOTP. A API exige attestation exata, acesso atual e permissão específica. Expiração máxima de uma hora e nunca além do token; refresh sem nova prova não cria attestation. Troca/recuperação de MFA ou suspensão invalida sessões. Token de primeiro acesso/enrollment sem SOFTWARE_TOKEN_MFA concluído não ganha permissão administrativa.

A ferramenta de emissão da attestation roda com papel de infraestrutura restrito, não com permissão atribuída livremente ao próprio operador ou ao app cliente. Logs sem credenciais. Bootstrap cria operador sem permissão operacional até inscrição TOTP e autenticação comprovada; outro responsável revisa/ativa ACCESS. Procedimento local pode ser preparado sem AWS. Recuperação exige verificação por responsável distinto, revogação de sessões e novo enrollment; não há bypass de MFA por endpoint. Nomes dos responsáveis e política IAM devem estar configurados antes de habilitar administração real; falta de prova mantém rotas administrativas desabilitadas. O painel completo precisará integrar o mesmo protocolo ou equivalente revisado em seu próprio slice.

Esse protocolo é desenho de integração, não prova de que Cognito/MFA funciona. Testes reais do fluxo inicial/enrollment/refresh/recuperação pertencem a S02/S09; planos e custo Cognito continuam a verificar antes de provisionar.

## Revisão de falhas e concorrência

| Disputa/falha | Condição/resultado esperado | Onde demonstrar |
| --- | --- | --- |
| Dois usernames iguais com caixas distintas | Uma CLAIM normalizada, um vencedor; sem perfil parcial | S02 |
| 49→50 e 999→1000 simultâneos | CONTROL CAS, marco único e teto respeitado; deletar não libera vaga | S02 |
| Mesma conclusão repetida após resposta perdida | CMD durável e CLAIM; mesmos IDs, sem segundo efeito | S04/S06 |
| Duas chaves diferentes para mesma edição | CLAIM existente retorna 409 e orientação para registro existente | S04/S06 |
| Arquivar catálogo versus concluir | Condição HEAD na mesma transação; vencedor define resultado | S03/S06 |
| Editar review versus concluir/excluir/mudar edição | PART/REVIEW versões verificadas; efeito monotônico, sem review órfã | S06/S08 |
| Validar arquivo e depois sobrescrever upload | VersionId fixado; original/versão nova não alteram derivado validado | S05 |
| Limpar imagem versus vincular | IMAGE valid/refcount CAS na mesma transação do vínculo | S05/S06 |
| Evento v3 antes de v2, duplicado ou após delete | Reconciliar fonte/contribuição e negar payload ausente/excluído; sem soma duplicada | S07/S08 |
| S3 gravou mas confirmação falhou | Objeto determinístico + integridade; retentar confirmação, não novo histórico | S07 |
| Replay/restauração de versões antigas | Epoch/fonte/controle atual prevalecem, tráfego fechado até expurgo | S07–S09 |
| GSI ou índice de catálogo atrasado | Fonte atual revalidada, sem vazamento; resultado pode ser eventual | S03/S08 |

Nenhuma linha da tabela é declarada teste de concorrência executado nesta etapa. Critérios pertencem aos testes de implementação, não a mocks que apenas reproduzem o desenho.

## Fontes técnicas verificadas

Consultadas em 28/10/2026; escolhas do RunPass acima são desenho de engenharia, não recomendações automáticas da AWS.

- [DynamoDB transactions](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transaction-apis.html): até 100 itens distintos/4 MiB, sem duas ações no mesmo item.
- [Query pagination](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Query.Pagination.html): cursor pode continuar mesmo com página filtrada vazia.
- [DynamoDB TTL](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html): remoção eventual, insuficiente como garantia de prazo máximo.
- [SQS parameters](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-configure-queue-parameters.html): retenção configurável; não é arquivo permanente de recuperação.
- [Presigned URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html) e [S3 versions](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html): URL permite sobrescrita; VersionId e derivado separado protegem referência finalizada.
- [Cognito access tokens](https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-the-access-token.html) e [MFA](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-mfa.html): validar access token e não inferir desafio MFA de qualquer token.

## Evidências e dependências restantes

A execução de `make check` gera `VALIDACAO-OPENAPI-RunPass.json` com hash, estrutura, exemplos positivos/negativos e 64 combinações de presença dos filtros de catálogo aceitas pelos schemas dos parâmetros. Isso não testa o plano DynamoDB, datas cruzadas, autenticação, tamanho de foto ou concorrência. S00 havia 12 exemplos; S01 adiciona limites, origem exclusiva do rascunho, bootstrap, estados de upload e proibição de dados privados no histórico público.

Resultado executado: OpenAPI sem erros, 55 caminhos, 72 operações, 673 referências internas, **39 exemplos** aprovados e **64 combinações** de parâmetros aceitas. Ruff/análise de formatação passaram; `git diff --check` sem erros. O contrato foi revalidado após os ajustes finais de descrições. Hash atual no relatório, conferido contra o arquivo.

A importação dos pacotes na `.venv` do workspace ficou lenta em leitura de arquivos de schemas (diagnóstico por traceback). Repetida instalação limpa do mesmo `requirements-dev.lock` em `/private/tmp/runpass-s01-validation-venv`, seguida de `make check PYTHON=/private/tmp/runpass-s01-validation-venv/bin/python RUFF=/private/tmp/runpass-s01-validation-venv/bin/ruff`, com sucesso. A última revalidação usou `make contract` com esse Python. Não foi necessário alterar dependências. O aviso de depreciação de RefResolver já documentado na S00 permanece, sem falha de validação.

S02 pode iniciar implementação local da identidade/admissão e seus testes após revisão deste desenho. Operação real é condicionada à configuração e evidências descritas; S03–S08 dependem dos slices anteriores.

Antes de S07: decisão sobre descarte de payload de auditoria pendente aos 60 dias, frequência/prazo de descarte físico do lake e prova de reconstrução concorrente. Antes de habilitar módulos fora do primeiro fluxo: busca pública de perfis, solicitações/espera/feedback e suas políticas de retenção, feed/social e painel completo. Antes de S09: orçamento completo/autorização, conta DEV e IAM/segredos/armazenamento de recuperação, benchmark, testes reais Android/iPhone e restore. Nenhuma pendência histórica já resolvida é reaberta por esta lista.

Sem implementação de API, recursos, deploy, commit, push ou publicação por este slice. Alterações S00 do workspace foram preservadas.


## Revisão com o usuário — perfil e cadastro, 28/10/2026

O usuário respondeu “concordo” ao bloco apresentado: nome obrigatório até 80 caracteres com espaços/acentos; username único de 3–30 caracteres ASCII (letras, números e underscore), convertido para minúsculas; cidade opcional até 100; bio opcional até 500; número de peito opcional até 40 e privado. Nome e username preenchidos antes da admissão, sem conceder acesso às corridas/funções sociais somente pela criação do perfil. Bloco aprovado; não constitui aceite dos demais blocos ou da S01 integral.


## Revisão S01 — catálogo e avaliações aprovados, 28/10/2026

O usuário respondeu “concordo” ao bloco apresentado: combinar cidade, estado, distância, período e início do nome na busca; ignorar acentos e caixa na comparação do nome; ordenar por data crescente, ou alfabeticamente na busca apenas por nome; carregar 20 resultados por vez com continuação; comentário de avaliação opcional até 2.000 caracteres, com aviso de excesso e sem truncamento. Oito notas e RunScore por edição permanecem conforme aprovação anterior. Bloco aprovado, sem inferir aceite do bloco de fotos/falhas ou da S01 integral.


## Revisão S01 — fotos e falhas aprovados, 28/10/2026

O usuário respondeu “concordo” ao último bloco: conversão HEIC→JPEG no aplicativo; redução local acima de 25 megapixels; preservação do rascunho e nova tentativa em interrupção; sessão de envio de 15 minutos, com nova sessão após expiração; conclusão somente após validação aprovada; falha/timeout de processamento informado sem perder rascunho, com limite técnico de 15 minutos após finalize. JPEG/PNG, 10 MB e remoção de GPS permanecem definidos; a meta de cinco segundos pós-upload não é substituída pelo limite de tentativa travada. Compatibilidade e desempenho precisam de testes nos slices de implementação.

## Aceite da revisão S01 — 28/10/2026

Concluída a revisão sequencial dos três blocos apresentados (perfil/cadastro; catálogo/avaliações; fotos/falhas), todos com resposta “concordo”. S01 aceita no escopo do desenho revisado, com detalhes internos de engenharia sob responsabilidade técnica e controle mínimo de exclusões de 15 dias aprovado separadamente. O aceite não comprova implementação, concorrência, segurança/MFA, desempenho ou integração real; evidências futuras e dependências registradas continuam obrigatórias. Próximo slice: S02 local de identidade, perfil e admissão. Não há autorização de custo, provisionamento, deploy ou beta por este aceite.
