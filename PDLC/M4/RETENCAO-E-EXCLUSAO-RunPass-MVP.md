# RunPass — Retenção e exclusão no MVP

Estado: proposta técnica para revisão. Somente as regras identificadas como aprovadas constituem decisões anteriores. Prazos propostos abaixo são metas operacionais, dependentes de aprovação e testes; não constituem análise jurídica. O prazo e o escopo de exclusão de conta descritos como aprovados foram confirmados posteriormente pelo usuário; os demais prazos continuam propostos.

## Base aprovada

| Categoria | Regra aprovada |
| --- | --- |
| Participações, avaliações atuais e medalhas | Sem expiração automática; remoção pelos fluxos previstos, inclusive exclusão da conta |
| Histórico de alterações de avaliações no lake | 60 dias desde a ocorrência original; replay não renova prazo |
| Pontos de recuperação em PROD | Janela de sete dias durante o beta; revisão ao final |
| Exclusão da conta | Bloquear acesso à API e ocultar perfil/conteúdo ao aceitar; limpeza em segundo plano |
| Imagens oficiais | Preservar versões ainda referenciadas; substituição do catálogo não altera medalhas existentes |

Ocultação não é exclusão. Dados ocultos continuam sujeitos a autorização e à política de retenção. Os sete dias de recuperação não determinam a retenção dos dados ativos nem dos eventos de auditoria.

## Decisão aprovada: prazo da exclusão da conta

Aprovado pelo usuário: prazo de até sete dias corridos desde a aceitação para concluir a remoção dos dados pessoais dos sistemas ativos sob controle do RunPass. Bloqueio e ocultação continuam imediatos. O prazo é requisito de implementação aprovado, ainda sem comprovação por testes; não é apresentado como prazo legal.

O escopo aprovado de limpeza dos sistemas ativos inclui identidade e atributos privados de cadastro, perfil, participações, avaliações, medalhas, wishlist, relações sociais, comentários e curtidas de autoria do titular, notificações e fotos próprias, bem como suas projeções, índices, filas e histórico identificável de avaliações no lake. Exclusão de conta prevalece sobre a retenção ordinária de 60 dias desse histórico; essa precedência foi aprovada pelo usuário.

Preservar catálogo e imagens oficiais compartilhadas. Em publicações de terceiros, remover comentários/curtidas do titular sem apagar a publicação de terceiro. Ao excluir uma publicação do titular, remover também suas interações subordinadas, sem excluir contas ou publicações independentes dos demais participantes. Evidências restritas de denúncias, auditoria administrativa, feedbacks e eventuais exceções exigem política específica antes do beta; não presumir retenção permanente nem apagamento automático de registros necessários de terceiros.

Recalcular RunScore e retirar referências dos feeds. Métricas do beta só podem permanecer sem vínculo identificável após aprovação do tratamento: manter o total de admitidos não autoriza preservar indefinidamente uma lista pessoal de contas excluídas. Não pressupor que trocar um nome por um ID produz anonimização.

## Execução proposta

1. Persistir comando durável e idempotente de exclusão; gravar bloqueio autoritativo e ocultação antes de confirmar aceitação. Falha em persistir não pode produzir recibo de sucesso.
2. Interromper novas escritas do titular, inclusive com tokens já emitidos. Workers consultam bloqueio e versão para não recriar conteúdo após exclusão.
3. Identificar objetos por referência interna protegida; eliminar dados e derivados nos destinos inventariados. Outbox, filas de falha e cópias intermediárias entram no inventário.
4. Registrar progresso por destino, retentar falhas e alertar a equipe RunPass. O prazo não pode ser reiniciado a cada tentativa. Não marcar concluído com destinos obrigatórios pendentes.
5. Guardar recibo e controle mínimo para impedir ressurreição por replay/restauração, separados do conteúdo excluído. Atributos, acesso e prazo desse controle precisam de definição; não guardar cópias completas como comprovante.
6. Reaplicar exclusões em restauração isolada antes de liberar acesso ou consumidores. Remover identidade no provedor sem criar dependência de um token revogado para acompanhar a conclusão; mecanismo seguro de recibo/suporte continua pendente.

## Cópias de recuperação

Não prometer remoção seletiva imediata dentro de pontos de recuperação. Após limpar a origem, cópias anteriores podem persistir até expirar a janela aprovada de sete dias. Assim, sete dias para limpar ativos não equivalem a sete dias para desaparecer de todas as cópias. Com limpeza no último dia e expiração subsequente de sete dias, o horizonte projetado seria de até 14 dias desde a solicitação, condicionado à configuração efetiva e à ausência de cópias adicionais. Essa projeção precisa de teste e não é SLA aprovado.

S3 versionado exige remoção das versões elegíveis; delete marker não elimina bytes antigos. Não aplicar regra de sete dias indistintamente a imagens oficiais ainda referenciadas nem habilitar replicações/exportações adicionais sem incluí-las na política.

## Outras propostas de prazo — ainda não aprovadas

| Item | Proposta técnica | Condição |
| --- | --- | --- |
| URL assinada de upload | 15 minutos | Validade não equivale a revogação imediata; chave por sessão e proteção contra sobrescrita após validação |
| Sessão não finalizada/arquivo temporário | Limpeza em até 24 horas após expiração da sessão | Sem remover objeto publicado ou em processamento ativo; incidente pendente tem tratamento explícito |
| Derivado validado nunca vinculado | Limpeza após sete dias sem vínculo | Rechecagem autoritativa de referências e proteção contra corrida com publicação |
| Histórico de avaliação expirado no lake | Negar leitura ao completar 60 dias; descarte físico em até 24 horas depois | Remover versões e cópias elegíveis; monitorar atrasos |
| Evento de auditoria ainda não entregue ao completar 60 dias | Não entregar conteúdo vencido; descartar payload com registro técnico mínimo de falha/expiração | Exceção explícita à preservação de pendências; aprovação necessária |

TTL é mecanismo auxiliar eventual e não garante nenhum prazo acima. O descarte com prazo exige trabalho controlado, verificação e alerta. Ledger/idempotência/outbox concluída precisam de janela compatível com replay e recuperação; não fixar prazo sem fechar esse contrato. Pendências de negócio não expiram silenciosamente por uma regra de limpeza genérica.

## Pendências para fechar a política

- Implementar e comprovar o prazo e o escopo aprovados da exclusão dos sistemas ativos, incluindo precedência sobre histórico do lake.
- Definir tratamento e prazo de denúncias/evidências, feedbacks, auditoria administrativa e logs, com acesso mínimo.
- Definir prazo e atributos do controle de exclusões e sua compatibilidade com recuperação/replay.
- Definir retenção de rascunhos, solicitações de catálogo e lista de espera; não atribuir os 60 dias do beta automaticamente.
- Revisar finalidade e retenção da data de nascimento e demais atributos privados.
- Fechar expiração das URLs de leitura/cache e comunicação do encerramento da conta.
- Validar a política de dados e a comunicação ao usuário antes do beta.

## Verificações antes da liberação

Testar exclusão concorrente com publicação, retry de eventos antigos, falha parcial por destino, versão antiga de imagem S3, saída de histórico do lake, contribuição ao RunScore, preservação de catálogo compartilhado, token emitido antes da exclusão e restauração que contenha conta já excluída. Só considerar concluído após conferir todos os destinos obrigatórios; nenhuma dessas verificações foi executada nesta revisão documental.

## Exclusão de conta — decisão aprovada

O usuário aprovou bloquear acesso e ocultar perfil/conteúdo imediatamente ao aceitar a exclusão, com remoção dos dados pessoais dos sistemas ativos em até sete dias corridos desde a aceitação. O escopo inclui fotos próprias e histórico identificável de avaliações no data lake: a exclusão da conta prevalece sobre a retenção ordinária de 60 dias desse histórico. Preservar catálogo e imagens oficiais compartilhadas ainda referenciadas. A limpeza deve abranger projeções, índices e cópias intermediárias sob controle do RunPass, com processamento idempotente, retentativas e acompanhamento por destino.

Backups mantêm a janela própria de sete dias no beta; a aprovação não significa eliminação de todas as cópias em sete dias desde a solicitação. Reaplicar exclusões antes de liberar qualquer restauração. Tratamento de denúncias/evidências, auditoria e controle mínimo de exclusões continua pendente de definição específica, sem autorização para retenção indefinida. Os demais prazos propostos no documento de retenção não foram aprovados por esta decisão. Prazo de exclusão é requisito aprovado, ainda sem comprovação por implementação ou testes; a SPEC integral permanece em revisão.
## Retenção de denúncias e auditoria — prazos aprovados

O usuário aprovou a recomendação para o beta: denúncias em análise permanecem enquanto necessárias, com revisão semanal pela equipe RunPass; denúncias encerradas e evidências necessárias permanecem por até 60 dias desde o encerramento; auditoria administrativa mínima permanece por até 90 dias desde a ocorrência original da ação. Consulta, cópia, retentativa ou replay não renovam esses prazos. Denúncia aberta exige acompanhamento; o prazo máximo de resolução continua pendente, sem autorizar retenção indefinida sem revisão.

Acesso restrito por permissão e MFA, respeitando a separação entre Administração e Moderação. A retenção ordinária não estende o prazo aprovado para exclusão da conta: dados pessoais identificáveis continuam sujeitos à remoção em até sete dias corridos, incluindo os presentes nesses registros. Não presumir anonimização por troca de nome ou ID. Preservar registros independentes de terceiros somente sem reter indevidamente os dados do titular excluído; necessidade excepcional de retenção identificável exige política específica ainda não definida.

Essas janelas não se aplicam automaticamente a logs técnicos, feedbacks, lista de espera ou controles de exclusão/idempotência. Descarte físico em até 24 horas após expiração continua proposta não aprovada. O lake de alterações de avaliações mantém sua própria regra de 60 dias desde a ocorrência. Detalhamento: RETENCAO-DENUNCIAS-E-AUDITORIA-RunPass.md. Requisitos registrados, sem implementação ou testes de execução; SPEC integral em revisão.
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