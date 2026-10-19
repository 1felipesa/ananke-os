# Síntese de Estilo de Vídeo a partir de `brand-guidelines.md`

> **Princípio de Ouro do Ananke OS:**  
> A identidade visual de qualquer vídeo deve ser derivada da **Fonte Primária da Verdade do Projeto**: o arquivo `brand-guidelines.md` (localizado em `./.specify/brand-guidelines.md`, `./brand-guidelines.md` ou caminho apontado pelo operador).

Este documento orienta o agente `motion-video-engineer` a inspecionar as diretrizes de marca do projeto e sintetizar automaticamente as especificações para as **5 camadas do vídeo**, sem fazer perguntas redundantes sobre dados já estabelecidos.

---

## 1. Protocolo de Leitura e Extração de Diretrizes

O agente DEVE ler `brand-guidelines.md` e mapear os seguintes tokens:

| Seção no `brand-guidelines.md` | O que extrair | Destino nas 5 Camadas de Vídeo |
| :--- | :--- | :--- |
| **Paleta de Cores (Hex/HSL)** | Cores primária, secundária, background, acento e destaque | Fundo, contornos de cards, cor de destaque da legenda (Camada 2), gráficos e barras (Camada 4) |
| **Tipografia & Fontes** | Famílias tipográficas (Google Fonts), pesos e letter-spacing | Títulos de gancho no Frame 0, legendas sincronizadas (Camada 2), dados e rótulos gráficos (Camada 4) |
| **Tom de Voz & Personalidade** | Adjetivos de marca (ex: técnico, sofisticado, dinâmico, acessível) | Ritmo de animação GSAP (easing suave vs. corte esportivo rápido) e estilo de sonoplastia |
| **Componentes Visuais** | Raio de borda (border-radius), sombras (box-shadow), glassmorphism | Formato do card do rosto (Camada 3), molduras de mídias e caixas de texto |
| **Metáforas e Elementos Gráficos** | Ícones, ilustrações, grids ou diagramas comuns da marca | Motion graphics ilustrativos sincronizados com a fala (Camada 4) |
| **Restrições Éticas / Marca** | Avisos legais, proibições de afirmações, selos obrigatórios | Rodapés de advertência ("Ilustrativo / Simulação"), posicionamento de logos |

---

## 2. Tradução Automática para as 5 Camadas de Vídeo (via `primitives/`)

A partir dos dados lidos em `brand-guidelines.md`, o agente NÃO inventa CSS do zero. Ele parametriza o arquivo `primitives/video-tokens.css` e seleciona as curvas em `primitives/motion-curves.js`:

1. **Camada 1 — O Take:** Mantém a imagem natural sem filtros destrutivos, posicionando-a dentro da moldura do card da Camada 3.
2. **Camada 2 — A Legenda (Kinetic Punch):**
   - Importa `primitives/templates/layer2-kinetic-caption.html`.
   - Aplica a fonte de texto (`--brand-font-body`) e cor de texto (`--brand-text`).
   - A palavra ativa no milissegundo de fala é grifada na **Cor de Acento** (`--brand-accent`) com escala elástica e emissão de brilho (*glow*).
3. **Camada 3 — O Rosto em Card (Volumetric Face Card):**
   - Importa `primitives/templates/layer3-face-card.html`.
   - Injeta `--brand-radius-lg` e a cor primária no gradiente do *ambient glow* traseiro (`.face-card-glow`).
   - Alternância fluida de layout (`.layout-center` $\rightarrow$ `.layout-side` $\rightarrow$ `.layout-pip` $\rightarrow$ `.layout-fullscreen`) via `morphFaceCard()`.
4. **Camada 4 — Os Gráficos (Vector & Metric Primitives):**
   - Importa `primitives/templates/layer4-vector-graphics.html`.
   - Utiliza as primitivas vetoriais: `.metric-card` (com contador GSAP via `animateCounter`), `.chart-card` (SVG animado via `drawSvgPath`) ou `.split-compare-container`.
   - É expressamente proibido o uso de caixas divs estáticas não estilizadas.
5. **Camada 5 — Zoom & Sound Design:**
   - Easing mapeado a partir do tom de voz:
     - Marcas enérgicas/vendas: `EASINGS.snappy` (`back.out(1.7)`) + punch-in de câmera (1.06x) via `punchInCamera()`.
     - Marcas corporativas/técnicas: `EASINGS.smooth` (`expo.out`) + punch-in sutil (1.03x).
   - Efeitos sonoros sincronizados no quadro exato de entrada (*whoosh* nas transições, *pop* nos badges, digitação nos textos).

---

## 3. Socratic Gate: Perguntas Residuais Exclusivas de Vídeo

Se o arquivo `brand-guidelines.md` já estiver preenchido, **NÃO pergunte cores nem fontes**. Pergunte apenas se houver dúvidas operacionais de audiovisual:

1. **Enquadramento do Rosto:** O apresentador prefere janela lateral fixa enquanto dados ocupam a tela, ou transição fluida entre card e tela cheia?
2. **Ritmo de Aparição:** Prefere uma nova animação/gráfico a cada 2 segundos (estilo alta retenção) ou apenas nos momentos-chave da fala?

---

## 4. Injeção Direta no `video-tokens.css` do Projeto

Após o parse, o agente inicializa o projeto HyperFrames e injeta os valores nas variáveis de `video-tokens.css`:

```css
:root {
  --brand-primary: [Hex do brand-guidelines];
  --brand-secondary: [Hex do brand-guidelines];
  --brand-accent: [Hex do brand-guidelines];
  --brand-bg: [Hex de fundo escuro do brand-guidelines];
  --brand-surface: rgba([RGB da superfície], 0.75);
  --brand-text: [Hex de texto principal];
  --brand-font-display: '[Nome da Fonte Display]', sans-serif;
  --brand-font-body: '[Nome da Fonte Body]', sans-serif;
  --brand-radius-lg: [Token de raio de borda, ex: 24px];
}
```
