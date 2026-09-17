#!/usr/bin/env python3
"""
extract_pdf_tables.py - Extrator de Tabelas e Conteúdo Estruturado de Documentos PDF
Parte do Ananke OS (Skill: pdf-document-processing).
"""

import sys
import os
import argparse
import pdfplumber
import pandas as pd
from pypdf import PdfReader

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


def parse_page_range(pages_str, max_pages):
    """Interpreta ranges como '1-3', '1,5,8' ou 'all' (1-indexado)."""
    if not pages_str or pages_str.lower() == "all":
        return list(range(1, max_pages + 1))
    
    selected_pages = set()
    parts = pages_str.split(",")
    for part in parts:
        part = part.strip()
        if "-" in part:
            start, end = part.split("-")
            start, end = int(start), int(end)
            selected_pages.update(range(start, min(end, max_pages) + 1))
        elif part.isdigit():
            val = int(part)
            if 1 <= val <= max_pages:
                selected_pages.add(val)
                
    return sorted(list(selected_pages))


def clean_table(table_data):
    """Limpa linhas vazias e formata quebras de linha dentro de células."""
    if not table_data:
        return None

    cleaned_rows = []
    for row in table_data:
        cleaned_row = []
        for cell in row:
            if cell is None:
                cleaned_row.append("")
            else:
                # Substituir múltiplas quebras de linha e espaços
                cleaned_cell = " ".join(str(cell).split())
                cleaned_row.append(cleaned_cell)
        
        # Ignorar linhas onde todas as células estão em branco
        if any(bool(c.strip()) for c in cleaned_row):
            cleaned_rows.append(cleaned_row)

    if not cleaned_rows:
        return None

    header = cleaned_rows[0]
    data = cleaned_rows[1:]
    
    # Se o cabeçalho tiver colunas vazias, preencher com nomes padrão
    header = [h if h.strip() else f"col_{i+1}" for i, h in enumerate(header)]
    
    # Ajustar linhas com tamanho diferente do cabeçalho
    norm_data = []
    for r in data:
        if len(r) < len(header):
            r = r + [""] * (len(header) - len(r))
        elif len(r) > len(header):
            r = r[:len(header)]
        norm_data.append(r)

    df = pd.DataFrame(norm_data, columns=header)
    return df


def extract_from_pdf(pdf_path, pages_str="all", mode="auto", extract_text_also=False):
    """Extrai tabelas e opcionalmente texto estruturado de cada página."""
    extracted_tables = []
    page_texts = []

    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        pages_to_process = parse_page_range(pages_str, total_pages)

        for p_num in pages_to_process:
            page = pdf.pages[p_num - 1]
            
            # 1. Extração de Texto
            if extract_text_also:
                txt = page.extract_text() or ""
                page_texts.append((p_num, txt.strip()))

            # 2. Extração de Tabelas
            # Configurações de estratégia (lattice vs stream)
            table_settings = {}
            if mode == "lattice":
                table_settings = {"vertical_strategy": "lines", "horizontal_strategy": "lines"}
            elif mode == "stream":
                table_settings = {"vertical_strategy": "text", "horizontal_strategy": "text"}
            
            tables = page.extract_tables(table_settings) if table_settings else page.extract_tables()

            for t_idx, raw_table in enumerate(tables):
                df = clean_table(raw_table)
                if df is not None and not df.empty:
                    extracted_tables.append({
                        "page": p_num,
                        "table_index": t_idx + 1,
                        "df": df
                    })

    return extracted_tables, page_texts


def main():
    parser = argparse.ArgumentParser(description="Extrai tabelas e texto de PDFs para análise estruturada.")
    parser.add_argument("--pdf", "-p", required=True, help="Caminho do arquivo PDF")
    parser.add_argument("--pages", default="all", help="Páginas a processar (ex: '1-3', '1,4,7' ou 'all')")
    parser.add_argument("--mode", choices=["auto", "lattice", "stream"], default="auto", 
                        help="Modo de extração (lattice=com linhas, stream=sem linhas, auto=padrão)")
    parser.add_argument("--text", action="store_true", help="Extrair também o texto das páginas")
    parser.add_argument("--output", "-o", default=None, help="Arquivo de destino (.csv ou .md)")

    args = parser.parse_args()

    if not os.path.exists(args.pdf):
        print(f"❌ Erro: Arquivo PDF não encontrado: {args.pdf}", file=sys.stderr)
        sys.exit(1)

    try:
        tables, texts = extract_from_pdf(args.pdf, pages_str=args.pages, mode=args.mode, extract_text_also=args.text)

        output_lines = []
        output_lines.append(f"# 📄 Relatório de Extração de PDF: `{os.path.basename(args.pdf)}`\n")
        output_lines.append(f"Tabelas identificadas: **{len(tables)}**\n")

        if tables:
            for t in tables:
                p = t["page"]
                idx = t["table_index"]
                df = t["df"]
                output_lines.append(f"\n### 📊 Tabela {idx} (Página {p})\n")
                output_lines.append(to_markdown_safe(df, index=False))
                output_lines.append("\n")

        if args.text and texts:
            output_lines.append("\n---\n## 📝 Texto Extraído por Página\n")
            for p, txt in texts:
                output_lines.append(f"### Página {p}\n")
                output_lines.append(txt if txt else "*(Sem texto detectado)*")
                output_lines.append("\n")

        report_content = "\n".join(output_lines)

        if args.output:
            ext = os.path.splitext(args.output)[1].lower()
            if ext == ".csv" and tables:
                # Salva a primeira ou concatena se tiver a mesma estrutura
                concat_df = pd.concat([t["df"] for t in tables], ignore_index=True)
                concat_df.to_csv(args.output, index=False)
                print(f"✅ Tabelas exportadas para CSV: {args.output}")
            else:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(report_content)
                print(f"✅ Relatório salvo em: {args.output}")
        else:
            print(report_content)

    except Exception as e:
        print(f"❌ Falha ao processar PDF: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
