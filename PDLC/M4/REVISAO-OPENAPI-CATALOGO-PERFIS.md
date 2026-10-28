# RunPass — Contratos de catálogo, perfis e solicitações

**Estado:** OpenAPI 0.4.0-draft; propostas técnicas em revisão, sem endpoints implementados.

## Rotas acrescentadas

| Método | Rota | Finalidade |
| --- | --- | --- |
| GET | /editions | Catálogo aprovado com prefixo de nome, cidade, estado, período e distância |
| GET | /editions/{id} | Detalhe da edição e RunScore |
| GET | /editions/{id}/reviews | Avaliações válidas da edição, filtráveis por distância |
| GET | /profiles | Busca de corredores por nome ou username |
| GET | /profiles/{id} | Perfil público autorizado |
| GET, PATCH | /me | Consulta e edição do próprio perfil |
| GET | /profiles/{id}/participations | Histórico concluído e autorizado; nunca rascunhos |
| GET | /profiles/{id}/medals | Medalheiro respeitando visibilidade dos resultados |
| POST | /edition-requests | Solicitar inclusão de prova ausente |
| GET | /me/edition-requests | Solicitações do usuário |
| GET, PATCH | /edition-requests/{id} | Consulta e correção da solicitação recusada |
| POST | /edition-requests/{id}/resubmit | Reenvio para revisão humana |

São 21 caminhos e 26 operações no contrato acumulado, contando as operações anteriores de participação e upload.

## Aplicação das regras confirmadas

- Perfil público: nome de exibição e username, foto/cidade/bio opcionais, sem e-mail ou nascimento na projeção pública. Campos privados não são acrescentados ao schema público por conveniência.
- Nome de prova apenas por início do título, junto dos filtros aprovados. Não prometer busca aproximada ou substring.
- Reviews: apenas representação atual autorizada; histórico do data lake nunca retornado nessas rotas.
- Excluir/moderar/bloquear exige revalidação da fonte, mesmo quando índice atrasar. Resultados ocultos não devem aparecer no JSON público.
- Solicitação pendente não vira catálogo público nem conclui participação automaticamente. Rejeição admite correção e reenvio, preservando rascunho.
- Rascunho de prova ausente aceita editionRequestId e distância em quilômetros, pois ainda não existe distanceId do catálogo; para edição existente, usa editionId/distanceId. Essa estrutura é proposta de contrato, sem nova exigência funcional ao usuário.

## Detalhes ainda em revisão

- Normalização de nome/acentos e identificadores de cidade/distância; plano de índices para combinações do catálogo.
- Busca de corredores: regra exata de correspondência e tamanho mínimo do termo, sem restringir silenciosamente o requisito a username.
- Tamanho de página proposto: padrão 20 e máximo 100. Limites de bio, nomes, comentários e frequência de alteração de username ainda não aprovados.
- Vocabulário do estado da edição é rascunho: distinguir situação temporal e arquivamento no desenho final.
- Fotos de perfil não devem herdar automaticamente a obrigação da foto da medalha; fluxo/limites próprios a detalhar.
- Decisões administrativas de aprovação/vinculação/recusa terão contratos privilegiados separados e auditados; não podem ser enviados pelo PATCH do solicitante.
- Reserva de username, versionamento e limpeza de campos opcionais são propostas técnicas sujeitas à validação.

## Verificações realizadas

JSON legível, referências internas resolvidas, operationIds únicos, parâmetros de caminho correspondentes às rotas e ausência de e-mail/nascimento em PublicProfile. Exemplos básicos de schemas validados localmente com jsonschema (não substitui validador semântico OpenAPI, ainda não instalado).

Não existem testes de API executada, cliente gerado, deploy ou aprovação técnica integral. Próximos contratos: social/wishlist/avisos, admissão e exclusão de conta, administração e consulta autorizada ao histórico informacional.
