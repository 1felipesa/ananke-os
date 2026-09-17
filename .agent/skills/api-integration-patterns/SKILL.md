---
name: api-integration-patterns
description: Padrões avançados de engenharia de integrações, conectores de APIs e servidores MCP (Model Context Protocol). Cobre arquitetura Stdio/SSE, autenticação segura (OAuth2, API Keys), resiliência com backoff e scripts de healthcheck.
---

# Padrões de Integração de APIs & Servidores MCP

Esta skill fornece diretrizes de engenharia, arquitetura e resiliência para conceber, desenvolver e testar **conectores de APIs externas** e **servidores MCP** (Model Context Protocol).

---

## 🏛️ 1. Arquitetura de Servidores MCP (Model Context Protocol)

O protocolo MCP padroniza a forma como sistemas de IA descobrem e executam ferramentas (*Tools*), leem dados estruturados (*Resources*) e recebem *Prompts*.

### Tipos de Transporte

| Transporte | Protocolo Base | Caso de Uso Primário | Configuração Típica |
| :--- | :--- | :--- | :--- |
| **Stdio (Padrão)** | Entrada/Saída padrão (stdin/stdout) | Ferramentas locais, CLIs, scripts de máquina e IDEs | Executado como subprocesso local (`npx`, `python -m`) |
| **SSE (Server-Sent Events)** | HTTP Streaming unidirecional + POST | Conexões remotas, containers Docker, nuvem e microsserviços | Porta HTTP dedicada (`http://localhost:8000/sse`) |

### Regras de Ouro na Criação de MCP Tools

1. **Nomes Semânticos e Diretos:** Use verbos de ação explícitos em snake_case (ex: `query_database`, `fetch_invoice`, `send_slack_message`).
2. **Schemas JSON Estritos:** Sempre declare tipos explícitos (`string`, `integer`, `boolean`, `array`, `object`) e liste propriedades obrigatórias (`required`).
3. **Descrições Contextuais Ricas:** A IA decide se chama a ferramenta baseando-se na descrição. Explique com clareza **o que a ferramenta faz**, **quando usá-la** e **o significado de parâmetros críticos**.
4. **Respostas Estruturadas:** Retorne objetos previsíveis contendo `status`, `data` e `error` (se houver).

---

## 🛡️ 2. Segurança e Gestão de Credenciais

### Princípio Zero Trust para Secrets
* **PROIBIÇÃO ABSOLUTA:** Jamais armazene chaves de API, segredos de cliente ou tokens privados em código-fonte de conectores.
* **Uso de Variáveis de Ambiente:** Sempre carregue segredos via `process.env` (Node.js) ou `os.environ` / `pydantic-settings` (Python).
* **Arquivo `.env.example` Obrigatório:** Toda pasta de integração deve incluir um arquivo `.env.example` documentando as variáveis necessárias com valores fictícios e descrições claras de onde obtê-las.

### Padrões de Autenticação

1. **API Keys / Bearer Tokens:**
   * Enviar via cabeçalho HTTP seguro (`Authorization: Bearer <token>` ou `X-API-Key: <key>`).
2. **OAuth2 (Client Credentials & Authorization Code):**
   * Automatizar a rotação e renovação de `access_token` usando o `refresh_token` antes da expiração.
3. **Webhooks com HMAC:**
   * Sempre verificar a assinatura no cabeçalho da requisição (ex: `X-Hub-Signature-256`, `Stripe-Signature`) usando tempo constante para prevenir ataques de timing.

---

## ⚡ 3. Resiliência e Tolerância a Falhas

APIs externas sofrem lentidões, limites de cota e instabilidades de rede. Conectores de alta qualidade devem implementar:

### A. Exponential Backoff com Jitter
Para erros temporários de rede ou status HTTP `429 (Too Many Requests)` e `5xx`:
$$\text{Delay} = 2^{\text{tentativa}} \times 1000\text{ms} + \text{random}(0, 500)\text{ms}$$

### B. Timeouts Explícitos
Nunca faça chamadas HTTP sem timeout definido. Padrão recomendado:
* Conexão: 5 segundos.
* Leitura/Resposta: 15 a 30 segundos.

### C. Circuit Breaker
Se um serviço externo falhar consecutivamente 5 vezes, interrompa novas chamadas imediatamente por 60 segundos antes de tentar novamente, protegendo a aplicação contra travamentos em cascata.

---

## 🩺 4. Padrão de Healthcheck & Smoke Test

Toda integração criada deve ser acompanhada de um script executável chamado `test_connection.{ts|py}`.

### O que o Smoke Test deve verificar:
1. **Presença das Chaves:** Valida se as variáveis de ambiente necessárias estão preenchidas no `.env`.
2. **Conectividade Básica (Ping):** Dispara uma requisição leve de leitura (ex: `GET /v1/me` ou `GET /health` ou `GET /users?limit=1`).
3. **Diagnóstico Amigável no Terminal:**
   * Se der sucesso: Exibe `[OK] Conexão estabelecida com sucesso!` e mostra o status `200` e a conta/projeto conectado.
   * Se falhar por autenticação (`401/403`): Exibe `[ERRO] Credencial inválida ou escopo insuficiente`.
   * Se falhar por cota (`429`): Exibe `[ALERTA] Limite de requisições atingido no provedor`.
