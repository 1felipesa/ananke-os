#!/usr/bin/env python3
"""
Ingest & Sanitize Batch Files
Part of Ananke OS Automations Suite.

Features:
- Multi-format ingestion: CSV, TSV, XLSX, JSON
- Auto-detection of encodings (utf-8, latin1, cp1252) and delimiters (,, ;, \\t)
- Brazilian currency normalization (R$ 1.250,50 -> 1250.50)
- Date normalization to ISO 8601 (YYYY-MM-DD)
- Deduplication and data health metrics
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path
from typing import Dict, Any, Tuple, Optional
import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def detect_encoding_and_delimiter(file_path: Path) -> Tuple[str, str]:
    """Detect the most likely encoding and delimiter for a delimited file."""
    encodings = ["utf-8-sig", "utf-8", "latin1", "cp1252"]
    sample_bytes = b""
    detected_encoding = "utf-8"

    for enc in encodings:
        try:
            with open(file_path, "rb") as f:
                sample_bytes = f.read(16384)
            sample_bytes.decode(enc)
            detected_encoding = enc
            break
        except (UnicodeDecodeError, Exception):
            continue

    sample_text = sample_bytes.decode(detected_encoding, errors="ignore")
    
    # Check delimiters in header line
    lines = [line for line in sample_text.splitlines() if line.strip()]
    header = lines[0] if lines else ""

    delimiters = [",", ";", "\t", "|"]
    counts = {d: header.count(d) for d in delimiters}
    detected_delimiter = max(counts, key=counts.get)
    if counts[detected_delimiter] == 0:
        detected_delimiter = ","

    return detected_encoding, detected_delimiter


def clean_currency_and_numbers(val: Any) -> Any:
    """Normalize Brazilian currency/numbers or percentage to float if applicable."""
    if pd.isna(val):
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    if not isinstance(val, str):
        return val

    s = val.strip()
    if not s:
        return 0.0

    # Pattern for Brazilian currency / decimals: e.g. R$ 1.234,56 or 1.234,56 or 50,00%
    if re.search(r"^[+-]?\s*(?:R\$\s*)?-?[\d\.]+(?:,\d+)?\s*%?$", s, re.IGNORECASE):
        cleaned = re.sub(r"[R\$\s%]", "", s)
        # Check if comma is decimal separator
        if "," in cleaned and "." in cleaned:
            cleaned = cleaned.replace(".", "").replace(",", ".")
        elif "," in cleaned:
            cleaned = cleaned.replace(",", ".")
        elif "." in cleaned:
            # Check if it's Brazilian thousand separator (e.g. 25.000 or 1.120)
            parts = cleaned.split(".")
            if len(parts) > 1 and all(len(p) == 3 for p in parts[1:]):
                cleaned = "".join(parts)
        try:
            return float(cleaned)
        except ValueError:
            pass

    return val


def normalize_dates(series: pd.Series) -> pd.Series:
    """Attempt to parse dates into ISO 8601 YYYY-MM-DD."""
    sample = series.dropna().head(20)
    if sample.empty:
        return series

    # Check if strings look like dates (e.g. DD/MM/YYYY or YYYY-MM-DD)
    date_patterns = [
        r"^\d{1,2}/\d{1,2}/\d{2,4}",
        r"^\d{1,2}-\d{1,2}-\d{2,4}",
        r"^\d{4}-\d{1,2}-\d{1,2}",
    ]
    is_likely_date = False
    for val in sample:
        if isinstance(val, str) and any(re.match(pat, val.strip()) for pat in date_patterns):
            is_likely_date = True
            break

    if not is_likely_date and not pd.api.types.is_datetime64_any_dtype(series):
        return series

    try:
        parsed = pd.to_datetime(series, dayfirst=True, errors="coerce")
        # Format as string YYYY-MM-DD
        return parsed.dt.strftime("%Y-%m-%d").fillna("")
    except Exception:
        return series


def ingest_file(file_path: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Ingest and sanitize a file, returning (cleaned_dataframe, metadata_dict).
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    suffix = path.suffix.lower()
    raw_df = pd.DataFrame()

    if suffix in [".csv", ".tsv", ".txt"]:
        encoding, delimiter = detect_encoding_and_delimiter(path)
        raw_df = pd.read_csv(path, encoding=encoding, sep=delimiter, dtype=str, on_bad_lines="skip")
    elif suffix in [".xlsx", ".xls"]:
        raw_df = pd.read_excel(path, dtype=str)
    elif suffix == ".json":
        raw_df = pd.read_json(path, dtype=str)
    else:
        raise ValueError(f"Formato não suportado: {suffix}. Formatos aceitos: .csv, .tsv, .xlsx, .json")

    raw_rows = len(raw_df)

    # Normalize column names: strip, lowercase, replace spaces with underscores
    clean_cols = [
        re.sub(r"[^\w]+", "_", str(col).strip().lower()).strip("_")
        for col in raw_df.columns
    ]
    raw_df.columns = clean_cols

    # Deduplicate rows
    df_dedup = raw_df.drop_duplicates().copy()
    dedup_rows = len(df_dedup)
    duplicates_removed = raw_rows - dedup_rows

    # Normalize numeric columns and dates
    date_col = None
    for col in df_dedup.columns:
        # Check if it's a date column by name or content
        if "data" in col or "date" in col or "dia" in col or "period" in col:
            df_dedup[col] = normalize_dates(df_dedup[col])
            if date_col is None:
                date_col = col

        # Clean numeric candidates
        df_dedup[col] = df_dedup[col].apply(clean_currency_and_numbers)

    meta = {
        "source_file": str(path.resolve()),
        "file_name": path.name,
        "format": suffix,
        "raw_rows": raw_rows,
        "clean_rows": dedup_rows,
        "duplicates_removed": duplicates_removed,
        "columns": list(df_dedup.columns),
        "inferred_date_column": date_col,
    }

    return df_dedup, meta


def main():
    parser = argparse.ArgumentParser(description="Ingestão e sanitização de dados em lote.")
    parser.add_argument("file", help="Caminho do arquivo (.csv, .xlsx, .json)")
    parser.add_argument("--output", "-o", help="Salvar dataframe higienizado em CSV", default=None)
    args = parser.parse_args()

    try:
        df, meta = ingest_file(args.file)
        print(f"\n[OK] Ingestão concluída com sucesso:")
        print(f"  - Arquivo: {meta['file_name']}")
        print(f"  - Linhas brutas: {meta['raw_rows']}")
        print(f"  - Linhas após deduplicação: {meta['clean_rows']} ({meta['duplicates_removed']} removidas)")
        print(f"  - Colunas ({len(meta['columns'])}): {', '.join(meta['columns'][:8])}...")
        if meta['inferred_date_column']:
            print(f"  - Coluna temporal identificada: {meta['inferred_date_column']}")

        if args.output:
            out_path = Path(args.output)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(out_path, index=False)
            print(f"  - Salvo em: {out_path}")

    except Exception as e:
        print(f"[ERRO] Falha na ingestão: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
