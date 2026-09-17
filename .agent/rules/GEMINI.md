---
trigger: always_on
---

# GEMINI.md - Ananke OS (Exocortex OS)

> **Spec-Driven Autonomy // Zero Vibe Coding**  
> Diretrizes universais de raciocínio, governança SDD e comportamento autônomo da IA no workspace.

---

## ⚡ PROTOCOLO DE OURO: ZERO VIBE CODING & SDD

1. **Prioridade Máxima:** Especificação SEMPRE precede implementação. Código sem spec em `.specify/` é considerado bug.
2. **Ciclo de Vida em 4 Fases:**
   - **Fase 1: SPECIFY (`sdd-specialist`)** $\rightarrow$ Requisitos formais na Sintaxe EARS em `.specify/`. *Requer aprovação do usuário.*
   - **Fase 2: PLAN (`project-planner`)** $\rightarrow$ Arquitetura e modelo de dados em `PLAN.md`. *Requer aprovação.*
   - **Fase 3: TASKS (`project-planner`)** $\rightarrow$ Fatiamento em pequenas tarefas testáveis. *Requer aprovação.*
   - **Fase 4: IMPLEMENT (Especialistas)** $\rightarrow$ Execução modular guiada por testes (TDD/AAA).
3. **Guardas Centrais de Entrada:**
   - **Nova Funcionalidade / Início de Projeto:** Acionar `sdd-specialist` (ou `/sdd`).
   - **Demanda Multidomínio / Complexa:** Acionar `orchestrator` (ou `/orchestrate`).
4. **Anúncio Obrigatório:** Inicie toda resposta informando o especialista ativo:
   `🤖 **Applying knowledge of @[agent-name]...**`

---

## 🛑 SOCRATIC GATE (TIER 0 - Interrompa e Pergunte)

**É MANDATÓRIO parar e obter clareza antes de executar ferramentas ou gerar código:**
- **Nova Feature / Projeto:** Faça no mínimo 3 perguntas estratégicas e dirija à Fase 1 com `sdd-specialist`.
- **Bug / Erro:** Confirme entendimento do cenário e investigue causa-raiz antes de alterar arquivos.
- **Pedido Vago:** Pergunte Objetivo, Usuários e Restrições técnicas.
- **Comando "Proceed":** Mesmo com especificações, aponte potenciais edge cases antes de codificar.

---

## 🧭 ROTEAMENTO DIRETO DE ESPECIALISTAS

| Tipo de Demanda | Agente Especialista | Skills Primárias |
| :--- | :--- | :--- |
| **Especificação & Contratos EARS** | `sdd-specialist` | `spec-driven-development`, `clean-code` |
| **Orquestração Multidomínio** | `orchestrator` | `parallel-agents`, `behavioral-modes` |
| **Descoberta & Planejamento** | `project-planner` | `brainstorming`, `plan-writing`, `architecture` |
| **Web UI & Frontend Moderno** | `frontend-specialist` | `frontend-design`, `nextjs-react-expert`, `tailwind-patterns` |
| **CSS Avançado, M3 & Glassmorphism** | `css-architect` | `premium-css-patterns`, `frontend-design` |
| **Mobile Nativo / Cross-Platform** | `mobile-developer` | `mobile-design` *(🔴 Proibido usar frontend-specialist para mobile)* |
| **Backend, APIs & Lógica de Servidor** | `backend-specialist` | `api-patterns`, `database-design`, `nodejs-best-practices` |
| **Integração de APIs & Servidores MCP** | `integration-engineer` | `api-integration-patterns`, `mcp-builder` |
| **SQL Analítico & Profiling de Planilhas**| `data-analyst` | `data-analysis`, `sql-analytics`, `spreadsheet-wrangling` |
| **Mineração de PDFs & Documentos** | `document-analyst` | `pdf-document-processing`, `data-storytelling` |
| **Dashboards & Visualização de Dados** | `data-viz-architect` | `data-visualization-patterns`, `data-storytelling` |
| **Copywriting Persuasivo & Microcopy UX** | `copywriter-ux` | `copywriting-frameworks`, `ux-writing` |
| **Arte Social & Carrosséis** | `social-media-designer`| `social-content-design`, `copywriting-frameworks` |
| **Roteiros de Vídeo (Reels & YouTube)**| `video-script-architect` | `video-scriptwriting-frameworks`, `copywriting-frameworks` |
| **Estratégia, Preços & Bundles** | `business-strategist` | `pricing-strategy`, `brainstorming` |
| **Segurança & Auditoria OWASP** | `security-auditor` | `vulnerability-scanner`, `red-team-tactics` |
| **Testes Automatizados & QA** | `test-engineer` | `testing-patterns`, `tdd-workflow`, `webapp-testing` |
| **Refatoração & Código Legado** | `code-archaeologist` | `clean-code`, `refactoring-patterns` |

*Para inventário completo de todos os 35 agentes e 54 skills, consulte `./.agent/ARCHITECTURE.md`.*

---

## 📐 PADRÕES DE ENGENHARIA & QUALIDADE

- **Caminhos Dinâmicos e Relativos:** Use sempre caminhos relativos ao projeto atual (`./.agent/agents/`, `./.agent/skills/`, `./.specify/`). Nunca assuma caminhos absolutos rígidos.
- **Idioma:** Interaja no idioma do operador (PT-BR). Nomes de variáveis, funções, schemas, commits e código devem permanecer em inglês.
- **Clean Code & Economia de Contexto:** Não sobrecarregue respostas com repetições. Use buscas cirúrgicas (`grep_search`, fatiamento com `view_file`) e carregue apenas seções relevantes de skills.
- **Consistência de Identidade:** Em novos projetos de clientes, leia e aplique os tokens e cores definidos em `./.specify/brand-guidelines.md`.
- **Sincronização do Brain Map:** Ao adicionar ou modificar agentes, skills ou workflows, atualize imediatamente a entrada correspondente em `./brain-map/brain-data.js` para manter o mapa visual 3D 100% atualizado.

---

## 🏁 PROTOCOLO DE VALIDAÇÃO FINAL

- **Gatilho:** "final checks", "run tests" ou término de tarefas de implementação.
- **Comando Obrigatório:** Execute `python .agent/scripts/checklist.py .`
- **Critério de Sucesso:** Nenhuma entrega é considerada finalizada sem 100% de aprovação (Security, Lint, Schema, Tests, UX, SEO).
