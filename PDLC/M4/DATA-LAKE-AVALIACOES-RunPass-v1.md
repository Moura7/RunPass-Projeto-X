# RunPass — Entrega e descarte do histórico de avaliações

**Estado:** DRAFT de implementação; não há recursos criados. Regras de conteúdo, acesso, destino e retenção aprovadas; parâmetros operacionais abaixo são propostas a revisar.

## Regras já aprovadas

- Avaliação atual pode perder seu comentário quando omitido no PUT. Preservar antes/depois de notas e comentário no histórico informacional.
- S3 privado, isolado por conta DEV/PROD, sem acesso pelo fluxo de fotos do app.
- Consulta humana apenas por Administradores especificamente autorizados, com MFA e auditoria; não por Moderadores/corredores por padrão.
- Entrega assíncrona com evento persistido na alteração operacional. Retenção de 60 dias desde ocorrência original, não renovada por replay.
- Política de exclusão de dados pessoais continua necessária; não assumir que os 60 dias suspendem seu atendimento.

## Entrega proposta

1. PUT valida oito notas, versão e autorização. Lê versão anterior e grava nova representação junto do evento de auditoria em transação DynamoDB. Se a gravação durável do evento falhar, não confirmar a substituição.
2. Evento de negócio para RunScore é separado do payload de auditoria, evitando distribuir comentários antigos aos demais consumidores. Compartilhar identificadores de correlação, sem duplicar contribuição de score.
3. Publicador recebe sinal de Streams e encaminha a fila dedicada ou explicitamente segregada por política. Não usar fila compartilhada com consumidores que não podem ler comentários históricos.
4. Worker cria objeto JSON UTF-8, um por evento no MVP, com chave determinística por ambiente, data UTC original e eventId. Isso é proposta de formato, não aprovação de retenção imutável. Não colocar nome, e-mail ou texto livre na chave.
5. Expiração lógica: occurredAt + 60 dias. Preservar bytes e versão do evento nas retentativas. Usar criação condicional do objeto ou verificação de existência e integridade; mesmo ID com conteúdo divergente é conflito auditável, não sobrescrita silenciosa.
6. Registrar confirmação de entrega somente após persistência verificada. Se worker falhar entre gravar objeto e confirmar, reenvio deve identificar o objeto e confirmar sem duplicá-lo.
7. Reconciliador consulta índice de eventos pendentes; não depende da retenção limitada de Streams. Destino de falha, alarmes para equipe RunPass e procedimento de reprocessamento documentados.

Outbox temporária, ledger de entrega e objeto histórico têm ciclos distintos. Não copiar todo comentário para logs, métricas ou erros. Retentativas de escrita não criam nova ocorrência para renovar prazo.

## Descarte e acesso após expiração

- Verificar expiresAt na consulta, impedindo acesso ao conteúdo expirado mesmo se a remoção física estiver atrasada.
- Proposta: job diário consulta manifesto/índice de expiração por partição temporal e elimina objetos vencidos; não executar listagem integral de todo o lake por consulta de usuário.
- Lifecycle baseado somente na data de criação do S3 é insuficiente para objetos entregues tardiamente. Usá-lo apenas como defesa complementar com prazo coerente, nunca como única execução da regra de 60 dias.
- Versionamento, delete markers, replicação e exportações podem manter cópias. Definir estratégia explícita antes de habilitar esses mecanismos; não presumir que DeleteObject remove versões antigas.
- Rotina precisa de retentativas, registro sem conteúdo sensível e alerta de falha. Prazo máximo entre expiração e eliminação física ainda depende de aprovação; job diário é proposta, não SLA aprovado.
- Evento ainda não entregue com mais de 60 dias: não estender prazo automaticamente nem publicar conteúdo expirado. Encaminhar para tratamento restrito, alertar operação e aplicar decisão de privacidade/recuperação registrada. Não preservar payload indefinidamente sob justificativa de pendência. Essa exceção precisa ser fechada antes da implementação.
- Exclusão de conta exige localizar dados por referência protegida de titular/avaliação, removendo ou anonimizando conforme política aprovada. Não há política de anonimização aprovada. Reaplicar exclusões após restauração.

## Consulta administrativa proposta

MVP pode oferecer consulta mediada e paginada por avaliação/período, com autorização específica e MFA, sem acesso público ao bucket. Tecnologia de consulta ainda não escolhida; não adicionar Athena/Glue por consequência automática. Auditoria registra ator, ação, filtro/referência e resultado, sem replicar o comentário completo em outro log.

## Testes necessários

Falha da transação; duplicidade; conflito de eventId; mensagens fora de ordem; indisponibilidade S3; DLQ/replay; entrega atrasada sem renovação; consulta de expirado; descarte com versões; exclusão de titular; recuperação de backup; acesso negado a Moderador; MFA administrativo; inexistência de dados privados de cadastro no evento. Validar exemplos com EVENTO-AUDITORIA-AVALIACAO.schema.json, incluindo antes/depois e remoção de comentário.

## Custos e limites

Um objeto por evento facilita idempotência e descarte, mas pode encarecer requisições em grande escala. Lotes/Parquet podem ser evolução, exigindo tratamento de expiração e exclusão por registro. Recalcular custos de outbox, fila, worker, S3, consulta e auditoria. Nenhum benchmark foi executado. Propostas ainda a aprovar: tamanho dos eventos, frequência do reconciliador, agrupamento e janela de descarte.

## Exclusão de conta — decisão aprovada

O usuário aprovou bloquear acesso e ocultar perfil/conteúdo imediatamente ao aceitar a exclusão, com remoção dos dados pessoais dos sistemas ativos em até sete dias corridos desde a aceitação. O escopo inclui fotos próprias e histórico identificável de avaliações no data lake: a exclusão da conta prevalece sobre a retenção ordinária de 60 dias desse histórico. Preservar catálogo e imagens oficiais compartilhadas ainda referenciadas. A limpeza deve abranger projeções, índices e cópias intermediárias sob controle do RunPass, com processamento idempotente, retentativas e acompanhamento por destino.

Backups mantêm a janela própria de sete dias no beta; a aprovação não significa eliminação de todas as cópias em sete dias desde a solicitação. Reaplicar exclusões antes de liberar qualquer restauração. Tratamento de denúncias/evidências, auditoria e controle mínimo de exclusões continua pendente de definição específica, sem autorização para retenção indefinida. Os demais prazos propostos no documento de retenção não foram aprovados por esta decisão. Prazo de exclusão é requisito aprovado, ainda sem comprovação por implementação ou testes; a SPEC integral permanece em revisão.