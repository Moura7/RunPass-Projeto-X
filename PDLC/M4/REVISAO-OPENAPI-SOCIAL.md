# RunPass — Revisão dos contratos sociais

**Estado:** complemento OpenAPI 0.5.0-draft. Rotas e representações propostas a partir do produto aprovado; não há implementação ou deploy.

## Operações incluídas

| Método | Rota | Finalidade |
| --- | --- | --- |
| GET | /feed | Seguidos primeiro, demais depois, recência dentro de cada grupo |
| GET, PATCH | /posts/{id} | Consultar publicação e alterar sua visibilidade |
| PUT, DELETE | /profiles/{id}/follow | Seguir/deixar de seguir, sem duplicar relação |
| PUT, DELETE | /profiles/{id}/block | Bloquear/desbloquear, sem apagar interações anteriores |
| PUT, DELETE | /posts/{id}/like | Curtir/descurtir com unicidade |
| GET, POST | /posts/{id}/comments | Consultar comentários autorizados e comentar |
| DELETE | /comments/{id} | Excluir o próprio comentário |
| GET | /me/wishlist | Consultar wishlist própria |
| GET | /profiles/{id}/wishlist | Consultar wishlist pública autorizada |
| PUT, DELETE | /me/wishlist/{id} | Salvar/remover edição futura |
| PUT | /me/wishlist/visibility | Definir visibilidade da wishlist |
| GET | /me/notices | Consultar avisos internos |
| PUT | /me/notices/{id}/read | Marcar aviso próprio como lido — detalhe técnico proposto |

## Regras preservadas

- Conteúdo oculto, removido, suspenso ou bloqueado não pode reaparecer por índice, cache, link ou aviso antigo.
- Não modificar a data original do post por editar a participação. A representação pública nunca inclui nascimento ou e-mail.
- PATCH do post altera visibilidade; não edita livremente a conquista nem publica foto solta.
- PUT de seguir/curtir representa relação única; retentativa não duplica contador, aviso ou métrica.
- Publicação oculta não exclui participação do perfil; exclusão da participação remove o post e vínculos conforme fluxo aprovado.
- Bloqueio preserva dados anteriores, ocultando-os entre os envolvidos. API verifica acesso além da interface.
- Wishlist pública por padrão e ocultável. Salvar não equivale a inscrição em prova.
- Avisos somente no app; alertas operacionais por e-mail são mecanismo separado.

## Lacunas explícitas para revisão

- Bloqueio remove seguimentos nos dois sentidos, preservando curtidas/comentários anteriores ocultos entre os envolvidos. Desbloqueio permite reexibir interações ainda autorizadas, sem recriar seguimentos. Cada usuário decide seguir novamente, se permitido. Atualização de relações/feed e concorrência precisam ser testadas.
- Atualização posterior aprovada: PATCH /comments/{id} permite ao autor editar texto com versão esperada, indicação de editado e preservação da data original. Limites de texto e testes de implementação ainda pendentes.
- Limite de texto, frequência de comentários, auto-curtidas e moderação de posts precisam de critérios explícitos; não usar ausência de maxLength como autorização de conteúdo ilimitado.
- Cursor do feed precisa de prova DynamoDB para evitar duplicações e varreduras globais. Limites 20/100 são propostas, não decisão de produto.
- Ocultação em URLs de imagem previamente emitidas mantém limitações de expiração já documentadas.
- Wishlist após a data da prova, política de avisos lidos/expiração e agrupamento de curtidas ainda a definir.
- Status de erro para recursos privados/inacessíveis deve evitar enumeração sem confundir acesso negado com lista realmente vazia.

## Verificação e sequência

Verificar sintaxe, referências, operationIds, parâmetros de rota, respostas sem corpo em 204 e exemplos positivos/negativos dos schemas. Isso não substitui validação semântica integral OpenAPI ou testes de aplicação.

Próximos contratos: admissão e lista de espera, exclusão de conta, denúncia/feedback, operações administrativas e consulta restrita ao histórico de avaliações. Não publicar como pronto para implementação enquanto os critérios pendentes não forem fechados.
