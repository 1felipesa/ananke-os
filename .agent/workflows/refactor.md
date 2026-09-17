---
name: refactor
description: Fluxo focado estritamente na melhoria interna do código, redução de dívida técnica e padrões SOLID. Sem alteração de comportamento.
agent: code-archaeologist
---

# ♻️ Refatorar (Refactor Workflow)

O comando `/refactor` é acionado quando o código funciona, mas está desorganizado, complexo ou difícil de manter. Diferente de `/enhance` (que pode incluir novas features), este comando garante uma refatoração **pura**: o comportamento externo do código permanecerá idêntico, mas o código interno ficará impecável.

## Como Usar

Digite `/refactor` seguido do arquivo ou pasta que precisa de limpeza.

**Exemplos:**
- `/refactor src/utils/api.ts`
- `/refactor a pasta components/ para separar a lógica de estado em hooks customizados.`

## O que acontece por baixo dos panos?

1. O `code-archaeologist` assume o controle.
2. Analisa o código em busca de violações do SOLID e código repetido (Dry).
3. Desmembra funções gigantes, limpa variáveis não utilizadas e cria abstrações melhores.
4. Gera e aplica as alterações com extrema cautela para não quebrar a lógica de negócio.
