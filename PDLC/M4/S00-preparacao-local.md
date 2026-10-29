# S00 — Preparação local

Data: 28/10/2026. Estado: **em revisão**, implementação da preparação concluída e verificada localmente; aceite humano ainda não registrado.

## Entrega

- `AGENTS.md`: precedência das fontes, escopo e regras de execução.
- `docs/desenvolvimento.md` e `Makefile`: setup, análise estática, formatação e validação de contrato reproduzíveis.
- `.python-version`, `requirements-dev.in`, `requirements-dev.lock` e `pyproject.toml`: Python e ferramentas fixados/configurados.
- `backend/` e `infra/`: fronteiras documentadas, sem API ou recursos fictícios.
- `mobile/`: scaffold Android/iOS com tela RunPass e lockfile, sem fluxo funcional.
- Validador OpenAPI existente adaptado para localizar contrato/relatório pelo diretório do script. Os dois scripts Python existentes receberam formatação Ruff; regras de produto e cálculo de orçamento preservados.

## Evidências

| Verificação | Resultado |
| --- | --- |
| Python | 3.11.4; ambiente `.venv` criado |
| Flutter / Dart | 3.47.7 stable / 3.13.5 |
| `make check` | Ruff sem erros, dois arquivos formatados; contrato válido |
| Contrato OpenAPI | 0.7.0-draft, 55 caminhos, 71 operações, 661 referências internas e 12 exemplos aprovados |
| `make mobile-check` | `flutter analyze` sem problemas; formatação sem mudanças |
| `make mobile-setup` | Dependências resolvidas com `--enforce-lockfile` |
| `pip check` / `git diff --check` | Sem dependências quebradas ou erros de whitespace |
| `flutter doctor -v` | Sem problemas; Android SDK 36.0.0, Xcode 27.1 e CocoaPods 1.17.0 encontrados |

Relatório de contrato: `VALIDACAO-OPENAPI-RunPass.json`. A nova execução corrigiu o hash desatualizado do relatório para `109b917fca4a747997bebca56d4dc8ef9fbc362539b070feaa2bcc40e89e2531`; o arquivo OpenAPI não foi alterado.

## Limites e próxima entrega

Não há implementação de domínio no backend; os 12 exemplos de contrato são os testes pertinentes da lógica existente. A tela provisória não recebeu teste artificial. O harness de testes de domínio/mobile será acrescentado junto ao comportamento implementado. Fixtures atuais são os exemplos sintéticos do validador; políticas de isolamento constam no guia local.

Não foram executados builds, emuladores, simuladores ou aparelhos Android/iPhone. Doctor detectou apenas macOS/Chrome como destinos disponíveis. O identificador mobile é provisório. O validador emite aviso de depreciação de `jsonschema.RefResolver`; as versões estão fixadas e a migração poderá ocorrer junto à revisão do contrato.

Sem testes de API real, IAM/MFA, concorrência, imagens, AWS ou recuperação. Sem credenciais, provisionamento, custo AWS, deploy, commit ou push. SDK Flutter e dependências exigiram acesso ao cache/rede do ambiente; não foram atualizadas versões do SDK.

Próximo passo técnico: S01, fechando acessos, chaves/índices, transações e contratos do fluxo inicial. Aceite da S00 não resolve essas dependências nem autoriza provisionamento ou beta.
