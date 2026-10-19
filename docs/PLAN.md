# Plano Técnico de Implementação: Subsistema de E-mail Marketing & Outbound

> **Módulo:** Ananke OS E-mail Marketing Suite  
> **Status:** Fase 2 - PLAN (Aguardando Aprovação)  
> **Especificação Base:** `.specify/email-marketing-system.md`  
> **Agente Responsável pelo Plano:** `project-planner` / `orchestrator`

---

## 1. Arquitetura da Solução

O subsistema será composto por 4 camadas essenciais integradas nativamente ao Ananke OS:

```plaintext
                              [ /email Workflow ]
                                       │
                         [ email-marketing-specialist ]
                                       │
       ┌──────────────────┬────────────┴─────────────┬──────────────────┐
       ▼                  ▼                          ▼                  ▼
[ Strategy & Funnel ] [ Cold Outreach ]   [ Template Engineering ] [ Lead Scraping ]
  (email-marketing-     (cold-email-        (email-template-         (lead-scraping-
      strategy)           outreach)             design)                enrichment)
       │                  │                          │                  │
  KPIs & Réguas      SPAM Score &          HTML Tabular + Inline   Scripts Python &
   de Nutrição      Aquecimento DNS         CSS cross-client        Regex de Extração
```

---

## 2. Inventário de Arquivos e Estrutura

### 2.1 Novo Agente Especialista
* **`.agent/agents/email-marketing-specialist.md`**: Persona do agente de e-mail marketing com papéis, workflows, filosofia, gatilhos de ativação e sinergias com `copywriter-ux`, `business-strategist` e `marketing-analyst`.

### 2.2 Novo Workflow de Comando
* **`.agent/workflows/email.md`**: Slash command `/email` que guia o usuário de forma interativa através de 5 sub-rotinas:
  1. Cold Outreach Sequencer (Cadência B2B)
  2. Inbound Newsletter & Promo Builder (HTML Tabular)
  3. Web Scraping & Contact Extraction
  4. Deliverability & Anti-Spam Auditor
  5. Campaign Analytics & Benchmark Review

### 2.3 Novas Skills Especializadas
1. **`.agent/skills/email-marketing-strategy/SKILL.md`**:
   * Arquitetura de réguas de automação (Onboarding, Nutrição, Carrinho Abandonado, Reengajamento).
   * Matriz de segmentação comportamental e demográfica.
   * Benchmarks da indústria e fórmulas de cálculo de ROI, CTR, CTOR e Churn.
2. **`.agent/skills/cold-email-outreach/SKILL.md`**:
   * Engenharia de abordagem B2B (Frameworks: PAS, BAB, AIDA adaptados para cold mail).
   * Regras de ouro de cold email (tamanho ideal de 50 a 125 palavras, CTA de baixa fricção).
   * Checklist de entregabilidade técnica: registros DNS (SPF, DKIM, DMARC, BIMI), aquecimento de domínio e filtros de spam.
3. **`.agent/skills/email-template-design/SKILL.md`**:
   * Princípios de codificação de HTML para e-mail (layouts baseados em `table`, largura de 600px, font fallbacks, bulletproof buttons).
   * Script Python utilitário: `.agent/skills/email-template-design/scripts/inline_styler.py` (converte CSS `<style>` em atributos `style=""` inline e gera versão Plain Text espelho).
4. **`.agent/skills/lead-scraping-enrichment/SKILL.md`**:
   * Metodologia de prospecção e extração ética de e-mails em fontes públicas da web.
   * Script Python utilitário: `.agent/skills/lead-scraping-enrichment/scripts/lead_scraper.py` (faz crawling simples de páginas institucionais, extrai e-mails válidos com regex, remove falsos positivos e exporta para CSV formatado).

### 2.4 Atualizações de Sistema e Sincronização
* **`.agent/ARCHITECTURE.md`**: Atualizar a contagem total para 36 agentes, 58 skills e 22 workflows.
* **`brain-map/brain-data.js`**: Adicionar os novos nós e conexões do novo agente, workflow e 4 skills no grafo neural 3D do ecossistema.

---

## 3. Plano de Fases e Verificação

| Tarefa | Componente | Responsável | Verificação |
| :--- | :--- | :--- | :--- |
| **T1** | Criar Agente `email-marketing-specialist` | `sdd-specialist` / `project-planner` | Validação de frontmatter e regras |
| **T2** | Criar Workflow `/email` | `orchestrator` | Validação de sintaxe e subcomandos |
| **T3** | Criar Skill `email-marketing-strategy` | `business-strategist` / `marketing-analyst` | SKILL.md com matriz e benchmarks |
| **T4** | Criar Skill `cold-email-outreach` | `copywriter-ux` / `email-marketing-specialist` | SKILL.md com frameworks e entregabilidade |
| **T5** | Criar Skill `email-template-design` + script | `frontend-specialist` / `css-architect` | Script Python `inline_styler.py` testado |
| **T6** | Criar Skill `lead-scraping-enrichment` + script | `data-analyst` / `integration-engineer` | Script Python `lead_scraper.py` testado |
| **T7** | Atualizar `ARCHITECTURE.md` e `brain-data.js` | `orchestrator` | Integridade do grafo e contagem |
| **T8** | Executar Checklist de Validação Geral | `test-engineer` | `python .agent/scripts/checklist.py .` |
