---
name: reel
description: Fluxo especialista em edição programática de vídeo em 5 camadas (take, legenda temporalizada, máscara dinâmica de rosto, motion graphics GSAP, zoom e som) usando HyperFrames e Remotion.
agent: motion-video-engineer
---

# 🎂 Edição Programática de Vídeos (Reel Workflow)

O comando `/reel` é a porta de entrada para a montagem e renderização programática de vídeos verticais (1080×1920) em **5 camadas**. Ele transforma uma gravação bruta de fala (*talking head*) num produto final dinâmico através de código declarativo em **HyperFrames** (HTML5 + CSS + GSAP) ou **Remotion**.

---

## Como Usar

Digite `/reel` indicando o arquivo do seu take. O estilo visual será inferido automaticamente do `brand-guidelines.md` do seu projeto.

**Exemplos:**
- `/reel take=public/take.mp4` (utiliza tokens e identidade de `brand-guidelines.md`)
- `/reel take=public/take.mp4 brand=docs/cliente-a-guidelines.md`
- `/reel take=public/take.mp4 archetype=financas refs=refs/` (combina arquétipo com brand guidelines)

---

## O Que Acontece por Baixo dos Panos? (5 Passos)

1. **Ativação:** O agente especialista `motion-video-engineer` assume a regência e carrega a skill `programmatic-video-editing`.
2. **Ingestão, Setup & Leitura de Marca:**
   - Cria o scaffold do projeto HyperFrames (`npx hyperframes init meu-reel --resolution portrait`).
   - Copia o motor de primitivas (`primitives/video-tokens.css`, `primitives/motion-curves.js` e templates da pasta `primitives/templates/`).
   - Localiza e lê o arquivo `brand-guidelines.md` (`./.specify/brand-guidelines.md` ou raiz) e injeta os tokens nas variáveis CSS de `video-tokens.css`.
   - Caso haja referências em `refs/`, extrai stills via script FFmpeg para mapear estilo e timing.
3. **Socratic Gate & Roteiro de Diretor (Aprovação Prévia Obrigatória):**
   - Transcreve o áudio gerando marcas de tempo a nível de palavra (Whisper).
   - Monta a **Tabela de Cenas** aplicando os tokens do `brand-guidelines.md`:
     - Segundo a segundo
     - Palavras faladas
     - Geometria do rosto na tela (card central, pílula, lateral, tela cheia)
     - Primitivas visuais da Camada 4 (tickers numéricos, curvas SVG, comparativos)
     - Efeitos sonoros e zooms de ênfase
   - **Interrompe o fluxo para aprovação explícita do operador.**
4. **Codificação Declarativa sobre as Primitivas (Zero Vibe Coding):**
   - Utiliza `layer2-kinetic-caption.html` para legendas sincronizadas com escala elástica e glow na palavra ativa.
   - Utiliza `layer3-face-card.html` para enquadramento do rosto com iluminação volumétrica (*ambient bloom* e borda translúcida).
   - Utiliza `layer4-vector-graphics.html` para construir gráficos vetoriais com traçado SVG dinâmico e contadores GSAP, sendo proibido o uso de caixas divs estáticas simples.
   - Aplica as curvas de física de `motion-curves.js` (`EASINGS.snappy` para marcas enérgicas ou `EASINGS.smooth` para corporativas).
   - Permite preview interativo em tempo real via `npx hyperframes preview`.
5. **Auditoria de Safe Zones & Renderização Final:**
   - Executa o script de validação de safe zones (`validate_safe_zones.py`) garantindo conformidade com Instagram, TikTok e Shorts.
   - Gera quadros de prova (*stills*) nos marcos de tempo essenciais (0s, 5s e clímax).
   - Renderiza o arquivo MP4 final (`npx hyperframes render`).
