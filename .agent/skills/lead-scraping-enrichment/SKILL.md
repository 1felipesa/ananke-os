---
name: lead-scraping-enrichment
description: Prospecção ativa de contatos (leads), raspagem ética da web (web scraping), extração de e-mails corporativos, remoção de falsos positivos e normalização tabular em CSV/JSON.
---

# Prospecção & Raspagem Ética de Leads (Web Scraping & Enrichment)

Esta skill fornece diretrizes e ferramental automatizado para prospecção ativa de contatos B2B em diretórios abertos, páginas corporativas ("Sobre Nós", "Equipe", "Contato") e enriquecimento de bases tabulares.

---

## 🧭 1. Princípios de Prospecção Ética & Conformidade

1. **Apenas Dados Públicos e Abertos:** Extraia apenas informações intencionalmente publicadas em sites corporativos oficiais ou diretórios profissionais públicos.
2. **Respeito ao `robots.txt` e Delays Amigáveis:** Evite rajadas agressivas de requisições que possam sobrecarregar os servidores alvo. Aplique pausas (*delays*) entre requisições.
3. **Higienização Preventiva de Falsos Positivos:**
   * Descarte e-mails genéricos de suporte (`noreply@`, `contato@`, `suporte@`) quando o objetivo for prospecção executiva, a menos que seja o único ponto de entrada para mapear o padrão de domínio (ex: `nome.sobrenome@empresa.com`).
   * Elimine arquivos falsamente capturados por regex (ex: `imagem@2x.png`, `bootstrap@5.3.js`).
4. **Enriquecimento Estruturado:** Sempre armazene o e-mail acompanhado do domínio de origem, nome/cargo inferido (quando disponível) e data da captura.

---

## 💻 2. Script Utilitário: `lead_scraper.py`

A skill disponibiliza um script Python para varredura de páginas corporativas, extração de e-mails válidos via regex rigoroso e exportação direta para CSV higienizado.

### Como Executar:
```bash
# Varredura de uma URL ou lista de URLs
python .agent/skills/lead-scraping-enrichment/scripts/lead_scraper.py https://empresaexemplo.com -o leads.csv

# Varredura a partir de arquivo de texto com múltiplas URLs
python .agent/skills/lead-scraping-enrichment/scripts/lead_scraper.py --file urls.txt -o leads_consolidados.csv
```
