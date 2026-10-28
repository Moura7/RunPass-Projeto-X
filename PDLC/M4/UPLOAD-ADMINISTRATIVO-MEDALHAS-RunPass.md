# RunPass — Upload administrativo de imagens oficiais

Estado: parâmetros de formato, tamanho e meta de processamento aprovados pelo usuário; demais detalhes técnicos em revisão; não implementada. Complementa a SPEC e a política aprovada de preservação da versão vinculada a cada medalha.

## Fluxo proposto

1. Administrador autenticado com MFA solicita uma sessão de upload, informando a edição e, quando aplicável, a distância. Moderadores e corredores não podem utilizar essa operação.
2. A API verifica a autorização e o destino, cria um identificador de upload e permite enviar o arquivo para uma área privada temporária do S3. O cliente não escolhe uma chave arbitrária nem fornece uma URL externa para importação.
3. O administrador envia o arquivo e solicita sua finalização. O backend verifica o objeto da sessão e inicia o processamento idempotente.
4. O processamento verifica o formato real, tamanho e decodificação, corrige a orientação, remove metadados de localização e gera a imagem otimizada. Propõe-se reutilizar JPEG/PNG, original de até 10 MB e meta de até 1 MB para o derivado, já definidos para fotos dos corredores. Limite de pixels deve ser definido antes da implementação.
5. O painel acompanha o estado pendente, válido ou falha. Propõe-se a mesma meta de retorno em até cinco segundos após o upload, em condições normais. Exceder a meta mantém o estado pendente; não autoriza publicação nem implica arquivo inválido.
6. Após visualizar a imagem validada, o administrador confirma sua vinculação à edição/distância. A confirmação exige a versão esperada do cadastro e produz registro de auditoria. Um conflito exige recarregar o cadastro antes de confirmar novamente.

## Publicação e preservação

O upload, isoladamente, não altera o catálogo. Até a confirmação, permanece a imagem vigente. Na ausência de imagem oficial, permanece disponível o fluxo já definido de foto própria obrigatória do corredor.

Cada imagem publicada recebe referência imutável. Novas medalhas vinculam a versão vigente; medalhas existentes mantêm sua referência anterior. Fotos próprias não são substituídas. Uma tentativa repetida de confirmação deve retornar o mesmo resultado ou conflito explícito, sem criar versões repetidas inadvertidamente.

Objetos temporários e versões validadas ainda não vinculadas precisam de limpeza com prazo a definir. A limpeza não pode remover versões referenciadas, inclusive por medalhas ocultas. Uma imagem anteriormente vinculada ao catálogo também não deve ser apagada apenas porque deixou de ser a versão vigente.

Correções retroativas permanecem uma operação separada, explícita e auditada; este fluxo não as executa.

## Contrato candidato

| Método | Rota | Finalidade |
| --- | --- | --- |
| POST | /admin/medal-image-uploads | Criar sessão com edição e distância opcional |
| POST | /admin/medal-image-uploads/{id}/finalize | Confirmar envio e iniciar validação |
| GET | /admin/medal-image-uploads/{id} | Consultar estado e motivo de falha |
| PATCH | /admin/editions/{id} | Vincular referência validada usando o contrato existente e a versão esperada |

As novas rotas estão incorporadas ao OpenAPI 0.7.0-draft como proposta técnica, sem implementação. A API deve verificar que a referência pertence ao fluxo administrativo, ao ambiente e ao destino informado; uma referência de upload de corredor não basta. A URL de upload não concede permissão de publicação.

## Auditoria e verificações de aceite

Registrar ator, edição/distância, referências anterior e nova, instante, resultado e identificador de correlação. Não registrar tokens nem URLs assinadas. O destino e a retenção dessa auditoria administrativa precisam de definição própria; a retenção de 60 dias do histórico de avaliações não se aplica automaticamente.

- Corredor, moderador e administrador sem MFA não conseguem iniciar ou publicar.
- Upload pendente, inválido ou de outro destino não pode ser vinculado.
- Falha no processamento preserva a imagem vigente e permite novo envio.
- Duas alterações concorrentes não sobrescrevem silenciosamente uma à outra.
- Substituir a imagem não muda medalhas antigas nem fotos próprias.
- Repetir finalização ou confirmação não duplica efeitos.
- Original não tratado não é disponibilizado aos corredores; derivados não contêm GPS.
- Limpeza preserva qualquer imagem ainda referenciada.

## Revisão necessária

Reutilização aprovada: JPEG/PNG, original de até 10 MB, otimização com meta de até 1 MB e meta de validação de cinco segundos após o upload, em condições normais e sujeita a testes. Essa confirmação não aprova automaticamente as rotas candidatas nem a SPEC integral. Definir depois limites de pixels, expiração das sessões e arquivos não vinculados, retenção da auditoria e o mecanismo de correção retroativa. Nenhuma infraestrutura foi provisionada e a SPEC integral continua em revisão.
