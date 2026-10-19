# Pedidos Prontos e Prompts de Operação

Modelos de comando para acionar o pipeline de vídeo programático no Ananke OS via chat ou slash command.

---

## 1. Inicialização do Projeto
> `/reel`  
> "Usa a skill `programmatic-video-editing` no estilo [corretor / personal / inglês / chef / finanças]. O meu take bruto gravado está em `public/take.mp4`. Transcreve com tempos, me mostra a tabela de cenas e só escreve o código depois que eu aprovar."

---

## 2. Envio de Vídeos de Referência
> "Coloquei 2 vídeos de referência em `refs/`. Executa o script de extração de stills, analisa o ritmo de cortes e o tipo de transição de elementos gráficos e me apresenta um resumo do que podemos adaptar no nosso estilo."

---

## 3. Direção Fina de Cena
> "Na Cena 2:
> 1. Quando eu disser '[palavra]', o título deve entrar letra por letra de baixo para cima com espaçamento fechando;
> 2. O gráfico de barras deve subir em 0.4s acompanhando o número citado;
> 3. O card do meu rosto deve encolher suavemente para a lateral direita abrindo espaço para a tela principal."

---

## 4. Auditoria de Safe Zones & Renderização
> "Gera os stills dos instantes 0s, 5s e 12s e roda a validação de safe zones para garantir que nada fique coberto pelos botões do Instagram. Estando tudo aprovado, renderiza o MP4 final via HyperFrames."

---

## 5. Criação de Novo Nicho
> "Minha profissão é [profissão]. Vamos estruturar o estilo visual dela usando o modelo `references/nichos/novo-nicho.md`. Me faça as perguntas necessárias para montar o preset."
