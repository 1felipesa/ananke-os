---
name: api-design
description: Fluxo focado na criação de contratos de API, especificações OpenAPI e arquitetura de integração.
agent: api-designer
---

# 🔌 Design de API (API Design Workflow)

O comando `/api-design` é a porta de entrada para definir como os sistemas conversam entre si, **antes** de escrever uma única linha de código. Ele garante que integrações complexas e serviços internos tenham contratos sólidos.

## Como Usar

Digite `/api-design` seguido dos requisitos da sua integração.

**Exemplos:**
- `/api-design Preciso desenhar uma API REST para um sistema de e-commerce (produtos, carrinho, checkout) usando padrão OpenAPI.`
- `/api-design Como devo estruturar os webhooks para receber atualizações da API do Facebook Graph sobre novos leads?`

## O que acontece por baixo dos panos?

1. O `api-designer` carrega a skill de padrões de API (`api-patterns`).
2. Ele define as rotas (endpoints), os verbos HTTP corretos (GET, POST, PUT, DELETE), os códigos de status (200, 400, 404, 500) e os *payloads* esperados de requisição e resposta.
3. Se solicitado, ele constrói o arquivo `swagger.yaml` ou `openapi.json` completo, servindo de contrato blindado para as equipes de Frontend e Backend implementarem com segurança.
