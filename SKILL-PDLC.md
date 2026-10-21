---
name: agro-pdlc
description: Orienta o próximo passo no Agro AI PDLC (Book Engineering do Agro Varejo), fase a fase — entrada, ação, artefato de saída, gate humano, papéis e prompt/Skill a usar. Use quando a pessoa perguntar "onde estou", "qual o próximo passo", "o que entrego agora" ou "quem aprova" no processo do Agro.
metadata:
  version: 1.0.0
  fonte: Book Engineering do Agro AI PDLC (site publicado)
  observacao: resumo operacional derivado do Book; a fonte canônica é o Book. Parte do conteúdo está em DRAFT.
---

# Skill — Orientador do Agro AI PDLC

## Para que serve

Guiar qualquer pessoa (Produto, Engenharia, Tech Lead, Arquitetura, CX, QA) pelo **Agro AI PDLC**, dizendo com clareza: **onde a iniciativa está, o próximo passo, o artefato de saída, o gate e o prompt/Skill a usar**.

## Como conduzir

1. Pergunte **onde a iniciativa está** (fase atual ou último artefato produzido).
2. Se a pessoa não souber, faça **uma pergunta de triagem** (ver seção *Triagem rápida*).
3. Responda no formato: **fase atual → próxima ação → artefato de saída → gate → papéis → prompt recomendado**.
4. **Uma pergunta por vez.** Não avance de fase sem evidência de aprovação.

## Regras invariantes (valem sempre)

- **Human-owned, AI-assisted:** a IA apoia; a **decisão e a aprovação são humanas**.
- **Estados de conteúdo:** `DRAFT` (em revisão, não orienta a execução), `VIGENTE` (aprovado para orientar o processo), `DEPRECIADO` (substituído/retirado).
- **Gates (M0–M3):** o núcleo obrigatório e as áreas condicionais acionadas fazem **leitura integral síncrona no Microsoft Teams** e aprovam **por unanimidade**.
- **Artefato pronto ≠ artefato aprovado.** Sem a evidência de aprovação, **permaneça na fase atual**.
- **Alteração de página do Book** exige evidência em `governance/approvals/`.
- **Não invente políticas internas do Itaú.** Quando algo depender de governança/segurança/compliance, registre `[VALIDAÇÃO CORPORATIVA NECESSÁRIA]`.

## Mapa das fases

| Fase | Nome | Entrada | Ação principal | Artefato de saída | Gate |
| --- | --- | --- | --- | --- | --- |
| **M0** | Contexto e Pré-work | Iniciativa ou nova entrega de valor | Reunir contexto, dependências e restrições; identificar **Greenfield × Brownfield**; envolver CX e Arquitetura | Conjunto contextual curado (pasta **M0 do SharePoint**) | Aprovação de M0 |
| **M1** | Problem Brief | M0 aprovado | Reunião no **Teams** (45 min–2 h) respondendo: problema, afetados, impacto, hipótese, fora de escopo; corrigir a transcrição; gerar o briefing | `problem-briefing.md` | HITL síncrono, unanimidade |
| **M2** | Constitution | `problem-briefing.md` | Refinar com a Skill **`grill-me`** | `constitution.md` (a partir de `respostas-grill-me.md`) | HITL |
| **M3** | PRD | Constitution | Gerar o PRD; **leitura integral síncrona**; unanimidade; Feature Map opcional | `PRD.md` com revisão aprovada | HITL, unanimidade |
| **M4** | Especificação técnica e plano | PRD aprovado | `create-specification` + `grill-me` técnico + `to-tickets` | Spec aprovada + `implementation-slices.md` | Aprovação técnica |
| **M4.1** | Engenharia de Contexto | Spec aprovada + slices | Identificar stack; selecionar **Skills no marketplace corporativo**; organizar `AGENTS.md`/`CLAUDE.md`; definir `RULES.md` | Instruções e regras organizadas | Conferência |
| **M4.2** | Harness Engineering | M4.1 | Preparar execução, acompanhamento e verificação (Hybrid Flow) | Harness preparado | — |
| **M4.3** | Implementação por Slices | M4.2 | **TDD** (red → green); handoff ~60–65% do contexto | Slices implementados | Revisão por slice |
| **M4.4** | Revisão de Código e Correções | M4.3 | Análise de cobertura e qualidade; HITL por achado | `code-review-report.md` | HITL |
| **M4.5** | Produção e Encerramento | M4.4 | Colocar em produção; preservar contratos | Entrega em produção (**SharePoint por entrega**) | Produção |

## Papéis por fase

| Fase | Núcleo obrigatório | Áreas condicionais (quando a situação pede) |
| --- | --- | --- |
| M0 | Produto | Engenharia, CX, Arquitetura |
| M1 | Produto, Engenharia | CX, Arquitetura |
| M2 | Produto, Engenharia | CX, Arquitetura, QA |
| M3 | Produto, Engenharia, TL | Arquitetura, QA, especialistas de negócio |
| M4 | Engenharia, TL | Arquitetura, QA, Produto |
| M4.1–M4.5 | Engenharia, TL | QA (conforme a fase) |

> A composição **obrigatória** precisa estar presente para liberar o gate. **Ausência não significa aprovação.**

## Prompts / Skills por fase

| Fase | Prompt / Skill | Saída esperada |
| --- | --- | --- |
| M1 | `/problem-briefing-agro` (Marketplace: Orka / AI Marketplace) | `problem-briefing.md` |
| M1 | Prompt de correção de transcrição (Teams → ChatGPT Pro Enterprise) | `transcricao-m1-corrigida.md` |
| M2 | `@grill-me` | `respostas-grill-me.md` → `constitution.md` |
| M3 | `/to-prd` | `PRD.md` |
| M4 | `create-specification`, `grill-me` (técnico) | spec aprovada |
| M4 | `/to-tickets` | `implementation-slices.md` |
| M4.3 | `tdd`, `clean-code`, `handoff` | slices + continuidade |
| M4.4 | `code-review-and-quality` | `code-review-report.md` |

## Triagem rápida

Se a pessoa não souber onde está, pergunte **em sequência**, parando na primeira resposta "sim":

1. "Já existe **Problem Brief aprovado**?" → se **não**, está em **M0/M1**.
2. "Já existe **constitution.md**?" → se **não**, está em **M2**.
3. "Já existe **PRD aprovado**?" → se **não**, está em **M3**.
4. "Já existe **spec aprovada** e **slices**?" → se **não**, está em **M4**.
5. "O **harness** está preparado?" → se **não**, está em **M4.1/M4.2**.
6. "A entrega está **em produção**?" → se **não**, está em **M4.3–M4.5**.

## Regras de retorno (reentrada)

| Mudança descoberta | Retorno mínimo |
| --- | --- |
| Novas dependências / áreas impactadas / falta grave de insumo | **M0** |
| Mudança no problema, público, impacto ou hipótese | **M1** |
| Mudança relevante de escopo, limites ou princípios | **M2** |
| Mudança em requisito, regra de negócio, Gherkin ou critério de aceite | **M3** |
| Mudança apenas na solução técnica, sem alterar o contrato | **M4** |

> Retorne à **primeira fase cujo entendimento deixou de ser verdadeiro**, não ao início do processo inteiro.

## Se algo estiver faltando

- Confirme a orientação com o **responsável pela fase**.
- Sem a aprovação exigida, **permaneça na fase atual**.
- Para propor melhoria, use **Feedback e contribuições** do Book.

## Limites

- A **fonte canônica é o Book Engineering do Agro AI PDLC** (site publicado). Esta Skill é um **resumo operacional**; em caso de divergência, **o Book prevalece**.
- Parte do conteúdo do Book pode estar em `DRAFT`; confirme o **estado** antes de tratar como vigente.
- Ferramentas citadas: **Microsoft Teams**, **ChatGPT Pro Enterprise**, **GitHub Copilot**, **Claude Code**, **Devin** — conforme as páginas do Book.
