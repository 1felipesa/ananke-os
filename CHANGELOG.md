# 📜 Changelog — Ananke OS

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.  
O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## [2.4.0] - 2026-10-19

### 🚀 Novas Funcionalidades (Added)
* **HyperFrames Parametric Motion Engine (`/reel`):**
  * Motor de edição programática vertical (1080×1920) em 5 camadas:
    1. *O Take*: vídeo bruto de fala;
    2. *A Legenda*: kinetic typography com sincronização por palavra e emissão de brilho na cor de acento;
    3. *O Rosto em Card*: máscara geométrica e card com iluminação ambiente e ambient bloom;
    4. *O Gráfico*: primitivas visuais paramétricas a cada 2-3s (contadores GSAP, gráficos SVG via `stroke-dashoffset`, glassmorphism);
    5. *Zoom e Som*: punch-in de câmera e sonoplastia pontual.
  * Módulo de curvas físicas de animação com inércia real (`motion-curves.js` usando `back.out(1.7)`, `expo.out`, `drawSvgPath`, `animateCounter`, `punchInCamera`).
  * Design tokens padronizados (`video-tokens.css`) integrados com o leitor dinâmico de marcas (`novo-nicho.md` / `brand-guidelines.md`).
  * Cálculo e auditoria de áreas seguras (*safe zones*) para Instagram Reels, TikTok e YouTube Shorts (`validate_safe_zones.py`).
  * Novo especialista: `@motion-video-engineer`.
  * Nova skill: `programmatic-video-editing`.
* **Google Flow Bridge (`flow.google.com`):**
  * Conector autônomo via Playwright (`google_flow_bridge.py`) integrado ao fluxo de trabalho do Ananke OS.
  * Autenticação global de sessão única persistida em `~/.ananke/google_flow_profile/`, permitindo o uso direto dos créditos da conta Google Pro do operador em qualquer projeto.
  * Capacidade de listar projetos remotos no Google Flow, baixar assets de vídeo e submeter prompts de cena para geração determinística de B-rolls cinematográficos (Veo e Imagen).
* **NotebookLM Thought Leadership Suite (`/blog`):**
  * Suíte especialista em redação de artigos de blog analíticos e liderança de pensamento (*Thought Leadership*).
  * Ancoragem factual estrita em fontes e cadernos do Google NotebookLM via conector MCP nativo, eliminando alucinações de dados e citações inexistentes.
  * Protocolo de co-construção socrática em 4 blocos iterativos (Tese, Antítese, Síntese e Aplicação prática).
  * Trava rigorosa anti-clichê (*Zero AI Fluff*) e otimização semântica para motores de busca e motores de resposta de IA (SEO & GEO).
  * Novo especialista: `@blog-content-specialist`.
  * Novas skills: `thought-leadership-writing`, `notebooklm-knowledge-retrieval`, `seo-blog-architecture`.
* **E-mail Marketing & Outbound Leads Suite (`/email`):**
  * Arquitetura completa de réguas de automação de ciclo de vida (onboarding, nutrição, recuperação de carrinho, reengajamento).
  * Engenharia de cadências de prospecção fria B2B (Cold Outreach) com limitação estrita de extensão (50–125 palavras) e CTAs de baixa fricção.
  * Auditoria técnica de entregabilidade DNS (SPF, DKIM, DMARC, BIMI) e cálculo preditivo de pontuação anti-spam.
  * Diagramação de templates de e-mail em HTML tabular responsivo (`inline_styler.py`) com inlining automático de CSS e espelho em texto simples (*Plain Text mirror*).
  * Ferramenta de raspagem ética de contatos corporativos em páginas web institucionais com validação regex e exportação CSV (`lead_scraper.py`).
  * Novo especialista: `@email-marketing-specialist`.
  * Novas skills: `email-marketing-strategy`, `cold-email-outreach`, `email-template-design`, `lead-scraping-enrichment`.
* **Especificações Formais EARS (`.specify/`):**
  * Adicionados contratos funcionais formais: `.specify/programmatic-video-editing.md`, `.specify/email-marketing-system.md` e `.specify/thought-leadership-system.md`.

### 🔄 Modificações & Aprimoramentos (Changed)
* **3D Brain Map (`brain-map/brain-data.js`):**
  * Topologia neural WebGL atualizada para **38 Agentes Especialistas**, **62 Skills de Engenharia**, **24 Workflows de Comando** e **8 Macro-Núcleos**.
* **Arquitetura & Taxonomia:**
  * Atualizados `.agent/ARCHITECTURE.md` e `.agent/docs/categorias.md` com as 24 macro-categorias de serviço e tabela de consulta rápida expandida.
* **Master Checklist:**
  * Validação 100% aprovada (6/6 gates) incluindo Security, Lint, Schema, Tests, UX Audit e SEO Check.

---

## [2.0.0] - 2026-10-15

### 🚀 Lançamento Inicial (Initial Release)
* **Spec-Driven Autonomy (SDD):**
  * Governança em 4 fases sequenciais (`SPECIFY` → `PLAN` → `TASKS` → `IMPLEMENT`).
  * Socratic Gate mandatório (Tier 0 - Interrompa e Pergunte).
* **Panteão de 35 Agentes Especialistas:**
  * Divisão em 8 grandes centros de competência: Governança, Frontend, Backend/MCP, Dados/BI, Marketing/Mídia, Segurança/Infra, Qualidade/Testes e Estratégia de Negócio.
* **Suíte de 54 Skills de Domínio e 21 Workflows de Comando:**
  * Incluindo `/sdd`, `/create`, `/plan`, `/orchestrate`, `/connect`, `/script`, `/post`, `/batch`, `/analyze`, `/debug`, `/test`, `/deploy`.
* **Visualizador 3D Brain Map:**
  * Gêmeo digital em WebGL Three.js com navegação 360°, física orgânica de forças, filtros de busca e painel lateral de inspeção.
* **Master Checklist de Qualidade:**
  * Script automatizado `python .agent/scripts/checklist.py .` com 6 portões de qualidade inegociáveis.
