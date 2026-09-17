---
name: refactoring-patterns
description: Padrões de refatoração, identificação de Code Smells e aplicação de princípios de clean architecture (SOLID, DRY, KISS).
allowed-tools: Read, Grep, Glob, Bash, Write
---

# Padrões de Refatoração (Refactoring Patterns)

Esta skill guia o agente na análise e modificação de código legado ou mal estruturado, aplicando melhorias estruturais sem alterar o comportamento externo.

## 🕵️ Identificação de Code Smells (Sintomas de Código Ruim)

1.  **Bloaters (Inchaço):**
    *   *Long Method:* Funções gigantescas com muitas responsabilidades.
    *   *Large Class:* Classes que tentam fazer tudo (God Object).
    *   *Data Clumps:* Mesmos grupos de variáveis passando de função em função (ex: `startDate`, `endDate`).
    
2.  **Object-Orientation Abusers:**
    *   *Switch Statements:* Uso excessivo de `switch/if-else` em vez de Polimorfismo.
    
3.  **Dispensables (Descartáveis):**
    *   *Comments:* Comentários que explicam "o que" o código faz (sinal de que o código não é autoexplicativo).
    *   *Dead Code:* Variáveis, funções ou classes que não são usadas.

## 🛠️ Técnicas de Refatoração Aplicáveis

### 1. Extração (Extraction)
*   **Extract Method:** Mova parte do código de um método longo para um novo método bem nomeado.
*   **Extract Class:** Quando uma classe faz o trabalho de duas, crie uma nova classe e mova a responsabilidade (Single Responsibility Principle).
*   **Extract Variable:** Substitua expressões complexas por variáveis descritivas.

### 2. Simplificação de Condicionais
*   **Decompose Conditional:** Extraia a condição complexa de um `if/else` para um método nomeado (ex: `if (isEligibleForDiscount())`).
*   **Replace Conditional with Polymorphism:** Substitua condicionais que verificam tipos por chamadas polimórficas de métodos.
*   **Early Return (Guard Clauses):** Evite aninhamento excessivo retornando assim que uma condição de erro/exceção for encontrada.

### 3. Organização de Dados
*   **Introduce Parameter Object:** Substitua múltiplos parâmetros (`Data Clumps`) por um objeto/classe de configuração.
*   **Replace Magic Number with Symbolic Constant:** Evite números "mágicos" no código. Dê a eles nomes constantes e significativos.

## 🧠 Princípios Direcionadores (SOLID / DRY / KISS)

1.  **SRP (Single Responsibility):** Uma classe/função deve ter apenas UM motivo para mudar.
2.  **DRY (Don't Repeat Yourself):** Se uma lógica existe em dois lugares, abstraia.
3.  **KISS (Keep It Simple, Stupid):** A solução mais simples que funciona é geralmente a melhor. Não faça over-engineering prematuro.

## 🚧 Regras ao Refatorar

1.  **Refatore primeiro, adicione features depois:** Não misture alteração de comportamento com refatoração estrutural no mesmo commit/passo.
2.  **Preserve os Testes:** Certifique-se de que testes não quebrem (ou os adapte, caso a assinatura mude).
3.  **Faça Passos Pequenos:** Refatore iterativamente.
