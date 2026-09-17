---
name: sql-analytics
description: Padrões avançados de SQL Analítico (OLAP), Window Functions, CTEs recursivas, agregações multi-nível e execução de consultas de alta performance em arquivos locais (CSV, Parquet, JSON) usando DuckDB.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# SQL Analytics Skill

Habilidade especializada na formulação e execução de consultas SQL analíticas de alto nível (OLAP), combinando os recursos modernos do **DuckDB** e boas práticas de modelagem analítica.

---

## 🚀 Motor Analítico Local: DuckDB

O **DuckDB** permite executar queries SQL completas diretamente sobre arquivos locais (`.csv`, `.parquet`, `.json`) sem a necessidade de criar tabelas prévias ou instalar servidores como PostgreSQL.

### Sintaxe de Consulta Direta sobre Arquivos:

```sql
-- Consultar CSV diretamente
SELECT * FROM 'dados/vendas.csv' LIMIT 10;

-- Consultar com detecção automática de tipos
SELECT cliente, SUM(valor) as total_gasto
FROM read_csv_auto('dados/vendas.csv')
GROUP BY cliente
ORDER BY total_gasto DESC;

-- Fazer JOIN entre um CSV e um arquivo Parquet
SELECT v.id_venda, v.data, c.nome, c.regiao
FROM 'vendas.csv' v
JOIN 'clientes.parquet' c ON v.id_cliente = c.id;
```

---

## 🛠️ Ferramenta Utilitária: `query_duckdb.py`

Esta skill conta com o script de execução em `scripts/query_duckdb.py`.

### Exemplos de Uso:

```bash
# Executar query direta
python .agent/skills/sql-analytics/scripts/query_duckdb.py -q "SELECT * FROM 'dataset.csv' LIMIT 5"

# Executar arquivo .sql e salvar em CSV
python .agent/skills/sql-analytics/scripts/query_duckdb.py -f analise_cohort.sql -o resultado.csv --format csv

# Analisar plano de execução (EXPLAIN)
python .agent/skills/sql-analytics/scripts/query_duckdb.py -q "SELECT * FROM 'vendas.csv'" --explain
```

---

## 📊 Padrões Essenciais de SQL Analítico

### 1. Window Functions (Funções de Janela)

#### A. Ranking e Paginação
```sql
SELECT 
    categoria,
    produto,
    faturamento,
    ROW_NUMBER() OVER (PARTITION BY categoria ORDER BY faturamento DESC) as ranking_categoria,
    DENSE_RANK() OVER (ORDER BY faturamento DESC) as ranking_global
FROM 'produtos.csv';
```

#### B. Comparação com Linhas Anteriores / Posteriores (Lead / Lag)
```sql
SELECT 
    data_venda,
    faturamento_dia,
    LAG(faturamento_dia, 1) OVER (ORDER BY data_venda) as faturamento_ontem,
    ROUND((faturamento_dia - LAG(faturamento_dia, 1) OVER (ORDER BY data_venda)) / LAG(faturamento_dia, 1) OVER (ORDER BY data_venda) * 100, 2) as pct_crescimento_diario
FROM 'vendas_diarias.csv';
```

#### C. Média Móvel (Rolling Window)
```sql
SELECT 
    data_venda,
    faturamento_dia,
    AVG(faturamento_dia) OVER (
        ORDER BY data_venda 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as media_movel_7_dias
FROM 'vendas_diarias.csv';
```

### 2. Common Table Expressions (CTEs)
Para quebrar problemas analíticos complexos em etapas modulares e legíveis:

```sql
WITH metricas_base AS (
    SELECT 
        id_cliente,
        COUNT(id_pedido) as total_pedidos,
        SUM(valor) as total_gasto,
        MIN(data_pedido) as primeira_compra,
        MAX(data_pedido) as ultima_compra
    FROM 'pedidos.csv'
    GROUP BY id_cliente
),
segmentacao AS (
    SELECT 
        id_cliente,
        total_gasto,
        CASE 
            WHEN total_gasto > 5000 THEN 'VIP'
            WHEN total_gasto > 1000 THEN 'Frequente'
            ELSE 'Ocasional'
        END as segmento
    FROM metricas_base
)
SELECT segmento, COUNT(*) as qtd_clientes, ROUND(AVG(total_gasto), 2) as ticket_medio
FROM segmentacao
GROUP BY segmento;
```

---

## ⚠️ Diretrizes Anti-Erros em Consultas Analíticas

1. **Evitar Cartesian Product (JOIN sem ON):** Sempre certifique-se da cardinalidade das chaves nos JOINs para não multiplicar linhas e distorcer somas.
2. **Cuidado com `NULL` em Agregações:** Funções como `AVG()` ignoram valores `NULL`, enquanto `COUNT(*)` conta linhas e `COUNT(coluna)` conta valores não-nulos.
3. **Limite Preventivo:** Ao explorar bases desconhecidas com milhões de linhas, utilize `LIMIT` na camada externa para não sobrecarregar a memória do processo.
