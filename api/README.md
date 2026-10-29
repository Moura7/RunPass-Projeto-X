# Testar APIs locais com Bruno ou Insomnia

O harness executa os serviços reais Python de S02/S03, com armazenamento em memória, identidades sintéticas e tokens RSA locais. Não usa AWS/Cognito real, não é servidor de produção e só escuta em 127.0.0.1. O simulador de iPhone não é necessário.

## Iniciar

Na raiz:

```sh
make setup
make api-local
```

Ou use ambiente já instalado: `make api-local PYTHON=/caminho/venv/bin/python`. Porta alternativa: `PYTHONPATH=backend /caminho/venv/bin/python -m runpass.local_api --port 8001`.

O processo gera automaticamente, com permissão 0600 e ignorados pelo Git:

- `api/bruno/environments/Local.bru`: ambiente Bruno, URL e dois tokens locais.
- `.local/runpass-api/insomnia-environment.json`: variáveis para colar no editor de ambiente Insomnia.
- `.local/runpass-api/RunPass-local.openapi.json`: contrato com somente as 19 operações implementadas e servidor localhost. O contrato canônico integral continua em PDLC/M4.

Tokens expiram após uma hora; reiniciar o servidor gera outros tokens e apaga todas as alterações em memória. Recarregar o ambiente no cliente após reiniciar. `runnerToken` pertence a um corredor sintético já admitido e permite testar catálogo imediatamente; `newRunnerToken` começa sem perfil/admissão para testar a jornada completa. Não inserir dados reais. O token local não é aceito pela composição Cognito/AWS.

## Bruno

1. Open Collection → selecionar a pasta `api/bruno`.
2. Selecionar o ambiente `Local`.
3. Executar requests 01–14 na ordem, ou começar por 06–08 para catálogo e 13–14 para rascunhos.

A coleção `.bru` é suportada pelo Bruno e fica versionável no repositório; ambientes gerados com tokens ficam fora do Git. Os requests incluem códigos de resposta esperados (200/201, 409 para versão e 422 para entradas inválidas). Após o PATCH 05, a versão corrente é 2; o request 09 demonstra conflito usando 1. Os requests 13–14 criam e listam o rascunho privado da S04. Repetir os comandos originais com a mesma Idempotency-Key não deve duplicar seus efeitos.

Para paginação, o request 07 usa limit=1: copie `nextCursor` da resposta e acrescente `cursor` ao mesmo request, mantendo cidade, UF, distância e limit. Alterar filtros/limit com o cursor existente deve retornar 422.

Exclusão é opcional: `api/examples/Excluir conta sintetica.bru` fica fora da coleção principal para não bloquear automaticamente a jornada de testes. Ao executá-la com newRunnerToken, chamadas seguintes desse usuário retornam 403; reinicie o servidor para recuperar o estado inicial. A limpeza física completa continua S08, não é comprovada pelo recibo.

## Insomnia

1. Import → File → `.local/runpass-api/RunPass-local.openapi.json`.
2. No editor do ambiente, usar JSON view e colar o conteúdo de `.local/runpass-api/insomnia-environment.json`.
3. Na autenticação Bearer, escolher a variável runnerToken para catálogo ou newRunnerToken para a jornada inicial. Não acrescentar a palavra Bearer dentro do campo de token.
4. Para PUT/POST/PATCH/DELETE, adicionar Idempotency-Key (por exemplo, insomnia-perfil-1) e usar os corpos dos requests Bruno como exemplos. Content-Type: application/json para corpos JSON.

A importação não executa automaticamente a sequência nem configura a autenticação pelo usuário. O contrato gerado contém somente o que pode ser testado agora; feed, medalhas, uploads e rascunhos ainda não implementados não entram nele.

## Exemplos de comportamento

| Operação | Resultado |
| --- | --- |
| GET /editions sem token | 401 |
| GET /editions com newRunnerToken antes da admissão | 403 |
| PUT /me com displayName/username e chave idempotente | 201 |
| POST /beta/admissions com birthDate e declaresAdult=true | 201 se elegível e houver vaga |
| GET /editions com runnerToken | Cinco edições sintéticas, filtros/paginação disponíveis |
| PATCH /me com expectedVersion antiga | 409 |
| Cursor inválido ou filtro de data invertido | 422 |

Os testes automatizados executam os requests salvos contra o app ASGI real; não equivalem a teste de UI do Bruno/Insomnia ou integração AWS. A abertura do simulador iOS é uma verificação independente.

Referências: [linguagem Bruno](https://docs.usebruno.com/bru-lang/language), [suporte .bru](https://docs.usebruno.com/bru-lang/overview), [importação Insomnia/OpenAPI](https://developer.konghq.com/insomnia/import-export/).
