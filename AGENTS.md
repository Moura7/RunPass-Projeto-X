# RunPass

## Antes de implementar

- Use `PRD_RunPass_MVP_v2.md` para produto e `PDLC/M4/SPEC_RunPass_MVP_v1.md` como única SPEC ativa. Decisões explícitas posteriores prevalecem sobre pendências históricas.
- Consulte `PDLC/M4/implementation-slices.md` para escopo, dependências e aceite de cada entrega. Resolva as dependências da parte afetada antes de implementá-la.
- Para alterar rotas ou persistência, leia também `PDLC/M4/API-RunPass-v1.openapi.json` e `PDLC/M4/MODELO-DYNAMODB-RunPass-v1.md`; mantenha contrato, desenho e SPEC coerentes.

## Execução e verificação

- Setup e comandos locais: `docs/desenvolvimento.md`. Execute `make check` para Python/contrato e `make mobile-check` quando alterar o mobile.
- Use dados sintéticos e adaptadores locais nos testes; serviços AWS reais pertencem à integração DEV autorizada.
- A primeira entrega é autenticação → catálogo → rascunho → imagem → conclusão → avaliação e medalha. Preserve autorização, privacidade, versões e idempotência desde o primeiro fluxo.
- Registre resultados e limitações no slice. Diferencie teste local, integração real e aceite humano.
- Desenvolvimento local está autorizado. Provisionamento pago exige orçamento e autorização; PROD/beta tem aprovação própria. Mantenha credenciais e dados reais fora do Git.
