# RunPass mobile — S02 a S04

Flutter Android/iOS com cadastro, confirmação/reenvio de código, login, recuperação de senha, perfil e admissão/lista de espera. Setup/comandos/configuração: [desenvolvimento local](../docs/desenvolvimento.md).

`make mobile-check` executa análise, formatação e testes com transporte sintético. Tokens ficam somente em memória; expiração/reinício exige login novamente. Sem endpoints/client configurados, app falha fechado. Não há credenciais embutidas nem login falso. Não há catálogo ainda. Integração real Cognito/AWS e execução em aparelhos pertencem a DEV/S09 autorizado.

O identificador `br.com.runpass.runpass` continua provisório, sujeito à confirmação antes da distribuição. O template Android ainda usa assinatura debug para release; não é build publicável.

S03 acrescenta busca com filtros, paginação, detalhe e seleção de distância. S04 permite criar e editar o rascunho privado a partir dessa seleção, sem medalha ou publicação. Demonstração visual sem rede: `flutter run --debug -t lib/main_demo.dart -d ID_DO_IPHONE`, com banner e dados fictícios; usuário `demo@runpass.test`, senha `RunpassDemo123!` e código de confirmação `123456`. Estado reinicia com o processo. Para o erro de assinatura por metadados de Documents, há `scripts/run-ios-demo.sh` na raiz. Consulte o guia antes de confundir demonstração com autenticação real.
