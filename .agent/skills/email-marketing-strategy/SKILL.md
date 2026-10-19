---
name: email-marketing-strategy
description: Estratégia de e-mail marketing, arquitetura de réguas de automação (lifecycle), segmentação de audiência, KPIs analíticos e benchmarks de conversão.
---

# Estratégia de E-mail Marketing & Lifecycle Funnels

Esta skill consolida os princípios estratégicos para arquitetar funis de e-mail de alta conversão, réguas automatizadas de relacionamento e mensuração cirúrgica de métricas de desempenho.

---

## 🎯 1. Arquitetura de Réguas de Automação (Lifecycle Flows)

### 1.1 Régua de Boas-Vindas & Onboarding (Welcome Series)
* **Objetivo:** Estabelecer autoridade, alinhar expectativas e incentivar a primeira interação.
* **Cadência Típica (3 e-mails):**
  * **E-mail 1 (Imediato):** Entrega da promessa/recurso gratuito + Quem somos + O que esperar.
  * **E-mail 2 (+2 dias):** A história/propósito de origem + O maior erro que o público comete.
  * **E-mail 3 (+4 dias):** Estudo de caso/prova social + Chamada para o próximo passo lógico.

### 1.2 Régua de Nutrição de Leads (Lead Nurturing)
* **Objetivo:** Educar o lead ao longo da jornada de compra, alternando valor técnico e oferta.
* **Proporção de Valor (Regra 80/20):** 80% do conteúdo focado em resolver problemas práticos sem pedir nada; 20% focado em demonstrar a solução paga.

### 1.3 Régua de Carrinho / Checkout Abandonado
* **Objetivo:** Recuperar vendas com timing de alta urgência.
* **Cadência Típica (3 e-mails):**
  * **E-mail 1 (1 hora após abandono):** Lembrete prestativo ("Houve algum problema com o pagamento?").
  * **E-mail 2 (24 horas após):** Quebra de objeções frequentes + depoimentos de compradores.
  * **E-mail 3 (48 horas após):** Escassez real ("Seu carrinho será liberado para a fila").

### 1.4 Régua de Reengajamento & Limpeza de Base (Win-back & Sunset Flow)
* **Objetivo:** Reativar contatos dormentes (sem abertura há 60-90 dias) ou removê-los para preservar a reputação do remetente.
* **Mensagem Clássica:** "Ainda faz sentido mantermos contato?" com botão de confirmação e descadastro automático se inativo.

---

## 👥 2. Matriz de Segmentação de Audiência

Nunca envie a mesma mensagem para toda a base. Segmente por:
1. **Engajamento Recente:** Ativos (abriram nos últimos 30 dias), Regulares (31-60 dias), Em Risco (61-90 dias) e Inativos (>90 dias).
2. **Estágio de Consciência:** Inconsciente do problema $\rightarrow$ Consciente do problema $\rightarrow$ Consciente da solução $\rightarrow$ Consciente do produto $\rightarrow$ Totalmente consciente.
3. **Comportamento de Compra:** Não compradores (Leads), Compradores de Primeira Viagem, Clientes Recorrentes (VIPs) e Ex-clientes.

---

## 📊 3. Métricas Vitais & Benchmarks da Indústria

| Métrica | Fórmula de Cálculo | Benchmark Médio B2B/B2C | Diagnóstico de Saúde |
| :--- | :--- | :--- | :--- |
| **Open Rate (Taxa de Abertura)** | $\frac{\text{Aberturas Únicas}}{\text{E-mails Entregues}} \times 100$ | **20% a 30%** | Abaixo de 15% indica linhas de assunto fracas ou problemas de entregabilidade/spam. |
| **Click-Through Rate (CTR)** | $\frac{\text{Cliques Únicos}}{\text{E-mails Entregues}} \times 100$ | **2% a 4%** | Avalia a atratividade do e-mail como um todo. |
| **Click-to-Open Rate (CTOR)** | $\frac{\text{Cliques Únicos}}{\text{Aberturas Únicas}} \times 100$ | **9% a 15%** | Mede a qualidade e persuasão do conteúdo interno pós-abertura. |
| **Reply Rate (Taxa de Resposta)** | $\frac{\text{Respostas}}{\text{E-mails Entregues}} \times 100$ | **5% a 12% (Cold Mail)** | Métrica rainha do outbound. |
| **Bounce Rate (Rejeição)** | $\frac{\text{Bounces Totais}}{\text{E-mails Enviados}} \times 100$ | **< 2%** | Acima de 2% arrisca suspensão imediata no provedor (SES, SendGrid, etc.). |
| **Unsubscribe Rate** | $\frac{\text{Descadastros}}{\text{E-mails Entregues}} \times 100$ | **< 0.5%** | Acima de 0.5% sinaliza conteúdo desalinhado com a expectativa do lead. |
