---
name: social-media-analytics
description: Analyzes social media campaign results, parses advertising spreadsheets (.xlsx) and qualitative analysis files (.md), identifies top/worst performing ads, and generates interactive Material Design 3 dark-themed HTML dashboards.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Social Media Analytics Skill

Specialized knowledge and script tools to parse, analyze, and visualize social media metrics from campaign exports and qualitative feedback.

---

## 1. Core Objectives for Analysis

When auditing social media performance, focus on these analysis vectors:

1.  **Efficiency Analysis**: Calculate cost per results (e.g., Custo por Seguidor, Custo por Visita, Custo por Clique) to identify which campaigns are financially efficient.
2.  **Creative & Copy Correlation**: Match the qualitative analysis in `.md` (which details ad hooks, images, copy tone) with quantitative metrics in `.xlsx` to discover *why* certain ads performed well.
3.  **Pattern Recognition**: Segment ads by format (Image, Carousel, Video/Reels) and copy style to find the overall winning creative recipe.
4.  **Actionable Recommendations**: Deliver a concise "O que fazer a seguir" (Next Steps) list in plain Portuguese for business owners.

---

## 2. Spreadsheet Column Mapping

Social media exports vary by platform (Meta/Facebook Ads, Instagram, Google Ads). The python parser must robustly map varied header names to normalized internal metrics:

| Normalized Metric | Common Excel Headers |
|-------------------|----------------------|
| **Ad Name**       | Nome do anúncio, Ad Name, Creative, Título |
| **Spend**         | Valor gasto, Gasto, Spend, Valor investido, Cost |
| **Impressions**   | Impressões, Impressions, Exibições |
| **Reach**         | Alcance, Reach |
| **Profile Visits**| Visitas ao perfil, Profile visits, Cliques no perfil |
| **Followers**     | Seguidores, Novos seguidores, Followers, Leads |
| **Interactions**  | Interações, Cliques, Cliques no link, Engajamento, Clicks, Results |

---

## 3. Python Helper Script: `generate_dashboard.py`

This skill includes an automated dashboard builder at `scripts/generate_dashboard.py`.

### Execution Command:
```bash
python .agent/skills/social-media-analytics/scripts/generate_dashboard.py --xlsx <caminho_da_planilha> --md <caminho_do_markdown> --out <caminho_do_painel_html>
```

### Dashboard Content Sections:
1.  **KPI Header Summary**: Metric cards for total investment, total reach/impressions, total followers/profile visits, and average cost per result.
2.  **Performance Charts**: Interactive charts (Reach/Impressions over time, Followers/Visits comparison) via Chart.js or ApexCharts.
3.  **Ad Standouts**: Distinct listings of **Melhores Anúncios (Destaques)** and **Oportunidades de Melhoria (Pior Desempenho)**.
4.  **Qualitative Synthesis**: The user's own analysis and observations (parsed from the `.md` file) rendered cleanly.
5.  **Executive Insights**: AI-generated or structured recommendations with direct steps to improve CTR, followers, and costs.
