# Plano Técnico de Implementação: Edição Programática de Vídeo & Motion (HyperFrames)

> **Módulo:** Ananke OS Programmatic Video Suite  
> **Status:** Fase 2 - PLAN (Documentação de Arquitetura & Roadmap)  
> **Motor Principal:** [HyperFrames](https://hyperframes.dev) (HeyGen) · *Suporte legado/opcional: Remotion*  
> **Metodologia Base:** "Bolo de Camadas" (@cauhi) adaptado ao padrão Spec-Driven Autonomy  
> **Agente Responsável pelo Plano:** `project-planner` / `orchestrator`

---

## 1. Visão Geral & Justificativa Técnica

O objetivo deste subsistema é dotar o **Ananke OS** da capacidade de produzir, animar e renderizar vídeos verticais (Reels, TikToks e Shorts em 1080×1920) em nível de produção, transformando um vídeo bruto de fala (*talking head*) em um vídeo final de alta retenção através de **código declarativo**.

### Por que o HyperFrames é a escolha prioritária sobre o Remotion?
1. **Agent-Native por Design:** O HyperFrames foi concebido pela equipe da HeyGen especificamente para ser manipulado por coding agents (Claude Code, Antigravity, Gemini). Sua API e padrões de projeto minimizam atritos de contexto de LLMs.
2. **Pilha Web Pura (HTML5 + CSS3 + GSAP / WAAPI):**
   - Elimina a sobrecarga de bundlers pesados de React, hooks de ciclo de vida (`useCurrentFrame`) e re-renderizações desnecessárias.
   - LLMs produzem estruturas HTML semânticas e animações CSS/GSAP com previsibilidade superior e menor índice de alucinação sintática.
3. **Preview Ultrarrápido & Renderização Determinística:**
   - Live-reload local leve via navegador (`npx hyperframes preview`).
   - Compilação determinística quadro a quadro para MP4 utilizando Chromium headless e FFmpeg (`npx hyperframes render`).
4. **Alinhamento com o Ananke OS:** O Ananke OS já possui profundo domínio de frontend (`frontend-specialist`, `css-architect`, `premium-css-patterns`), o que torna a criação de layouts e microanimações em HTML/CSS uma extensão natural das capacidades já existentes.

---

## 2. Arquitetura da Solução: O Modelo das 5 Camadas

O pipeline transforma a gravação do operador em um "bolo" composto por 5 camadas empilhadas com precisão milimétrica:

```plaintext
                              [ /reel Workflow ]
                                       │
                          [ motion-video-engineer ]
                                       │
     ┌──────────────────┬──────────────┴───────────────┬──────────────────┐
     ▼                  ▼                              ▼                  ▼
[ Camada 1 & 2 ]   [ Camada 3 ]                  [ Camada 4 ]       [ Camada 5 ]
  Take Bruto &     Rosto em Card /              Motion Graphics      Zoom Dinâmico
Legenda Whisper     Máscara Dinâmica             Sincronizado       & Sound Design
 (Word-by-word)     (Troca a cada ~5s)         (Novo a cada 2-3s)   (Whoosh/Pop/Pits)
     │                  │                              │                  │
     └──────────────────┴──────────────┬───────────────┴──────────────────┘
                                       │
                                       ▼
                         [ HyperFrames Engine ]
                      (HTML5 + CSS + GSAP Timeline)
                                       │
                                       ▼
                       [ Safe Zones Audit (Instagram) ]
                     (Y: 250-800 Graphics | Y: 820-1300 Face)
                                       │
                                       ▼
                         [ FFmpeg / MP4 Renderer ]
```

### Detalhamento das 5 Camadas:
1. **Camada 1 — O Take (Base):** O arquivo de vídeo gravado pelo usuário (`take.mp4`), mantido sem compressão destrutiva ou cortes não autorizados.
2. **Camada 2 — A Legenda Dinâmica:** Transcrição temporalizada palavra por palavra via Whisper (`whisper.cpp` ou Python Whisper), exibindo de 1 a 3 palavras por vez com destaque de cor na palavra de ênfase.
3. **Camada 3 — O Rosto em Card / Máscara:** O take recortado em molduras estilizadas (card central, janela lateral, pílula flutuante, tela cheia) que alternam suavemente a cada mudança de assunto (~5 s).
4. **Camada 4 — Os Gráficos / Motion Graphics:** Visual que ilustra em tempo real o termo falado (entra ~4 quadros antes da palavra). GSAP Timelines desenhando gráficos, barras, números em contagem, fotos com efeito Ken Burns ou diagramas.
5. **Camada 5 — Zoom & Sound Design:** Escala de câmera (punch-in de 1.05x–1.15x) na ênfase da fala e sonoplastia sincronizada em cada movimento (*whoosh* nas transições, *pop/click* nas entradas, som de digitação em textos).

---

## 3. Safe Zones & Regras de Composição (1080×1920 @ 30/60 fps)

Para evitar que a interface das redes sociais cubra o conteúdo:
- **Gráficos & Ilustrações:** Y entre `250px` e `800px`.
- **Rosto / Card do Take:** Y entre `820px` e `1300px`.
- **Legenda:** Y entre `1360px` e `1480px`.
- **Área Proibida Inferior:** Abaixo de `Y = 1520px` (coberta por legendas do app, nome de usuário e áudio).
- **Margem Direita Reservada:** `~130px` da borda direita (botões de like, comentário, salvar e compartilhar).
- **Margens Laterais Seguras:** $\ge$ `90px`.
- **Gancho no Quadro 1:** O título de abertura deve estar 100% visível já no primeiro frame (serve como capa de feed).

---

## 4. Inventário de Arquivos e Componentes no Ananke OS

### 4.1 Novo Agente Especialista
* **`.agent/agents/motion-video-engineer.md`**:
  - Persona responsável pela direção de arte em movimento, cronometragem de cenas, animação declarativa e orquestração de renderização.
  - Sinergias: `video-script-architect` (fornece o roteiro), `copywriter-ux` (ajuste do gancho), `css-architect` (design tokens e efeitos visuais).

### 4.2 Novo Workflow de Comando
* **`.agent/workflows/reel.md`** (acionável via `/reel`):
  1. **Passo 1 (Ingestão & Setup):** Inicialização do projeto HyperFrames (`npx hyperframes init`), depósito do take em `public/take.mp4`.
  2. **Passo 2 (Extração de Referências):** Análise de ritmo e estilos de referências visuais via stills FFmpeg.
  3. **Passo 3 (Socratic Gate / Roteiro de Diretor):** Transcrição com timestamps, montagem da tabela de cenas (tempo, palavra, formato do rosto, gráficos) e **aprovação mandatória do usuário antes de codificar**.
  4. **Passo 4 (Codificação & Preview):** Construção das timelines GSAP/HTML, verificação em `npx hyperframes preview`.
  5. **Passo 5 (Validação de Safe Zones & Render):** Geração de stills dos momentos 0s, 5s e clímax; verificação no gabarito do Instagram; renderização do MP4 final (`npx hyperframes render`).

### 4.3 Nova Skill Modular & Motor de Primitivas
* **`.agent/skills/programmatic-video-editing/SKILL.md`**:
  - Manual de engenharia de vídeo declarativo para HyperFrames (e Remotion como alternativa).
  - **Identidade Baseada em `brand-guidelines.md`:** A fonte primária da verdade para paleta, Google Fonts, raios de borda e tom de voz é o arquivo `brand-guidelines.md` do projeto.
  - `novo-nicho.md`: Protocolo que lê `brand-guidelines.md`, extrai tokens e injeta diretamente no motor de primitivas.
  - **Motor de Primitivas Parametrizáveis (`primitives/`):**
    - `video-tokens.css`: Variáveis CSS dinâmicas (`--brand-*`), safe zones e iluminação volumétrica/ambient bloom.
    - `motion-curves.js`: Motor de física GSAP (curvas `back.out`, `expo.out`, `elastic.out`, contadores rolantes, traçado SVG e punch-in de câmera).
    - `templates/layer2-kinetic-caption.html`: Legenda cinética sincronizada palavra por palavra com realce elástico e glow na palavra ativa.
    - `templates/layer3-face-card.html`: Card do apresentador com borda translúcida, ambient glow e alternância suave de layout.
    - `templates/layer4-vector-graphics.html`: Primitivas vetoriais (curva de escala SVG animada, ticker de métrica e comparativo split-screen).
  - Exemplos e Prompts em `references/prompts.md`.

### 4.4 Scripts Python Utilitários
* **`.agent/skills/programmatic-video-editing/scripts/extract_stills.py`**:
  - Extrai frames de referência (`ffmpeg -i input.mp4 -vf fps=1 stills/%02d.jpg`) para inspeção de ritmo sem assistir o vídeo completo.
* **`.agent/skills/programmatic-video-editing/scripts/validate_safe_zones.py`**:
  - Valida se os seletores e coordenadas de elementos do template HTML respeitam os limites de segurança da UI do Instagram.
* **`.agent/skills/programmatic-video-editing/scripts/whisper_transcribe.py`**:
  - Utilitário local para extração do arquivo de áudio e geração de JSON com timestamps a nível de palavra.

---

## 5. Pré-requisitos & Dependências do Ambiente Windows

Para a execução sem atrito no ambiente local do usuário:
1. **Node.js 18+ & npm** (já ativo no workspace).
2. **HyperFrames CLI**: Instalável sob demanda via `npx hyperframes`.
3. **FFmpeg**: Necessário no PATH do Windows para manipulação de mídia e montagem final do vídeo.
4. **Whisper**: Ferramenta local (`whisper.cpp` ou módulo Python `openai-whisper` / API) para transcrição temporalizada.

---

## 6. Plano de Ação por Fases (SDD Lifecycle)

| Tarefa | Entregável | Agente Responsável | Critério de Aceite |
| :--- | :--- | :--- | :--- |
| **Fase 1** | Especificação Formal EARS (`.specify/programmatic-video-editing.md`) | `sdd-specialist` | Requisitos funcionais e não-funcionais validados |
| **Fase 2** | Agente `motion-video-engineer.md` | `project-planner` | Frontmatter, responsabilidades e sinergias integradas |
| **Fase 3** | Skill `programmatic-video-editing` + nichos e templates | `project-planner` / `css-architect` | Pasta completa com `SKILL.md`, `references/` e scripts |
| **Fase 4** | Workflow `/reel` | `orchestrator` | Fluxo guiado em 5 passos com Socratic Gate |
| **Fase 5** | Scripts utilitários (`extract_stills`, `validate_safe_zones`) | `integration-engineer` | Scripts testados via CLI |
| **Fase 6** | Atualização de `ARCHITECTURE.md` e `brain-data.js` | `orchestrator` | Grafo 3D sincronizado e métricas de sistema atualizadas |
| **Fase 7** | Quality Gate & Validação | `test-engineer` | `python .agent/scripts/checklist.py .` com 100% de aprovação |
