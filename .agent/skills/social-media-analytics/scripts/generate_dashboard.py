#!/usr/bin/env python3
import argparse
import os
import re
import json
import sys

def check_dependencies():
    try:
        import pandas
        import openpyxl
    except ImportError:
        print("Erro: As dependências 'pandas' e/ou 'openpyxl' não estão instaladas.", file=sys.stderr)
        print("Por favor, instale executando: pip install pandas openpyxl", file=sys.stderr)
        sys.exit(1)

def parse_markdown_to_html(md_path):
    if not md_path or not os.path.exists(md_path):
        return "<p class='text-gray-400 italic'>Nenhuma análise qualitativa fornecida.</p>"
    
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Process blocks
    lines = content.split('\n')
    html_blocks = []
    in_list = False
    
    for line in lines:
        line = line.strip()
        if not line:
            if in_list:
                html_blocks.append("</ul>")
                in_list = False
            continue
            
        # Headers
        if line.startswith('# '):
            if in_list:
                html_blocks.append("</ul>")
                in_list = False
            html_blocks.append(f'<h2 class="text-2xl font-bold text-[#D0BCFF] mt-6 mb-4 border-b border-[#381E72] pb-2">{line[2:]}</h2>')
        elif line.startswith('## '):
            if in_list:
                html_blocks.append("</ul>")
                in_list = False
            html_blocks.append(f'<h3 class="text-xl font-semibold text-[#CCC2DC] mt-4 mb-2">{line[3:]}</h3>')
        elif line.startswith('### '):
            if in_list:
                html_blocks.append("</ul>")
                in_list = False
            html_blocks.append(f'<h4 class="text-lg font-medium text-purple-300 mt-3 mb-1">{line[4:]}</h4>')
        # Lists
        elif line.startswith('- ') or line.startswith('* '):
            item_text = line[2:]
            # Replace bold
            item_text = re.sub(r'\*\*(.*?)\*\*', r'<strong class="text-white">\1</strong>', item_text)
            if not in_list:
                html_blocks.append('<ul class="list-disc pl-5 mb-4 space-y-2 text-gray-300">')
                in_list = True
            html_blocks.append(f'<li>{item_text}</li>')
        # Paragraphs
        else:
            if in_list:
                html_blocks.append("</ul>")
                in_list = False
            # Replace bold
            line_html = re.sub(r'\*\*(.*?)\*\*', r'<strong class="text-white">\1</strong>', line)
            html_blocks.append(f'<p class="text-gray-300 leading-relaxed mb-4">{line_html}</p>')
            
    if in_list:
        html_blocks.append("</ul>")
        
    return '\n'.join(html_blocks)

def normalize_data(df):
    import pandas as pd
    
    # Lowercase all columns for matching
    cols = [str(c).lower().strip() for c in df.columns]
    
    # Patterns
    patterns = {
        'name': r'(an.ncio|ad.name|creative|t.tulo|anunc|ad_name|campanha|name|nome|post)',
        'spend': r'(gasto|spend|invest|custo|cost|valor|valor.gasto)',
        'impressions': r'(impress.es|impression|exibi..o|exibicao|alcance|reach)',
        'visits': r'(visita|visit|perfil|profile|clique.no.perfil)',
        'followers': r'(seguidor|follower|novo.seguidor|lead|novos)',
        'clicks': r'(clique|click|intera..o|interacao|engaj|engagement|resultado)'
    }
    
    mapped_cols = {}
    for key, pattern in patterns.items():
        for i, col in enumerate(cols):
            if re.search(pattern, col):
                mapped_cols[key] = df.columns[i]
                break
                
    # If not found, fallbacks
    if 'name' not in mapped_cols and len(df.columns) > 0:
        mapped_cols['name'] = df.columns[0] # assume 1st column is name
        
    cleaned_df = pd.DataFrame()
    
    # Populate cleaned df
    cleaned_df['Ad Name'] = df[mapped_cols['name']].astype(str) if 'name' in mapped_cols else df.index.astype(str)
    
    for key in ['spend', 'impressions', 'visits', 'followers', 'clicks']:
        if key in mapped_cols:
            # Convert to numeric, replace NaN with 0
            cleaned_df[key.capitalize()] = pd.to_numeric(df[mapped_cols[key]], errors='coerce').fillna(0)
        else:
            cleaned_df[key.capitalize()] = 0.0
            
    return cleaned_df

def main():
    parser = argparse.ArgumentParser(description="Gera painel HTML com resultados de campanhas das redes sociais.")
    parser.add_argument("--xlsx", required=True, help="Caminho da planilha Excel (.xlsx)")
    parser.add_argument("--md", required=False, help="Caminho da análise qualitativa em Markdown (.md)")
    parser.add_argument("--out", default="dashboard.html", help="Caminho de saída do dashboard HTML")
    
    args = parser.parse_args()
    
    check_dependencies()
    import pandas as pd
    
    # Read Excel
    try:
        df = pd.read_excel(args.xlsx)
    except Exception as e:
        print(f"Erro ao ler arquivo Excel: {e}", file=sys.stderr)
        sys.exit(1)
        
    cleaned_df = normalize_data(df)
    
    # Calculate global metrics
    total_spend = float(cleaned_df['Spend'].sum())
    total_impressions = int(cleaned_df['Impressions'].sum())
    total_visits = int(cleaned_df['Visits'].sum())
    total_followers = int(cleaned_df['Followers'].sum())
    total_clicks = int(cleaned_df['Clicks'].sum())
    
    # Choose primary metric for sorting
    primary_metric = 'Followers' if total_followers > 0 else ('Visits' if total_visits > 0 else 'Clicks')
    primary_label = 'Novos Seguidores' if primary_metric == 'Followers' else ('Visitas ao Perfil' if primary_metric == 'Visits' else 'Interações')
    
    # Calculate costs
    cost_per_follower = total_spend / total_followers if total_followers > 0 else 0
    cost_per_visit = total_spend / total_visits if total_visits > 0 else 0
    cost_per_click = total_spend / total_clicks if total_clicks > 0 else 0
    
    # Sort ads to find winners and losers (only for active ads with >0 reach/impressions or >0 results)
    active_ads = cleaned_df[(cleaned_df['Impressions'] > 0) | (cleaned_df[primary_metric] > 0)].copy()
    
    if len(active_ads) == 0:
        active_ads = cleaned_df.copy()
        
    # Cost per result calculation per ad for sorting
    if total_spend > 0:
        # If there is spend, lower cost per result is better.
        # Avoid division by zero by setting a penalty for 0 results.
        active_ads['Cost_Per_Result'] = active_ads.apply(
            lambda r: r['Spend'] / r[primary_metric] if r[primary_metric] > 0 else (r['Spend'] * 1000 if r['Spend'] > 0 else 999999), axis=1
        )
        # Winners = lowest cost per result
        winners = active_ads.sort_values(by='Cost_Per_Result', ascending=True).head(3)
        # Losers = highest cost per result, but must have spend > 0 to be a loss
        losers = active_ads[active_ads['Spend'] > 0].sort_values(by='Cost_Per_Result', ascending=False).head(3)
    else:
        # If no spend, sort purely by primary result
        winners = active_ads.sort_values(by=primary_metric, ascending=False).head(3)
        losers = active_ads.sort_values(by=primary_metric, ascending=True).head(3)
        
    winners_list = winners.to_dict(orient='records')
    losers_list = losers.to_dict(orient='records')
    
    # Prepare chart data (Top 10 ads by primary metric)
    top_chart_data = cleaned_df.sort_values(by=primary_metric, ascending=False).head(10)
    chart_labels = top_chart_data['Ad Name'].tolist()
    chart_values = top_chart_data[primary_metric].tolist()
    chart_spends = top_chart_data['Spend'].tolist()
    
    # Read qualitative analysis
    qualitative_html = parse_markdown_to_html(args.md)
    
    # Render dashboard template
    html_template = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Painel de Performance - Redes Sociais</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{
                        sans: ['Outfit', 'sans-serif'],
                    }},
                    colors: {{
                        m3: {{
                            background: '#1C1B1F',
                            surface: '#25232A',
                            surfaceVariant: '#49454F',
                            primary: '#D0BCFF',
                            onPrimary: '#381E72',
                            secondary: '#CCC2DC',
                            onSecondary: '#332D41',
                            error: '#F2B8B5',
                            onError: '#601410',
                            outline: '#938F99',
                            success: '#81C784'
                        }}
                    }}
                }}
            }}
        }}
    </script>
    <style>
        body {{
            background-color: #1C1B1F;
            color: #E6E1E5;
        }}
    </style>
</head>
<body class="min-h-screen pb-16 font-sans">
    <!-- Header -->
    <header class="bg-m3-surface border-b border-m3-surfaceVariant px-6 py-6 lg:px-12 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
            <span class="text-xs uppercase tracking-widest text-m3-primary font-semibold">Relatório Executivo</span>
            <h1 class="text-3xl font-bold text-white tracking-tight mt-1">Desempenho de Presença Digital</h1>
        </div>
        <div class="text-left md:text-right bg-m3-surfaceVariant/30 px-4 py-2 rounded-2xl border border-m3-surfaceVariant/50">
            <span class="text-xs text-m3-outline block">Métrica Principal</span>
            <span class="text-lg font-bold text-m3-secondary">{primary_label}</span>
        </div>
    </header>

    <main class="max-w-7xl mx-auto px-6 lg:px-12 mt-10 space-y-10">
        
        <!-- KPI Row -->
        <section class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <!-- KPI Gasto -->
            <div class="bg-m3-surface border border-m3-surfaceVariant/50 p-6 rounded-3xl hover:border-m3-primary/30 transition-all duration-300">
                <span class="text-xs font-medium text-m3-outline uppercase block">Investimento Total</span>
                <span class="text-2xl md:text-3xl font-bold text-white block mt-2">R$ {total_spend:,.2f}</span>
                <span class="text-xs text-m3-outline mt-1 block">Recurso utilizado nos anúncios</span>
            </div>

            <!-- KPI Alcance -->
            <div class="bg-m3-surface border border-m3-surfaceVariant/50 p-6 rounded-3xl hover:border-m3-primary/30 transition-all duration-300">
                <span class="text-xs font-medium text-m3-outline uppercase block">Visualizações / Alcance</span>
                <span class="text-2xl md:text-3xl font-bold text-white block mt-2">{total_impressions:,}</span>
                <span class="text-xs text-m3-outline mt-1 block">Vezes que sua marca apareceu</span>
            </div>

            <!-- KPI Resultado Principal -->
            <div class="bg-m3-surface border border-m3-surfaceVariant/50 p-6 rounded-3xl hover:border-m3-primary/30 transition-all duration-300">
                <span class="text-xs font-medium text-m3-outline uppercase block">{primary_label}</span>
                <span class="text-2xl md:text-3xl font-bold text-m3-primary block mt-2">+{cleaned_df[primary_metric].sum():,.0f}</span>
                <span class="text-xs text-m3-outline mt-1 block">Pessoas engajadas ou atraídas</span>
            </div>

            <!-- KPI Custo Unitário -->
            <div class="bg-m3-surface border border-m3-surfaceVariant/50 p-6 rounded-3xl hover:border-m3-primary/30 transition-all duration-300">
                <span class="text-xs font-medium text-m3-outline uppercase block">Custo por Resultado</span>
                <span class="text-2xl md:text-3xl font-bold text-white block mt-2">
                    {"R$ " + f"{total_spend / cleaned_df[primary_metric].sum():,.2f}" if cleaned_df[primary_metric].sum() > 0 and total_spend > 0 else "N/A"}
                </span>
                <span class="text-xs text-m3-outline mt-1 block">Custo unitário do objetivo principal</span>
            </div>
        </section>

        <!-- Charts and Breakdown -->
        <section class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- Chart Card -->
            <div class="bg-m3-surface border border-m3-surfaceVariant/50 p-6 rounded-3xl lg:col-span-2">
                <h2 class="text-xl font-bold text-white mb-6">Top 10 Anúncios por {primary_label}</h2>
                <div class="relative h-[300px] w-full">
                    <canvas id="performanceChart"></canvas>
                </div>
            </div>

            <!-- Cost Comparison Card -->
            <div class="bg-m3-surface border border-m3-surfaceVariant/50 p-6 rounded-3xl flex flex-col justify-between">
                <div>
                    <h2 class="text-xl font-bold text-white mb-4">Custo Unitário Médio</h2>
                    <p class="text-sm text-m3-outline mb-6">Comparação do custo de atração para cada objetivo das campanhas.</p>
                </div>
                <div class="space-y-4 mb-4">
                    <!-- Seguidor -->
                    <div class="bg-m3-surfaceVariant/30 p-4 rounded-2xl border border-m3-surfaceVariant/30">
                        <span class="text-xs text-m3-outline block">Custo por Novo Seguidor</span>
                        <span class="text-xl font-bold text-white block mt-1">
                            {f"R$ {cost_per_follower:,.2f}" if cost_per_follower > 0 else "Sem registros"}
                        </span>
                    </div>
                    <!-- Visita -->
                    <div class="bg-m3-surfaceVariant/30 p-4 rounded-2xl border border-m3-surfaceVariant/30">
                        <span class="text-xs text-m3-outline block">Custo por Visita ao Perfil</span>
                        <span class="text-xl font-bold text-white block mt-1">
                            {f"R$ {cost_per_visit:,.2f}" if cost_per_visit > 0 else "Sem registros"}
                        </span>
                    </div>
                    <!-- Clique -->
                    <div class="bg-m3-surfaceVariant/30 p-4 rounded-2xl border border-m3-surfaceVariant/30">
                        <span class="text-xs text-m3-outline block">Custo por Clique / Interação</span>
                        <span class="text-xl font-bold text-white block mt-1">
                            {f"R$ {cost_per_click:,.2f}" if cost_per_click > 0 else "Sem registros"}
                        </span>
                    </div>
                </div>
            </div>
        </section>

        <!-- Winners and Opportunities -->
        <section class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Winners Card -->
            <div class="bg-m3-surface border border-m3-surfaceVariant/50 p-6 rounded-3xl">
                <div class="flex items-center gap-3 mb-6">
                    <div class="w-8 h-8 rounded-full bg-m3-success/20 flex items-center justify-center text-m3-success">
                        ★
                    </div>
                    <h2 class="text-xl font-bold text-white">Anúncios Vencedores (Destaques)</h2>
                </div>
                <div class="space-y-4">
                    {"" if winners_list else "<p class='text-gray-400 italic text-sm'>Nenhum dado ativo disponível.</p>"}
                    {"".join([f'''
                    <div class="bg-m3-surfaceVariant/10 p-4 rounded-2xl border border-m3-success/20">
                        <span class="text-sm font-semibold text-white block truncate">{w['Ad Name']}</span>
                        <div class="flex justify-between items-center mt-3 text-xs text-m3-outline">
                            <span>Resultado: <strong class="text-m3-success">+{w[primary_metric]:,.0f} {primary_label}</strong></span>
                            <span>Investimento: <strong>R$ {w['Spend']:,.2f}</strong></span>
                        </div>
                    </div>
                    ''' for w in winners_list])}
                </div>
            </div>

            <!-- Opportunities Card -->
            <div class="bg-m3-surface border border-m3-surfaceVariant/50 p-6 rounded-3xl">
                <div class="flex items-center gap-3 mb-6">
                    <div class="w-8 h-8 rounded-full bg-m3-error/20 flex items-center justify-center text-m3-error">
                        ⚠
                    </div>
                    <h2 class="text-xl font-bold text-white">Oportunidades de Melhoria (Custo Alto)</h2>
                </div>
                <div class="space-y-4">
                    {"" if losers_list else "<p class='text-gray-400 italic text-sm'>Nenhum anúncio com custo identificável.</p>"}
                    {"".join([f'''
                    <div class="bg-m3-surfaceVariant/10 p-4 rounded-2xl border border-m3-error/20">
                        <span class="text-sm font-semibold text-white block truncate">{l['Ad Name']}</span>
                        <div class="flex justify-between items-center mt-3 text-xs text-m3-outline">
                            <span>Resultado: <strong class="text-m3-error">+{l[primary_metric]:,.0f} {primary_label}</strong></span>
                            <span>Investimento: <strong>R$ {l['Spend']:,.2f}</strong></span>
                        </div>
                    </div>
                    ''' for l in losers_list])}
                </div>
            </div>
        </section>

        <!-- Qualitative insights and observations -->
        <section class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- MD Qualitative file content -->
            <div class="bg-m3-surface border border-m3-surfaceVariant/50 p-8 rounded-3xl lg:col-span-2">
                <h2 class="text-xl font-bold text-white mb-6 flex items-center gap-2">
                    <span class="text-m3-primary">🗎</span> Análise Qualitativa e Observações
                </h2>
                <div class="prose prose-invert max-w-none">
                    {qualitative_html}
                </div>
            </div>

            <!-- High Level Action Plan -->
            <div class="bg-m3-primary/10 border border-m3-primary/20 p-8 rounded-3xl flex flex-col justify-between">
                <div>
                    <span class="text-xs uppercase tracking-wider text-m3-primary font-bold">Plano de Ação</span>
                    <h2 class="text-2xl font-bold text-white mt-1 mb-4">Recomendações do Especialista</h2>
                    <ul class="space-y-4 mt-6 text-sm text-gray-200">
                        <li class="flex items-start gap-3">
                            <span class="text-m3-primary text-lg">✔</span>
                            <span><strong>Pressione os Vencedores:</strong> Aloque mais orçamento nos top 3 anúncios que possuem menor custo por seguidor/visita.</span>
                        </li>
                        <li class="flex items-start gap-3">
                            <span class="text-m3-primary text-lg">✔</span>
                            <span><strong>Ajuste os Criativos:</strong> Identifique no texto qualitativo o formato/copy dos anúncios com pior desempenho e suspenda-os para evitar desperdício.</span>
                        </li>
                        <li class="flex items-start gap-3">
                            <span class="text-m3-primary text-lg">✔</span>
                            <span><strong>Foque no Perfil:</strong> Para campanhas de reconhecimento, certifique-se de que a biografia e os destaques do perfil estejam atualizados para otimizar a conversão de visitas em seguidores.</span>
                        </li>
                    </ul>
                </div>
                <div class="mt-8 pt-6 border-t border-m3-primary/10 text-xs text-m3-outline">
                    Gerado automaticamente pelo Agente de Análise de Redes Sociais.
                </div>
            </div>
        </section>

    </main>

    <script>
        const ctx = document.getElementById('performanceChart').getContext('2d');
        new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps(chart_labels)},
                datasets: [{{
                    label: '{primary_label}',
                    data: {json.dumps(chart_values)},
                    backgroundColor: '#D0BCFF',
                    borderRadius: 12,
                    borderSkipped: false,
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }},
                scales: {{
                    x: {{
                        grid: {{
                            display: false
                        }},
                        ticks: {{
                            color: '#938F99',
                            font: {{
                                family: 'Outfit'
                            }},
                            callback: function(val, index) {{
                                // Truncate long labels
                                let label = this.getLabelForValue(val);
                                return label.length > 15 ? label.substr(0, 15) + '...' : label;
                            }}
                        }}
                    }},
                    y: {{
                        grid: {{
                            color: '#49454F'
                        }},
                        ticks: {{
                            color: '#938F99',
                            font: {{
                                family: 'Outfit'
                            }}
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""
    
    # Write output
    try:
        with open(args.out, 'w', encoding='utf-8') as f:
            f.write(html_template)
        print(f"Sucesso: Dashboard gerado com êxito em {args.out}")
    except Exception as e:
        print(f"Erro ao salvar arquivo HTML de saída: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
