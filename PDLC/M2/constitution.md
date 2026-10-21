# M2 — RunPass: Constitution

> Aprovação atual: todos os artefatos deste pacote foram aprovados explicitamente pelo usuário na conversa, pela instrução «Coloque todos os artefatos como Aprovados». Este registro prevalece sobre referências anteriores a aprovação de conteúdo pendente. Lacunas identificadas permanecem documentadas; não se presume reunião, unanimidade de outros participantes, aprovação técnica ou liberação de produção.

**Estado:** APROVADO PELO USUÁRIO — princípios derivados das decisões já confirmadas, aguardando revisão do artefato e gate aplicável.

**Base:** problem-briefing.md, respostas-grill-me.md e PRD_RunPass_MVP_v2.md. Conteúdo do PRD aprovado pelo usuário; essa aprovação não é transferida automaticamente para esta Constitution.

## 1. Propósito

Entregar um histórico social de experiências em provas de rua, conectando corridas concluídas, medalhas, avaliações, descoberta e interação entre corredores.

## 2. Unidade e integridade do histórico

- Edição é a ocorrência específica da prova, não apenas seu ano.
- Uma participação por usuário e edição, restrita a conclusão autodeclarada.
- Corrigir dados não cria registros duplicados. Conflito exige editar ou excluir o registro existente, sem sobrescrita automática.
- Rascunho/concluída é estado da participação; publicação/ocultação no feed é independente.
- Edição com participações é arquivada para novas ações, preservando histórico e referências.

## 3. Conclusão e medalha

- Conclusão inicial exige oito notas de 1 a 5: organização, percurso, kit, medalha, hidratação, estrutura, segurança e custo-benefício.
- Tempo e comentário opcionais; colocação e número do peito opcionais.
- Medalha vinculada automaticamente. Sem imagem do catálogo, foto enviada pelo usuário é obrigatória; sem imagem, manter rascunho.
- Foto própria não altera nem abastece automaticamente o catálogo de outros usuários.

## 4. Avaliação e confiança

- RunScore separado por edição: média das médias simples dos oito critérios, pesos iguais, uma casa decimal na exibição.
- Filtrar avaliações por distância não cria automaticamente outro score.
- Usuário pode editar e excluir seus registros; atualizar agregados e vínculos consistentemente.
- Revisão humana pode ocultar texto sem invalidar notas.
- Invalidação retira notas do público e do RunScore, preserva participação/medalha/post e permite correção sujeita a revisão. Essa exceção posterior não dispensa notas no cadastro inicial.

## 5. Controle e exposição

- Perfil público; nome de exibição e username obrigatórios, foto do perfil/cidade/bio opcionais, e-mail privado.
- Publicações e resultados informados visíveis por padrão, ocultáveis durante ou após publicação.
- Tempo e colocação controlados por participação. Ocultar tempo oculta pace em todas as superfícies controladas pelo produto, inclusive cards novos.
- Wishlist pública e ocultável.
- Fotos da medalha vinculadas ao usuário podem aparecer no perfil e na publicação; vinculação individual não equivale a sigilo.
- Bloqueio impede novas interações e oculta conteúdo/interações anteriores entre os envolvidos, sem apagar registros.

## 6. Escopo social e catálogo

- Feed de conclusões e medalhas com curtidas/comentários, aberto ao conteúdo público de outros usuários e priorizando quem o corredor segue como ordenação.
- Sem site público no MVP; painel administrativo interno mínimo necessário à operação.
- Equipe RunPass mantém catálogo e modera conteúdo; cadastro de prova por usuário exige aprovação antes de publicação.
- Solicitações duplicadas podem ser vinculadas à edição existente; preservar rascunho, avisar e permitir revisão. Recusas têm motivo e reenvio.
- Catálogo inicial: São Paulo capital, dois anos de histórico e eventos futuros; provas mais antigas podem ser solicitadas.

## 7. Validar antes de ampliar

- Beta gratuito, por convite, maiores de 18 anos; meta/teto 1.000, 60 dias desde os primeiros 50.
- Ativação sobre admitidos reais: 50%; repetição e interação: 30% dos ativados cada.
- “Ativo” na visão de adesão significa ao menos um cadastro completo, não uso frequente.
- Cobertura do catálogo medida por lista congelada de edições dos primeiros convidados, com mínimo de 90% no recorte.
- Feedback após primeiro registro, canal contínuo, pesquisas aos 30/60 dias e pergunta opcional após sete dias sem registro; consolidação semanal.
- Sem monetização, site público, push, clubes, rankings, treino/GPS ou integrações avançadas nesta fase.

## 8. Limites técnicos e evolução

Não aprovar arquitetura por inferência. Flutter/AWS são referências a validar na especificação. Regras de privacidade, elegibilidade, retenção, distribuição, limites de conteúdo e observabilidade exigem detalhamento próprio. Não transformar ausência de pesquisa em evidência de demanda.

Mudanças no problema/público retornam a M1; nos princípios/escopo, a M2; nos requisitos, a M3; apenas na solução técnica, a M4, conforme a skill. A entrevista encerrada não autoriza ampliar o escopo sem revisão humana.

## 9. Gate e lacunas

Produto e Engenharia são obrigatórios em M2; CX, Arquitetura e QA conforme impacto. Não há nomes, pareceres nem evidência de rito formal. Princípios sintetizados aqui precisam de revisão; não há aprovação automática deste arquivo.

M0/M1 continuam sem gate evidenciado. Book canônico não fornecido. Adaptação dos ritos corporativos para o projeto privado não aprovada. Detalhes ainda abertos devem permanecer identificados, sem nova entrevista automática nem execução de fases posteriores por presunção.
