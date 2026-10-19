---
name: email
description: Fluxo unificado para e-mail marketing, cold email outbound B2B, newsletters responsivas, scraping de leads e análise de entregabilidade.
agent: email-marketing-specialist
---

# ✉️ E-mail Marketing & Outbound Engine (/email)

O comando `/email` é a porta de entrada para a criação, automação e análise de campanhas de e-mail no **Ananke OS**. Ele combina estratégia de vendas, redação persuasiva, engenharia de templates HTML à prova de falhas em clientes legados e rotinas de prospecção ativa.

## 🚀 Modos de Operação

O `/email` atende 5 verticais essenciais:

1. **Cold Outreach (B2B):** Redação de cadências frias de 3 a 5 e-mails, com foco em alta entregabilidade, personalização e baixo atrito.
2. **Newsletter & Promo (Inbound):** Criação de newsletters ricas ou comunicados promocionais com diagramação HTML tabular responsiva (600px).
3. **Lead Scraping & Enriquecimento:** Extração e normalização de contatos a partir de páginas corporativas públicas via scripts Python.
4. **Auditoria Anti-Spam & Entregabilidade:** Varredura de gatilhos de spam na copy e checklist de configurações DNS (SPF, DKIM, DMARC, BIMI).
5. **Métricas & Benchmarks:** Avaliação de performance de campanhas (Open Rate, CTR, CTOR, Bounce, Unsubscribe).

---

## 💡 Exemplos de Uso

* `/email Crie uma sequência de cold email de 4 toques para vender consultoria de dados para diretores de e-commerce.`
* `/email Gere uma newsletter semanal de tecnologia em HTML tabular responsivo com inlining de CSS e versão plain text.`
* `/email Extraia contatos corporativos da página https://exemplo.com/equipe e salve em CSV higienizado.`
* `/email Faça uma auditoria anti-spam neste assunto e corpo de e-mail e aponte palavras de risco.`
* `/email Analise estas métricas de disparo: 12.000 enviados, 28% abertura, 1.4% clique e 0.8% bounce.`

---

## ⚙️ O que acontece por baixo dos panos?

1. O `email-marketing-specialist` assume o comando da operação.
2. São ativadas as skills especializadas necessárias:
   * `email-marketing-strategy` para posicionamento e réguas de relacionamento.
   * `cold-email-outreach` para copy persuasiva e prevenção de spam.
   * `email-template-design` para renderização tabular e execução de `inline_styler.py`.
   * `lead-scraping-enrichment` para extração via `lead_scraper.py`.
3. Sinergia automática com `copywriter-ux` (refinamento textual) e `data-analyst` (processamento tabular).
4. Entrega de artefatos prontos para envio ou integração com provedores (Resend, Brevo, SendGrid, etc.).
