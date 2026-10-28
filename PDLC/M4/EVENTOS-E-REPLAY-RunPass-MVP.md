# RunPass — Eventos e reprocessamento no beta

Estado: política de alcance de replay aprovada pelo usuário; mecanismos técnicos abaixo são proposta de implementação. Não aprova modelo físico integral, implantação ou testes.

## Política aprovada

- Eventos concluídos podem ser reprocessados por até sete dias, alinhados à janela de recuperação do beta.
- Eventos pendentes continuam recuperáveis até resolução, respeitando exclusão e retenção de dados pessoais. Não descartar trabalho pendente por uma limpeza genérica.
- Reconstruções mais antigas de feed e RunScore partem dos dados operacionais vigentes, sem exigir conservação indefinida de eventos.
- Reprocessamento é operação interna controlada pela equipe RunPass. O papel e a permissão técnica específicos ainda serão detalhados; não é concedido automaticamente a todo Administrador.

Para tornar a janela inequívoca, a proposta técnica é contá-la desde a última confirmação dos destinos obrigatórios, coerente com a retenção já aprovada dos payloads entregues. Replay não altera esse marco nem renova a retenção. Até validação do contrato operacional, essa âncora é detalhe técnico proposto, não uma nova decisão de produto presumida.

## Contrato técnico proposto

Cada evento tem eventId estável, tipo e versão do schema, agregado/ID, versão monotônica do agregado, occurredAt original e correlação. Retentativa preserva identidade e conteúdo. Separar evento de negócio do payload restrito de auditoria de avaliação; consumidores de feed/RunScore não recebem comentários históricos.

A alteração operacional e a outbox são persistidas atomicamente. Confirmação da API depende de persistência durável, não da conclusão de todos os consumidores. Cada destino obrigatório possui estado de entrega; publicar em transporte não comprova aplicação pelo consumidor.

Consumidores devem tolerar duplicação e fora de ordem: combinar versão do agregado, registro de processamento por consumidor/evento e escrita condicional/transacional do efeito. Sempre que possível, gravar efeito e confirmação de deduplicação juntos. Operação entre serviços que não compartilham transação precisa de protocolo idempotente específico; ledger sozinho não garante exatamente uma execução.

Não reexecutar uma operação apagada ou bloqueada apenas porque seu evento é válido. Conferir estado/versão e controle de exclusões antes de aplicar efeitos. Revisão ou exclusão de avaliação precisa remover a contribuição anterior ao atualizar o RunScore, sem somar repetidamente o mesmo resultado. A fórmula e o armazenamento dessa contribuição serão definidos no modelo físico.

## Retenção dos controles: desenho a fechar

Os sete dias de replay não bastam, isoladamente, para definir o TTL do ledger: existem entregas pendentes, mensagens em trânsito, processamento em curso e restaurações. Expirar controle antes do último efeito possível pode duplicar trabalho.

O modelo deve representar a expiração de replay por evento e comprovar cobertura de consumidores e referências de exclusão. Selecionar margem de segurança, prazo do ledger e política para mensagens antigas após desenhar transporte/recuperação. Retentativas não prolongam arbitrariamente a retenção de payloads pessoais.

Conservar payload concluído fora da janela de replay para aguardar limpeza não o torna elegível a replay. Requisição fora da janela retorna recusa explícita ou orienta reconstrução, sem redefinir occurredAt, eventId ou marco de conclusão.

## Reconstrução de projeções antigas

Reconstruir somente o que é derivável do estado operacional atual: não prometer recuperar comentários antigos ou estados históricos já descartados. Feed respeita visibilidade, bloqueios e exclusões atuais; RunScore usa avaliações atuais válidas.

Proposta: reconstrução isolada com versão/geração própria, leitura paginada e conciliação de alterações concorrentes antes de promover a projeção. Não substituir uma projeção atual por uma leitura antiga nem misturar cegamente snapshots com deltas. Estratégia final e custo precisam de validação técnica.

## Falhas e auditoria operacional

Consulta de pendências e reconciliador devem permitir recuperação independente de uma única cópia no transporte. Falhas exigem alerta e acompanhamento; fila de falhas não equivale a armazenamento definitivo de recuperação.

Replay registra ator autorizado, motivo, seleção, quantidade, resultado e correlação, sem copiar payloads pessoais para logs. Limites de lote, autorização e confirmação para ações de impacto serão detalhados antes da implementação.

O histórico restrito de avaliações mantém prazo de 60 dias desde ocorrência e a precedência da exclusão de conta. O tratamento específico de payload de auditoria ainda pendente ao vencer continua em avaliação; esta aprovação não o transforma em entregue nem autoriza preservação indefinida.

## Próximo desenho de dados

Produzir matriz de consultas/escritas e requisitos operacionais dos agregados: identidade/perfil, catálogo, histórico de corrida, social, projeções, beta, outbox e controles. A decisão anterior de agrupar dados relacionados orienta a modelagem, sem impor uma tabela para toda a aplicação. Apresentar tabelas, PK/SK, índices, transações e requisitos de recuperação como proposta consolidada, sem exigir aprovação por nome de atributo.

## Evidências necessárias

Duplicação; ordem invertida; falha entre efeito e confirmação; replay no limite da janela e após expiração; consumidor atrasado; restauração com evento já aplicado; exclusão concorrente; recomposição de RunScore; reconstrução de feed com bloqueio/ocultação; carga e custo de conciliação. Nenhuma evidência de execução foi produzida nesta revisão documental.
