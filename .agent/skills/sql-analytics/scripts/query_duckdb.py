#!/usr/bin/env python3
"""
query_duckdb.py - Motor SQL Analítico in-process para consultas em CSV, Parquet, JSON e XLSX
Parte do Ananke OS (Skill: sql-analytics).
"""

import sys
import os
import argparse
import duckdb
import pandas as pd

# Configurar encoding UTF-8 para stdout e stderr no Windows
try:
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass


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


def execute_sql(query, limit=50, explain=False, output_format="md"):
    """Executa consulta SQL no DuckDB e formata a resposta."""
    con = duckdb.connect(database=":memory:")
    
    # Habilitar extensão para leitura de Excel caso necessário
    try:
        con.execute("INSTALL spatial; LOAD spatial;")
    except Exception:
        pass

    if explain:
        explain_res = con.execute(f"EXPLAIN {query}").fetchall()
        print("🔍 Plano de Execução (EXPLAIN):")
        for row in explain_res:
            print(row[1] if len(row) > 1 else row[0])
        print("\n" + "=" * 50 + "\n")

    # Executar query
    try:
        rel = con.execute(query)
        df = rel.fetchdf()
    except Exception as e:
        print(f"❌ Erro na execução SQL: {e}", file=sys.stderr)
        sys.exit(1)

    total_rows = len(df)
    display_df = df.head(limit)

    if output_format == "csv":
        return display_df.to_csv(index=False)
    elif output_format == "json":
        return display_df.to_json(orient="records", indent=2, force_ascii=False)
    else:
        # Markdown table
        md = to_markdown_safe(display_df, index=False)
        footer = f"\n\n*Exibindo {len(display_df)} de {total_rows} registros.*" if total_rows > limit else f"\n\n*Total de registros: {total_rows}*"
        return (md if md else "*(Nenhum registro retornado)*") + footer


def main():
    parser = argparse.ArgumentParser(description="Executa consultas analíticas SQL em arquivos locais usando DuckDB.")
    parser.add_argument("--query", "-q", default=None, help="String SQL a ser executada")
    parser.add_argument("--file", "-f", default=None, help="Arquivo .sql contendo a consulta")
    parser.add_argument("--limit", "-l", type=int, default=50, help="Limite de linhas na exibição (padrão: 50)")
    parser.add_argument("--explain", action="store_true", help="Exibir plano de execução antes dos resultados")
    parser.add_argument("--format", choices=["md", "csv", "json"], default="md", help="Formato de saída (padrão: md)")
    parser.add_argument("--output", "-o", default=None, help="Caminho do arquivo para salvar a saída")

    args = parser.parse_args()

    sql_query = None
    if args.query:
        sql_query = args.query
    elif args.file:
        if not os.path.exists(args.file):
            print(f"❌ Erro: Arquivo SQL não encontrado: {args.file}", file=sys.stderr)
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8") as f:
            sql_query = f.read()
    else:
        print("❌ Erro: Forneça uma query via --query ou um arquivo via --file.", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    result = execute_sql(sql_query, limit=args.limit, explain=args.explain, output_format=args.format)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"✅ Resultado salvo com sucesso em: {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
