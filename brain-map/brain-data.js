/**
 * Ananke OS - 3D Neural Brain Map Dataset
 * Spec-Driven Autonomy // Zero Vibe Coding
 * Complete ontological network graph data representing the entire system:
 * - 35 Specialist Agents
 * - 54 Skills
 * - 21 Workflows
 * - 4 SDD Lifecycle Phases
 * - 8 Macro-Categories / Central Nuclei
 * 
 * High Contrast Color Palette:
 * 🟡 Yellow (#FACC15)  - Specialist Agents (35)
 * 🔴 Red (#EF4444)     - Command Workflows (21)
 * 🔵 Cyan/Blue (#00D2FF) - Engineering Skills (54)
 * 🟠 Orange (#FB923C)  - Macro-Categories / Core Nuclei (8)
 * 🟢 Green (#10B981)   - SDD Lifecycle Phases (4)
 */

const KIT_BRAIN_DATA = {
  config: {
    colors: {
      agent: "#FACC15",
      workflow: "#EF4444",
      skill: "#00D2FF",
      category: "#FB923C",
      sdd: "#10B981"
    },
    labels: {
      agent: "Agentes Especialistas",
      workflow: "Workflows de Comando",
      skill: "Skills de Engenharia",
      category: "Macro-Categorias / Núcleos",
      sdd: "Ciclo de Governança SDD"
    }
  },

  nodes: [
    // --- 1. CICLO SDD (VERDE) ---
    {
      id: "sdd-specify",
      type: "sdd",
      name: "Fase 1: SPECIFY",
      subtitle: "Requisitos Formais EARS",
      description: "Especificação obrigatória antes de qualquer código. Derivação de regras de negócio sem ambiguidade no diretório .specify/.",
      target: ".specify/*.md",
      command: "/sdd"
    },
    {
      id: "sdd-plan",
      type: "sdd",
      name: "Fase 2: PLAN",
      subtitle: "Arquitetura & Dados",
      description: "Transformação da especificação aprovada em modelo de dados, rotas e arquitetura técnica no arquivo PLAN.md.",
      target: "PLAN.md",
      command: "/plan"
    },
    {
      id: "sdd-tasks",
      type: "sdd",
      name: "Fase 3: TASKS",
      subtitle: "Fatiamento Modular",
      description: "Decomposição do plano em pequenas tarefas testáveis com critérios de aceite independentes.",
      target: "PLAN.md",
      command: "/plan"
    },
    {
      id: "sdd-implement",
      type: "sdd",
      name: "Fase 4: IMPLEMENT",
      subtitle: "Construção Guiada",
      description: "Construção de código estritamente aderente ao contrato da especificação, sem vibe coding e validada pelo checklist.",
      target: "src/ ou integrations/",
      command: "/test"
    },

    // --- 2. MACRO-CATEGORIAS / NÚCLEOS (LARANJA) ---
    {
      id: "core-sdd",
      type: "category",
      name: "Núcleo de Governança SDD",
      subtitle: "Zero Vibe Coding",
      description: "Garante que nenhuma linha de código seja gerada sem especificação prévia aprovada pelo operador."
    },
    {
      id: "core-backend",
      type: "category",
      name: "Backend, APIs & MCP",
      subtitle: "Engenharia de Conexão",
      description: "Servidores robustos, APIs REST/GraphQL, servidores MCP e integração resiliente com serviços externos."
    },
    {
      id: "core-frontend",
      type: "category",
      name: "Frontend, UI/UX & CSS",
      subtitle: "Design de Alto Padrão",
      description: "Interfaces web modernas em Next.js/React, CSS puro, Material Design 3, microinterações e ergonomia."
    },
    {
      id: "core-data",
      type: "category",
      name: "Dados, Analytics & Automações",
      subtitle: "Data Intelligence",
      description: "EDA, consultas OLAP com DuckDB, normalização de planilhas, mineração de PDFs e pipelines em lote."
    },
    {
      id: "core-growth",
      type: "category",
      name: "Conteúdo, Roteiros & Growth",
      subtitle: "Engenharia de Atenção",
      description: "Roteirização para vídeos curtos e longos, arte para redes sociais, copywriting de conversão e microcopy UX."
    },
    {
      id: "core-qa",
      type: "category",
      name: "Qualidade, Testes & Segurança",
      subtitle: "Defesa & Auditoria",
      description: "Pirâmide de testes, automação E2E, varredura de vulnerabilidades OWASP e depuração metódica."
    },
    {
      id: "core-devops",
      type: "category",
      name: "DevOps & Infraestrutura",
      subtitle: "Entrega Contínua",
      description: "Automação de deploy seguro, Docker, processos de servidor e validações pré-voo."
    },
    {
      id: "core-strategy",
      type: "category",
      name: "Estratégia & Produto",
      subtitle: "Viabilidade Econômica",
      description: "Modelagem de negócios, precificação socrática, pacotes comerciais e priorização de escopo."
    },

    // --- 3. AGENTES ESPECIALISTAS (AMARELO) - 35 AGENTES ---
    {
      id: "agent-orchestrator",
      type: "agent",
      name: "orchestrator",
      category: "core-sdd",
      description: "Coordenação multiagente, resolução de conflitos técnicos e síntese de entregas multidomínio."
    },
    {
      id: "agent-sdd-specialist",
      type: "agent",
      name: "sdd-specialist",
      category: "core-sdd",
      description: "Autoridade máxima em Spec-Driven Development e formulação de requisitos formais na sintaxe EARS."
    },
    {
      id: "agent-project-planner",
      type: "agent",
      name: "project-planner",
      category: "core-sdd",
      description: "Planejamento executivo de projetos, levantamento técnico de escopo e arquitetura de entrega em PLAN.md."
    },
    {
      id: "agent-integration-engineer",
      type: "agent",
      name: "integration-engineer",
      category: "core-backend",
      description: "Pesquisa, arquitetura e construção de conectores de APIs e servidores MCP com decisão compartilhada de stack."
    },
    {
      id: "agent-backend-specialist",
      type: "agent",
      name: "backend-specialist",
      category: "core-backend",
      description: "Lógica de servidor de alta robustez, APIs REST/GraphQL, microsserviços e concorrência."
    },
    {
      id: "agent-api-designer",
      type: "agent",
      name: "api-designer",
      category: "core-backend",
      description: "Design de contratos semânticos de API e especificações padronizadas OpenAPI/Swagger."
    },
    {
      id: "agent-database-architect",
      type: "agent",
      name: "database-architect",
      category: "core-backend",
      description: "Modelagem de dados relacional e NoSQL, planos de execução e integridade referencial."
    },
    {
      id: "agent-frontend-specialist",
      type: "agent",
      name: "frontend-specialist",
      category: "core-frontend",
      description: "Aplicações web modernas em Next.js/React, eliminação de waterfalls e ergonomia visual."
    },
    {
      id: "agent-css-architect",
      type: "agent",
      name: "css-architect",
      category: "core-frontend",
      description: "CSS puro avançado, Material Design 3, microinterações, glassmorphism e temas fluidos."
    },
    {
      id: "agent-mobile-developer",
      type: "agent",
      name: "mobile-developer",
      category: "core-frontend",
      description: "Desenvolvimento nativo e híbrido para iOS e Android com ergonomia de toque e estados off-line."
    },
    {
      id: "agent-game-developer",
      type: "agent",
      name: "game-developer",
      category: "core-frontend",
      description: "Mecânicas de jogo 2D/3D no navegador, gamificação, loops de atualização e WebGL."
    },
    {
      id: "agent-data-analyst",
      type: "agent",
      name: "data-analyst",
      category: "core-data",
      description: "Análise exploratória (EDA), estatística descritiva, consultas OLAP via DuckDB e métricas de negócio."
    },
    {
      id: "agent-document-analyst",
      type: "agent",
      name: "document-analyst",
      category: "core-data",
      description: "Mineração e extração tabular de alta fidelidade em documentos PDF, demonstrativos e faturas."
    },
    {
      id: "agent-data-viz-architect",
      type: "agent",
      name: "data-viz-architect",
      category: "core-data",
      description: "Engenharia de visualização de dados e data storytelling sem ruído visual (chartjunk)."
    },
    {
      id: "agent-marketing-analyst",
      type: "agent",
      name: "marketing-analyst",
      category: "core-data",
      description: "Análise de campanhas de anúncios, identificação de criativos campeões e dashboards M3."
    },
    {
      id: "agent-meta-ads-specialist",
      type: "agent",
      name: "meta-ads-specialist",
      category: "core-data",
      description: "Estratégia e auditoria de anúncios no Meta Ads (Instagram/Facebook), públicos e ROAS."
    },
    {
      id: "agent-google-analytics-specialist",
      type: "agent",
      name: "google-analytics-specialist",
      category: "core-data",
      description: "Parametrização GA4, funis de conversão e relatórios analíticos em tempo real via MCP."
    },
    {
      id: "agent-social-listening-analyst",
      type: "agent",
      name: "social-listening-analyst",
      category: "core-data",
      description: "Análise semântica e sentimento de opiniões do público com NLP local e agrupamento temático."
    },
    {
      id: "agent-video-script-architect",
      type: "agent",
      name: "video-script-architect",
      category: "core-growth",
      description: "Roteirização audiovisual com teleprompter de baixa carga cognitiva e tabela de edição em 2 colunas."
    },
    {
      id: "agent-social-media-designer",
      type: "agent",
      name: "social-media-designer",
      category: "core-growth",
      description: "Direção de arte e criação visual de posts e carrosséis com preservação de brand guidelines."
    },
    {
      id: "agent-copywriter-ux",
      type: "agent",
      name: "copywriter-ux",
      category: "core-growth",
      description: "Copywriting persuasivo de vendas aliado a UX Writing empático e sem atrito na interface."
    },
    {
      id: "agent-seo-specialist",
      type: "agent",
      name: "seo-specialist",
      category: "core-growth",
      description: "Otimização para motores de busca (Google) e citação em motores de IA generativa (GEO)."
    },
    {
      id: "agent-test-engineer",
      type: "agent",
      name: "test-engineer",
      category: "core-qa",
      description: "Estratégia de testes unitários, de integração e fluxo TDD rigoroso (Padrão AAA)."
    },
    {
      id: "agent-qa-automation-engineer",
      type: "agent",
      name: "qa-automation-engineer",
      category: "core-qa",
      description: "Automação de testes de ponta a ponta (E2E) com Playwright em pipelines contínuos."
    },
    {
      id: "agent-debugger",
      type: "agent",
      name: "debugger",
      category: "core-qa",
      description: "Diagnóstico metódico de causa-raiz de bugs complexos em 4 fases baseadas em evidências."
    },
    {
      id: "agent-security-auditor",
      type: "agent",
      name: "security-auditor",
      category: "core-qa",
      description: "Auditoria de vulnerabilidades (SAST), segredos embutidos e dependências de código."
    },
    {
      id: "agent-penetration-tester",
      type: "agent",
      name: "penetration-tester",
      category: "core-qa",
      description: "Simulação de ataques ofensivos (Red Team), injeção e exploração de superfícies de risco."
    },
    {
      id: "agent-performance-optimizer",
      type: "agent",
      name: "performance-optimizer",
      category: "core-qa",
      description: "Eliminação de gargalos de processamento, auditoria de Core Web Vitals e renderização."
    },
    {
      id: "agent-code-archaeologist",
      type: "agent",
      name: "code-archaeologist",
      category: "core-qa",
      description: "Refatoração cirúrgica de código legado, redução de dívida técnica e padrões SOLID."
    },
    {
      id: "agent-devops-engineer",
      type: "agent",
      name: "devops-engineer",
      category: "core-devops",
      description: "Automação de releases, containers Docker, processos de servidor e deploy seguro."
    },
    {
      id: "agent-documentation-writer",
      type: "agent",
      name: "documentation-writer",
      category: "core-devops",
      description: "Redação técnica de manuais, documentação viva de sistemas e especificações operacionais."
    },
    {
      id: "agent-explorer-agent",
      type: "agent",
      name: "explorer-agent",
      category: "core-sdd",
      description: "Navegação e inventário de código em repositórios complexos sem alteração de arquivos."
    },
    {
      id: "agent-business-strategist",
      type: "agent",
      name: "business-strategist",
      category: "core-strategy",
      description: "Estratégia comercial, precificação socrática, pacotes de valor e sensibilidade de margens."
    },
    {
      id: "agent-product-manager",
      type: "agent",
      name: "product-manager",
      category: "core-strategy",
      description: "Alinhamento de visão de produto, requisitos de negócio e métricas de impacto (KPIs)."
    },
    {
      id: "agent-product-owner",
      type: "agent",
      name: "product-owner",
      category: "core-strategy",
      description: "Refinamento de backlog, redação de User Stories, critérios de aceite e priorização."
    },

    // --- 4. WORKFLOWS DE COMANDO (VERMELHO) - 21 WORKFLOWS ---
    { id: "wf-sdd", type: "workflow", name: "/sdd", agent: "agent-sdd-specialist", description: "Inicia a fase 1 de especificação formal EARS antes de qualquer código." },
    { id: "wf-create", type: "workflow", name: "/create", agent: "agent-orchestrator", description: "Scaffolding de novas aplicações completas com portão obrigatório de SDD." },
    { id: "wf-plan", type: "workflow", name: "/plan", agent: "agent-project-planner", description: "Gera o plano técnico, arquitetura e tarefas em PLAN.md." },
    { id: "wf-orchestrate", type: "workflow", name: "/orchestrate", agent: "agent-orchestrator", description: "Coordena múltiplos agentes em paralelo para resolver demandas complexas." },
    { id: "wf-brainstorm", type: "workflow", name: "/brainstorm", agent: "agent-project-planner", description: "Exploração socrática de alternativas de design ou negócio." },
    { id: "wf-analyze", type: "workflow", name: "/analyze", agent: "agent-data-analyst", description: "Análise exploratória de dados, planilhas e PDFs com extração de métricas." },
    { id: "wf-batch", type: "workflow", name: "/batch", agent: "agent-data-analyst", description: "Pipeline de automação periódica e geração de relatórios/dashboards em lote." },
    { id: "wf-connect", type: "workflow", name: "/connect", agent: "agent-integration-engineer", description: "Pesquisa e construção de conectores de APIs e servidores MCP testados." },
    { id: "wf-sql", type: "workflow", name: "/sql", agent: "agent-data-analyst", description: "Consultas analíticas OLAP ultrarrápidas em arquivos locais via DuckDB." },
    { id: "wf-strategy", type: "workflow", name: "/strategy", agent: "agent-business-strategist", description: "Modelagem de negócio, bundles comerciais e precificação estratégica." },
    { id: "wf-copy", type: "workflow", name: "/copy", agent: "agent-copywriter-ux", description: "Textos persuasivos de venda para landing pages e microcopy de interface." },
    { id: "wf-post", type: "workflow", name: "/post", agent: "agent-social-media-designer", description: "Geração de posts e carrosséis para redes sociais com roteiro visual." },
    { id: "wf-script", type: "workflow", name: "/script", agent: "agent-video-script-architect", description: "Roteirização audiovisual para teleprompter e tabela de edição em 2 colunas." },
    { id: "wf-refactor", type: "workflow", name: "/refactor", agent: "agent-code-archaeologist", description: "Refatoração estrutural de código e eliminação de débito técnico." },
    { id: "wf-debug", type: "workflow", name: "/debug", agent: "agent-debugger", description: "Investigação metódica em 4 fases para identificação de causa-raiz." },
    { id: "wf-test", type: "workflow", name: "/test", agent: "agent-test-engineer", description: "Criação e execução de suítes de teste automatizadas (AAA/TDD)." },
    { id: "wf-preview", type: "workflow", name: "/preview", agent: "agent-orchestrator", description: "Gerencia o servidor de desenvolvimento local para inspeção de telas." },
    { id: "wf-deploy", type: "workflow", name: "/deploy", agent: "agent-devops-engineer", description: "Validações pré-voo e publicação segura de releases em produção." },
    { id: "wf-status", type: "workflow", name: "/status", agent: "agent-orchestrator", description: "Exibe o quadro de progresso e estado operacional do projeto." },
    { id: "wf-api-design", type: "workflow", name: "/api-design", agent: "agent-api-designer", description: "Criação de contratos de API e especificações OpenAPI." },
    { id: "wf-enhance", type: "workflow", name: "/enhance", agent: "agent-frontend-specialist", description: "Evolução incremental de funcionalidades em código existente." }
  ],

  // Gerador dinâmico de conexões (Links)
  getLinks: function() {
    const links = [];

    // Conectar fases SDD sequencialmente
    links.push({ source: "sdd-specify", target: "sdd-plan" });
    links.push({ source: "sdd-plan", target: "sdd-tasks" });
    links.push({ source: "sdd-tasks", target: "sdd-implement" });

    // Conectar SDD aos seus agentes guardiões
    links.push({ source: "sdd-specify", target: "agent-sdd-specialist" });
    links.push({ source: "sdd-plan", target: "agent-project-planner" });
    links.push({ source: "sdd-tasks", target: "agent-project-planner" });
    links.push({ source: "sdd-implement", target: "agent-frontend-specialist" });
    links.push({ source: "sdd-implement", target: "agent-backend-specialist" });

    // Conectar Macro-Categorias aos Agentes
    this.nodes.forEach(node => {
      if (node.type === "agent" && node.category) {
        links.push({ source: node.category, target: node.id });
      }
    });

    // Conectar Workflows aos Agentes Responsáveis
    this.nodes.forEach(node => {
      if (node.type === "workflow" && node.agent) {
        links.push({ source: node.id, target: node.agent });
      }
    });

    // Interconexões neurais estratégicas entre agentes
    const agentPairs = [
      ["agent-orchestrator", "agent-sdd-specialist"],
      ["agent-orchestrator", "agent-project-planner"],
      ["agent-frontend-specialist", "agent-css-architect"],
      ["agent-backend-specialist", "agent-integration-engineer"],
      ["agent-backend-specialist", "agent-database-architect"],
      ["agent-data-analyst", "agent-document-analyst"],
      ["agent-data-analyst", "agent-data-viz-architect"],
      ["agent-marketing-analyst", "agent-meta-ads-specialist"],
      ["agent-marketing-analyst", "agent-google-analytics-specialist"],
      ["agent-video-script-architect", "agent-copywriter-ux"],
      ["agent-social-media-designer", "agent-copywriter-ux"],
      ["agent-test-engineer", "agent-qa-automation-engineer"],
      ["agent-debugger", "agent-code-archaeologist"],
      ["agent-security-auditor", "agent-penetration-tester"],
      ["agent-devops-engineer", "agent-performance-optimizer"],
      ["agent-business-strategist", "agent-product-manager"]
    ];

    agentPairs.forEach(([src, tgt]) => {
      links.push({ source: src, target: tgt });
    });

    return links;
  },

  // Helper para adicionar novos nós facilmente no futuro
  addNode: function(nodeData) {
    if (!nodeData.id || !nodeData.type || !nodeData.name) {
      console.error("Dados de nó inválidos. Campos obrigatórios: id, type, name");
      return false;
    }
    this.nodes.push(nodeData);
    return true;
  },

  // Estatísticas calculadas dinamicamente
  getStats: function() {
    const stats = { agent: 0, workflow: 0, skill: 54, category: 0, sdd: 0 };
    this.nodes.forEach(n => {
      if (stats[n.type] !== undefined) stats[n.type]++;
    });
    return stats;
  }
};
