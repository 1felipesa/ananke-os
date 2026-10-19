---
name: email-template-design
description: Engenharia e diagramação de templates de e-mail em HTML tabular responsivo, inlining de CSS, compatibilidade com Microsoft Outlook e Gmail, e geração de versão Plain Text espelho.
---

# Engenharia de Templates de E-mail (HTML Tabular Responsivo)

Esta skill define as regras inegociáveis para desenhar e codificar e-mails em HTML compatíveis com dezenas de clientes de e-mail (Microsoft Outlook desktop, web e mobile, Apple Mail, Gmail web e mobile, Yahoo).

---

## 🏗️ 1. Princípios Estruturais Inegociáveis

1. **Estrutura Tabular Obrigatória (`<table>`):**
   * Clientes de e-mail desktop (especialmente o Microsoft Outlook no Windows, que usa o motor de renderização do Word) NÃO suportam `display: flex` nem `display: grid`.
   * Toda divisão visual, colunas e alinhamentos DEVEM ser construídos com `<table cellpadding="0" cellspacing="0" border="0" width="100%">`.
2. **Largura Padrão de 600px:**
   * A tabela container mestre deve ter `max-width: 600px; width: 100%;` e estar centralizada (`align="center"`).
3. **Inlining Obrigatório de Estilos CSS:**
   * Provedores como Gmail móvel e web frequentemente desconsideram blocos `<style>` no `<head>`.
   * Todos os estilos críticos (`font-family`, `color`, `font-size`, `line-height`, `padding`) DEVEM ser inseridos diretamente no atributo `style="..."` das tags `<td>`, `<a>` e `<p>`.
4. **Font Stacks Seguras:**
   * Nunca use apenas fontes customizadas do Google Fonts sem fallback testado.
   * Padrão recomendado: `font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;`.
5. **Botões Blindados (Bulletproof Buttons):**
   * Use botões construídos com `<td>` preenchido e link `<a>` em bloco (`display: inline-block; padding: 12px 24px; text-decoration: none;`), garantindo que toda a área seja clicável sem depender de imagens.
6. **Versão Espelho em Texto Puro (`text/plain`):**
   * Todo e-mail HTML gerado deve possuir sua versão equivalente em texto simples, garantindo leitura em dispositivos com HTML desativado ou smartwatches e pontuação máxima em filtros anti-spam.

---

## 💻 2. Script Utilitário: `inline_styler.py`

A skill disponibiliza um script Python que lê um arquivo HTML com estilos em tags `<style>` ou dicionários CSS, aplica o inlining diretamente nas tags e extrai a versão espelho Plain Text limpa.

### Como Executar:
```bash
python .agent/skills/email-template-design/scripts/inline_styler.py caminho/do/template.html
```

O script gerará dois arquivos de saída:
* `template_inlined.html`: HTML pronto para disparo em qualquer ferramenta.
* `template_plain.txt`: Versão textual espelho.
