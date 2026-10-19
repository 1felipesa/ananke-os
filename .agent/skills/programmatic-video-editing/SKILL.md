---
name: programmatic-video-editing
description: Engenharia e direção de edição de vídeo vertical (1080×1920) em 5 camadas (take, legenda temporalizada por palavra, máscara dinâmica de rosto, motion graphics a cada 2-3s, zoom e sound design) usando HyperFrames (HTML/CSS/GSAP) e Remotion. Contém motor de primitivas (video-tokens.css, motion-curves.js, templates SVG), cálculo de safe zones do Instagram e scripts de extração de stills.
---

# Programmatic Video Editing (Edição Programática de Vídeo & Motion)

> **Metodologia:** Bolo de 5 Camadas (Take, Legenda Kinetic, Rosto em Card, Gráficos Vetoriais, Zoom & Som)  
> **Motores Suportados:** HyperFrames (Prioritário - HTML5/CSS/GSAP) e Remotion (React)  
> **Guarda de Qualidade:** É expressamente proibido o "Vibe Coding" de divs simples ou animações lineares. Todo projeto deve importar e parametrizar o motor de primitivas em `primitives/`.

---

## 1. As 5 Camadas do Bolo

1. **Camada 1 — O Take (Base):** O vídeo bruto do apresentador falando para a câmera em `public/take.mp4`.
2. **Camada 2 — A Legenda (Kinetic Punch):** Baseada em `primitives/templates/layer2-kinetic-caption.html`. Transcrição temporalizada via Whisper, 1 a 3 palavras por vez, destacando a palavra falada ativa na cor de acento com escala elástica e glow (`kineticWordPunch()`).
3. **Camada 3 — O Rosto em Card (Volumetric Face Card):** Baseada em `primitives/templates/layer3-face-card.html`. O take é cortado dentro de uma moldura de vidro com iluminação ambiente traseira (*ambient glow*), badge de contexto e transição suave de geometria a cada virada de assunto (`morphFaceCard()`).
4. **Camada 4 — O Gráfico (Vector & Metric Primitives):** Baseada em `primitives/templates/layer4-vector-graphics.html`. Elementos vetoriais SVG desenhados a traço (`drawSvgPath()`), contadores numéricos com rolagem de dígitos (`animateCounter()`) ou comparativos split-screen.
5. **Camada 5 — Zoom e Som:** Zoom sutil na câmera via `punchInCamera()` (1.04x a 1.08x) em ênfases da fala e sonoplastia sincronizada milissegundo a milissegundo (*whoosh*, *pop*, digitação).

---

## 2. Safe Zones & Grade Visual (1080×1920)

Para garantir que o vídeo funcione perfeitamente no feed e no player de Reels/TikTok:
- **Gráficos e Ilustrações:** `Y = 240px` a `Y = 820px` (`--safe-graphics-top` / `--safe-graphics-bottom`)
- **Rosto / Card do Apresentador:** `Y = 840px` a `Y = 1320px` (`--safe-face-top` / `--safe-face-bottom`)
- **Legenda Dinâmica:** `Y = 1360px` a `Y = 1480px` (`--safe-caption-top` / `--safe-caption-bottom`)
- **Área Bloqueada (Interface de App):** `Y >= 1520px` (onde ficam username, áudio e descrição)
- **Margem Lateral Direita Reservada:** `140px` livres (botões de like, comentários e compartilhamento)
- **Margens Laterais Seguras:** No mínimo `90px` em ambos os lados
- **Capa no Frame 0:** O primeiro frame do vídeo já exibe o gancho principal completo.

---

## 3. Identidade Visual Parametrizada por `brand-guidelines.md`

O Ananke OS adota o **`brand-guidelines.md`** do projeto como **Fonte Primária da Verdade**, injetando os tokens diretamente no motor de primitivas:

1. **Leitura Automática de Diretrizes:** O agente lê `brand-guidelines.md` e extrai tokens (paleta de cores, tipografia Google Fonts, raios de borda, sombras, tom de voz) conforme documentado em [`novo-nicho.md`](references/nichos/novo-nicho.md).
2. **Injeção em `video-tokens.css`:** As cores e fontes são inseridas nas variáveis CSS do projeto gerado, herdando automaticamente a profundidade e iluminação profissional.
3. **Seleção de Física em `motion-curves.js`:** O tom de voz determina se as animações usam `EASINGS.snappy` (`back.out(1.7)` com overshoot para tons dinâmicos/vendas) ou `EASINGS.smooth` (`expo.out` para tons técnicos/corporativos).

---

## 4. O Pipeline de Execução com HyperFrames

1. **Scaffold do Projeto:**
   ```bash
   npx hyperframes init meu-reel --resolution portrait
   cd meu-reel
   ```
2. **Cópia do Motor de Primitivas:**
   Copia `primitives/video-tokens.css`, `primitives/motion-curves.js` e os templates HTML necessários para a pasta do projeto.
3. **Ingestão do Take & Diretrizes:**
   - Take bruto em `public/take.mp4`.
   - Injeta os tokens do `brand-guidelines.md` nas variáveis de `video-tokens.css`.
4. **Extração de Referências (Opcional):**
   ```bash
   python .agent/skills/programmatic-video-editing/scripts/extract_stills.py refs/ref-1.mp4 stills/
   ```
5. **Geração de B-Rolls no Google Flow (Opcional):**
   ```bash
   python .agent/skills/programmatic-video-editing/scripts/google_flow_bridge.py --prompt "Descrição cinematográfica da cena..." --output ./assets/reels/b-rolls/cena1.mp4
   ```
6. **Roteiro de Diretor (Tabela de Cenas):**
   Gera a tabela cena a cena com timing, palavras, transição de rosto e gráficos, e obtém a aprovação do operador no Socratic Gate.
6. **Codificação Declarativa sobre as Primitivas:**
   Monta a timeline GSAP importando os helpers de `motion-curves.js`.
7. **Pré-visualização Local:**
   ```bash
   npx hyperframes preview
   ```
8. **Auditoria de Safe Zones & Render Final:**
   ```bash
   python .agent/skills/programmatic-video-editing/scripts/validate_safe_zones.py
   npx hyperframes render --output dist/reel.mp4
   ```

---

## 5. Diretrizes de Áudio & Sound Design

- **Voz do Take:** Nivelada em torno de `-20 LUFS`.
- **Efeitos Sonoros (SFX):** De `3 a 6 LU` abaixo da voz.
- **Música de Fundo:** Opcional (apenas se solicitada), mixada a `-15 LU` abaixo da voz principal.
- **Fontes de Áudio:** Somente bibliotecas com licença livre (Mixkit, Freesound CC0).

