---
name: post
description: Fluxo focado em design gráfico e geração de imagens estáticas para redes sociais (posts de tela única e carrosséis).
agent: social-media-designer
---

# 🎨 Design para Redes Sociais & Criação Visual (Post Workflow)

O comando `/post` é o atalho para a criação profissional de **posts estáticos de tela única e carrosséis panorâmicos** para redes sociais (Instagram, LinkedIn, X/Twitter). Ele une direção de arte, identidade visual da marca e geração de imagens com tipografia integrada, organizando tudo na pasta `assets/posts/<slug>/`.

---

## 🚀 Como Usar

Digite `/post` seguido do tema ou objetivo do conteúdo:

**Exemplos:**
- `/post Crie um carrossel de 5 slides explicando o que é Spec-Driven Development (SDD) e por que ele elimina bugs.`
- `/post Crie um post estático de tela única formato 4:5 anunciando a nova versão do Ananke OS.`
- `/post Crie um carrossel comparativo: Programação Tradicional vs Desenvolvimento com Agentes de IA.`

---

## ⚙️ O que acontece por baixo dos panos?

1. **Leitura da Marca:** O [`social-media-designer`](../agents/social-media-designer.md) é acionado e lê obrigatoriamente as cores, tipografia e regras de [`brand-guidelines.md`](../../.specify/brand-guidelines.md).
2. **Definição de Formato e Roteiro:** Escolhe o aspect ratio ideal (`4:5`, `1:1` ou `9:16`) e elabora a narrativa visual slide a slide.
3. **Criação da Estrutura de Pastas:** Executa o script auxiliar `asset_organizer.py` para gerar `assets/posts/<slug>/copy.md`.
4. **Geração de Imagens via Ananke Engine:** Gera cada imagem com tipografia e elementos visuais no diretório do post (`slide-01.png`, `slide-02.png`, etc.).
5. **Apresentação e Revisão:** Entrega um relatório visual com o preview das telas geradas e a legenda pronta para publicação.
