---
name: connect
description: Fluxo focado em pesquisar, estruturar e implementar conexões com APIs externas e servidores MCP (Model Context Protocol).
agent: integration-engineer
---

# 🔌 Conexão de APIs & MCP (Connect Workflow)

O comando `/connect` é o canal oficial para conectar o seu sistema a qualquer serviço externo da internet (CRMs, gateways de pagamento, plataformas de anúncios, inteligências artificiais ou ferramentas de produtividade).

Em vez de você ter que ler centenas de páginas de documentação técnica ou adivinhar formatos de autenticação, o `integration-engineer` assume o trabalho pesado de pesquisa, te orienta a gerar as credenciais certas e entrega o conector pronto com um teste de conexão executável.

---

## Como Usar

Digite `/connect` seguido do nome do serviço, biblioteca ou link da documentação oficial.

**Exemplos:**
- `/connect Stripe`
- `/connect HubSpot via MCP`
- `/connect https://developers.notion.com/reference`
- `/connect Criar servidor MCP para ler dados do meu banco local PostgreSQL`

---

## O Ciclo Operacional em 4 Passos

1. **Investigação & Viabilidade:** O agente pesquisa a documentação oficial na web, descobre a autenticação necessária e verifica se já existe solução MCP pronta na comunidade.
2. **Decisão de Stack:** O agente te pergunta se você prefere implementar em **TypeScript/Node.js** ou em **Python**.
3. **Guia Passo a Passo de Credenciais:** Você recebe um tutorial rápido indicando exatamente em que tela do provedor você deve clicar para gerar as chaves de API e preencher o `.env`.
4. **Código & Teste de Conexão:** O conector é salvo em `integrations/{servico}/` junto com um script `test_connection` para você rodar no terminal e confirmar que o handshake foi um sucesso.
