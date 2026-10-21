# M0 — RunPass: contexto e pré-work

> Aprovação atual: todos os artefatos deste pacote foram aprovados explicitamente pelo usuário na conversa, pela instrução «Coloque todos os artefatos como Aprovados». Este registro prevalece sobre referências anteriores a aprovação de conteúdo pendente. Lacunas identificadas permanecem documentadas; não se presume reunião, unanimidade de outros participantes, aprovação técnica ou liberação de produção.

**Estado:** APROVADO PELO USUÁRIO — reconstrução documental para revisão, sem gate aprovado.

## Origem e limites

Derivado do PRD_RunPass_MVP_v2.md aprovado quanto ao conteúdo de produto e da conversa grill-me consolidada em RUNPASS-CONTEXTO-E-DEFINICOES.md. Não houve reunião ou transcrição Teams fornecida. Não se pretende comprovar uma sequência de gates que não ocorreu.

## Iniciativa

Criar uma rede social de experiências em corridas de rua para Android e iPhone. Corredores registram provas concluídas, medalhas e avaliações, descobrem eventos e interagem com conhecidos e outros participantes.

Classificação proposta: **Greenfield**, pois a solicitação é de novo produto e não há aplicação existente identificada. Não foi feita auditoria de repositórios externos.

## Público e recorte

- Corredores de rua; persona de referência recreativa, inicialmente conectada a conhecidos.
- São Paulo capital como prioridade do catálogo, com dois anos de histórico e provas futuras.
- Beta gratuito e por convite, para maiores de 18 anos.
- Meta e teto de 1.000 admitidos; janela de 60 dias iniciada com os primeiros 50.

## Contexto e restrições confirmados

- Sem site para corredores no MVP; painel interno mínimo incluído.
- Provas de usuários exigem revisão humana pela equipe RunPass.
- Sem GPS, treino, monetização, clubes, push ou integrações esportivas/IA nesta fase.
- Perfis e publicações públicos por padrão, com controles de ocultação; dados privados de conta não se tornam públicos.
- Conteúdo do PRD v2 aprovado pelo usuário; arquitetura Flutter/AWS é referência preliminar, não decisão técnica aprovada.

## Dependências e preparação

| Dependência | Situação / lacuna |
| --- | --- |
| Catálogo e imagens das medalhas | Equipe responsável definida como RunPass; pessoas, capacidade, fontes e condições de uso dos dados/imagens ainda não registradas. |
| Lista para cobertura de 90% | Método aprovado: edições distintas citadas pelos primeiros convidados; coleta e congelamento ainda a executar. |
| Recrutamento | Convites e teto definidos; responsáveis, canais e cronograma não definidos. |
| Moderação e feedback | Revisão humana e consolidação semanal aprovadas; escala de operação e prazos não definidos. |
| Distribuição Android/iOS | Contas, publicação, testes e links para lojas ainda a validar tecnicamente. |
| Engenharia e infraestrutura | Equipe, orçamento, acessos, stack final e custos não confirmados. |
| Privacidade e segurança | Requisitos no PRD; textos, retenção, descarte e verificação etária ainda exigem detalhamento e revisão especializada. |

## Riscos de descoberta

- Oito notas obrigatórias e foto obrigatória sem imagem do catálogo podem aumentar abandono.
- Autodeclaração pode produzir avaliações falsas; moderação e confiança precisam ser observadas.
- Qualidade do catálogo e rapidez de revisão afetam a ativação.
- Conteúdo público exige controles de visibilidade consistentes.
- Contar segunda prova histórica mede repetição de registro, sem provar retenção recorrente.

## Responsáveis e gate

Skill original: Produto obrigatório; Engenharia, CX e Arquitetura conforme a situação. Não há nomes e pareceres desses papéis registrados. Não atribuir ao assistente a aprovação humana.

Gate M0 pendente. Não há evidência de leitura síncrona/unanimidade. Teams/SharePoint e governança corporativa da skill não foram adaptados formalmente ao RunPass. O Book canônico não foi fornecido nem verificado; não inventar políticas do Itaú ou presumir aplicabilidade corporativa.

## Checklist para revisão

- Confirmar classificação Greenfield e responsáveis reais.
- Registrar dependências, recursos e restrições ainda desconhecidos.
- Executar coleta do catálogo antes de liberar beta.
- Registrar aprovação de M0 ou adaptação explícita do processo antes de declarar sua conclusão.
