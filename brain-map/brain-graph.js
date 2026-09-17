/**
 * Ananke OS - 3D Neural Brain Map Graph Engine
 * Spec-Driven Autonomy // Zero Vibe Coding
 * High-performance 3D Force-Directed Constellation powered by Three.js & 3d-force-graph.
 */

let Graph = null;
let selectedNode = null;
let highlightNodes = new Set();
let highlightLinks = new Set();
let activeFilter = "all";
let isAutoRotating = true;
let userInteracted = false;

document.addEventListener("DOMContentLoaded", () => {
  initBrainMap();
  initUIEvents();
});

function initBrainMap() {
  const container = document.getElementById("canvas-container");
  if (!container) return;

  const data = {
    nodes: KIT_BRAIN_DATA.nodes.map(n => ({ ...n })),
    links: KIT_BRAIN_DATA.getLinks()
  };

  // Node sizes based on ontological hierarchy
  const sizeMap = {
    category: 12,
    sdd: 9,
    agent: 6.5,
    workflow: 5.5,
    skill: 4
  };

  try {
    Graph = ForceGraph3D({ controlType: 'orbit' })(container)
      .graphData(data)
      .backgroundColor("#07090e")
      .showNavInfo(false)
      // Node Styling
      .nodeLabel(node => `
        <div style="background: rgba(15,20,30,0.95); padding: 8px 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.15); font-family: Outfit, sans-serif; font-size: 13px; color: #fff; box-shadow: 0 8px 24px rgba(0,0,0,0.5);">
          <div style="color: ${KIT_BRAIN_DATA.config.colors[node.type]}; font-weight: 700; text-transform: uppercase; font-size: 10px; letter-spacing: 0.5px; margin-bottom: 2px;">
            ${KIT_BRAIN_DATA.config.labels[node.type] || node.type}
          </div>
          <strong style="font-size: 14px;">${node.name}</strong>
          ${node.subtitle ? `<div style="color: #94a3b8; font-size: 11px;">${node.subtitle}</div>` : ''}
        </div>
      `)
      .nodeColor(node => {
        if (activeFilter !== "all" && node.type !== activeFilter) {
          return "rgba(255, 255, 255, 0.08)";
        }
        if (highlightNodes.size > 0 && !highlightNodes.has(node)) {
          return "rgba(255, 255, 255, 0.12)";
        }
        return KIT_BRAIN_DATA.config.colors[node.type] || "#ffffff";
      })
      .nodeVal(node => sizeMap[node.type] || 5)
      .nodeResolution(24)
      // Link Styling - High-Presence Luminous Neural Wires
      .linkColor(link => {
        if (highlightLinks.has(link)) {
          return "#00FFFF";
        }
        if (highlightNodes.size > 0) {
          return "rgba(0, 210, 255, 0.08)";
        }
        const srcType = typeof link.source === "object" ? link.source.type : "";
        const tgtType = typeof link.target === "object" ? link.target.type : "";
        if (srcType === "category" || tgtType === "category") {
          return "rgba(251, 146, 60, 0.65)"; // Vibrant orange axon
        }
        if (srcType === "sdd" || tgtType === "sdd") {
          return "rgba(16, 185, 129, 0.65)"; // Emerald governance synapse
        }
        return "rgba(0, 210, 255, 0.55)"; // High-contrast electric cyan
      })
      .linkWidth(link => {
        if (highlightLinks.has(link)) return 3.5;
        const srcType = typeof link.source === "object" ? link.source.type : "";
        const tgtType = typeof link.target === "object" ? link.target.type : "";
        if (srcType === "category" || tgtType === "category" || srcType === "sdd" || tgtType === "sdd") {
          return 2.4;
        }
        return 1.8;
      })
      .linkDirectionalParticles(link => (highlightLinks.has(link) ? 6 : 2))
      .linkDirectionalParticleWidth(link => (highlightLinks.has(link) ? 3.5 : 2.2))
      .linkDirectionalParticleSpeed(0.007)
      .linkDirectionalParticleColor(link => {
        if (highlightLinks.has(link)) return "#FFFFFF";
        const srcType = typeof link.source === "object" ? link.source.type : "";
        if (srcType === "category") return "#FDBA74";
        if (srcType === "sdd") return "#6EE7B7";
        return "#67E8F9";
      })
      // Interactivity
      .onNodeClick(node => {
        focusNode(node);
      })
      .onBackgroundClick(() => {
        resetFocus();
      })
      .onNodeHover(node => {
        container.style.cursor = node ? "pointer" : "default";
      });

    // Custom Physics Tuning for Organic Neural Brain Layout
    Graph.d3Force("charge").strength(-120);
    Graph.d3Force("link").distance(link => {
      if (link.source.type === "category" || link.target.type === "category") return 70;
      if (link.source.type === "sdd" || link.target.type === "sdd") return 50;
      return 35;
    });

    // Camera initial position
    Graph.cameraPosition({ x: 0, y: 0, z: 450 });

    // Native OrbitControls setup for smooth 360 rotation & responsive zooming
    const controls = Graph.controls();
    if (controls) {
      controls.enableZoom = true;
      controls.zoomSpeed = 1.2;
      controls.minDistance = 30;
      controls.maxDistance = 2500;
      controls.enablePan = true;
      controls.panSpeed = 1.0;
      controls.enableRotate = true;
      controls.rotateSpeed = 1.0;
      controls.autoRotate = true;
      controls.autoRotateSpeed = 0.5;
    }

    // Stop auto-rotation when user interacts with mouse or scroll wheel
    container.addEventListener("pointerdown", () => {
      if (Graph && Graph.controls()) {
        Graph.controls().autoRotate = false;
      }
    });

    window.addEventListener("wheel", (e) => {
      if (e.target.closest && (e.target.closest("#drawer-inspector") || e.target.closest("#brain-search"))) {
        return;
      }
      if (Graph && Graph.controls()) {
        Graph.controls().autoRotate = false;
      }
    }, { passive: true });

  } catch (err) {
    console.error("Erro ao inicializar 3D Force Graph:", err);
    const isOffline = typeof ForceGraph3D === "undefined";
    container.innerHTML = `
      <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); max-width: 480px; padding: 32px; background: rgba(15, 23, 42, 0.95); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; text-align: center; color: #f8fafc; font-family: Outfit, sans-serif; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6); z-index: 1000;">
        <div style="font-size: 40px; margin-bottom: 12px;">⚡</div>
        <h2 style="font-size: 20px; font-weight: 700; margin-bottom: 8px; color: #00FFFF;">${isOffline ? 'Conexão com a CDN Necessária' : 'Aceleração WebGL Indisponível'}</h2>
        <p style="color: #94a3b8; font-size: 14px; line-height: 1.6; margin-bottom: 20px;">
          ${isOffline 
            ? 'Não foi possível carregar o motor 3D da CDN unpkg. Verifique sua conexão com a internet para navegar pela rede neural tridimensional.' 
            : 'Seu navegador não conseguiu inicializar o contexto 3D. Verifique se a aceleração gráfica por hardware está ativa.'}
        </p>
        <button onclick="window.location.reload()" style="background: linear-gradient(135deg, #00D2FF, #0072FF); color: #fff; border: none; padding: 10px 20px; background-color: #00D2FF; border-radius: 8px; font-weight: 600; cursor: pointer; font-size: 13px;">Tentar Novamente</button>
      </div>
    `;
  }
}

function focusNode(node) {
  selectedNode = node;
  isAutoRotating = false;

  // Build connected highlights
  highlightNodes.clear();
  highlightLinks.clear();

  if (node) {
    highlightNodes.add(node);
    const graphData = Graph.graphData();
    graphData.links.forEach(link => {
      const srcId = typeof link.source === "object" ? link.source.id : link.source;
      const tgtId = typeof link.target === "object" ? link.target.id : link.target;

      if (srcId === node.id || tgtId === node.id) {
        highlightLinks.add(link);
        highlightNodes.add(link.source);
        highlightNodes.add(link.target);
      }
    });

    // Camera fly to node safely
    if (typeof node.x === "number" && typeof node.y === "number" && typeof node.z === "number") {
      const distance = 90;
      const hyp = Math.hypot(node.x, node.y, node.z) || 1;
      const distRatio = 1 + distance / hyp;
      Graph.cameraPosition(
        { x: node.x * distRatio, y: node.y * distRatio, z: node.z * distRatio },
        node,
        1200
      );
    }

    openDrawer(node);
  }

  // Refresh visual state
  Graph.nodeColor(Graph.nodeColor())
    .linkColor(Graph.linkColor())
    .linkWidth(Graph.linkWidth());
}

function resetFocus() {
  selectedNode = null;
  highlightNodes.clear();
  highlightLinks.clear();
  closeDrawer();

  if (Graph) {
    Graph.nodeColor(Graph.nodeColor())
      .linkColor(Graph.linkColor())
      .linkWidth(Graph.linkWidth());
  }
}

function openDrawer(node) {
  const drawer = document.getElementById("drawer-inspector");
  const badgeType = document.getElementById("drawer-type-badge");
  const title = document.getElementById("drawer-title");
  const subtitle = document.getElementById("drawer-subtitle");
  const desc = document.getElementById("drawer-desc");
  const connectionsContainer = document.getElementById("drawer-connections");

  if (!drawer) return;

  const color = KIT_BRAIN_DATA.config.colors[node.type] || "#fff";
  badgeType.style.backgroundColor = `rgba(${hexToRgb(color)}, 0.15)`;
  badgeType.style.color = color;
  badgeType.style.border = `1px solid rgba(${hexToRgb(color)}, 0.4)`;
  badgeType.textContent = KIT_BRAIN_DATA.config.labels[node.type] || node.type;

  title.textContent = node.name;
  subtitle.textContent = node.subtitle || node.target || (node.command ? `Disparo: ${node.command}` : "");
  desc.textContent = node.description || "Nenhum detalhe adicional cadastrado.";

  // Render direct connections
  connectionsContainer.innerHTML = "";
  const neighbors = Array.from(highlightNodes).filter(n => n.id !== node.id);
  if (neighbors.length > 0) {
    neighbors.forEach(neighbor => {
      const chip = document.createElement("div");
      chip.className = "conn-chip";
      chip.textContent = neighbor.name;
      chip.style.borderColor = `rgba(${hexToRgb(KIT_BRAIN_DATA.config.colors[neighbor.type] || "#ffffff")}, 0.3)`;
      chip.onclick = () => focusNode(neighbor);
      connectionsContainer.appendChild(chip);
    });
  } else {
    connectionsContainer.innerHTML = "<span style='font-size: 12px; color: #64748b;'>Sem conexões diretas mapeadas.</span>";
  }

  drawer.classList.add("open");
}

function closeDrawer() {
  const drawer = document.getElementById("drawer-inspector");
  if (drawer) drawer.classList.remove("open");
}

function initUIEvents() {
  // Close drawer button
  const closeBtn = document.getElementById("drawer-close-btn");
  if (closeBtn) {
    closeBtn.addEventListener("click", () => {
      resetFocus();
    });
  }

  // Search input filter
  const searchInput = document.getElementById("brain-search");
  if (searchInput) {
    searchInput.addEventListener("input", e => {
      const query = e.target.value.toLowerCase().trim();
      if (!query) {
        resetFocus();
        return;
      }

      highlightNodes.clear();
      highlightLinks.clear();

      const matchedNodes = KIT_BRAIN_DATA.nodes.filter(
        n =>
          n.name.toLowerCase().includes(query) ||
          (n.description && n.description.toLowerCase().includes(query)) ||
          (n.subtitle && n.subtitle.toLowerCase().includes(query))
      );

      if (matchedNodes.length > 0) {
        matchedNodes.forEach(n => {
          const liveNode = Graph.graphData().nodes.find(gn => gn.id === n.id);
          if (liveNode) highlightNodes.add(liveNode);
        });

        // Focus on first match safely
        const first = Array.from(highlightNodes)[0];
        if (first && typeof first.x === "number" && typeof first.y === "number" && typeof first.z === "number") {
          Graph.cameraPosition(
            { x: first.x * 1.5, y: first.y * 1.5, z: first.z * 1.5 },
            first,
            1000
          );
        }
      }

      Graph.nodeColor(Graph.nodeColor());
    });
  }

  // Legend and Filter clicks
  document.querySelectorAll("[data-filter]").forEach(el => {
    el.addEventListener("click", () => {
      const filterType = el.getAttribute("data-filter");
      activeFilter = filterType;
      resetFocus();

      document.querySelectorAll("[data-filter]").forEach(item => {
        item.style.opacity = item.getAttribute("data-filter") === filterType ? "1" : "0.6";
      });

      Graph.nodeColor(Graph.nodeColor());
    });
  });

  // Floating Zoom Buttons
  const btnZoomIn = document.getElementById("btn-zoom-in");
  const btnZoomOut = document.getElementById("btn-zoom-out");
  const btnResetView = document.getElementById("btn-reset-view");

  if (btnZoomIn) {
    btnZoomIn.addEventListener("click", () => zoomCamera(0.7));
  }
  if (btnZoomOut) {
    btnZoomOut.addEventListener("click", () => zoomCamera(1.4));
  }
  if (btnResetView) {
    btnResetView.addEventListener("click", () => resetView());
  }
}

function zoomCamera(factor) {
  if (!Graph) return;
  const controls = Graph.controls();
  if (controls) {
    controls.autoRotate = false;
  }
  const cam = Graph.camera();
  const target = controls && controls.target ? controls.target : { x: 0, y: 0, z: 0 };
  
  const currentDist = Math.hypot(cam.position.x - target.x, cam.position.y - target.y, cam.position.z - target.z);
  const newDist = Math.max(40, Math.min(2500, currentDist * factor));
  const ratio = newDist / (currentDist || 1);

  Graph.cameraPosition(
    {
      x: target.x + (cam.position.x - target.x) * ratio,
      y: target.y + (cam.position.y - target.y) * ratio,
      z: target.z + (cam.position.z - target.z) * ratio
    },
    target,
    350
  );
}

function resetView() {
  if (!Graph) return;
  const controls = Graph.controls();
  if (controls) {
    controls.autoRotate = true;
  }
  resetFocus();
  Graph.cameraPosition({ x: 0, y: 0, z: 450 }, { x: 0, y: 0, z: 0 }, 900);
}

function hexToRgb(hex) {
  hex = hex.replace("#", "");
  if (hex.length === 3) {
    hex = hex.split("").map(c => c + c).join("");
  }
  const bigint = parseInt(hex, 16);
  const r = (bigint >> 16) & 255;
  const g = (bigint >> 8) & 255;
  const b = bigint & 255;
  return `${r}, ${g}, ${b}`;
}
