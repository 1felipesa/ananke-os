#!/usr/bin/env python3
"""
Aggregate Metrics Module
Part of Ananke OS Automations Suite.

Features:
- Template-driven agnostic calculations (Marketing, Sales, or custom schemas)
- Automatic fuzzy mapping between dataset columns and template metric definitions
- Safe KPI calculations with zero-division handling
- High-performance DuckDB analytical processing
- Summary KPIs, temporal breakdowns, and categorical rankings (Top 5)
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

try:
    import duckdb
    HAS_DUCKDB = True
except ImportError:
    HAS_DUCKDB = False


def load_template(template_name_or_path: str) -> Dict[str, Any]:
    """Load template JSON by name or file path."""
    # Check if direct file exists
    p = Path(template_name_or_path)
    if p.exists() and p.is_file():
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)

    # Check built-in templates folder
    templates_dir = Path(__file__).resolve().parents[3] / "data" / "templates"
    candidate = templates_dir / f"{template_name_or_path}.json"
    if candidate.exists():
        with open(candidate, "r", encoding="utf-8") as f:
            return json.load(f)

    # Default fallback to marketing_ads
    candidate_default = templates_dir / "marketing_ads.json"
    if candidate_default.exists():
        with open(candidate_default, "r", encoding="utf-8") as f:
            return json.load(f)

    raise FileNotFoundError(f"Template não encontrado: {template_name_or_path}")


def resolve_column_mappings(df_columns: List[str], metric_mappings: Dict[str, List[str]]) -> Dict[str, Optional[str]]:
    """Map canonical metric keys to actual dataframe columns."""
    resolved = {}
    lower_cols = {col.lower(): col for col in df_columns}

    for canonical_key, aliases in metric_mappings.items():
        found_col = None
        # Check canonical name first
        if canonical_key.lower() in lower_cols:
            found_col = lower_cols[canonical_key.lower()]
        else:
            # Check aliases
            for alias in aliases:
                a_clean = alias.lower().replace(" ", "_")
                if a_clean in lower_cols:
                    found_col = lower_cols[a_clean]
                    break
                # Partial match
                for col in df_columns:
                    if a_clean == col or a_clean in col:
                        found_col = col
                        break
                if found_col:
                    break

        resolved[canonical_key] = found_col

    return resolved


def safe_divide(numerator: float, denominator: float, multiplier: float = 1.0) -> float:
    """Safely divide two numbers, avoiding ZeroDivisionError."""
    if denominator == 0 or pd.isna(denominator) or pd.isna(numerator):
        return 0.0
    return float((numerator / denominator) * multiplier)


def aggregate_dataset(df: pd.DataFrame, template_name_or_path: str = "marketing_ads") -> Dict[str, Any]:
    """
    Apply analytical aggregation using the template schema.
    Returns structured results with overall totals, calculated KPIs, time-series, and category rankings.
    """
    template = load_template(template_name_or_path)
    mappings = resolve_column_mappings(list(df.columns), template.get("metric_mappings", {}))

    # Convert mapped metric columns to numeric
    for canonical, actual_col in mappings.items():
        if actual_col and actual_col in df.columns:
            df[actual_col] = pd.to_numeric(df[actual_col], errors="coerce").fillna(0.0)

    # Calculate raw totals
    totals: Dict[str, float] = {}
    for canonical, actual_col in mappings.items():
        if actual_col and actual_col in df.columns:
            totals[canonical] = float(df[actual_col].sum())
        else:
            totals[canonical] = 0.0

    # Calculate derived KPIs
    calculated: List[Dict[str, Any]] = []
    for spec in template.get("calculated_metrics", []):
        key = spec["key"]
        formula = spec["formula"]
        format_type = spec.get("format", "decimal")
        label = spec.get("label", key)

        val = 0.0
        # Common formula mappings
        if key == "ctr":
            val = safe_divide(totals.get("clicks", 0), totals.get("impressions", 0), 100.0)
        elif key == "cpc":
            val = safe_divide(totals.get("spend", 0), totals.get("clicks", 0))
        elif key == "cpa":
            val = safe_divide(totals.get("spend", 0), totals.get("conversions", 0))
        elif key == "roas":
            val = safe_divide(totals.get("revenue", 0), totals.get("spend", 0))
        elif key == "average_ticket":
            val = safe_divide(totals.get("revenue", 0), totals.get("orders", 0))
        elif key == "items_per_order":
            val = safe_divide(totals.get("items_sold", 0), totals.get("orders", 0))
        elif key == "discount_rate":
            rev = totals.get("revenue", 0)
            disc = totals.get("discounts", 0)
            val = safe_divide(disc, rev + disc, 100.0)

        calculated.append({
            "key": key,
            "label": label,
            "value": round(val, 2),
            "format": format_type,
            "higher_is_better": spec.get("higher_is_better", True)
        })

    # Time series breakdown
    time_series = []
    date_col = None
    for candidate in ["date", "data", "dia", "periodo", "mes"]:
        for col in df.columns:
            if candidate in col.lower():
                date_col = col
                break
        if date_col:
            break

    if date_col:
        # Group by date
        agg_dict = {}
        for canonical, actual_col in mappings.items():
            if actual_col:
                agg_dict[actual_col] = "sum"

        if agg_dict:
            ts_grouped = df.groupby(date_col).agg(agg_dict).reset_index().sort_values(by=date_col)
            for _, row in ts_grouped.tail(30).iterrows():
                item = {"date": str(row[date_col])}
                for canonical, actual_col in mappings.items():
                    if actual_col:
                        item[canonical] = round(float(row[actual_col]), 2)
                time_series.append(item)

    # Categorical breakdown & rankings
    cat_col = None
    for candidate in ["campaign_name", "campanha", "campaign", "category", "categoria", "produto", "product", "platform", "plataforma"]:
        for col in df.columns:
            if candidate in col.lower():
                cat_col = col
                break
        if cat_col:
            break

    rankings = []
    if cat_col:
        primary_metric = mappings.get("spend") or mappings.get("revenue") or (list(mappings.values())[0] if mappings else None)
        if primary_metric:
            grouped_cat = df.groupby(cat_col)[primary_metric].sum().reset_index()
            grouped_cat = grouped_cat.sort_values(by=primary_metric, ascending=False).head(10)
            for _, row in grouped_cat.iterrows():
                rankings.append({
                    "name": str(row[cat_col]),
                    "metric_col": primary_metric,
                    "value": round(float(row[primary_metric]), 2)
                })

    return {
        "template": template.get("name"),
        "template_title": template.get("title"),
        "total_rows": len(df),
        "raw_totals": {k: round(v, 2) for k, v in totals.items()},
        "calculated_kpis": calculated,
        "time_series": time_series,
        "rankings": rankings,
        "mapped_columns": mappings,
        "date_column": date_col,
        "category_column": cat_col
    }


def main():
    parser = argparse.ArgumentParser(description="Agregação analítica e cálculo de métricas em lote.")
    parser.add_argument("file", help="Arquivo tabular limpo (.csv)")
    parser.add_argument("--template", "-t", default="marketing_ads", help="Template (marketing_ads, sales_ecommerce)")
    args = parser.parse_args()

    try:
        df = pd.read_csv(args.file)
        results = aggregate_dataset(df, args.template)
        print(json.dumps(results, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"[ERRO] Falha na agregação: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
