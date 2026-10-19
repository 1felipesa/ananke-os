# Ananke OS - 3D Interactive Brain Map

> **Spec-Driven Autonomy // Zero Vibe Coding**  
> *Visualizador Tridimensional e Mapeamento Ontológico do Ecossistema Ananke OS*

O **Brain Map** é uma aplicação visual interativa em 3D WebGL que renderiza todo o ecossistema do **Ananke OS** como uma constelação neural viva. Foi projetado para acelerar o onboarding de novos membros da equipe, clientes e desenvolvedores, tornando tangível a conexão entre todos os 38 agentes, 62 skills, 24 comandos e a esteira de governança SDD.

---

## 🚀 Como Visualizar

Você tem duas formas simples de abrir o Brain Map:

### 1. Abertura Direta no Navegador
Dê um duplo clique no arquivo [`index.html`](index.html) ou arraste-o para qualquer navegador moderno (Google Chrome, Microsoft Edge, Firefox, Safari). Nenhuma instalação de dependências ou build é necessária.

### 2. Via Servidor de Desenvolvimento Local
```bash
# Na raiz do repositório:
python -m http.server 3000

# Acesse no navegador:
# http://localhost:3000/brain-map/
```

---

## 🎨 Código de Cores & Legenda Neural

Para assegurar máxima distinção cromática e contraste visual, os nós utilizam a seguinte paleta:

| Cor | Significado | Quantidade | Descrição |
| :--- | :--- | :---: | :--- |
| 🟡 **Amarelo Ouro** (`#FACC15`) | **Agentes Especialistas** | 38 nós | Personas ativas de IA responsáveis pela execução especializada. |
| 🔴 **Vermelho Coral** (`#EF4444`) | **Workflows de Comando** | 24 nós | Comandos `/slash` de entrada acionados pelo operador no chat. |
| 🔵 **Azul / Ciano** (`#00D2FF`) | **Skills de Engenharia** | 62 nós | Módulos de conhecimento técnico carregados sob demanda. |
| 🟠 **Laranja Quente** (`#FB923C`) | **Macro-Categorias** | 8 núcleos | Grandes núcleos funcionais de serviço do kit. |
| 🟢 **Verde Esmeralda** (`#10B981`)| **Fases do SDD** | 4 fases | Esteira mandatória de governança (Specify, Plan, Tasks, Implement). |

---

## 🕹️ Controles de Navegação

- **Girar a Câmera:** Clique com o botão esquerdo e arraste em 360°.
- **Aproximar / Afastar (Zoom):** Use a roda do mouse (scroll) ou os botões flutuantes táteis **`+`** e **`−`** no canto inferior direito.
- **Restaurar Visão Global:** Clique no botão **`↺`** para centralizar a câmera e reiniciar a rotação suave.
- **Mover o Cenário (Pan):** Clique com o botão direito e arraste.
- **Inspecionar Detalhes:** Clique em qualquer esfera para centralizar a câmera, destacar conexões e abrir o painel lateral com instruções de uso.
- **Filtrar por Tipo:** Clique nos itens da legenda ou nos botões da barra inferior para isolar categorias específicas.
- **Busca Neural:** Digite qualquer termo na barra de busca superior para localizar nós instantaneamente.

---

## 🛠️ Como Adicionar Novos Agentes ou Nós (Extensibilidade)

O mapa foi projetado para ser **100% declarativo e extensível**. Quando você criar um novo agente, skill ou workflow no kit, basta adicionar um objeto no array `nodes` dentro de [`brain-data.js`](brain-data.js):

```javascript
// Exemplo de inclusão de novo agente em brain-data.js:
{
  id: "agent-novo-especialista",
  type: "agent",              // "agent" | "workflow" | "skill" | "category" | "sdd"
  name: "novo-especialista",
  category: "core-backend",   // ID do núcleo pai (ex: core-backend, core-frontend, core-data)
  description: "Responsabilidade principal do novo especialista..."
}
```

O motor 3D recalcula automaticamente as forças de atração, cores, contadores da legenda e conexões em tempo de execução sem exigir nenhuma alteração no código gráfico.
