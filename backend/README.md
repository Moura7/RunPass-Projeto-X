# RunPass backend — S02 a S04

Implementação local de perfil, identidade e admissão. Setup/testes na raiz: `make setup` e `make check`. Dependências diretas em `requirements.in`, versões transitivas fixadas no lock da raiz. Instalação de runtime isolado: `python -m pip install -r backend/requirements.in -c requirements-dev.lock`.

## Organização

- `runpass/api.py`: nove operações HTTP da S02 e erros sem ecoar dados privados.
- `runpass/service.py`: perfil/username, idade, teto/marco do beta, espera, idempotência, bloqueio da exclusão e job durável.
- `runpass/store.py`: protocolo transacional, adaptador local em memória e adaptador DynamoDB com condições por versão/leitura forte.
- `runpass/identity.py`: validação RSA/JWT, consulta corrente Cognito, JWKS de issuer configurado e autorização de operadores.
- `runpass/operators.py`: emissão interna de sessão somente depois do desafio TOTP observado pelo componente confiável.
- `runpass/composition.py`: composição AWS com clientes/configuração explicitamente fornecidos; não descobre credenciais nem cria recursos.
- `runpass/participation.py`: rascunho privado, reserva por edição, versão esperada, idempotência e paginação do titular; sem conclusão ou efeitos públicos.
- `tests/`: regras, concorrência local, JWT assinado, fluxo HTTP e requests DynamoDB interceptadas por Stubber.

## Execução e configuração

```sh
.venv/bin/python -m uvicorn runpass.api:app --app-dir backend --host 127.0.0.1 --port 8000 --no-access-log
```

A aplicação padrão recusa acesso com 503 porque não tem provedor/store configurados. Não há tokens de desenvolvimento aceitos por padrão, login falso ou persistência em memória habilitada por variável de PROD. O harness injeta identidades sintéticas exclusivamente nos testes. Para AWS, um entrypoint futuro deve chamar `create_aws_app(AwsSettings(...), dynamodb_client, cognito_client)` com tabelas, pool/client da conta correta e chave HMAC de pelo menos 32 bytes fornecida por configuração segura. A chave é estável por ambiente/versão; nunca gerar outra silenciosamente ao reiniciar. Os SDK clients são passados, não construídos importando o aplicativo.

Cognito signup/login/recuperação são chamadas diretas pelo mobile; o backend usa access token RS256, issuer/client_id, token_use, exp/iat/sub e GetUser corrente com scope `aws.cognito.signin.user.admin`. Nenhuma propriedade de e-mail enviada pelo app concede admissão. Perfil próprio não devolve e-mail/nascimento. Metadados internos `_rev` são filtrados.

O job de exclusão tem aceitação e prazo, mas o worker de limpeza física/Cognito ainda pertence a S08. Não publicar esta aplicação antes de implementar e testar limpeza, descarte, IAM, logs, segredos, stores reais, limitação de abuso e demais requisitos de S09. Rotas fora da S02 não estão implementadas e retornam 404. Foto de perfil não nula retorna 503 até existir validação de imagem; `null` remove o vínculo atual.

## Operação restrita

Operadores usam pool/client distintos, sem autocadastro. O template de identidade está em `infra/identity.template.json`; não foi aplicado. Procedimento de bootstrap/recuperação: `docs/operadores.md`. `require_operator` verifica permissão, estado e sessão exata; escritas administrativas futuras também devem condicionar o commit à versão de ACCESS, para proteger revogação concorrente.

`MemoryStore` só garante isolamento em um processo. Os testes de threads não comprovam concorrência real DynamoDB, e Stubber não é integração AWS. Evidências/limites completos em `PDLC/M4/S02-identidade-admissao.md`.

## Catálogo S03

`runpass/catalog.py` implementa filtros/cursor cifrado, leitura de versão ativa, importação interna condicionada à autorização e retirada de índices antigos. `GET /editions` e `GET /editions/{id}` exigem admissão corrente. `MemoryStore.query` emula partição para testes; `DynamoStore.query` envia Query real, sem Scan, e precisa de integração DEV antes de liberação. `make catalog-seed` verifica carga sintética idempotente somente em memória.

`AwsSettings.catalog_table` e `cursor_encryption_key` habilitam a composição do catálogo, sempre com configuração explícita. Não foi criado recurso. Campos de score são rejeitados pelo importador e não são fabricados na leitura. S03 não implementa reviews, rascunhos, processamento de imagem ou painel completo. Relatório: `PDLC/M4/S03-catalogo.md`.
