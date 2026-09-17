---
name: script
description: Fluxo focado em roteirização audiovisual para vídeos curtos (Reels/Shorts/TikTok) e longos (YouTube), entregando versões para Teleprompter e Tabela de 2 Colunas.
agent: video-script-architect
---

# 🎬 Roteirização de Vídeos (Script Workflow)

O comando `/script` é a porta de entrada para a criação de roteiros audiovisuais de alta performance. Desenvolvido especialmente para apresentadores que não são atores profissionais, este fluxo cria textos com linguagem oral natural e baixa carga cognitiva, gerando simultaneamente o roteiro linear para gravação e a tabela sincronizada para o editor de vídeo.

---

## Como Usar

Digite `/script` seguido do tema, formato e, opcionalmente, o caminho de documentos de referência (arquivos `.md`, `.pdf` ou notas de briefing).

**Exemplos:**
- `/script Crie um roteiro de Reels (60s) sobre os 3 maiores erros ao precificar projetos de consultoria, com gancho contraintuitivo.`
- `/script YouTube longo (12 min) ensinando iniciantes a estruturar seu primeiro SaaS, baseado nas notas em docs/briefing-saas.md.`
- `/script Vídeo curto para TikTok focado em quebra de crença sobre investimentos para médicos.`

---

## O Que Acontece por Baixo dos Panos?

1. **Ativação:** O agente `video-script-architect` é acionado automaticamente.
2. **Ingestão:** Lê e interpreta quaisquer arquivos de documentação ou briefing fornecidos como fonte primária da verdade.
3. **Aplicação de Frameworks:** Carrega a skill `video-scriptwriting-frameworks` para selecionar o gancho (*hook*) ideal e estruturar o timing.
4. **Geração Dupla:**
   - **Parte 1 (Teleprompter Linear):** Redige a fala do apresentador com frases curtas, pontuação respirável e tags de ação (`[PAUSA]`, `[SORRISO]`).
   - **Parte 2 (Tabela de 2 Colunas):** Monta a tabela de produção com Áudio e Vídeo/Edição (B-rolls, zooms, efeitos e cortes).
5. **Salvamento:** Grava o arquivo formatado em `assets/scripts/{data}-{slug-do-video}.md`.
