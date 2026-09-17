# Ananke OS Architecture

> **Spec-Driven Autonomy // Zero Vibe Coding**  
> Comprehensive AI Agent Capability Operating System powered by Spec-Driven Development (SDD)

---

## 📋 Overview

**Ananke OS** is a deterministic cognitive operating system consisting of:

- **35 Specialist Agents** - Role-based AI personas
- **54 Skills** - Domain-specific knowledge modules
- **21 Workflows** - Slash command procedures

---

## 🏗️ Directory Structure

```plaintext
ananke-os/
├── .agent/                  # 35 Agents, 54 Skills, 21 Workflows, Rules & Master Scripts
├── brain-map/               # Interactive 3D Neural Constellation Map (WebGL)
├── data/                    # Ingestion, Templates & Automated Batch Reports
├── integrations/            # External APIs, Google Analytics, Meta Ads & MCP Connectors
└── .specify/                # Formal SDD Requirements Specifications (EARS)
```

---

## 🤖 Agents (35)

Specialist AI personas for different domains.

| Agent                    | Focus                      | Skills Used                                              |
| ------------------------ | -------------------------- | -------------------------------------------------------- |
| `orchestrator`           | Multi-agent coordination   | parallel-agents, behavioral-modes                        |
| `sdd-specialist`         | Spec-Driven Development    | spec-driven-development, clean-code, tdd-workflow        |
| `project-planner`        | Discovery, task planning   | brainstorming, plan-writing, architecture                |
| `integration-engineer`   | API connectors & MCP       | api-integration-patterns, api-patterns, mcp-builder, nodejs-best-practices, python-patterns, clean-code |
| `data-analyst`           | EDA, SQL, Spreadsheets     | clean-code, data-analysis, sql-analytics, spreadsheet-wrangling, data-storytelling, python-patterns |
| `document-analyst`       | PDF & Document Mining      | clean-code, pdf-document-processing, data-storytelling, python-patterns |
| `frontend-specialist`    | Web UI/UX                  | frontend-design, nextjs-react-expert, tailwind-patterns |
| `css-architect`          | Modern CSS, UI styling     | premium-css-patterns, frontend-design                    |
| `social-media-designer`  | Social media art & carousels| social-content-design, copywriting-frameworks, frontend-design |
| `video-script-architect` | Video scripts (Reels & YT) | video-scriptwriting-frameworks, copywriting-frameworks, clean-code |
| `marketing-analyst`      | Social media, ads analytics| social-media-analytics, python-patterns, frontend-design  |
| `meta-ads-specialist`    | Meta/Instagram Ads, ROAS   | social-media-analytics, copywriting-frameworks, clean-code |
| `google-analytics-specialist` | GA4, Conversions, Tracking | mcp-builder, python-patterns, clean-code             |
| `data-viz-architect`     | Data Viz & Dashboards      | data-visualization-patterns, data-storytelling           |
| `copywriter-ux`          | Copy & UX Writing          | copywriting-frameworks, ux-writing, brainstorming        |
| `backend-specialist`     | API, business logic        | api-patterns, nodejs-best-practices, database-design, rust-pro |
| `database-architect`     | Schema, SQL                | database-design                                          |
| `mobile-developer`       | iOS, Android, RN           | mobile-design                                            |
| `game-developer`         | Game logic, mechanics      | game-development                                         |
| `api-designer`           | API Architecture & Design  | api-patterns, clean-code, plan-writing                   |
| `devops-engineer`        | CI/CD, Docker              | deployment-procedures, server-management                 |
| `security-auditor`       | Security compliance        | vulnerability-scanner, red-team-tactics                  |
| `penetration-tester`     | Offensive security         | red-team-tactics                                         |
| `test-engineer`          | Testing strategies         | testing-patterns, tdd-workflow, webapp-testing           |
| `debugger`               | Root cause analysis        | systematic-debugging                                     |
| `performance-optimizer`  | Speed, Web Vitals          | performance-profiling                                    |
| `seo-specialist`         | Ranking, visibility        | seo-fundamentals, geo-fundamentals                       |
| `social-listening-analyst` | Social listening, semantic | semantic-social-listening, clean-code, python-patterns, data-storytelling |
| `documentation-writer`   | Manuals, docs              | documentation-templates                                  |
| `product-manager`        | Requirements, user stories | plan-writing, brainstorming                              |
| `product-owner`          | Strategy, backlog, MVP     | plan-writing, brainstorming                              |
| `qa-automation-engineer` | E2E testing, CI pipelines  | webapp-testing, testing-patterns                         |
| `code-archaeologist`     | Legacy code, refactoring   | clean-code, refactoring-patterns, code-review-checklist  |
| `explorer-agent`         | Codebase analysis          | clean-code, architecture, plan-writing, brainstorming, systematic-debugging |
| `business-strategist`    | Business strategy & pricing| brainstorming, pricing-strategy, plan-writing            |

---

## 🧩 Skills (54)

Modular knowledge domains that agents can load on-demand. based on task context.

### Frontend & UI

| Skill                   | Description                                                           |
| ----------------------- | --------------------------------------------------------------------- |
| `nextjs-react-expert`   | React & Next.js performance optimization                              |
| `web-design-guidelines` | Web UI audit - 100+ rules for accessibility, UX, performance (Vercel) |
| `tailwind-patterns`     | Tailwind CSS v4 utilities                                             |
| `frontend-design`       | UI/UX patterns, design systems                                        |
| `premium-css-patterns`  | Modern CSS, M3, Glassmorphism                                         |

### Backend & API

| Skill                   | Description                    |
| ----------------------- | ------------------------------ |
| `api-integration-patterns` | Conectores de APIs, MCP, resiliência e healthcheck |
| `api-patterns`          | REST, GraphQL, tRPC            |
| `nodejs-best-practices` | Node.js async, modules         |
| `python-patterns`       | Python standards, FastAPI      |
| `rust-pro`              | Rust best practices            |

### Database & SQL

| Skill             | Description                 |
| ----------------- | --------------------------- |
| `database-design` | Schema design, optimization |
| `sql-analytics`   | OLAP queries, Window Functions, CTEs, DuckDB |

### Data Analysis & Documents

| Skill                     | Description                                                           |
| ------------------------- | --------------------------------------------------------------------- |
| `data-analysis`           | EDA, estatística descritiva, detecção de outliers, métricas de negócio|
| `spreadsheet-wrangling`   | Profiling e normalização de planilhas CSV/XLSX/TSV com formatos BR    |
| `pdf-document-processing` | Extração de alta fidelidade de tabelas e textos em documentos PDF     |

### Cloud & Infrastructure

| Skill                   | Description               |
| ----------------------- | ------------------------- |
| `deployment-procedures` | CI/CD, deploy workflows   |
| `server-management`     | Infrastructure management |

### Testing & Quality

| Skill                   | Description              |
| ----------------------- | ------------------------ |
| `testing-patterns`      | Jest, Vitest, strategies |
| `webapp-testing`        | E2E, Playwright          |
| `tdd-workflow`          | Test-driven development  |
| `code-review-checklist` | Code review standards    |
| `lint-and-validate`     | Linting, validation      |

### Security

| Skill                   | Description              |
| ----------------------- | ------------------------ |
| `vulnerability-scanner` | Security auditing, OWASP |
| `red-team-tactics`      | Offensive security       |

### Architecture & Planning

| Skill           | Description                |
| --------------- | -------------------------- |
| `spec-driven-development` | Methodology & SDD phases   |
| `app-builder`   | Full-stack app scaffolding |
| `architecture`  | System design patterns     |
| `intelligent-routing` | Intelligent agent selection |
| `plan-writing`  | Task planning, breakdown   |
| `brainstorming` | Socratic questioning       |
| `pricing-strategy`| Pricing methods and bundles|

### Mobile

| Skill           | Description           |
| --------------- | --------------------- |
| `mobile-design` | Mobile UI/UX patterns |

### Game Development

| Skill              | Description           |
| ------------------ | --------------------- |
| `game-development` | Game logic, mechanics |

### Marketing, SEO & Growth

| Skill                    | Description                                              |
| ------------------------ | -------------------------------------------------------- |
| `social-content-design`  | Social media graphic design, carousels, prompt art       |
| `seo-fundamentals`       | SEO, E-E-A-T, Core Web Vitals                            |
| `geo-fundamentals`       | GenAI optimization                                       |
| `semantic-social-listening` | Semantic & sentiment analysis of social media text       |
| `social-media-analytics` | Social media results, xlsx parsing & MD3 dark dashboards |
| `data-visualization-patterns` | Gráficos (JS/Python), melhores práticas de data viz      |
| `data-storytelling`      | Redução de chartjunk, uso de cores e anotações           |
| `copywriting-frameworks` | Frameworks de persuasão (AIDA, PAS), gatilhos mentais    |
| `ux-writing`             | Diretrizes de escrita para interfaces claras             |
| `video-scriptwriting-frameworks` | Roteirização audiovisual, ganchos e teleprompter |

### Shell/CLI

| Skill                | Description               |
| -------------------- | ------------------------- |
| `bash-linux`         | Linux commands, scripting |
| `powershell-windows` | Windows PowerShell        |

### Other

| Skill                     | Description               |
| ------------------------- | ------------------------- |
| `clean-code`              | Coding standards (Global) |
| `behavioral-modes`        | Agent personas            |
| `parallel-agents`         | Multi-agent patterns      |
| `mcp-builder`             | Model Context Protocol    |
| `documentation-templates` | Doc formats               |
| `i18n-localization`       | Internationalization      |
| `performance-profiling`   | Web Vitals, optimization  |
| `systematic-debugging`    | Troubleshooting           |

---

## 🔄 Workflows (21)

Slash command procedures. Invoke with `/command`.

| Command          | Description              |
| ---------------- | ------------------------ |
| `/analyze`       | Data analytics & charts  |
| `/api-design`    | OpenAPI specifications   |
| `/batch`         | Batch processing & reports |
| `/brainstorm`    | Socratic discovery       |
| `/connect`       | API connectors & MCP     |
| `/copy`          | UX writing & persuasion  |
| `/create`        | Create new features      |
| `/debug`         | Debug issues             |
| `/deploy`        | Deploy application       |
| `/enhance`       | Improve existing code    |
| `/orchestrate`   | Multi-agent coordination |
| `/plan`          | Task breakdown           |
| `/post`          | Social posts & carousels |
| `/preview`       | Preview changes          |
| `/refactor`      | Clean code & tech debt   |
| `/script`        | Video scripts (Reels/YT) |
| `/sdd`           | Start Spec-Driven flow   |
| `/sql`           | DuckDB SQL queries       |
| `/status`        | Check project status     |
| `/strategy`      | Business model & pricing |
| `/test`          | Run tests                |

---

## 🎯 Skill Loading Protocol

```plaintext
User Request → Skill Description Match → Load SKILL.md
                                            ↓
                                    Read references/
                                            ↓
                                    Read scripts/
```

### Skill Structure

```plaintext
skill-name/
├── SKILL.md           # (Required) Metadata & instructions
├── scripts/           # (Optional) Python/Bash scripts
├── references/        # (Optional) Templates, docs
└── assets/            # (Optional) Images, logos
```

### Enhanced Skills (with scripts/references)

| Skill                     | Files | Coverage                            |
| ------------------------- | ----- | ----------------------------------- |
| `app-builder`             | 20    | Full-stack scaffolding              |
| `spreadsheet-wrangling`   | 2     | CSV/XLSX profiling & normalization  |
| `sql-analytics`           | 2     | DuckDB SQL query engine             |
| `pdf-document-processing` | 2     | PDF table & text extraction         |

---

## 📜 Scripts (5)

Master validation and management scripts that orchestrate skill-level scripts.

### Master Scripts

| Script                   | Purpose                                 | When to Use              |
| ------------------------ | --------------------------------------- | ------------------------ |
| `checklist.py`           | Priority-based validation (Core checks) | Development, pre-commit  |
| `verify_all.py`          | Comprehensive verification (All checks) | Pre-deployment, releases |
| `auto_preview.py`        | Dev server preview management           | Local UI/UX preview      |
| `session_manager.py`     | Agent session tracking and context      | Session management       |
| `automations/run_batch.py` | Periodic batch ingestion & reporting   | Periodic data pipelines  |

### Usage

```bash
# Quick validation during development
python .agent/scripts/checklist.py .

# Full verification before deployment
python .agent/scripts/verify_all.py . --url http://localhost:3000

# Periodic batch pipeline execution
python .agent/scripts/automations/run_batch.py
```

### What They Check

**checklist.py** (Core checks):

- Security (vulnerabilities, secrets)
- Code Quality (lint, types)
- Schema Validation
- Test Suite
- UX Audit
- SEO Check

**verify_all.py** (Full suite):

- Everything in checklist.py PLUS:
- Lighthouse (Core Web Vitals)
- Playwright E2E
- Bundle Analysis
- Mobile Audit
- i18n Check

For details, see [scripts/README.md](scripts/README.md)

---

## 📊 Statistics

| Metric              | Value                         |
| ------------------- | ----------------------------- |
| **Total Agents**    | 35                            |
| **Total Skills**    | 54                            |
| **Total Workflows** | 21                            |
| **Total Scripts**   | 5 (master) + 21 (skill-level) |
| **Coverage**        | ~90% web/mobile development   |

---

## 🔗 Quick Reference

| Need         | Agent                    | Skills                                |
| ------------ | ------------------------ | ------------------------------------- |
| Web App      | `frontend-specialist`    | nextjs-react-expert, frontend-design  |
| UI/CSS       | `css-architect`          | premium-css-patterns, frontend-design |
| Social Post  | `social-media-designer`  | social-content-design, copywriting-frameworks |
| Video Script | `video-script-architect` | video-scriptwriting-frameworks, copywriting-frameworks |
| API & MCP    | `integration-engineer`   | api-integration-patterns, mcp-builder |
| Backend      | `backend-specialist`     | api-patterns, nodejs-best-practices   |
| Analytics    | `marketing-analyst`      | social-media-analytics, python-patterns |
| Listening    | `social-listening-analyst` | semantic-social-listening, data-storytelling |
| Mobile       | `mobile-developer`       | mobile-design                         |
| Database     | `database-architect`     | database-design                       |
| Security     | `security-auditor`       | vulnerability-scanner                 |
| Testing      | `test-engineer`          | testing-patterns, webapp-testing      |
| Debug        | `debugger`               | systematic-debugging                  |
| Specify      | `sdd-specialist`         | spec-driven-development               |
| Plan         | `project-planner`        | brainstorming, plan-writing           |
