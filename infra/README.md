# Infraestrutura

`identity.template.json` declara pools/clients Cognito separados para corredores e operadores, senha/e-mail, TOTP obrigatório para operadores e recuperação administrativa. `make infra-check` valida localmente com cfn-lint para sa-east-1. Nenhum template foi aplicado.

O template não inclui IAM, tabelas, rede, Lambda ou API Gateway. A composição completa e provas reais pertencem à integração DEV/S09. DEV e PROD usam contas distintas; parâmetros são por ambiente. Plano/tarifa Cognito, envio de e-mail, domínios/configuração de endpoints e respectivos custos precisam ser fechados antes de provisionar. O plano do serviço não foi fixado por inferência.

Configuração MFA ON não basta para conceder permissão administrativa: API exige sessão vinculada ao desafio concluído e papel atual. Bootstrap e recuperação em `docs/operadores.md`. Não há deploy, credenciais ou assinatura de release neste diretório.
