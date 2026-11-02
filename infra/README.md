# Infraestrutura

`identity.template.json` declara pools/clients Cognito separados para corredores e operadores, senha/e-mail, TOTP obrigatório para operadores e recuperação administrativa. `make infra-check` valida localmente com cfn-lint para sa-east-1. Nenhum template foi aplicado.

`data.template.yaml` acrescenta uma composição candidata, ainda não aplicada, para as seis tabelas lógicas, buckets privados/versionados de medalhas e auditoria, filas standard com DLQ e alarmes. Tabelas usam on-demand e criptografia; dados ativos têm PITR, enquanto ErasureControl deliberadamente não tem backup e usa TTL apenas como salvaguarda secundária. Buckets bloqueiam acesso público. Filas retêm referências por um dia, visibility inicia em 60 segundos e DLQ ocorre após cinco recepções.

O template ainda não inclui IAM de execução, Lambda, API Gateway, empacotamento, assinaturas SNS ou OIDC. A composição executável e provas reais pertencem à integração DEV/S09. DEV e PROD usam contas distintas; parâmetros são por ambiente. Plano/tarifa Cognito, envio de e-mail, domínios/configuração de endpoints e respectivos custos precisam ser fechados antes de provisionar. O plano do serviço não foi fixado por inferência.

Configuração MFA ON não basta para conceder permissão administrativa: API exige sessão vinculada ao desafio concluído e papel atual. Bootstrap e recuperação em `docs/operadores.md`. Não há deploy, credenciais ou assinatura de release neste diretório.
