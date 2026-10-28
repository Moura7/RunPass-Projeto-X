# RunPass — Proposta de retenção de denúncias e auditoria

Estado: prazos ordinários de denúncias e auditoria aprovados pelo usuário para o beta; implementação e demais parâmetros técnicos pendentes. Complementa RETENCAO-E-EXCLUSAO-RunPass-MVP.md. Não define prazos legais nem certifica conformidade.

## Prazos aprovados para o beta

| Categoria | Prazo aprovado | Marco inicial |
| --- | --- | --- |
| Denúncia em análise e evidência estritamente necessária | Enquanto necessária à análise, com revisão semanal pela equipe RunPass | Recebimento |
| Denúncia encerrada e evidência necessária à decisão | Até 60 dias | Encerramento |
| Auditoria administrativa mínima | Até 90 dias | Ocorrência original da ação |

Uma denúncia aberta não deve ficar indefinidamente sem responsável. A revisão semanal deve verificar finalidade, pendências e necessidade das evidências. Não há prazo máximo de resolução aprovado; escalonamento e exceções precisam de decisão operacional antes do beta.

Não renovar os prazos por consulta, cópia, retry ou replay. Reabrir denúncia não deve reiniciar automaticamente a retenção das evidências antigas: registrar nova decisão e sua justificativa, respeitando a política de exclusão. Novos fatos têm ocorrência própria; não copiar todo o histórico para contornar o prazo.

## Conteúdo e acesso

Evidência deve ser o recorte mínimo necessário do conteúdo denunciado e seu contexto; evitar cópia integral de perfil, conversas ou atributos privados. Não incluir e-mail ou nascimento por padrão. URLs assinadas, tokens, senhas e payloads completos de requisição não entram na auditoria.

Auditoria administrativa registra ator autorizado, ação, alvo por referência interna, instante, resultado, motivo quando necessário e correlação. Referências de ator/alvo continuam dados potencialmente identificáveis; não chamá-las de anônimas.

Manter evidências em armazenamento privado e acesso operacional por Moderador autorizado com MFA. Ser Administrador não concede automaticamente acesso à moderação. Para auditoria administrativa, definir permissão específica de consulta com MFA; não liberar para todo Administrador por inferência. Registrar consultas sem replicar o conteúdo sensível nos logs.

Não incorporar automaticamente evidências ou auditoria administrativa ao lake de avaliações: finalidade, conteúdo, acesso e retenção são distintos. A retenção aprovada desse lake continua de 60 dias desde a ocorrência de cada alteração de avaliação.

## Exclusão de conta: precedência preservada

Preservar o prazo aprovado de até sete dias para remover dados pessoais dos sistemas ativos, inclusive dos registros de denúncia e auditoria que identifiquem o titular, sem apagar automaticamente todo registro independente de terceiros. Eliminar ou reduzir evidências identificáveis do titular; não presumir que remover o userId anonimiza texto, imagem ou contexto. Na impossibilidade de desidentificar com segurança, remover o trecho identificável.

As janelas de 60 e 90 dias são limites ordinários e não autorizam manter dados pessoais após pedido de exclusão além do prazo aprovado. Manter apenas registro residual sem vínculo identificável quando sua desidentificação for comprovável. Qualquer necessidade excepcional de preservar dados identificáveis exige política específica e decisão fundamentada antes de implementá-la; esta proposta não cria essa exceção.

Evidências já coletadas não devem ser republicadas após remoção da publicação. Ocultar conteúdo denunciado não deve impedir por si só a análise autorizada; excluir conta, por outro lado, aciona o tratamento aprovado de exclusão.

## Expiração e verificação propostas

Negar consulta ordinária ao vencer a retenção. Propor descarte físico em até 24 horas, com retentativa e alerta; esse prazo também depende de aprovação. Incluir versões S3, derivados e cópias operacionais no inventário. Backups seguem a janela aprovada de sete dias e exigem reaplicação dos descartes/exclusões antes de restaurar acesso.

Testar expiração pelo marco correto, retries sem renovação, remoção de titular em evidência de terceiro, proibição de acesso por papel inadequado, falha do descarte e restauração. Nenhum teste de execução foi realizado nesta etapa.

## Fora desta decisão

Retenção de logs técnicos, feedbacks, lista de espera, controle mínimo de exclusões, idempotência e ledger de eventos deve ser definida separadamente. Não aplicar 90 dias a todos esses dados por consequência desta proposta. O desenho do controle de exclusões precisa permitir restauração segura sem preservar cópias completas do conteúdo removido.

## Retenção de denúncias e auditoria — prazos aprovados

O usuário aprovou a recomendação para o beta: denúncias em análise permanecem enquanto necessárias, com revisão semanal pela equipe RunPass; denúncias encerradas e evidências necessárias permanecem por até 60 dias desde o encerramento; auditoria administrativa mínima permanece por até 90 dias desde a ocorrência original da ação. Consulta, cópia, retentativa ou replay não renovam esses prazos. Denúncia aberta exige acompanhamento; o prazo máximo de resolução continua pendente, sem autorizar retenção indefinida sem revisão.

Acesso restrito por permissão e MFA, respeitando a separação entre Administração e Moderação. A retenção ordinária não estende o prazo aprovado para exclusão da conta: dados pessoais identificáveis continuam sujeitos à remoção em até sete dias corridos, incluindo os presentes nesses registros. Não presumir anonimização por troca de nome ou ID. Preservar registros independentes de terceiros somente sem reter indevidamente os dados do titular excluído; necessidade excepcional de retenção identificável exige política específica ainda não definida.

Essas janelas não se aplicam automaticamente a logs técnicos, feedbacks, lista de espera ou controles de exclusão/idempotência. Descarte físico em até 24 horas após expiração continua proposta não aprovada. O lake de alterações de avaliações mantém sua própria regra de 60 dias desde a ocorrência. Detalhamento: RETENCAO-DENUNCIAS-E-AUDITORIA-RunPass.md. Requisitos registrados, sem implementação ou testes de execução; SPEC integral em revisão.