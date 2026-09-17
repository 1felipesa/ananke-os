# Ananke OS - Master Scripts Guide

> Documentação técnica e guia de execução dos scripts mestres de validação, pré-visualização e gerenciamento de sessão localizados em `.agent/scripts/`.

---

## 📋 Visão Geral

Os scripts mestres orquestram validações estruturadas, automação de servidores locais e diagnóstico do projeto. Eles integram os scripts de validação granulares localizados dentro das pastas de cada skill (`.agent/skills/*/scripts/`).

| Script | Finalidade | Quando Executar | Prioridade |
| :--- | :--- | :--- | :---: |
| [`checklist.py`](checklist.py) | Validação por prioridade (P0 a P6) dos pilares centrais | Durante o desenvolvimento e pré-commit | **P0 (Obrigatório)** |
| [`verify_all.py`](verify_all.py) | Bateria exaustiva de verificação (Qualidade + E2E + Web Vitals) | Pré-deploy e homologação de releases | **P0 (Pré-Deploy)** |
| [`auto_preview.py`](auto_preview.py) | Gerenciamento do servidor de desenvolvimento local | Visualização interativa e testes de UI | **P1 (Operacional)** |
| [`session_manager.py`](session_manager.py) | Inspeção da stack tecnológica e estado do projeto | Descoberta e diagnóstico de sessão | **P2 (Suporte)** |
| [`automations/run_batch.py`](automations/run_batch.py) | Pipeline de ingestão periódica e geração de relatórios | Fechamentos quinzenais/mensais e batch | **P1 (Operacional)** |

---

## 🚀 Como Executar

### 1. `checklist.py` (Validação Incremental Rápida)

Executa checagens essenciais ordenadas por prioridade:
1. **P0 - Segurança:** Varredura de vulnerabilidades, secrets e dependências.
2. **P1 - Qualidade:** Linters, tipagem e convenções de código.
3. **P2 - Banco de Dados:** Validação de schemas e migrações (se aplicável).
4. **P3 - Testes:** Execução da suíte de testes unitários e de integração.
5. **P4 - UX Audit:** Conformidade com princípios de usabilidade e acessibilidade.
6. **P5 - SEO:** Meta tags e estrutura semântica.
7. **P6 - Performance:** Auditoria Lighthouse (se URL informada).

```bash
# Execução padrão (Core checks):
python .agent/scripts/checklist.py .

# Execução completa incluindo auditoria de performance em servidor local:
python .agent/scripts/checklist.py . --url http://localhost:3000
```

---

### 2. `verify_all.py` (Suíte Completa Pré-Deploy)

Executa toda a bateria do `checklist.py` somada a testes avançados:
- **Playwright E2E:** Navegação sintética ponta a ponta.
- **Lighthouse Completo:** Performance, Acessibilidade, Melhores Práticas e SEO.
- **Bundle Analysis:** Análise de tamanho e divisão de pacotes JS.
- **Mobile Audit:** Responsividade e zonas de toque.
- **i18n Check:** Detecção de strings hardcoded e arquivos de tradução.

```bash
# Homologação completa com URL do servidor de testes:
python .agent/scripts/verify_all.py . --url http://localhost:3000

# Execução pulando testes E2E para validação rápida:
python .agent/scripts/verify_all.py . --url http://localhost:3000 --no-e2e
```

---

### 3. `auto_preview.py` (Servidor de Desenvolvimento)

Inicia, monitora e finaliza o servidor local de desenvolvimento de forma compatível com Windows e Linux:

```bash
# Iniciar o preview (porta padrão 3000):
python .agent/scripts/auto_preview.py start

# Iniciar em porta personalizada (ex: 5173):
python .agent/scripts/auto_preview.py start 5173

# Verificar se o servidor está ativo:
python .agent/scripts/auto_preview.py status

# Encerrar o preview:
python .agent/scripts/auto_preview.py stop
```

---

### 4. `session_manager.py` (Diagnóstico de Sessão)

Inspeciona dependências, identifica a stack em uso (Next.js, React, Vue, Tailwind, Prisma, etc.) e analisa estatísticas de arquivos:

```bash
# Visualizar informações de stack e scripts:
python .agent/scripts/session_manager.py info .

# Visualizar contagem e estado de arquivos:
python .agent/scripts/session_manager.py status .
```

---

### 5. `automations/run_batch.py` (Processamento em Lote)

Orquestra a ingestão de arquivos periódicos (`.csv`, `.xlsx`, `.json`), agregação de métricas com DuckDB e renderização de Dashboard HTML (M3 Dark) e Sumário Markdown:

```bash
# Executar sobre o arquivo mais recente em data/incoming/:
python .agent/scripts/automations/run_batch.py

# Executar especificando arquivo e template:
python .agent/scripts/automations/run_batch.py --input ./data/incoming/ads_maio.csv --template marketing_ads --title "Fechamento de Tráfego - Maio"
```

