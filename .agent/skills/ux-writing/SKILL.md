---
name: ux-writing
description: Diretrizes de UX Writing para interfaces claras, botões amigáveis, mensagens de erro não-frustrantes e jornadas de usuário sem atrito.
---

# Diretrizes de UX Writing (Escrita para Experiência do Usuário)

O objetivo do UX Writing não é vender, mas **guiar**. Uma interface com um excelente UX Writing não precisa de manual de instruções. O tom deve ser útil, claro e conciso.

## 🧭 Princípios de Base

1. **Clareza (Clarity):** O texto precisa fazer sentido para qualquer pessoa. Evite jargões técnicos ou termos ambíguos.
2. **Concisão (Conciseness):** Cada palavra deve ter um propósito. Seja direto, economize espaço (especialmente no mobile).
3. **Utilidade (Usefulness):** A mensagem ajuda o usuário a dar o próximo passo? Se não, ela sobra.

---

## 🛠️ Padrões de Interface e Regras

### 1. Botões e CTAs (Call to Action)
* Comece com um **verbo de ação**.
* Descreva o que o botão fará *após* o clique.
* *Anti-padrão:* "Clique Aqui", "Enviar", "OK"
* *Padrão ideal:* "Salvar Alterações", "Criar Conta Grátis", "Excluir Projeto"

### 2. Mensagens de Erro (Error States)
Um momento de frustração para o usuário não pode se transformar em confusão.
* Diga **o que** aconteceu, **por que** aconteceu e **como** resolver.
* Evite culpar o usuário. 
* *Anti-padrão:* "Erro 402 - Impossível processar dados. Entrada inválida."
* *Padrão ideal:* "Não conseguimos salvar seu endereço. Por favor, verifique se o CEP está correto e tente novamente."

### 3. Estados de Loading / Empty States
* Quando não houver dados (uma lista vazia, por exemplo), use o texto para incentivar a primeira ação.
* *Anti-padrão:* "0 Projetos encontrados."
* *Padrão ideal:* "Você ainda não tem projetos. Que tal criar o seu primeiro agora?"

### 4. Textos de Confirmação (Success States)
* Comemore (mesmo que sutilmente) o término de uma tarefa e deixe claro o que acontecerá a seguir.
* *Padrão:* "E-mail enviado com sucesso! Você deve receber nossa resposta em até 2 horas."

---

## 🎨 Tom e Voz

* **Voz:** É a personalidade da marca (consistente e inalterável).
* **Tom:** Muda conforme a emoção do momento da jornada do usuário. 
    * Se for uma mensagem de erro grave: Tom sério e direto.
    * Se for um sucesso de conclusão de tarefa (ex: "Você finalizou todas as tarefas do dia!"): Tom alegre e recompensador.

## ⚠️ Acessibilidade Linguística
* Não confie em termos visuais, como "clique no botão verde abaixo" (pessoas com deficiência visual usando leitores de tela não saberão o que é). Use nomes e labels.
* Mantenha frases no formato mais simplificado possível: Sujeito + Verbo + Predicado.
