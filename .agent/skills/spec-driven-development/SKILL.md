---
name: spec-driven-development
description: Habilidade para aplicar o Spec-Driven Development (SDD), orientando os agentes a criar e respeitar documentos de especificação usando a sintaxe EARS e o GitHub Spec Kit.
---

# Spec-Driven Development (SDD) com GitHub Spec Kit

Esta habilidade (skill) foca em orientar o processo de desenvolvimento para ser focado na especificação, não na adivinhação (vibe coding).

## Diretrizes Principais

1. **A Especificação é a Fonte da Verdade:** Todo desenvolvimento de código DEVE ser precedido por uma especificação clara.
2. **Uso de EARS (Easy Approach to Requirements Syntax):**
   - **Ubiquitous:** "O sistema DEVE..."
   - **Event-driven:** "QUANDO <evento ocorre>, o sistema DEVE..."
   - **State-driven:** "ENQUANTO <estado é verdadeiro>, o sistema DEVE..."
   - **Optional:** "ONDE <recurso opcional existe>, o sistema DEVE..."
   - **Unwanted:** "SE <erro ocorre>, ENTÃO o sistema DEVE..."
3. **Pausas para Aprovação Humana:** O fluxo DEVE ser interrompido entre as fases de Especificação, Planejamento e Tarefas para pedir feedback ou aprovação.
4. **Sem Código Prematuro:** Não inicie a codificação sem antes ter criado um Plano Técnico que aborde a arquitetura e os contratos das APIs (ex. OpenAPI, GraphQL).

## Integração com GitHub Spec Kit

O GitHub Spec Kit fornece um esqueleto estruturado de Especificações para alinhar os agentes de IA aos requisitos do projeto.

Para aplicar a estrutura do Spec Kit no projeto atual em desenvolvimento, execute o seguinte comando:

```bash
uvx --from git+https://github.com/github/spec-kit.git specify init <NOME_DO_PROJETO>
```

**Nota:** Substitua `<NOME_DO_PROJETO>` pelo nome real do projeto ou módulo.

### O que este comando faz?
- Baixa diretamente o repositório do GitHub e cria a estrutura fundamental do Spec Kit no projeto.
- Gera as pastas `.github` (com templates de prompts para os agentes de IA) e `.specify` (com os esqueletos dos documentos de especificação).

## Como aplicar esta skill

- Sempre que estiver guiando um projeto ou desenvolvendo uma funcionalidade significativa, certifique-se de preencher os documentos de especificação antes de codificar.
- Utilize a infraestrutura gerada em `.specify` para padronizar as especificações em todos os desenvolvimentos do time ou sistema.
