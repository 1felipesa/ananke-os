---
name: notebooklm-knowledge-retrieval
description: Protocolo de consulta e extração de evidências via MCP NotebookLM para embasamento de artigos de blog. Garante ancoragem em fontes reais, validação prévia de notebooks e travas contra alucinação.
---

# NotebookLM Knowledge Retrieval & Source Grounding

Esta skill define os protocolos técnicos e lógicos para conectar, consultar e extrair conhecimento verificado a partir de cadernos do **Google NotebookLM** via conector **MCP (Model Context Protocol)**. Ela atua como o **guardião de evidências** do subsistema de blog do Ananke OS.

---

## 🛑 1. Trava Bloqueante de Fontes (The Grounding Gatekeeper)

> **Regra de Ouro:** Nenhum outline ou parágrafo de artigo pode ser concebido sem um repositório factual ativo e verificado no NotebookLM.

### Checklist de Validação Obrigatória:
1. **Identificação do Caderno:**
   * O operador DEVE fornecer o `notebook_id` ou o título exato para resolução via `notebook_list`.
   * Se ausente, o agente DEVE interromper a execução e solicitar o caderno antes de qualquer outra ação.
2. **Checagem de Densidade Mínima de Fontes:**
   * O caderno alvo DEVE conter pelo menos 2 fontes primárias indexadas ou notas estruturadas com conteúdo substantivo.
   * Se o caderno estiver vazio ou possuir dados insuficientes, o sistema DEVE emitir um alerta de bloqueio e pedir a inserção de fontes no NotebookLM.
3. **Resolução de Autenticação:**
   * Se a chamada falhar por expiração de credenciais, orientar o comando de `refresh_auth` ou reativação de sessão do MCP.

---

## 🛠️ 2. Ferramentas MCP Utilizadas

| Ferramenta MCP | Finalidade no Pipeline de Blog |
| :--- | :--- |
| `notebook_list` | Localizar cadernos disponíveis caso o operador forneça apenas o título ou tema. |
| `notebook_get` | Obter metadados do caderno, lista de fontes (`sources`) e notas existentes. |
| `source_describe` | Inspecionar resumos detalhados e conteúdo das fontes individuais anexadas. |
| `notebook_query` | Submeter perguntas e prompts analíticos direcionados contra a base vetorial do caderno. |
| `note` | Recuperar notas sintéticas criadas manualmente no caderno. |
| `cross_notebook_query` | Consultar múltiplos cadernos quando o tema exigir correlação interdisciplinar. |

---

## 📑 3. Protocolo de Extração do Dossiê Factual

Ao conectar ao caderno, o agente deve executar o seguinte ciclo de extração:

```
[notebook_id] 
      │
      ├─► 1. Mapeamento de Fontes: Listar documentos, PDFs, URLs e notas anexadas
      │
      ├─► 2. Query de Tese: `notebook_query("Quais são as principais teses e conclusões?")`
      │
      ├─► 3. Query de Evidências: `notebook_query("Quais dados estatísticos, casos ou exemplos concretos são citados?")`
      │
      └─► 4. Estruturação do Dossiê Factual
```

### Formato Padronizado do Dossiê de Evidências:

```markdown
### 📋 Dossiê Factual Extraído (NotebookLM: [Nome do Caderno])

* **ID do Caderno:** `[notebook_id]`
* **Total de Fontes Analisadas:** `[X fontes]`
* **Fontes Primárias:**
  1. `[Nome da Fonte 1]` (Tipo: PDF/Artigo/URL) - Resumo: [...]
  2. `[Nome da Fonte 2]` (Tipo: Nota/Relatório) - Resumo: [...]

#### 💡 Teses e Insights Centrais:
- Insight A: [Afirmação factual com citação de página/fonte]
- Insight B: [Ponto de atrito ou contra-intuição identificado nas fontes]

#### 📊 Dados Estatísticos e Citações Relevantes:
- Dado 1: "[Citação direta ou métrica precisa]" — *Fonte: [Documento X]*
- Dado 2: "[Citação direta ou métrica precisa]" — *Fonte: [Documento Y]*
```

---

## 🤝 4. Passagem de Bastão (Handoff) para o Checkpoint 1

Com o Dossiê Factual gerado:
1. O agente formula **3 Propostas de Ângulos Editoriais** baseadas nos insights reais das fontes.
2. O agente pausa e aguarda a decisão do operador no **Checkpoint 1**.
3. Nenhuma linha de outline é criada antes dessa aprovação.
