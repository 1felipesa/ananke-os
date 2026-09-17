---
name: data-storytelling
description: Princípios de Data Storytelling. Técnicas de redução de ruído visual (chartjunk), uso estratégico de cores para destacar insights e criação de hierarquia de informação.
---

# Princípios de Data Storytelling

Visualizar dados não é só jogar números num gráfico, é contar a história que os números escondem. Siga estas diretrizes para transformar *Data Viz* em *Data Storytelling*.

## 🧹 1. Maximize a Taxa "Tinta vs Dados" (Elimine o Chartjunk)

Inspirado em Edward Tufte: O gráfico deve conter a maior quantidade de dados com a menor quantidade possível de "tinta" ou elementos visuais inúteis.

* **O que remover:** 
  * Linhas de grade fortes e escuras (se necessárias, use um cinza muito claro, quase invisível).
  * Bordas e caixas delimitadoras ao redor do gráfico.
  * Efeitos 3D (bisel, sombras densas) e texturas.
  * Legendas reduntantes (se houver apenas uma linha ou série, o título já diz do que se trata).
* **Rótulos Diretos (Direct Labeling):** Em gráficos de linhas com muitas linhas, em vez de usar uma legenda separada que obrigue os olhos do usuário a fazerem um vai-e-vem, escreva o nome da série imediatamente ao final da própria linha.

## 🎨 2. Uso Estratégico da Cor

A cor é a ferramenta mais poderosa para contar histórias. Não a desperdice.

* **Cores Categóricas Aleatórias:** NUNCA pinte um gráfico de barras onde cada barra é de uma cor diferente se todas pertencem à mesma categoria de dados (ex: Vendas de Janeiro, Fev, Mar).
* **Destaque Visual (Highlighting):** 
  * Se você quer mostrar que a "Barra D" é o problema, pinte todas as barras (A, B, C, E) de Cinza Neutro, e pinte a "Barra D" de Vermelho de Alerta ou da cor principal da marca. 
* **Daltonismo:** Use paletas acessíveis. Evite combinar Verde e Vermelho puros lado a lado apenas por sua cor. Confie mais em contrastes de brilho.
* **Paletas Contínuas vs Divergentes:**
  * Valores como Renda (de muito baixa para muito alta): Use uma paleta Sequencial (ex: de azul claro para azul escuro).
  * Valores com ponto de divergência (ex: Lucro/Prejuízo centrados em 0): Use paletas Divergentes (ex: Laranja escuro no negativo, cinza no zero, Azul escuro no positivo).

## ✍️ 3. Títulos e Anotações

O usuário não deveria ter que "decifrar" o gráfico. O texto deve guiá-lo.

* **Títulos Ativos:** 
  * ❌ *Anti-padrão:* "Faturamento de Vendas por Trimestre"
  * ✅ *Padrão Storyteller:* "Q3 registrou a maior queda histórica em Vendas devido à ruptura de estoque"
* **Anotações Diretas no Gráfico:** Quando houver um pico, vale ou evento incomum num gráfico de linha, insira uma seta, um marcador ou uma caixa de texto *diretamente* apontando para aquele ponto de dado, explicando o que houve (ex: "Início da Campanha X").

## ⚖️ 4. Contexto é Rei
Um número isolado não significa nada. O número 400.000 é bom ou ruim? Mostre referências.
* Adicione uma linha alvo (Goal Line) cruzando o gráfico.
* Inclua dados de comparação com o período anterior (ex: MoM, YoY).
