# Especificação Funcional: Edição Programática de Vídeo & Motion (HyperFrames)

> **Módulo:** Ananke OS Programmatic Video Suite  
> **Tagline:** Spec-Driven Video As Code // 5-Layer Reels Engine  
> **Metodologia:** Spec-Driven Development (SDD) com Sintaxe EARS  
> **Status:** Aprovado / Baseline Operacional (Fase 1 - SPECIFY)  
> **Motor Principal:** HyperFrames (HeyGen) · Suporte compatível: Remotion  
> **Classificação:** Módulo Especialista de Produção Multimídia (P1)

---

## 1. Visão Geral e Propósito

Este módulo estabelece o pipeline determinístico e automatizado do **Ananke OS** para transformar gravações brutas de fala (*talking heads*) em vídeos verticais (1080×1920 - 9:16) com alto nível de retenção, legenda sincronizada palavra por palavra, máscara dinâmica de rosto, ilustrações gráficas (*motion graphics*) em tempo real, zoom dinâmico e sonoplastia, utilizando **HyperFrames** (HTML5 + CSS3 + GSAP) como motor principal de renderização baseada em código.

---

## 2. Requisitos do Sistema (Sintaxe EARS)

### 2.1 Requisitos Onipresentes (Ubiquitous)
* **UBIQ-VID-01:** O sistema DEVE construir todo vídeo com base no modelo rigoroso das 5 camadas empilhadas:
  1. *O Take*: gravação da fala do criador;
  2. *A Legenda*: transcrição dinâmica sincronizada por palavra com kinetic punch;
  3. *O Rosto em Card*: janela/máscara geométrica com iluminação ambiente e transições suaves;
  4. *O Gráfico*: primitivas vetoriais (SVG, tickers, métricas) ilustrando o conceito a cada 2–3 s;
  5. *Zoom e Som*: escala de ênfase (punch-in) e sonoplastia pontual (*whoosh*, *pop*, digitação).
* **UBIQ-VID-02:** O sistema DEVE adotar master vertical 1080×1920 @ 30 ou 60 fps e respeitar as áreas seguras (*safe zones*) da interface mobile (Instagram Reels / TikTok / Shorts), mantendo gráficos entre Y=250–800, rosto entre Y=820–1300, legendas entre Y=1360–1480 e proibindo elementos críticos abaixo de Y=1520 ou na margem direita de 130px.
* **UBIQ-VID-03:** O sistema DEVE utilizar o primeiro quadro (frame 0) como capa de feed, garantindo que o título do gancho esteja 100% visível e legível imediatamente.
* **UBIQ-VID-04:** O sistema DEVE estruturar o código visual do HyperFrames em torno de um **Design System Paramétrico de Vídeo** (`video-tokens.css`), injetando os tokens de `brand-guidelines.md` em variáveis CSS padronizadas (`--brand-primary`, `--brand-accent`, `--brand-surface`, `--brand-font-display`, `--brand-radius`) e aplicando iluminação volumétrica, bordas translúcidas de 1px e sombreamento multicamada em todos os cards.
* **UBIQ-VID-05:** O sistema DEVE empregar um **Motor de Física GSAP** (`motion-curves.js`), aplicando curvas de aceleração com inércia (`back.out(1.7)`, `expo.out`, `power4.out`) e revelações em cascata (*stagger* de 0.04s a 0.08s) em todas as transições de elementos, sendo expressamente proibido o uso de interpolações lineares ou padrões sem peso.
* **UBIQ-VID-06:** O sistema DEVE construir os elementos visuais da Camada 4 exclusivamente a partir de **Primitivas Abstratas Vetoriais** (traçado animado de SVG via `stroke-dashoffset`, contadores numéricos com interpolação de dígitos GSAP, painéis em glassmorphism e badges de status), sendo proibido o uso de divs quadradas simples ou caixas de texto com cores sólidas não estilizadas.
* **UBIQ-VID-07:** O sistema DEVE renderizar as legendas da Camada 2 utilizando um **Kinetic Typography Engine**, limitando a exibição a no máximo 1–3 palavras por bloco de tempo, com realce elástico (`scale(1.15)`) e emissão de brilho na cor de acento da marca para a palavra ativa no milissegundo de fala.

### 2.2 Requisitos Disparados por Eventos (Event-Driven)
* **EVT-VID-01:** QUANDO o operador acionar o comando `/reel` ou invocar o agente `motion-video-engineer`, o sistema DEVE iniciar o workflow em 5 passos para montagem declarativa do projeto.
* **EVT-VID-02:** QUANDO vídeos de referência forem fornecidos em `refs/`, o sistema DEVE extrair quadros estáticos (`stills`) via FFmpeg em vez de consumir buffers de vídeo inteiros, avaliando ritmo, paleta e transições sem copiar marcas registradas de terceiros.
* **EVT-VID-03:** QUANDO a transcrição temporalizada for gerada, o sistema DEVE apresentar a **Tabela de Cenas / Roteiro de Diretor** e EXIGIR a aprovação explícita do operador no Socratic Gate antes de escrever qualquer linha de código de animação.
* **EVT-VID-04:** QUANDO a animação for finalizada, o sistema DEVE gerar quadros de prova (*stills*) dos instantes 0s, 5s e clímax para auditoria de enquadramento antes de iniciar a renderização completa do MP4.
* **EVT-VID-05:** QUANDO o utilitário `google_flow_bridge.py` for executado com a flag `--login`, o sistema DEVE abrir uma instância interativa do navegador para autenticação do operador na conta Google Pro e persistência dos cookies e tokens de sessão em `~/.ananke/google-flow-session/`.
* **EVT-VID-06:** QUANDO o utilitário `google_flow_bridge.py` for acionado com um prompt de cena, o sistema DEVE navegar até `flow.google.com`, submeter a instrução de vídeo, aguardar a conclusão da geração e baixar o arquivo MP4 diretamente para o caminho de destino especificado no projeto ativo.

### 2.3 Requisitos Baseados em Estado (State-Driven)
* **STA-VID-01:** O sistema DEVE ler e extrair os tokens visuais e de identidade (paleta de cores, tipografia Google Fonts, raios de borda, sombras e tom de voz) diretamente do arquivo `brand-guidelines.md` do projeto (`./.specify/brand-guidelines.md` ou raiz) através do protocolo `novo-nicho.md`, parametrizando as variáveis de `video-tokens.css` e selecionando o perfil de curvas de `motion-curves.js` correspondente ao tom de voz da marca.
* **STA-VID-02:** ENQUANTO a renderização local estiver sendo executada, o sistema DEVE orquestrar o processo via subprocesso assíncrono não bloqueante (`hyperframes render` ou script FFmpeg).

### 2.4 Requisitos Opcionais (Optional)
* **OPT-VID-01:** ONDE a ferramenta `whisper.cpp` ou Python Whisper estiver disponível localmente, o sistema DEVE realizar a transcrição com marcas de tempo em nível de palavra localmente sem envio de áudio a APIs terceiras.
* **OPT-VID-02:** ONDE o operador preferir o ecossistema React, o sistema DEVE manter interoperabilidade e suporte a templates Remotion (`npx remotion render`).
* **OPT-VID-03:** ONDE o operador desejar gerar B-Rolls cinematográficos utilizando sua conta Google Pro no `flow.google.com`, o sistema DEVE fornecer o utilitário `google_flow_bridge.py`, armazenando a sessão de autenticação em diretório global (`~/.ananke/google-flow-session/`) e salvando os vídeos gerados no diretório do projeto ativo.

### 2.5 Requisitos de Tratamento de Exceções e Indesejados (Unwanted)
* **UNW-VID-01:** O sistema NUNCA DEVE inventar métricas, preços, depoimentos falsos ou simular telas sem adicionar a etiqueta de advertência "Ilustrativo / Simulação".
* **UNW-VID-02:** O sistema NUNCA DEVE posicionar legendas ou rostos sob as áreas cegas de navegação da interface do Instagram ou TikTok.
* **UNW-VID-03:** O sistema NUNCA DEVE renderizar elementos gráficos com interpolações lineares sem inércia ou utilizar layouts de páginas web comuns desprovidos de tratamento de profundidade e safe zones.
