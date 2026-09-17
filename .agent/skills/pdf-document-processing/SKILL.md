---
name: pdf-document-processing
description: Extração de alta fidelidade de tabelas, demonstrativos, faturas e texto contidos em documentos PDF digitais. Utiliza pdfplumber e pypdf com estratégias lattice/stream para lidar com tabelas sem bordas ou células mescladas.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# PDF Document Processing Skill

Habilidade especializada na extração analítica de documentos em formato PDF. Converte relatórios não estruturados, demonstrativos contábeis, faturas e tabelas embutidas em estruturas de dados limpas (DataFrames / CSV / JSON) com rastreabilidade total de páginas.

---

## 🎯 Desafios Críticos e Estratégias

1. **Tabelas com Bordas vs. Sem Bordas (Lattice vs Stream):**
   - **Lattice (`mode=lattice`):** Ideal quando a tabela possui linhas pretas ou cinzas delimitando células (ex: planilhas impressas em PDF). Usa detecção geométrica de vetores.
   - **Stream (`mode=stream`):** Essencial para tabelas sem bordas explícitas, onde as colunas são alinhadas apenas por espaços em branco (ex: faturas de cartão de crédito, extratos bancários, demonstrativos contábeis de empresas).
2. **Células Mescladas e Múltiplas Linhas:**
   - Textos longos dentro de uma mesma célula frequentemente geram quebras de linha (`\n`). A limpeza padronizada recombina os fragmentos preservando a integridade semântica da coluna.
3. **Cabeçalhos e Rodapés Repetitivos:**
   - Em relatórios de dezenas de páginas, cabeçalhos de página e numeração de rodapé introduzem ruído; devem ser filtrados antes de concatenar DataFrames entre páginas.

---

## 🛠️ Ferramenta Utilitária: `extract_pdf_tables.py`

Esta skill inclui o extrator em `scripts/extract_pdf_tables.py`.

### Comandos Comuns:

```bash
# Extrair todas as tabelas de um PDF para o console em formato Markdown
python .agent/skills/pdf-document-processing/scripts/extract_pdf_tables.py --pdf relatorio.pdf

# Extrair páginas específicas (ex: páginas 2 até 5) no modo sem bordas (stream)
python .agent/skills/pdf-document-processing/scripts/extract_pdf_tables.py --pdf fatura.pdf --pages 2-5 --mode stream

# Extrair tabelas e exportar diretamente para CSV
python .agent/skills/pdf-document-processing/scripts/extract_pdf_tables.py --pdf balanco.pdf --output balanco_estruturado.csv

# Extrair tabelas e o texto corrido completo das páginas
python .agent/skills/pdf-document-processing/scripts/extract_pdf_tables.py --pdf contrato.pdf --text --output analise_contrato.md
```

---

## 📋 Protocolo de Inspeção com Python

Ao trabalhar programmaticamente com arquivos PDF complexos:

```python
import pdfplumber

def inspect_pdf_structure(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Total de páginas: {len(pdf.pages)}")
        for idx, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            print(f"Página {idx+1}: {len(tables)} tabelas detectadas.")
            if tables:
                # Amostra do cabeçalho da primeira tabela
                print(f"  Cabeçalho: {tables[0][0]}")
```

---

## ⚠️ Tratamento de PDFs Escaneados (Raster)

Se a extração de texto retornar strings vazias ou nulas em um documento que visualmente contém texto, o arquivo trata-se de um **PDF escaneado** (imagem chapada).
- **Ação:** O agente deve informar imediatamente que o documento não possui camada vetorial de texto e sugerir pipeline de OCR antes da tabulação.
