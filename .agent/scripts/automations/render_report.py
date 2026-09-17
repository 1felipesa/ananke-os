#!/usr/bin/env python3
"""
Render Report Module
Part of Ananke OS Automations Suite.

Features:
- Standalone HTML Dashboard (Material Design 3 Dark Theme + Chart.js via CDN)
- Executive Markdown Summary for quick scanning and Notion/document copy
- Brazilian currency and metric formatting
- Synchronized dual generation with timestamps
"""

import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Tuple

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def format_currency_brl(val: float) -> str:
    """Format float into Brazilian currency string: R$ 1.234,56."""
    try:
        formatted = f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return f"R$ {formatted}"
    except Exception:
        return f"R$ {val}"


def format_metric_value(val: float, format_type: str) -> str:
    """Format value based on metric format definition."""
    if format_type == "currency":
        return format_currency_brl(val)
    elif format_type == "percent":
        return f"{val:.2f}%".replace(".", ",")
    elif format_type == "ratio":
        return f"{val:.2f}x".replace(".", ",")
    elif format_type == "integer":
        return f"{int(val):,}".replace(",", ".")
    else:
        return f"{val:.2f}".replace(".", ",")


def generate_markdown_report(data: Dict[str, Any], title: str, timestamp_str: str) -> str:
    """Build the executive markdown report."""
    md = []
    md.append(f"# {title}")
    md.append(f"\n> **Data de Geração:** {timestamp_str} | **Template:** `{data.get('template', 'default')}` | **Volume Processado:** {data.get('total_rows', 0):,} linhas\n")
    md.append("---\n")

    # KPIs Section
    md.append("## 📌 Indicadores-Chave (KPIs)\n")
    md.append("| Métrica | Valor Calculado | Status / Referência |")
    md.append("| :--- | :---: | :--- |")

    # Calculated KPIs
    for kpi in data.get("calculated_kpis", []):
        formatted_val = format_metric_value(kpi["value"], kpi.get("format", "decimal"))
        trend_badge = "🟢 Desejável" if kpi.get("higher_is_better") and kpi["value"] > 0 else "ℹ️ Informativo"
        md.append(f"| **{kpi['label']}** | **{formatted_val}** | {trend_badge} |")

    # Raw Totals
    md.append("\n### 📊 Volumes Brutos Agregados\n")
    md.append("| Dimensão Bruta | Total Consolidado |")
    md.append("| :--- | :---: |")
    for key, val in data.get("raw_totals", {}).items():
        if val > 0:
            formatted_val = format_currency_brl(val) if "spend" in key or "revenue" in key else f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            md.append(f"| {key.replace('_', ' ').title()} | {formatted_val} |")

    # Top Rankings
    rankings = data.get("rankings", [])
    if rankings:
        md.append("\n---\n")
        md.append("## 🏆 Top 10 Destaques de Desempenho\n")
        md.append("| Classificação | Nome / Dimensão | Valor Consolidado |")
        md.append("| :---: | :--- | :---: |")
        for i, rank in enumerate(rankings, 1):
            val_fmt = format_currency_brl(rank["value"]) if "spend" in rank["metric_col"] or "revenue" in rank["metric_col"] else f"{rank['value']:,.2f}"
            md.append(f"| #{i} | **{rank['name']}** | {val_fmt} |")

    # Strategic Insights
    md.append("\n---\n")
    md.append("## 💡 Observações & Próximas Ações Estratégicas\n")
    md.append("1. **Auditoria de Eficiência:** Identificar os 20% de campanhas/produtos que concentram 80% do resultado e alocar orçamento prioritário.")
    md.append("2. **Otimização Contínua:** Reavaliar itens com métricas de conversão abaixo da média do período.")
    md.append("3. **Próxima Rodada Batch:** Os dados consolidados foram registrados no histórico para comparação com a próxima janela periódica.")

    return "\n".join(md)


def generate_html_dashboard(data: Dict[str, Any], title: str, timestamp_str: str) -> str:
    """Build the standalone Material Design 3 Dark Theme dashboard."""
    kpi_cards_html = []
    for kpi in data.get("calculated_kpis", []):
        formatted_val = format_metric_value(kpi["value"], kpi.get("format", "decimal"))
        kpi_cards_html.append(f"""
        <div class="kpi-card">
            <div class="kpi-label">{kpi['label']}</div>
            <div class="kpi-value">{formatted_val}</div>
        </div>
        """)

    # Prepare chart data
    time_series = data.get("time_series", [])
    ts_labels = [item.get("date", "") for item in time_series]
    ts_spend = [item.get("spend", item.get("revenue", 0)) for item in time_series]
    ts_conv = [item.get("conversions", item.get("orders", 0)) for item in time_series]

    rankings = data.get("rankings", [])
    rank_labels = [r["name"][:20] for r in rankings]
    rank_values = [r["value"] for r in rankings]

    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Dashboard analítico de performance e métricas de negócios gerado pelo Ananke OS.">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="Dashboard executivo automatizado gerado pelo Ananke OS.">
    <meta property="og:type" content="website">
    <title>{title} - Ananke OS Batch Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-base: #0f1117;
            --bg-surface: #181b23;
            --bg-card: #202430;
            --primary: #8ab4f8;
            --primary-glow: rgba(138, 180, 248, 0.15);
            --accent: #c58af9;
            --success: #81c995;
            --text-main: #e3e3e3;
            --text-dim: #9aa0a6;
            --border-color: rgba(255, 255, 255, 0.08);
            --radius-lg: 16px;
            --radius-md: 10px;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg-base);
            color: var(--text-main);
            line-height: 1.5;
            padding: 32px;
            min-height: 100vh;
        }}
        h1, h2, h3 {{
            line-height: 1.2;
        }}
        @media (prefers-reduced-motion: reduce) {{
            *, ::before, ::after {{
                animation: none !important;
                transition: none !important;
            }}
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 28px;
            padding-bottom: 20px;
            border-bottom: 1px solid var(--border-color);
        }}
        .header-title h1 {{
            font-size: 28px;
            font-weight: 700;
            background: linear-gradient(135deg, #8ab4f8, #c58af9);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 6px;
        }}
        .header-meta {{
            font-size: 13px;
            color: var(--text-dim);
            display: flex;
            gap: 16px;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 10px;
            background: var(--primary-glow);
            color: var(--primary);
            border-radius: 20px;
            font-size: 12px;
            font-weight: 500;
        }}
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
            margin-bottom: 32px;
        }}
        .kpi-card {{
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 24px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
            transition: transform 0.2s, border-color 0.2s;
        }}
        .kpi-card:hover {{
            transform: translateY(-2px);
            border-color: rgba(138, 180, 248, 0.4);
        }}
        .kpi-label {{
            font-size: 13px;
            font-weight: 500;
            color: var(--text-dim);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 10px;
        }}
        .kpi-value {{
            font-size: 28px;
            font-weight: 700;
            color: var(--text-main);
            font-family: 'JetBrains Mono', monospace;
        }}
        .charts-grid {{
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 24px;
            margin-bottom: 32px;
        }}
        @media (max-width: 960px) {{
            .charts-grid {{ grid-template-columns: 1fr; }}
            body {{ padding: 16px; }}
        }}
        .chart-box {{
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 24px;
        }}
        .chart-box h2 {{
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 20px;
            color: var(--text-main);
        }}
        .table-box {{
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 24px;
            margin-bottom: 32px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 14px;
        }}
        th {{
            padding: 12px 16px;
            background: var(--bg-card);
            color: var(--text-dim);
            font-weight: 600;
            border-bottom: 1px solid var(--border-color);
        }}
        td {{
            padding: 14px 16px;
            border-bottom: 1px solid var(--border-color);
        }}
        tr:hover td {{
            background: rgba(255, 255, 255, 0.02);
        }}
        .footer {{
            text-align: center;
            font-size: 12px;
            color: var(--text-dim);
            padding-top: 24px;
            border-top: 1px solid var(--border-color);
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="header-title">
            <h1>{title}</h1>
            <div class="header-meta">
                <span>Gerado em: <strong>{timestamp_str}</strong></span>
                <span>Template: <span class="badge">{data.get('template', 'default')}</span></span>
                <span>Linhas: <strong>{data.get('total_rows', 0):,}</strong></span>
            </div>
        </div>
    </div>

    <div class="kpi-grid">
        {"".join(kpi_cards_html)}
    </div>

    <div class="charts-grid">
        <div class="chart-box">
            <h2>Evolução Temporal</h2>
            <canvas id="timeSeriesChart" height="130"></canvas>
        </div>
        <div class="chart-box">
            <h2>Top Desempenho</h2>
            <canvas id="rankingChart" height="130"></canvas>
        </div>
    </div>

    <div class="table-box">
        <h2>Top Registros Analisados</h2>
        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th>Dimensão / Categoria</th>
                    <th>Valor Consolidado</th>
                </tr>
            </thead>
            <tbody>
                {"".join([f"<tr><td>#{i}</td><td><strong>{r['name']}</strong></td><td>{format_currency_brl(r['value'])}</td></tr>" for i, r in enumerate(rankings, 1)])}
            </tbody>
        </table>
    </div>

    <div class="footer">
        Ananke OS • Suíte de Automações Periódicas & Batch Processing • {timestamp_str}
    </div>

    <script>
        // Time Series Chart
        const tsCtx = document.getElementById('timeSeriesChart').getContext('2d');
        new Chart(tsCtx, {{
            type: 'line',
            data: {{
                labels: {json.dumps(ts_labels)},
                datasets: [
                    {{
                        label: 'Investimento / Faturamento',
                        data: {json.dumps(ts_spend)},
                        borderColor: '#8ab4f8',
                        backgroundColor: 'rgba(138, 180, 248, 0.1)',
                        fill: true,
                        tension: 0.3
                    }},
                    {{
                        label: 'Conversões / Pedidos',
                        data: {json.dumps(ts_conv)},
                        borderColor: '#81c995',
                        backgroundColor: 'transparent',
                        borderDash: [5, 5],
                        yAxisID: 'y1',
                        tension: 0.3
                    }}
                ]
            }},
            options: {{
                responsive: true,
                scales: {{
                    x: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#9aa0a6' }} }},
                    y: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#9aa0a6' }} }},
                    y1: {{ position: 'right', grid: {{ display: false }}, ticks: {{ color: '#81c995' }} }}
                }},
                plugins: {{
                    legend: {{ labels: {{ color: '#e3e3e3' }} }}
                }}
            }}
        }});

        // Ranking Chart
        const rkCtx = document.getElementById('rankingChart').getContext('2d');
        new Chart(rkCtx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps(rank_labels)},
                datasets: [{{
                    label: 'Consolidado',
                    data: {json.dumps(rank_values)},
                    backgroundColor: 'rgba(197, 138, 249, 0.8)',
                    borderRadius: 6
                }}]
            }},
            options: {{
                indexAxis: 'y',
                responsive: true,
                scales: {{
                    x: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#9aa0a6' }} }},
                    y: {{ grid: {{ display: false }}, ticks: {{ color: '#e3e3e3' }} }}
                }},
                plugins: {{
                    legend: {{ display: false }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""
    return html_content


def render_all(data: Dict[str, Any], output_dir: str, title: Optional[str] = None) -> Tuple[Path, Path]:
    """Render both HTML and Markdown reports, saving with timestamped names."""
    now = datetime.now()
    timestamp_slug = now.strftime("%Y%m%d_%H%M%S")
    timestamp_str = now.strftime("%d/%m/%Y %H:%M:%S")

    final_title = title or data.get("template_title") or "Relatório Executivo Automatizado"

    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    html_file = out_path / f"report_{timestamp_slug}.html"
    md_file = out_path / f"report_{timestamp_slug}.md"

    # Write HTML
    html_content = generate_html_dashboard(data, final_title, timestamp_str)
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    # Write Markdown
    md_content = generate_markdown_report(data, final_title, timestamp_str)
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(md_content)

    return html_file, md_file


def main():
    parser = argparse.ArgumentParser(description="Renderizador de relatórios HTML e Markdown.")
    parser.add_argument("data_json", help="Arquivo JSON de agregação")
    parser.add_argument("--output-dir", "-o", default="./data/reports", help="Diretório de saída")
    parser.add_argument("--title", "-t", default=None, help="Título do relatório")
    args = parser.parse_args()

    try:
        with open(args.data_json, "r", encoding="utf-8") as f:
            data = json.load(f)

        html_path, md_path = render_all(data, args.output_dir, args.title)
        print(f"[OK] Relatórios gerados com sucesso:")
        print(f"  - Dashboard HTML: {html_path.resolve()}")
        print(f"  - Sumário Markdown: {md_path.resolve()}")
    except Exception as e:
        print(f"[ERRO] Falha na renderização: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
