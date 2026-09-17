---
name: strategy
description: Fluxo focado em modelo de negócio, definição de preços, estruturação de pacotes e roadmap estratégico.
agent: orchestrator
---

# 🧠 Estratégia de Negócios (Strategy Workflow)

O comando `/strategy` transforma o sistema em uma consultoria ativa de negócios. Ele não gera código imediatamente; em vez disso, ele foca no modelo comercial, monetização e no escopo do produto mínimo viável (MVP).

## Como Usar

Digite `/strategy` seguido da ideia de negócio ou problema comercial que deseja resolver.

**Exemplos:**
- `/strategy Sou um psicopedagogo e não sei como precificar minhas sessões e criar pacotes mensais. Me ajude a definir um modelo.`
- `/strategy Quero criar um SaaS de gestão de clínicas. Quais as features essenciais para um MVP e qual estratégia de preço sugere?`

## O que acontece por baixo dos panos?

1. O `orchestrator` invoca o `business-strategist`.
2. O estrategista inicia uma entrevista Socrática (se necessário) para entender seu público, seus custos e seu formato de trabalho.
3. Se envolver definição de software (SaaS), o `product-manager` e `product-owner` são trazidos para definir Histórias de Usuário e Roadmap.
4. No final, você recebe um documento de Negócios completo (Business Plan ou plano_precos.md) formatado para alavancar suas vendas.
