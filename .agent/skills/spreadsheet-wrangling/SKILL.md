---
name: spreadsheet-wrangling
description: Ingestão, higienização, profiling e normalização de planilhas e arquivos tabulares (CSV, XLSX, TSV). Trata especificidades regionais (formato de número e datas PT-BR), valores nulos e dados corrompidos.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Spreadsheet Wrangling Skill

Habilidade especializada na ingestão, auditoria de integridade, normalização e limpeza de arquivos tabulares (`.xlsx`, `.csv`, `.tsv`), garantindo dados consistentes para análise analítica e modelagem.

---

## 🎯 Objetivos Principais

1. **Diagnóstico Imediato (Profiling):** Mapear dimensões, tipos de dados inferidos, cardinalidade, proporção de nulos e identificar linhas duplicadas antes de qualquer transformação.
2. **Tratamento de Regionalização (PT-BR):** Identificar e converter formatos com separador de decimal por vírgula (`1.234,56`), separador de milhares por ponto e datas no formato `DD/MM/YYYY`.
3. **Higienização de Cabeçalhos:** Converter nomes de colunas com acentos, espaços e caracteres especiais em formato `snake_case` padronizado.
4. **Resolução de Encoding:** Tratar automaticamente arquivos salvos em `latin-1` (ISO-8859-1) ou `cp1252` comuns no ecossistema corporativo brasileiro.

---

## 🛠️ Ferramenta Utilitária: `profile_dataset.py`

Esta skill conta com o script automatizado de diagnóstico em `scripts/profile_dataset.py`.

### Como Executar:

```bash
# Diagnóstico direto no terminal
python .agent/skills/spreadsheet-wrangling/scripts/profile_dataset.py --file <caminho_do_arquivo>

# Salvar relatório formatado em Markdown
python .agent/skills/spreadsheet-wrangling/scripts/profile_dataset.py --file dados.csv --output relatorio_qualidade.md

# Especificar separador explícito se necessário (ex: ponto e vírgula)
python .agent/skills/spreadsheet-wrangling/scripts/profile_dataset.py --file export.csv --sep ";"
```

---

## 📋 Padrões de Normalização em Python / Pandas

### 1. Limpeza de Cabeçalhos (Snake Case)
```python
import re
import unicodedata

def clean_column_names(df):
    def normalize_col(col):
        c = unicodedata.normalize('NFKD', str(col)).encode('ASCII', 'ignore').decode('utf-8')
        c = re.sub(r'[^\w\s]', '', c)
        c = re.sub(r'\s+', '_', c.strip().lower())
        return c
    df.columns = [normalize_col(c) for c in df.columns]
    return df
```

### 2. Conversão de Moeda e Números PT-BR para Float
```python
def parse_br_currency(series):
    return (
        series.astype(str)
        .str.replace('R$', '', regex=False)
        .str.replace('.', '', regex=False)
        .str.replace(',', '.', regex=False)
        .str.strip()
        .astype(float)
    )
```

### 3. Tratamento e Imputação de Nulos
- **Numéricas assimétricas:** Imputar com **mediana** (menos sensível a outliers).
- **Numéricas simétricas:** Imputar com **média** ou valor fixo representativo (ex: 0).
- **Categóricas:** Preencher com `'NÃO INFORMADO'` ou categoria `'DESCONHECIDO'`.
- **Regra de Descarte:** Se uma coluna tiver **> 50% de valores nulos**, avaliar se ela deve ser descartada ou mantida apenas como flag booleana de presença.
