# RunPass — Retenção técnica no beta

Estado: conjunto de prazos de logs, URL de upload, temporários, imagens não vinculadas, idempotência da API e payloads entregues aprovado pelo usuário; demais propostas e detalhes técnicos pendentes. Complementa as políticas de exclusão e denúncias já registradas. Não altera os sete dias aprovados para exclusão de dados pessoais dos sistemas ativos.

## Prazos aprovados e proposta remanescente

| Categoria | Proposta | Marco de contagem |
| --- | --- | --- |
| Logs técnicos de DEV | 7 dias | Ocorrência original |
| Logs técnicos de PROD | 30 dias | Ocorrência original |
| URL assinada para upload | Validade de 15 minutos | Emissão |
| Arquivo temporário de upload abandonado | Remoção em até 24 horas após expirar a sessão | Expiração da sessão; janela operacional da sessão ainda a detalhar |
| Imagem validada nunca vinculada | Elegível ao descarte após 7 dias; remover em até 24 horas depois | Validação concluída |
| Registro de idempotência de comando da API | 7 dias | Primeira aceitação durável do comando |
| Payload de evento entregue a todos os destinos obrigatórios | Elegível ao descarte após 7 dias; remover em até 24 horas depois | Última confirmação obrigatória |
| Conteúdo expirado de lake, denúncia ou auditoria (ainda não aprovado neste conjunto) | Bloquear leitura no vencimento; remoção física em até 24 horas depois | Prazo aprovado para cada categoria |

Os seis primeiros itens da tabela foram aprovados pelo usuário; o prazo de descarte físico de lake/denúncia/auditoria continua proposto. Os requisitos aprovados ainda não foram comprovados em testes. Reenvio, consulta ou cópia não renovam a retenção. Arquivos vinculados ou em processamento ativo não são uploads abandonados. Limpeza requer proteção contra corrida com publicação e não remove imagens oficiais ainda referenciadas por medalhas, inclusive ocultas.

## Logs e privacidade

Logs devem registrar identificador de correlação, operação, duração, resultado e código de erro com conteúdo mínimo. Não registrar corpos de avaliações/comentários, nascimento, e-mail, tokens, URLs assinadas ou imagens. Identificadores internos podem permitir identificação; não tratá-los como anônimos.

Antes do beta, escolher mecanismo de logs que cumpra o prazo de exclusão aprovado quando houver dados identificáveis. Retenção geral de 30 dias não autoriza manter dados pessoais de conta excluída por 30 dias. Se a exclusão seletiva não for viável no destino escolhido, reduzir o conteúdo coletado ou ajustar o desenho antes da liberação; não prometer uma capacidade sem validação.

Auditoria administrativa de 90 dias e evidências de denúncias não são logs técnicos e não devem ser duplicadas nesses logs.

## Idempotência e eventos

Dentro dos sete dias propostos, a mesma chave de comando por ator/operação e mesmo corpo retorna o resultado original; corpo divergente gera conflito. Armazenar somente o mínimo necessário, evitando duplicar dados pessoais na resposta persistida. Após a janela, a chave não oferece deduplicação por si só: invariantes de negócio e versões continuam obrigatórias.

A retenção de payload entregue não define a retenção do ledger de consumo. Eventos repetidos fora de ordem ou restaurados de backup não podem duplicar medalhas, curtidas ou contribuição ao RunScore. O ledger e/ou verificação de versão do consumidor deve cobrir o horizonte permitido de replay e recuperação. Esse horizonte e sua implementação permanecem pendentes; não autorizar replay arbitrariamente antigo assumindo deduplicação de sete dias.

Não usar expiração automática para apagar eventos de negócio ainda pendentes de entrega, em retentativa ou falha. Reconciliar a partir do registro durável, acompanhar idade e alertar a equipe RunPass; filas e cópias de transporte não podem ser a única origem recuperável. Um limite de transporte não deve causar perda silenciosa de trabalho. O prazo operacional de tratamento de falhas precisa ser definido.

### Exceção proposta para auditoria de avaliação expirada

Ao completar 60 dias desde a ocorrência, ou antes quando exigido pela exclusão de conta, não entregar nem conservar indefinidamente o conteúdo histórico identificável pendente. Registrar falha/expiração sem copiar o comentário e remover o payload sujeito a descarte. Esta exceção precisa de aprovação e substitui somente para esse conteúdo a preservação genérica de pendências. Não declarar o evento como entregue com sucesso e não descartar junto o evento separado que atualiza o RunScore.

## Execução do descarte

Consulta nega conteúdo vencido mesmo quando a remoção física está pendente. Trabalho periódico controlado executa a remoção, registra progresso sem conteúdo pessoal e alerta atrasos. Expiração eventual por TTL é complementar e não demonstra o cumprimento de 24 horas.

Inventariar versões de objetos, derivados, filas de falha, exportações e cópias intermediárias. Backups mantêm a janela própria de sete dias durante o beta, com reaplicação dos descartes antes de liberar restauração. Não prometer eliminação física de todas as cópias em 24 horas nem aplicar limpeza de temporários às imagens compartilhadas ainda referenciadas.

## Pendências que esta proposta não resolve

- Janela máxima de replay, desenho e retenção do ledger de consumidores.
- Campos e prazo do controle de exclusões necessário à restauração segura.
- Prazo de sessão de processamento após finalização e critério de abandono recuperável.
- Retenção de rascunhos, lista de espera, solicitações de catálogo e feedbacks.
- Prazo de validade de URLs de leitura e comportamento do cache após ocultação.
- Metas de atendimento de falhas e tamanho máximo dos logs/eventos.

## Evidências necessárias

Testar descarte no marco correto, arquivos concorrentes com publicação, preservação de versões referenciadas, repetição do comando dentro e fora da janela, replay de evento antigo sem duplicação, payload de auditoria vencido, falha do job e reaplicação das exclusões em restauração. Recalcular armazenamento, jobs e requisições no orçamento após definir o desenho. Não houve implantação ou teste de execução nesta etapa.

## Retenção técnica — conjunto de prazos aprovado

O usuário aprovou o conjunto apresentado para o beta:
- Logs técnicos: sete dias em DEV e 30 dias em PROD, desde a ocorrência original, sem renovação por cópia/replay.
- URL assinada de upload: validade de 15 minutos desde emissão.
- Arquivo temporário abandonado: remoção em até 24 horas após expiração da sessão; não abrange arquivo publicado ou em processamento ativo. A janela operacional da sessão ainda será detalhada.
- Imagem validada nunca vinculada: elegível ao descarte após sete dias desde validação, com limpeza em até 24 horas depois e verificação de referências/concorrência.
- Registro de idempotência de comando da API: sete dias desde primeira aceitação durável; invariantes e versões continuam obrigatórias após a janela.
- Payload de evento entregue a todos os destinos obrigatórios: sete dias desde última confirmação obrigatória. O prazo não define a retenção do ledger dos consumidores.

Eventos de negócio pendentes continuam recuperáveis; não apagar trabalho pendente por regra genérica de limpeza. A retenção dos controles de deduplicação de consumidores e de exclusões depende da janela de replay/recuperação, ainda a definir. Os prazos ordinários não estendem os sete dias aprovados para exclusão de dados pessoais dos sistemas ativos. Logs devem minimizar conteúdo e permitir cumprimento dessa regra antes do beta.

Esta aprovação refere-se ao conjunto apresentado ao usuário. Não aprova por inferência o descarte físico em 24 horas de lake/denúncias/auditoria, a exceção para payload de auditoria ainda não entregue ao expirar, nem outros itens pendentes do documento. Backups mantêm janela própria de sete dias; não prometer remoção de todas as cópias pelos prazos de arquivos temporários. Requisitos registrados sem configuração de infraestrutura ou testes de execução; SPEC integral em revisão.
## Política de replay aprovada para o beta

O usuário aprovou reprocessar eventos concluídos por até sete dias, alinhados à janela de recuperação; preservar a recuperabilidade dos eventos pendentes até resolução, respeitando retenção/exclusão pessoal; reconstruir feed e RunScore mais antigos a partir dos dados operacionais vigentes; e restringir reprocessamento à operação interna controlada pela equipe RunPass. Não conservar eventos indefinidamente para reconstrução. Replay não recria conteúdo excluído nem renova retenção. O marco técnico proposto é a última confirmação dos destinos obrigatórios, coerente com o payload entregue; detalhar no contrato operacional.

EVENTOS-E-REPLAY-RunPass-MVP.md distingue a política aprovada dos mecanismos propostos. Ledger/deduplicação, margem para mensagens em trânsito, versões dos agregados, autorização operacional e reconstrução concorrente ainda serão projetados e validados. Não fixar automaticamente TTL de sete dias para todos os controles. A política não conclui o esquema físico DynamoDB nem aprova a SPEC integral; não houve implantação ou testes.