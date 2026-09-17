#!/usr/bin/env python3
"""
profile_dataset.py - Utilitário de Profiling e Diagnóstico para Planilhas (CSV, XLSX, TSV)
Parte do Ananke OS (Skill: spreadsheet-wrangling).
"""

import sys
import os
import argparse
import pandas as pd
import numpy as np

# Configurar encoding UTF-8 para stdout e stderr no Windows
try:
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass


def detect_separator(file_path, default=','):
    """Detecta se o CSV utiliza vírgula, ponto e vírgula ou tabulação."""
    separators = [';', ',', '\t', '|']
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = [f.readline() for _ in range(5)]
            sample = "".join(lines)
            counts = {sep: sample.count(sep) for sep in separators}
            best_sep = max(counts, key=counts.get)
            return best_sep if counts[best_sep] > 0 else default
    except Exception:
        return default


def load_dataset(file_path, sep=None, encoding='utf-8'):
    """Carrega dataset com tratamento de encoding e formatos."""
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext in ['.xlsx', '.xls']:
        return pd.read_excel(file_path)
    
    if ext in ['.csv', '.tsv', '.txt']:
        used_sep = sep if sep else detect_separator(file_path)
        try:
            return pd.read_csv(file_path, sep=used_sep, encoding=encoding)
        except UnicodeDecodeError:
            return pd.read_csv(file_path, sep=used_sep, encoding='latin-1')
        except Exception:
            # Tentar com decimal brasileiro se falhar
            return pd.read_csv(file_path, sep=used_sep, encoding='utf-8', decimal=',')

    raise ValueError(f"Extensão não suportada: {ext}. Use .csv, .xlsx, .tsv.")


def to_markdown_safe(df, index=False):
    """Converte DataFrame para tabela Markdown com fallback manual caso tabulate não esteja instalado."""
    try:
        return df.to_markdown(index=index)
    except Exception:
        cols = list(df.columns)
        header = "| " + " | ".join(str(c) for c in cols) + " |"
        sep = "| " + " | ".join(["---"] * len(cols)) + " |"
        rows = []
        for _, row in df.iterrows():
            rows.append("| " + " | ".join(str(val) for val in row) + " |")
        return "\n".join([header, sep] + rows)


def profile_dataframe(df, file_name="Dataset"):
    """Gera diagnóstico estatístico e de integridade em formato Markdown."""
    total_rows, total_cols = df.shape
    total_cells = total_rows * total_cols
    total_nulls = df.isnull().sum().sum()
    null_pct = (total_nulls / total_cells * 100) if total_cells > 0 else 0
    duplicate_rows = df.duplicated().sum()
    dup_pct = (duplicate_rows / total_rows * 100) if total_rows > 0 else 0

    lines = []
    lines.append(f"# 📊 Diagnóstico de Qualidade: `{file_name}`\n")
    lines.append(f"| Métrica | Valor |")
    lines.append(f"| :--- | :--- |")
    lines.append(f"| **Linhas** | `{total_rows:,}` |")
    lines.append(f"| **Colunas** | `{total_cols:,}` |")
    lines.append(f"| **Células Totais** | `{total_cells:,}` |")
    lines.append(f"| **Valores Nulos Globais** | `{total_nulls:,}` ({null_pct:.2f}%) |")
    lines.append(f"| **Linhas Duplicadas** | `{duplicate_rows:,}` ({dup_pct:.2f}%) |")
    lines.append(f"| **Uso de Memória** | `{df.memory_usage(deep=True).sum() / (1024*1024):.2f} MB` |")
    lines.append("\n---\n")

    lines.append("## 📋 Resumo por Coluna\n")
    lines.append("| Coluna | Tipo | Nulos | % Nulos | Únicos | Amostra de Valores |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")

    for col in df.columns:
        col_type = str(df[col].dtype)
        col_nulls = df[col].isnull().sum()
        col_null_pct = (col_nulls / total_rows * 100) if total_rows > 0 else 0
        n_unique = df[col].nunique(dropna=True)
        samples = df[col].dropna().unique()[:3]
        samples_str = ", ".join([f"`{str(s)[:25]}`" for s in samples])
        lines.append(f"| **{col}** | `{col_type}` | {col_nulls} | {col_null_pct:.1f}% | {n_unique} | {samples_str} |")

    # Sumário Estatístico de Numéricas
    num_df = df.select_dtypes(include=[np.number])
    if not num_df.empty:
        lines.append("\n---\n")
        lines.append("## 📈 Estatísticas Descritivas (Variáveis Numéricas)\n")
        lines.append("| Coluna | Mín | 25% | Mediana | Média | 75% | Máx | Desvio Padrão | Outliers (IQR) |")
        lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")

        for col in num_df.columns:
            s = num_df[col].dropna()
            if len(s) == 0:
                continue
            q25 = s.quantile(0.25)
            q75 = s.quantile(0.75)
            iqr = q75 - q25
            lower_bound = q25 - 1.5 * iqr
            upper_bound = q75 + 1.5 * iqr
            outliers = s[(s < lower_bound) | (s > upper_bound)].count()
            outliers_pct = (outliers / len(s) * 100) if len(s) > 0 else 0

            lines.append(
                f"| **{col}** | {s.min():.2f} | {q25:.2f} | {s.median():.2f} | {s.mean():.2f} | {q75:.2f} | {s.max():.2f} | {s.std():.2f} | {outliers} ({outliers_pct:.1f}%) |"
            )

    # Primeiras 5 linhas
    lines.append("\n---\n")
    lines.append("## 🔍 Prévia das Primeiras 5 Linhas\n")
    preview = to_markdown_safe(df.head(5), index=False)
    lines.append(preview if preview else "*(Nenhum dado para exibir)*")
    lines.append("\n")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Gera perfil e diagnóstico estatístico de planilhas e datasets.")
    parser.add_argument("--file", "-f", required=True, help="Caminho do arquivo (.csv, .xlsx, .tsv)")
    parser.add_argument("--sep", "-s", default=None, help="Separador (para CSV/TSV, ex: ',' ou ';')")
    parser.add_argument("--encoding", "-e", default="utf-8", help="Encoding do arquivo (padrão: utf-8)")
    parser.add_argument("--output", "-o", default=None, help="Arquivo de destino para salvar o relatório .md")

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"❌ Erro: Arquivo não encontrado: {args.file}", file=sys.stderr)
        sys.exit(1)

    try:
        df = load_dataset(args.file, sep=args.sep, encoding=args.encoding)
        report = profile_dataframe(df, file_name=os.path.basename(args.file))

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(report)
            print(f"✅ Diagnóstico salvo com sucesso em: {args.output}")
        else:
            print(report)

    except Exception as e:
        print(f"❌ Falha ao processar dataset: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
