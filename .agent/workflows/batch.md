---
description: Executa o pipeline de automação periódica e processamento em lote para ingestão de dados e renderização de relatórios/dashboards.
---

# /batch (Pipeline de Automação e Processamento em Lote)

Este fluxo orquestra o pipeline em lote para processar arquivos periódicos (quinzenais, mensais ou avulsos) depositados em `./data/incoming/` ou informados diretamente pelo operador.

---

## 🎯 Quando Utilizar

- Fechamentos quinzenais ou mensais de campanhas de anúncios (Meta Ads, Google Ads).
- Consolidação de relatórios de vendas e faturamento de e-commerce.
- Ingestão em lote de planilhas (`.csv`, `.xlsx`, `.json`) com geração instantânea de Dashboard HTML e Sumário Markdown.

---

## ⚙️ Protocolo de Execução (4 Etapas)

### 1. Descoberta de Arquivos de Entrada
- Verificar se o operador passou um arquivo específico como argumento (ex: `/batch data/incoming/campanha_maio.xlsx`).
- Caso nenhum argumento tenha sido fornecido, inspecionar `./data/incoming/` e selecionar o arquivo tabular mais recente.
- Se o diretório estiver vazio, orientar o operador a depositar o arquivo em `./data/incoming/` ou informar o caminho.

### 2. Inferência / Seleção de Template
- Apresentar ou confirmar o template adequado com base nas colunas:
  - **`marketing_ads`**: Para dados de mídia paga (Spend, Cliques, Impressões, Conversões).
  - **`sales_ecommerce`**: Para dados comerciais (Faturamento, Pedidos, Itens, Descontos).
  - **Template customizado**: Arquivo JSON em `./data/templates/`.

### 3. Execução do Pipeline CLI
Executar o orquestrador master via terminal:
```bash
python .agent/scripts/automations/run_batch.py --input ./data/incoming/ --output ./data/reports/
```
Ou com parâmetros customizados:
```bash
python .agent/scripts/automations/run_batch.py --input <arquivo> --template <marketing_ads|sales_ecommerce> --title "Relatório Executivo Quinzenal"
```

### 4. Apresentação dos Resultados
- Ler o relatório gerado em `./data/reports/report_<timestamp>.md` e exibir um sumário direto no chat.
- Fornecer o link clicável para visualização do dashboard local: `[Abrir Dashboard HTML](./data/reports/report_<timestamp>.html)`.
- Destacar os 3 principais insights e recomendações práticas para tomada de decisão.
