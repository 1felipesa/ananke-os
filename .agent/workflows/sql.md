---
name: sql
description: Fluxo direto para consultas analíticas SQL em arquivos locais (CSV, Parquet, JSON, XLSX) ou bancos de dados via DuckDB.
agent: data-analyst
---

# ⚡ Consulta SQL Analítica (SQL Workflow)

O comando `/sql` aciona diretamente o **Data Analyst** para processar consultas SQL sobre arquivos locais ou bancos de dados, utilizando o motor analítico in-process **DuckDB**.

---

## 🎯 Como Usar

Digite `/sql` seguido da sua consulta ou da pergunta em linguagem natural especificando o arquivo-alvo:

**Exemplos:**
- `/sql SELECT categoria, SUM(faturamento) as total FROM 'vendas.csv' GROUP BY categoria ORDER BY total DESC`
- `/sql Qual foi a evolução percentual de vendas dia a dia no arquivo 'vendas_2025.csv'? Use Window Functions.`
- `/sql Fazer JOIN entre 'pedidos.csv' e 'clientes.parquet' trazendo os top 10 clientes por volume de compras.`
- `/sql Execute o arquivo analise_clientes.sql e exporte o resultado para 'resultado.csv'.`

---

## 🔄 Fluxo de Execução

1. O `data-analyst` recebe o comando e a instrução SQL.
2. Se a instrução for uma pergunta em linguagem natural, o agente formula o SQL idiomático (com CTEs, Window Functions ou agregações).
3. Executa a query através do utilitário:
   ```bash
   python .agent/skills/sql-analytics/scripts/query_duckdb.py -q "<sua_query>"
   ```
4. Apresenta o resultado formatado em tabela Markdown com métricas de total de linhas e síntese explicativa.
