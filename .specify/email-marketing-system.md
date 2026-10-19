# Especificação Funcional: Subsistema de E-mail Marketing & Outbound

> **Módulo:** Ananke OS E-mail Marketing Suite  
> **Tagline:** Spec-Driven Lifecycle & Outbound Engineering  
> **Metodologia:** Spec-Driven Development (SDD) com Sintaxe EARS  
> **Status:** Aprovado / Baseline Operacional (Fase 1 - SPECIFY)  
> **Classificação:** Módulo Especialista de Aquisição & Retenção (P1)

---

## 1. Visão Geral e Propósito

Este módulo estabelece a esteira de engenharia de e-mail marketing, cadências de prospecção fria B2B (Cold Outreach), diagramação de templates em HTML tabular compatível com 60+ clientes (Outlook, Gmail, Apple Mail) e prospecção ativa ética de contatos no **Ananke OS**.

---

## 2. Requisitos do Sistema (Sintaxe EARS)

### 2.1 Requisitos Onipresentes (Ubiquitous)
* **UBIQ-EML-01:** O sistema DEVE garantir conformidade técnica estrita de entregabilidade de e-mail, exigindo e validando registros DNS (SPF, DKIM, DMARC e alinhamento de envelope).
* **UBIQ-EML-02:** O sistema DEVE codificar templates de e-mail em HTML tabular baseado em elementos `<table>`, `<tr>` e `<td>`, mantendo largura fixa máxima de 600px, fontes seguras de fallback e CSS inline obrigatório.
* **UBIQ-EML-03:** O sistema DEVE gerar automaticamente uma versão em texto simples (*Plain Text mirror*) idêntica em conteúdo para todo template HTML compilado.
* **UBIQ-EML-04:** O sistema DEVE submeter todo texto de e-mail ao cálculo preditivo de pontuação anti-spam (*Spam Trigger Words Score*), sinalizando gatilhos promocionais excessivos.

### 2.2 Requisitos Disparados por Eventos (Event-Driven)
* **EVT-EML-01:** QUANDO o operador invocar o comando `/email` ou o agente `email-marketing-specialist`, o sistema DEVE guiar interativamente a definição da régua ou campanha (Cold Outreach, Newsletter, Recuperação, Scraping).
* **EVT-EML-02:** QUANDO o script `inline_styler.py` for executado sobre um arquivo HTML, o sistema DEVE converter todas as regras de folhas de estilo `<style>` em atributos `style="..."` inline nos elementos correspondentes.
* **EVT-EML-03:** QUANDO o script `lead_scraper.py` for acionado com um domínio institucional ou URL pública, o sistema DEVE extrair e-mails válidos através de regex, filtrar arquivos estáticos e exportar uma planilha CSV estruturada.

### 2.3 Requisitos Baseados em Estado (State-Driven)
* **STA-EML-01:** ENQUANTO uma cadência de prospecção fria B2B estiver sendo redigida, o sistema DEVE restringir o tamanho de cada e-mail a um intervalo de 50 a 125 palavras, exigindo CTAs de baixa fricção.
* **STA-EML-02:** ENQUANTO métricas de campanha forem analisadas, o sistema DEVE calcular e exibir taxas padronizadas de Entrega, Abertura, Cliques (CTR), Cliques sobre Abertura (CTOR) e Unsubscribe.

### 2.4 Requisitos de Tratamento de Exceções e Indesejados (Unwanted)
* **UNW-EML-01:** O sistema NUNCA DEVE sugerir ou realizar compra de listas de e-mails de terceiros ou prospecção em massa sem base de legitimidade.
* **UNW-EML-02:** O sistema NUNCA DEVE gerar templates com `<div>` flutuantes, `position: absolute`, flexbox ou CSS moderno não suportado por motores legados do Microsoft Word/Outlook.
