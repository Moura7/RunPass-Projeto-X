# PRD — RunPass MVP

## 1. Visão do Produto

**Nome:** RunPass  
**Categoria:** SportTech / Social Network / Running  
**Plataformas:** iOS e Android  
**Mercado inicial:** Brasil  
**Região inicial de lançamento:** São Paulo

O RunPass será uma plataforma social voltada para corredores de rua, permitindo registrar provas realizadas, organizar medalhas, avaliar eventos, descobrir novas corridas e compartilhar conquistas com outros corredores.

O foco inicial não será competir com aplicativos de tracking esportivo, mas registrar a **experiência do corredor em provas de rua**.

### Proposta de valor

> O RunPass é o lugar onde corredores registram suas provas, colecionam suas medalhas, avaliam eventos e descobrem onde correr a seguir.

---

## 2. Problema

Hoje a jornada do corredor é fragmentada entre diferentes plataformas.

O usuário normalmente:

- descobre uma corrida em redes sociais;
- realiza a inscrição em outra plataforma;
- registra a atividade no relógio ou aplicativo esportivo;
- compartilha fotos em uma rede social;
- guarda a medalha fisicamente;
- comenta informalmente com outros corredores sobre a qualidade da prova.

Não existe um local centralizado para registrar:

- provas realizadas;
- medalhas conquistadas;
- avaliações das provas;
- histórico de participação;
- experiências;
- próximas corridas desejadas.

---

## 3. Objetivo do MVP

Validar se corredores têm interesse em manter um histórico social de suas experiências em provas.

O MVP deverá permitir ao usuário:

1. criar sua conta;
2. criar seu perfil;
3. encontrar uma corrida;
4. informar que participou;
5. registrar seu resultado;
6. avaliar a prova;
7. adicionar a medalha à sua coleção;
8. visualizar o histórico de provas;
9. salvar provas futuras;
10. compartilhar uma conquista.

---

## 4. Objetivos de Negócio

O primeiro objetivo não será maximizar receita.

O objetivo será validar:

### Hipótese 1
Corredores querem manter um histórico digital das provas realizadas.

### Hipótese 2
Medalhas digitais aumentam o interesse em registrar provas.

### Hipótese 3
Corredores estão dispostos a avaliar provas.

### Hipótese 4
Avaliações ajudam outros corredores a decidir quais provas realizar.

### Hipótese 5
Compartilhar conquistas gera aquisição orgânica de novos usuários.

---

## 5. Público-Alvo

### Persona principal

#### Corredor recreativo

Características:

- 25 a 45 anos;
- participa de provas de rua;
- corre principalmente 5 km, 10 km ou 21 km;
- participa de 4 a 12 provas por ano;
- utiliza Instagram e WhatsApp;
- pode utilizar Strava, Garmin ou Apple Watch;
- gosta de registrar conquistas;
- valoriza medalhas;
- pesquisa novas provas com frequência.

### Principais necessidades

- lembrar das provas realizadas;
- guardar resultados;
- visualizar medalhas;
- descobrir novas corridas;
- saber se uma corrida vale a pena;
- compartilhar conquistas.

---

## 6. Proposta de Valor do MVP

O MVP será estruturado em quatro pilares.

### Collect
Registrar provas e medalhas.

### Review
Avaliar experiências em provas.

### Discover
Encontrar novas corridas.

### Share
Compartilhar conquistas.

---

## 7. Jornada Principal

```text
Usuário cria conta
    ↓
Completa perfil
    ↓
Encontra uma prova
    ↓
Seleciona "Eu participei"
    ↓
Registra distância e resultado
    ↓
Avalia a corrida
    ↓
Adiciona medalha
    ↓
RunPass registra a conquista
    ↓
Usuário compartilha a conquista
    ↓
Conquista aparece no perfil
```

---

## 8. Funcionalidades do MVP

### 8.1 Cadastro

O usuário poderá criar conta utilizando:

- e-mail;
- senha.

#### Requisitos

- validar e-mail;
- confirmação de cadastro;
- recuperação de senha;
- logout.

#### Futuro

- Google Login;
- Sign in with Apple.

---

## 9. Perfil do Usuário

Cada usuário terá um perfil.

### Informações

- foto;
- nome;
- username;
- cidade;
- bio;
- número de provas;
- número de medalhas;
- cidades onde correu.

### Exemplo

```text
Thiago Generoso
São Paulo
23 provas
23 medalhas
6 cidades
```

---

## 10. Catálogo de Corridas

O aplicativo deverá possuir um catálogo de provas.

Cada prova terá:

- nome;
- organizador;
- data;
- cidade;
- estado;
- distância;
- imagem;
- descrição;
- link oficial;
- link de inscrição;
- status da prova.

### Exemplo

```text
Circuito das Estações — Primavera
São Paulo
10 km
22/09/2027
```

---

## 11. Busca de Corridas

O usuário poderá pesquisar provas.

### Filtros iniciais

- nome;
- cidade;
- data;
- distância.

### Futuro

- faixa de preço;
- avaliação;
- tipo de percurso;
- organizador.

---

## 12. Página da Corrida

A página da corrida deverá apresentar:

- imagem;
- nome;
- data;
- cidade;
- distâncias;
- descrição;
- avaliação média;
- avaliações recentes;
- quantidade de participantes RunPass.

### CTAs

- **Eu participei**
- **Quero correr**

---

## 13. Participação

O usuário poderá informar que participou de uma corrida.

### Dados

- corrida;
- distância;
- tempo;
- pace;
- posição opcional;
- número do peito opcional;
- comentário opcional.

---

## 14. Avaliação da Corrida

Após registrar participação, o usuário poderá avaliar a prova.

### Critérios

- organização;
- percurso;
- kit;
- medalha;
- hidratação;
- estrutura;
- segurança;
- custo-benefício.

### Escala

1 a 5 estrelas.

Também haverá campo para comentário.

---

## 15. RunScore

Cada corrida terá uma avaliação consolidada.

### MVP

RunScore será inicialmente a média das avaliações.

```text
RunScore
4,7 / 5
Baseado em 847 avaliações
```

Em versões futuras o algoritmo poderá utilizar pesos por categoria.

---

## 16. Medalheiro

Cada usuário terá uma coleção de medalhas digitais.

### Informações

- imagem da medalha;
- prova;
- ano;
- cidade;
- distância;
- tempo.

---

## 17. Wishlist

O usuário poderá salvar provas futuras.

### CTA

**Quero correr**

A wishlist deverá mostrar:

- prova;
- cidade;
- data;
- distância.

O usuário poderá remover uma prova da lista.

---

## 18. Feed Social

O MVP terá um feed social básico.

Posts poderão ser gerados automaticamente quando o usuário:

- concluir uma prova;
- adicionar uma medalha;
- atingir uma conquista.

### Interações

- curtir;
- comentar.

### Fora do MVP

- mensagens privadas;
- stories;
- vídeos;
- reels;
- grupos.

---

## 19. Compartilhamento

Após registrar uma corrida, o aplicativo poderá gerar um card compartilhável.

### Canais

- Instagram;
- WhatsApp;
- compartilhamento nativo do celular.

O card deverá possuir a marca RunPass.

---

## 20. Conquistas

O MVP poderá possuir conquistas simples.

Exemplos:

- primeira corrida;
- 5 provas;
- 10 provas;
- primeiro 10K;
- primeira meia maratona;
- primeira maratona.

---

## 21. Painel Administrativo

Será necessário um painel web simples.

### Funções

- cadastrar corrida;
- editar corrida;
- remover corrida;
- cadastrar organizador;
- adicionar imagem;
- adicionar medalha;
- consultar avaliações;
- moderar conteúdo.

---

## 22. Moderação

O aplicativo deverá permitir:

- denunciar comentário;
- denunciar usuário;
- denunciar avaliação;
- bloquear conteúdo impróprio.

Administradores poderão:

- remover comentário;
- remover review;
- suspender usuário.

---

## 23. Requisitos Não Funcionais

### Performance

- tela inicial: meta inferior a 3 segundos em conexão adequada;
- APIs críticas: meta média inferior a 500 ms.

### Disponibilidade

- meta inicial: 99,5%.

### Segurança

- autenticação via token;
- HTTPS obrigatório;
- senhas não armazenadas diretamente;
- autorização por usuário;
- logs de operações sensíveis.

---

## 24. Privacidade e LGPD

O usuário deverá aceitar:

- Termos de Uso;
- Política de Privacidade.

O sistema deverá permitir:

- solicitar exclusão da conta;
- excluir dados pessoais;
- alterar dados pessoais.

Dados de localização precisa não serão necessários no MVP.

---

## 25. Arquitetura Inicial

### Mobile

Flutter.

### Backend

AWS.

### Componentes

- Amazon Cognito;
- API Gateway;
- AWS Lambda;
- DynamoDB;
- PostgreSQL;
- Amazon S3;
- CloudFront;
- CloudWatch.

### Fluxo

```text
App Flutter
    ↓
API Gateway
    ↓
Lambda
    ↓
Banco de dados
```

---

## 26. Analytics

Eventos mínimos:

- `user_registered`
- `login_completed`
- `race_viewed`
- `race_searched`
- `participation_created`
- `review_created`
- `medal_added`
- `wishlist_added`
- `post_liked`
- `post_commented`
- `achievement_unlocked`
- `share_clicked`

---

## 27. Métrica Principal

### North Star Metric

**Participações registradas por mês.**

Essa métrica representa diretamente o uso central do produto.

---

## 28. Métricas Secundárias

### Aquisição

- usuários cadastrados;
- custo por cadastro;
- origem do cadastro.

### Ativação

Percentual de usuários que registram pelo menos uma prova.

### Engajamento

- provas por usuário;
- reviews por usuário;
- medalhas por usuário;
- compartilhamentos.

### Retenção

- D7;
- D30;
- usuários ativos mensais.

---

## 29. Metas do Beta

Primeira fase:

- 100 usuários.

Metas:

- 70% completarem o perfil;
- 50% registrarem pelo menos uma corrida;
- 30% criarem pelo menos uma avaliação;
- 20% compartilharem uma conquista;
- 300 participações;
- 200 reviews;
- 100 medalhas registradas.

---

## 30. Meta Inicial de Catálogo

Antes do beta público:

**500 provas cadastradas.**

Prioridade:

- São Paulo;
- principais capitais;
- principais circuitos nacionais.

---

## 31. Escopo Fora do MVP

Não implementar inicialmente:

- tracking GPS;
- criação de treino;
- planos de treinamento;
- streaming;
- chat;
- marketplace próprio;
- pagamento;
- venda direta de inscrição;
- IA avançada;
- Garmin;
- Strava;
- Apple Health;
- Health Connect;
- turismo esportivo.

---

## 32. Prioridades

### P0 — Lançamento

- cadastro;
- autenticação;
- perfil;
- catálogo;
- detalhes da corrida;
- participação;
- reviews;
- medalheiro;
- wishlist;
- compartilhamento.

### P1 — Primeiras evoluções

- feed;
- curtidas;
- comentários;
- conquistas;
- ranking.

### P2 — Crescimento

- seguir usuários;
- notificações;
- clubes;
- assessorias;
- integrações esportivas.

### P3 — Monetização

- RunPass Premium;
- marketplace;
- afiliados;
- organizadores;
- analytics B2B.

---

## 33. Critérios de Sucesso do MVP

O MVP será considerado validado se, após o período inicial de testes:

- usuários registrarem espontaneamente múltiplas provas;
- pelo menos 30% dos participantes deixarem avaliações;
- medalheiro apresentar forte uso;
- usuários compartilharem cards externamente;
- houver retorno para descobrir novas provas;
- organizadores demonstrarem interesse nos dados coletados.

---

## 34. Perguntas que o MVP Precisa Responder

1. Usuários realmente querem cadastrar provas passadas?
2. A medalha é um incentivo forte para criar histórico?
3. Usuários estão dispostos a avaliar eventos?
4. Outros corredores consultam avaliações antes de escolher provas?
5. Compartilhamento gera aquisição?
6. O feed melhora a retenção?
7. Organizadores enxergam valor nos reviews?

---

## 35. Visão Pós-MVP

Caso as hipóteses sejam validadas, as próximas frentes serão:

### Social

- seguir corredores;
- clubes;
- assessorias.

### Intelligence

- RunScore avançado;
- rankings;
- recomendações.

### Integrações

- Strava;
- Garmin;
- Apple Health;
- Health Connect.

### Monetização

- afiliados;
- RunPass+;
- B2B para organizadores;
- campanhas patrocinadas.

### Marketplace

- inscrições;
- produtos;
- turismo esportivo.

---

## 36. Visão de Longo Prazo

Transformar o RunPass na principal plataforma de identidade e experiência de corredores de rua no Brasil.

O usuário deve conseguir responder:

- Onde corri?
- Quais medalhas conquistei?
- Como foi minha experiência?
- Onde meus amigos estão correndo?
- Qual deve ser minha próxima prova?

Tudo dentro do RunPass.
