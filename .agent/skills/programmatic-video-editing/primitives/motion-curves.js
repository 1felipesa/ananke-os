/**
 * ============================================================================
 * ANANKE OS — MOTION CURVES & ANIMATION ENGINE (GSAP)
 * Motor de física, interpolações e micro-interações para HyperFrames.
 * Elimina o "ar amador" substituindo interpolações secas por inércia e overshoot.
 * ============================================================================
 */

import { gsap } from 'gsap';

/**
 * 1. MATRIZ DE EASINGS PROFISSIONAIS
 * Proíbe interpolações lineares em movimento de objetos na tela.
 */
export const EASINGS = {
  // Entrada elástica com overshoot (o elemento ultrapassa 5-10% e assenta com peso)
  snappy: 'back.out(1.7)',
  
  // Entrada cinematográfica e editorial de alta tecnologia
  smooth: 'expo.out',
  
  // Impacto elástico para badges, selos e ícones de ênfase
  pop: 'elastic.out(1, 0.75)',
  
  // Saída acelerada para transições rápidas
  exit: 'power3.in',
  
  // Movimento de câmera e transição de enquadramento
  camera: 'power2.inOut',
};

/**
 * 2. CÂMERA DINÂMICA: Punch-in de ênfase (Camada 5)
 * Aplica uma leve aproximação de câmera (1.04x - 1.08x) sincronizada com a fala.
 * 
 * @param {HTMLElement|string} target - Container do viewport ou cena
 * @param {number} scale - Fator de escala (padrão: 1.05)
 * @param {number} duration - Duração em segundos (padrão: 0.35)
 */
export function punchInCamera(target = '#viewport', scale = 1.05, duration = 0.35) {
  return gsap.to(target, {
    scale,
    duration,
    ease: EASINGS.snappy,
    transformOrigin: 'center 40%',
  });
}

/**
 * Restaura a câmera para escala neutra (1.0)
 */
export function resetCamera(target = '#viewport', duration = 0.4) {
  return gsap.to(target, {
    scale: 1,
    duration,
    ease: EASINGS.smooth,
  });
}

/**
 * 3. REVELAÇÃO EM CASCATA (Stagger Reveal)
 * Faz elementos (palavras, itens de lista, barras de gráficos) entrarem em ordem.
 * 
 * @param {NodeList|Array} elements - Lista de elementos
 * @param {Object} options - Configurações de transição
 */
export function staggerReveal(elements, options = {}) {
  const {
    duration = 0.5,
    stagger = 0.06,
    y = 40,
    opacity = 0,
    ease = EASINGS.snappy,
  } = options;

  return gsap.from(elements, {
    y,
    opacity,
    duration,
    stagger,
    ease,
  });
}

/**
 * 4. TRAÇADO VETORIAL DE SVG (Camada 4 - Gráficos)
 * Desenha suavemente linhas de tendência, setas ou bordas de gráficos.
 * 
 * @param {SVGPathElement|string} pathElement - Elemento <path> SVG
 * @param {number} duration - Duração da animação em segundos
 */
export function drawSvgPath(pathElement, duration = 0.8) {
  const path = typeof pathElement === 'string' ? document.querySelector(pathElement) : pathElement;
  if (!path) return null;

  const length = path.getTotalLength();
  
  // Inicializa o traçado oculto
  gsap.set(path, {
    strokeDasharray: length,
    strokeDashoffset: length,
  });

  return gsap.to(path, {
    strokeDashoffset: 0,
    duration,
    ease: EASINGS.smooth,
  });
}

/**
 * 5. CONTADOR NUMÉRICO ROLANTE (Number Ticker)
 * Anima métricas (ex: +340%, R$ 1.500, 10x) de forma fluida.
 * 
 * @param {HTMLElement|string} target - Elemento de texto
 * @param {number} endVal - Valor numérico final
 * @param {Object} options - Opções de formatação e duração
 */
export function animateCounter(target, endVal, options = {}) {
  const el = typeof target === 'string' ? document.querySelector(target) : target;
  if (!el) return null;

  const {
    startVal = 0,
    duration = 1.0,
    prefix = '',
    suffix = '',
    decimals = 0,
    ease = 'power2.out',
  } = options;

  const counterObj = { val: startVal };

  return gsap.to(counterObj, {
    val: endVal,
    duration,
    ease,
    onUpdate: () => {
      const formatted = counterObj.val.toLocaleString('pt-BR', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals,
      });
      el.textContent = `${prefix}${formatted}${suffix}`;
    },
  });
}

/**
 * 6. KINETIC WORD PUNCH (Camada 2 - Legendas Karaoke)
 * Destaca a palavra ativa no milissegundo de fala com escala elástica e glow.
 * 
 * @param {HTMLElement} activeWordEl - Elemento <span> da palavra falada
 * @param {string} accentColor - Cor de destaque da marca
 */
export function kineticWordPunch(activeWordEl, accentColor = 'var(--brand-accent)') {
  if (!activeWordEl) return null;

  const tl = gsap.timeline();

  tl.to(activeWordEl, {
    scale: 1.18,
    color: accentColor,
    textShadow: `0 0 24px ${accentColor}`,
    duration: 0.12,
    ease: EASINGS.snappy,
  }).to(activeWordEl, {
    scale: 1.05,
    duration: 0.15,
    ease: 'power1.out',
  });

  return tl;
}

/**
 * 7. TRANSIÇÃO GEOMÉTRICA DO CARD DO APRESENTADOR (Camada 3)
 * Alterna suavemente o formato do card (central -> lateral -> pílula -> tela cheia)
 * 
 * @param {HTMLElement|string} cardEl - Elemento do card de vídeo
 * @param {Object} targetGeometry - Dimensões e posicionamento de destino
 */
export function morphFaceCard(cardEl, targetGeometry, duration = 0.6) {
  const el = typeof cardEl === 'string' ? document.querySelector(cardEl) : cardEl;
  if (!el) return null;

  return gsap.to(el, {
    top: targetGeometry.top,
    left: targetGeometry.left,
    width: targetGeometry.width,
    height: targetGeometry.height,
    borderRadius: targetGeometry.borderRadius || 'var(--brand-radius-lg)',
    duration,
    ease: EASINGS.snappy,
  });
}
