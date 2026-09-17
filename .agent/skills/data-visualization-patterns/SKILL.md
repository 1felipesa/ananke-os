---
name: data-visualization-patterns
description: Catálogo de boas práticas, seleção do tipo de gráfico e configurações de bibliotecas de Data Viz (Plotly, D3, Chart.js, Recharts, Seaborn, Matplotlib).
---

# Padrões de Visualização de Dados

Esta skill orienta a construção mecânica e teórica da visualização. Qual gráfico escolher e como implementá-lo nas principais bibliotecas.

## 📊 1. Seleção do Tipo de Gráfico

### Comparação (Ranking & Grandezas)
* **Recomendado:** Gráfico de Barras Horizontais (melhor para nomes de categorias longos) ou Verticais.
* **Anti-Padrão:** Gráfico de Radar ou Gráfico de Pizza (difíceis de comparar áreas e ângulos).

### Tendência (Evolução no Tempo)
* **Recomendado:** Gráfico de Linhas (para métricas contínuas) ou Gráfico de Áreas (quando houver volume a destacar).
* **Regra:** O eixo X deve SEMPRE ser o tempo, indo do passado (esquerda) para o futuro (direita).

### Correlação (Relação entre Duas Variáveis)
* **Recomendado:** Gráfico de Dispersão (Scatter Plot).
* **Alternativa:** Heatmap (quando houverem dados muito concentrados e densos).

### Distribuição
* **Recomendado:** Histograma ou Boxplot.

### Composição (Partes de um Todo)
* **Recomendado:** Gráfico de Barras Empilhadas ou Waffle Chart.
* **Tolerado:** Gráfico de Rosca (Donut), **APENAS** se houver no máximo 3 ou 4 fatias e se for colocar a métrica total no centro.

---

## 🛠️ 2. Ecossistema e Bibliotecas Recomendadas

Você pode e deve escolher a biblioteca mais adequada para a *stack* do usuário:

### Para Ecossistema Web (JavaScript / TypeScript)
1. **Recharts / ECharts:** Excelentes para dashboards React modernos. Interatividade rápida.
2. **Chart.js:** Mais fácil para HTML plano ou projetos Vanilla JS simples.
3. **D3.js:** Use **apenas** quando for necessária uma visualização 100% customizada e fora do padrão (ex: grafos de rede complexos), pois tem uma curva de aprendizado e código verboso.

### Para Ecossistema de Análise / Data Science (Python)
1. **Plotly:** A melhor opção para relatórios interativos e Dashboards (via Dash ou exportação HTML).
2. **Seaborn:** Ótima sintaxe reduzida para estatísticas complexas e visualizações estáticas elegantes.
3. **Matplotlib:** A base. Use quando houver restrições de ambiente ou necessidade de controle absoluto sobre cada pixel da imagem gerada.

---

## 🎛️ 3. Configurações e Boas Práticas Comuns a Todas as Libs

* **Eixo Y:** Em gráficos de barras, o Eixo Y **DEVE sempre** começar no 0. Truncar eixos gera desinformação visual (exagerando diferenças minúsculas). Em gráficos de linha, truncar o eixo é permitido se o foco for mostrar a flutuação.
* **Responsividade:** Garanta que a configuração contemple redimensionamento (ex: `responsive: true` em Chart.js, ou uso de `width='100%'`).
* **Tooltips:** Habilite os tooltips para gráficos interativos. Formate os valores (ex: colocar prefixo "$", agrupar milhares).
