# Template de Conector de API / Servidor MCP

Este é o modelo de referência estrutural para novos conectores gerados pelo agente `integration-engineer` através do comando `/connect`.

---

## 📋 Pré-requisitos & Configuração

1. Copie o arquivo `.env.example` para `.env`:
   ```bash
   cp .env.example .env
   ```
2. Preencha as credenciais obtidas no painel de desenvolvedor do serviço.
3. Instale as dependências:
   ```bash
   npm install
   # ou para Python:
   pip install -r requirements.txt
   ```

---

## 🩺 Como Testar a Conexão (Smoke Test)

Antes de integrar no código do seu produto ou registrar no Ananke OS IDE, execute o teste de saúde:

```bash
npx ts-node test_connection.ts
# ou para Python:
python test_connection.py
```

Se a autenticação e os endpoints estiverem corretos, o console exibirá:
`[OK] Conexão estabelecida com sucesso! Status: 200 OK`
