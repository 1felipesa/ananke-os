#!/usr/bin/env python3
"""
Run Batch Orchestrator
Master CLI orchestrator for Ananke OS Automations Suite.

Coordinates:
1. File discovery in incoming directory or direct path
2. Ingestion and sanitization (ingest_batch.py)
3. Template resolution and metrics calculation (aggregate_metrics.py)
4. Dashboard and Markdown generation (render_report.py)
5. Execution logs and summary output
"""

import sys
import os
import argparse
from pathlib import Path
from typing import Optional

# Ensure UTF-8 output on Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Support local module imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from ingest_batch import ingest_file
from aggregate_metrics import aggregate_dataset
from render_report import render_all, format_currency_brl, format_metric_value


def find_latest_file(directory: Path) -> Optional[Path]:
    """Find the most recently modified tabular file in a directory."""
    valid_extensions = [".csv", ".tsv", ".xlsx", ".xls", ".json"]
    files = [
        f for f in directory.iterdir()
        if f.is_file() and f.suffix.lower() in valid_extensions and not f.name.startswith(".")
    ]
    if not files:
        return None
    files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    return files[0]


def infer_template(columns: list) -> str:
    """Infer the best default template based on column names."""
    col_str = " ".join(columns).lower()
    if any(k in col_str for k in ["spend", "gasto", "custo", "cliques", "clicks", "impressoes", "impressions"]):
        return "marketing_ads"
    if any(k in col_str for k in ["pedido", "order", "venda", "faturamento", "cliente", "produto"]):
        return "sales_ecommerce"
    return "marketing_ads"


def run_pipeline(
    input_target: str = "./data/incoming",
    output_dir: str = "./data/reports",
    template_name: Optional[str] = None,
    title: Optional[str] = None
) -> dict:
    """Execute the end-to-end batch processing pipeline."""
    target_path = Path(input_target)
    
    # 1. Resolve Target File
    if target_path.is_dir():
        file_to_process = find_latest_file(target_path)
        if not file_to_process:
            raise FileNotFoundError(
                f"Nenhum arquivo tabular (.csv, .xlsx, .json) encontrado no diretório: {target_path.resolve()}\n"
                f"Adicione arquivos brutos em '{target_path}' ou passe o caminho do arquivo com --input <arquivo>."
            )
    else:
        file_to_process = target_path
        if not file_to_process.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {target_path}")

    print("=" * 60)
    print("      🚀 ANANKE OS - BATCH AUTOMATION PIPELINE      ")
    print("=" * 60)
    print(f"📁 Arquivo Alvo: {file_to_process.name}")
    print(f"📂 Diretório de Saída: {Path(output_dir).resolve()}")

    # 2. Stage 1: Ingestion & Sanitization
    print("\n🔄 [1/3] Executando Ingestão e Sanitização...")
    df_clean, meta = ingest_file(str(file_to_process))
    print(f"   ✓ Linhas brutas: {meta['raw_rows']} | Limpas: {meta['clean_rows']} | Duplicatas removidas: {meta['duplicates_removed']}")
    print(f"   ✓ Colunas identificadas ({len(meta['columns'])}): {', '.join(meta['columns'][:6])}...")

    # 3. Stage 2: Template Selection & Aggregation
    resolved_template = template_name or infer_template(meta["columns"])
    print(f"\n🔄 [2/3] Agregando Métricas com Template: '{resolved_template}'...")
    agg_results = aggregate_dataset(df_clean, resolved_template)
    print(f"   ✓ Template aplicado: {agg_results.get('template_title')}")
    print(f"   ✓ KPIs calculados: {len(agg_results.get('calculated_kpis', []))}")

    # 4. Stage 3: Rendering Reports
    print("\n🔄 [3/3] Renderizando Dashboard HTML e Sumário Markdown...")
    html_file, md_file = render_all(agg_results, output_dir, title)
    print(f"   ✓ Dashboard HTML: {html_file.resolve()}")
    print(f"   ✓ Relatório Markdown: {md_file.resolve()}")

    # 5. Executive Highlights
    print("\n" + "=" * 60)
    print("                 📊 RESUMO DE INDICADORES                 ")
    print("=" * 60)
    for kpi in agg_results.get("calculated_kpis", []):
        val_fmt = format_metric_value(kpi["value"], kpi.get("format", "decimal"))
        print(f"  • {kpi['label']:<26}: {val_fmt}")

    rankings = agg_results.get("rankings", [])
    if rankings:
        print("\n🏆 Top 3 Destaques:")
        for i, r in enumerate(rankings[:3], 1):
            val_fmt = format_currency_brl(r["value"]) if "spend" in r["metric_col"] or "revenue" in r["metric_col"] else f"{r['value']:,.2f}"
            print(f"  #{i} {r['name']} ({val_fmt})")

    print("\n✅ Processamento em Lote Concluído com Sucesso ✨\n")

    return {
        "source_file": str(file_to_process),
        "html_report": str(html_file.resolve()),
        "markdown_report": str(md_file.resolve()),
        "kpis": agg_results.get("calculated_kpis", [])
    }


def main():
    parser = argparse.ArgumentParser(description="Orquestrador do Pipeline de Automações e Processamento em Lote.")
    parser.add_argument(
        "--input", "-i",
        default="./data/incoming",
        help="Caminho do arquivo bruto ou pasta contendo arquivos (padrão: ./data/incoming)"
    )
    parser.add_argument(
        "--output", "-o",
        default="./data/reports",
        help="Diretório onde os relatórios gerados serão salvos (padrão: ./data/reports)"
    )
    parser.add_argument(
        "--template", "-t",
        default=None,
        help="Nome do template analítico (ex: marketing_ads, sales_ecommerce ou caminho customizado)"
    )
    parser.add_argument(
        "--title",
        default=None,
        help="Título personalizado do relatório gerado"
    )

    args = parser.parse_args()

    try:
        run_pipeline(
            input_target=args.input,
            output_dir=args.output,
            template_name=args.template,
            title=args.title
        )
    except Exception as e:
        print(f"\n[ERRO CRÍTICO NO PIPELINE]: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
