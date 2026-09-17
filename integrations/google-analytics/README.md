# Integração Google Analytics (GA4) • Ananke OS

> Guia seguro de configuração de credenciais para consultas automatizadas do Google Analytics via MCP.

---

## 🔐 Como Configurar a Conta de Serviço (Service Account)

Para que o agente `@marketing-analyst` ou `@data-analyst` consulte métricas do Google Analytics sem exigir login interativo:

1. **Acesse o Google Cloud Console:**
   - Crie ou selecione um projeto (ex: `ananke-analytics-prod`).
   - Ative a **Google Analytics Data API**.
2. **Crie uma Conta de Serviço (Service Account):**
   - No menu *IAM & Admin* > *Service Accounts*, crie uma conta (ex: `ananke-analytics@seu-projeto.iam.gserviceaccount.com`).
   - Crie uma chave no formato **JSON** e faça o download.
3. **Dê Acesso no Google Analytics (GA4):**
   - No painel administrativo do GA4 > *Gerenciamento de Acesso à Propriedade*, adicione o e-mail da Conta de Serviço como **Leitor (Viewer)**.
4. **Instale a Chave Localmente:**
   - Renomeie a chave baixada para `service-account.json` nesta pasta (`integrations/google-analytics/service-account.json`).
   - Utilize o arquivo [`service-account.example.json`](service-account.example.json) como referência da estrutura esperada.

> [!CAUTION]
> **Nunca faça commit de arquivos `service-account.json` com chaves reais em repositórios públicos.**
