# Como Iniciar Projetos com Spec-Driven Development (SDD)

Bem-vindo à nova era de desenvolvimento do Ananke OS. Agora operamos estritamente sob o **Spec-Driven Development (SDD)**. Isso significa o fim do "vibe coding" (codificação baseada em intuição sem planejamento). Todo código deve ser derivado de uma **Especificação Clara**.

Para que a inteligência artificial (nossos agentes) seja o mais eficiente possível e gere resultados precisos, é fundamental que você inicie o projeto fornecendo as informações corretas de forma contundente.

---

## 🚀 1. Como Iniciar o Projeto

Você tem duas formas principais de iniciar um novo desenvolvimento estruturado:

1. **Via Comando Dedicado (Recomendado):**
   Digite `/sdd <nome do projeto>` para acionar diretamente o Agente Especialista em SDD.
2. **Via Criação Padrão:**
   Digite `/create <nome do projeto>`. O orquestrador detectará que é um novo projeto e obrigatoriamente passará pela fase de Especificação.

---

## 📝 2. Como Escrever o Prompt Inicial Perfeito

Não inicie um projeto dizendo apenas: *"Crie um app de todo"*. Isso gera suposições erradas. 
Forneça um "Briefing de Especificação" contendo os 4 pilares abaixo:

### Os 4 Pilares do Briefing:
1. **O Problema Core:** O que estamos resolvendo e qual o objetivo principal?
2. **Atores/Usuários:** Quem vai usar o sistema? Existem perfis diferentes (ex: Admin, Cliente)?
3. **Fluxo Principal (Happy Path):** Qual é o passo a passo da jornada principal?
4. **Restrições:** Tecnologias obrigatórias, requisitos de segurança ou design?

### Exemplo de Prompt Excelente:
> "/sdd Crie um sistema de agendamento de consultas.
> **Problema:** Pacientes faltam muito e a clínica perde dinheiro.
> **Atores:** Paciente (agenda/cancela) e Médico (vê a agenda do dia).
> **Fluxo:** O paciente loga, escolhe um horário livre na tela do médico, e confirma. Ele deve receber um e-mail.
> **Restrições:** Usar Next.js, banco PostgreSQL, autenticação via Clerk. Design minimalista."

---

## 🔄 3. O Que Acontecerá em Seguida? (As 4 Fases)

Ao enviar o seu briefing, o agente não começará a escrever código imediatamente. Ele guiará você por 4 Fases rígidas. **Você precisará aprovar cada uma delas.**

### Fase 1: SPECIFY (Especificar)
O agente `sdd-specialist` irá pegar o seu briefing e criar regras de negócio exatas usando a **Sintaxe EARS**:
- *QUANDO* o paciente cancelar com menos de 24h, *ENTÃO* o sistema DEVE cobrar taxa.
> **Sua Ação:** Ler o arquivo gerado em `.specify/` e aprovar.

### Fase 2: PLAN (Planejar)
O agente `project-planner` transformará a especificação em um modelo de dados, rotas de API e arquitetura de pastas (`PLAN.md`).
> **Sua Ação:** Revisar a arquitetura técnica e aprovar.

### Fase 3: TASKS (Tarefas)
O trabalho será fatiado em pequenas tarefas gerenciáveis.
> **Sua Ação:** Aprovar a ordem de execução.

### Fase 4: IMPLEMENT (Implementar)
Finalmente, os agentes construtores (frontend, backend) entrarão em ação para escrever o código que cumpra *exatamente* o contrato definido na Especificação.

---

## 💡 Dica de Ouro
Se você perceber que o agente está escrevendo código sem antes ter gerado um arquivo na pasta `.specify/` ou o `PLAN.md`, interrompa-o! A Especificação é a única fonte da verdade.
