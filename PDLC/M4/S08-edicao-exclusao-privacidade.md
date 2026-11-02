# S08 — Edição, exclusão e privacidade

Data: 01/11/2026. Estado: **em execução local**. S06 e S07 estão disponíveis em revisão local; integração e descarte em serviços AWS permanecem S09.

## Implementação local

`PUT /participations/{id}/review` substitui as oito notas com versão esperada. Comentário omitido é removido. A fonte, o evento operacional sem comentário, o marcador durável e a fonte restrita de auditoria antes/depois são gravados atomicamente. Review invalidada corrigida volta como `pending_review`; as demais permanecem válidas. O consumidor da S07 recompõe contribuição e RunScore pela fonte vigente.

Participações concluídas aceitam edição versionada. Alterações de visibilidade não disparam score. Troca de edição/distância revalida catálogo e unicidade, move a claim e cria evento para retirar a contribuição antiga e aplicar a atual. A imagem já fixada permanece vinculada quando não há troca explícita.

`DELETE /participations/{id}` oculta imediatamente a fonte, libera a claim e cria job durável. Conflito de versão não altera conteúdo. A referência da imagem é decrementada, sem apagar imagem oficial compartilhada. O evento de exclusão invalida a review e remove a contribuição; o lake registra antes e ausência posterior. `GET /deletion-operations/{id}` expõe somente o status do próprio titular enquanto a conta permanece disponível.

A exclusão de conta já bloqueava tokens imediatamente e preservava controle pseudonimizado por até 15 dias. Agora também grava marcador durável. `ErasureProcessor` executa em etapas retomáveis: primeiro compensa contribuições/score; depois enumera e remove partições pessoais de identidade, histórico, operações, projeções, OWNER reverso, claim de username e marcadores de eventos; por fim remove job/marcador. O contador agregado do beta e o controle segregado aprovado não são apagados.

## Evidências e pendências

- Dezesseis testes focados S07/S08 aprovados: versão/conflito, comentário omitido, antes/depois, recomposição de score, transferência de edição, visibilidade, exclusão de participação e exclusão de conta em lotes pequenos.
- A primeira execução completa encontrou apenas a expectativa antiga de 19 operações no harness local; a API passou a expor 23 com as quatro rotas S08, e o teste foi atualizado.
- `make check` aprovado após a atualização: Ruff/formatação, OpenAPI sem erros (55 paths/72 operações), 82 testes backend e cfn-lint.
- Pendente: limpeza dos bytes no adaptador de objetos/fotos, lifecycle e enumeração real de índices, filas e S3 em DEV.
- Pendente: UI mobile para editar review/participação e solicitar exclusão; o backend local pode ser exercitado por HTTP/Bruno.
- Pendente: ensaio de falha/restauração, prazo real de sete dias, IAM/MFA e prova do descarte do controle de 15 dias em S09.

Nenhum recurso AWS foi criado e nenhum dado real foi utilizado.
