---
description: Inicia o Desenvolvimento Orientado por Especificações (SDD) para uma nova funcionalidade ou projeto. Usa o agente sdd-specialist.
---

# /sdd - Spec-Driven Development Mode

$ARGUMENTS

---

## 🔴 CRITICAL RULES

1. **NO VIBE CODING** - This workflow strictly enforces the Spec-Driven Development methodology.
2. **Use sdd-specialist agent** - The specialist agent MUST be used to drive the phases.
3. **Socratic Gate** - The agent must start by understanding the feature or product the user wants to specify.
4. **Human-in-the-Loop** - Stop and wait for approval between phases.

---

## Task

Use the `sdd-specialist` agent with this context:

```
CONTEXT:
- User Request: $ARGUMENTS
- Mode: SPEC-DRIVEN DEVELOPMENT
- Output: Follow the 4-Phase workflow (Specify, Plan, Tasks, Implement)

RULES:
1. Initialize by asking what to specify if $ARGUMENTS is empty.
2. Use the 'spec-driven-development' skill.
3. Propose running the GitHub Spec Kit initialization command if the project doesn't have the `.specify` structure yet.
4. Go through Phase 1 to Phase 4 sequentially. DO NOT skip any phase.
```

---

## Expected Output

| Phase | Deliverable | Location |
|-------|-------------|----------|
| 1. Specify | Functional Specification | `.specify/` or `docs/` |
| 2. Plan | Technical Plan | `docs/PLAN-{slug}.md` |
| 3. Tasks | Task Breakdown | `task.md` or in the Plan file |
| 4. Implement | Source Code & Tests | Project source directories |

---

## Usage Examples

```
/sdd novo sistema de autenticação
/sdd funcionalidade de carrinho de compras
/sdd dashboard de relatórios em tempo real
```

---

## Next Steps for User

Tell user:
```
[OK] Modo Spec-Driven Development iniciado.
O agente de SDD irá guiá-lo pelas 4 Fases (Especificar, Planejar, Tarefas, Implementar).
Certifique-se de ter rodado o GitHub Spec Kit (`uvx --from git+https://github.com/github/spec-kit.git specify init <NOME_DO_PROJETO>`) ou permita que o agente o guie.
```
