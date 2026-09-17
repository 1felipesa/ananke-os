---
name: social-content-design
description: Graphic design for social media platforms (Instagram, LinkedIn, Twitter/X) and AI image generation. Specializes in single-screen posts, high-retention carousels, typographic visual hierarchy, brand consistency, color theory, and asset organization in project directories.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Social Content Design

Especialidade de engenharia visual, direção de arte e design gráfico para redes sociais (Instagram, LinkedIn, X/Twitter, Threads). Guia a concepção estética, a renderização de tipografia em imagens por IA e a organização de carrosséis e posts estáticos.

---

## 🎯 Princípios Centrais da Direção de Arte

1. **Parada de Scroll em 1.5 Segundos:** A imagem do Slide 1 (ou post único) deve ter **um ponto focal dominante**. Evite elementos dispersos competindo por atenção.
2. **Respeito Absoluto à Marca:** Consulte obrigatoriamente o arquivo [`brand-guidelines.md`](../../../.specify/brand-guidelines.md) na raiz do projeto para capturar a paleta de cores hexadecimais, estilo de fontes e regras de logotipo.
3. **Legibilidade Móvel First:** 85%+ do consumo é mobile. Textos devem ser curtos, grandes e com contraste extremo em relação ao fundo.
4. **Organização Padronizada:** Todos os posts gerados devem residir na pasta:
   ```text
   assets/posts/<ano-mes-slug>/
   ├── slide-01.png
   ├── slide-02.png
   ├── ...
   └── copy.md
   ```

---

## 📐 Proporções de Tela (Aspect Ratios)

| Plataforma / Formato | Proporção | Dimensões Ideais | Quando Usar |
| :--- | :---: | :---: | :--- |
| **Feed Instagram / LinkedIn (Recomendado)** | `4:5` | `1080 x 1350 px` | Posts de tela única e carrosséis com máxima retenção vertical |
| **Feed Quadrado Universal** | `1:1` | `1080 x 1080 px` | Padrão clássico de feed, catálogo e grids simétricos |
| **Stories / Reels / TikTok** | `9:16` | `1080 x 1920 px` | Vídeos verticais, telas cheias imersivas e fundos para Stories |
| **Banner / Landscape / Twitter** | `16:9` | `1920 x 1080 px` | Capas, cabeçalhos do YouTube, Twitter/X cards |

---

## 🔤 Engenharia de Prompts para Tipografia Integrada

Ao solicitar ao modelo de IA que renderize imagem com texto embutido:

* **Coloque o texto exato entre aspas:** Especifique explicitamente `with clear bold typography text "TITULO AQUI" prominently centered`.
* **Descreva o estilo da fonte:** `bold sans-serif modern geometric typography`, `crisp sharp letters`, `clean graphic design poster`.
* **Defina a hierarquia espacial:** `headline at the top third of the canvas, leaving ample breathing room and negative space`.
* **Contraste de Iluminação:** `deep dark background #0B0F19 with vibrant electric cyan #00E5FF illumination casting rim light onto 3D tech shapes`.
* **Evite Poluição:** Não peça mais de 10 a 15 palavras no mesmo prompt visual; textos longos devem ir na legenda do post em `copy.md`.

---

## 🔄 Continuidade em Carrosséis (Efeito Panorâmico)

Para carrosséis no formato `4:5`:
* **Conexão de Bordas:** Elementos visuais na borda direita do Slide $N$ (como um cabo de luz neon, um card translúcido ou uma linha geométrica) devem conectar-se à borda esquerda do Slide $N+1$.
* **Indicadores Visuais:** Sempre inclua uma pista sutil de arraste (ex: seta minimalista, número do slide `01/06` ou barra de progresso no rodapé).
* **Consulte:** [`references/carousel-frameworks.md`](references/carousel-frameworks.md) para roteiros validados de alta retenção.

---

## 🛠️ Automação com o Script Auxiliar

Use o script da skill para inicializar e auditar a pasta de um post:

```bash
# Criar pasta de carrossel de 5 slides com template de roteiro:
python .agent/skills/social-content-design/scripts/asset_organizer.py create 2026-09-sdd-tutorial --slides 5 --title "Como Usar SDD na Prática"

# Checar arquivos e imagens geradas na pasta:
python .agent/skills/social-content-design/scripts/asset_organizer.py status 2026-09-sdd-tutorial
```
