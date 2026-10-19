---
name: seo-blog-architecture
description: Arquitetura da informação, hierarquia semântica H1-H4, pesquisa de Search Intent, clusterização de palavras-chave LSI, meta tags e otimização para Featured Snippets em artigos de blog.
---

# SEO Blog Architecture & Semantic Information Design

Esta skill estabelece os princípios de **arquitetura de conteúdo, engenharia semântica e SEO On-Page** para artigos de blog no ecossistema Ananke OS. O foco é garantir máxima relevância orgânica e legibilidade humana superior.

---

## 🧭 1. Determinação de Search Intent (Intenção de Busca)

Antes de traçar qualquer outline, o agente deve classificar o tema em um dos 4 vetores de intenção:

1. **Informacional Profundo:** O leitor busca dominar um conceito ou resolver um gargalo técnico complexo.
   * *Estrutura ideal:* Guia definitivo, desmistificação de conceitos, diagramas explicativos.
2. **Comparativo / Avaliativo:** O leitor quer comparar abordagens, ferramentas ou metodologias.
   * *Estrutura ideal:* Tabelas comparativas de prós/contras, matrizes de decisão, benchmarks.
3. **Estratégico / Thought Leadership:** O leitor quer perspectivas de líderes sobre o futuro de um setor.
   * *Estrutura ideal:* Ensaio crítico, antecipação de tendências, teses contra-intuitivas baseadas em dados.
4. **Acionável / How-to:** O leitor precisa de um passo a passo reproduzível.
   * *Estrutura ideal:* Listas ordenadas, blocos de código com destaque e checklists.

---

## 📐 2. Hierarquia Semântica e Escaneabilidade

### Regras de Cabeçalhos (H1 a H4)
* **H1 (Único por Artigo):** Título principal magnético e descritivo. Deve incluir a palavra-chave primária de forma fluida.
* **H2 (Grandes Módulos de Tese):** Blocos temáticos macro (geralmente entre 3 e 6 por artigo). Devem responder a dúvidas reais do usuário.
* **H3 (Subtópicos e Desdobramentos):** Detalhamento conceitual, exemplos práticos ou passos técnicos dentro de um H2.
* **H4 (Micro-elementos):** Uso pontual para notas de rodapé, parâmetros técnicos ou subseções de código.

### Padrão de Escaneabilidade Visual
* **Parágrafos Curtos:** Máximo de 3 a 4 frases por parágrafo (evitar "paredes de texto").
* **Uso de Destaques:** Negrito estratégico (`**termo**`) nas primeiras 3 palavras de ideias centrais.
* **Tabelas Comparativas:** Obrigatórias sempre que houver comparação entre 2 ou mais entidades.
* **Alertas e Callouts:** Blocos de nota (`> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`) para destacar insights do NotebookLM.

---

## 🎯 3. Engenharia de Metadados e Snippets

### Regras de Ouro de Metadados:
1. **Title Tag (SEO Title):**
   * Limite estrito: 50 a 60 caracteres.
   * Palavra-chave primária posicionada preferencialmente no primeiro terço.
   * Fórmula recomendada: `[Palavra-Chave Primária]: [Benefício / Tese / Ano] | [Marca]`
2. **Meta Description:**
   * Limite estrito: 135 a 155 caracteres.
   * Contém a palavra-chave primária + verbo de ação + promessa de valor clara.
3. **URL Slug:**
   * Curto, amigável, minúsculo, separado por hífens, sem stopwords (`de`, `para`, `com`, `o`, `a`).
   * Exemplo: `inteligencia-artificial-exocortex` em vez de `o-guia-sobre-a-inteligencia-artificial-para-o-exocortex`.

### Otimização para Featured Snippets (Posição Zero)
* **Parágrafo Definição:** Um bloco de 40 a 55 palavras imediatamente após o H2 correspondente, definindo o conceito de forma direta ("O que é X?", "Como funciona Y?").
* **Listas Ordenadas:** Listas numeradas para etapas cronológicas.
* **Tabelas Sintéticas:** Tabelas com pelo menos 3 colunas para dados comparativos.

---

## 🏗️ 4. Formato do Outline no Checkpoint 2

No **Checkpoint 2**, o agente entrega a arquitetura de informação detalhada antes de escrever o corpo:

```markdown
### 📐 Proposta de Outline Semântico (Checkpoint 2)

* **Palavra-Chave Primária:** `[termo central]`
* **Palavras-Chave Secundárias (LSI):** `[termo 1, termo 2, termo 3]`
* **Intenção de Busca:** `[Informacional / Estratégico / Comparativo]`
* **Slug Previsto:** `[slug-amigavel]`

#### Estrutura de Seções & Mapeamento de Fontes:
1. **H1: [Título Proposto]**
   * *Hook:* [Ângulo de abertura e tensão narrativa]
2. **H2: [Contexto / Ponto de Ruptura]**
   * *Tese:* [Resumo do argumento]
   * *Fonte NotebookLM:* [Documento/Nota referenciada]
3. **H2: [Análise Profunda & Estudo de Caso]**
   * *H3: [Detalhamento A]*
   * *H3: [Detalhamento B]*
   * *Fonte NotebookLM:* [Dados estatísticos indexados]
4. **H2: [Conclusão e Implicações Futuras]**
   * *Takeaways acionáveis*
```
