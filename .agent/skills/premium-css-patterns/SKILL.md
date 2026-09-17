---
name: premium-css-patterns
description: Advanced CSS architecture, Material Design 3 (M3) principles, modern layouts, micro-animations, and premium styling patterns.
allowed-tools: Read, Write, Edit, Glob, Grep
version: 1.0
priority: HIGH
---

# Premium CSS Patterns & Material Design 3 (M3)

> **PREMIUM SKILL** - Elevate UI design to a state-of-the-art, professional, and visually stunning level.

---

## 1. Material Design 3 (M3) Foundations

Material Design 3 (M3) is Google’s most adaptable design system. Every CSS implementation must respect its core principles:

| Core Concept | Implementation Rule |
|--------------|---------------------|
| **Dynamic Color** | Use CSS variables for color tokens. Group colors functionally (e.g., `--md-sys-color-primary`, `--md-sys-color-on-primary`, `--md-sys-color-surface`). |
| **Typography** | Use specific type scales (Display, Headline, Title, Body, Label). Set correct line-heights and font-weights following M3 guidelines. |
| **Elevation** | Avoid heavy drop shadows. Use surface tonal elevation (background color shifts) combined with subtle, layered shadows to denote depth. |
| **Shape** | Use rounded corners intentionally. Define shape families (e.g., `--md-sys-shape-corner-small: 8px`, `--md-sys-shape-corner-extra-large: 28px`). |

---

## 2. Modern CSS Architecture

| Principle | Rule |
|-----------|------|
| **CSS Variables (Custom Properties)** | Base all theming, spacing, and sizing on variables. Avoid hardcoded values. |
| **Logical Properties** | Use `margin-inline`, `padding-block`, etc., instead of `margin-left` or `padding-top` for native RTL support. |
| **Grid & Flexbox** | Use CSS Grid for overall page layouts and 2D alignment. Use Flexbox for 1D component layouts. |
| **Container Queries** | Use `@container` instead of `@media` for component-level responsiveness. |
| **Fluid Typography** | Use `clamp()` for responsive font sizes and spacing (e.g., `font-size: clamp(1rem, 2vw + 0.5rem, 1.5rem)`). |

---

## 3. Micro-Animations & Interactions

Premium UI feels alive. Use subtle animations to provide user feedback:

| Interaction | Standard Practice |
|-------------|-------------------|
| **Hover States** | Scale up slightly (`transform: scale(1.02)`), elevate shadow, or shift background color. |
| **Active/Click States** | Scale down slightly (`transform: scale(0.98)`). Apply M3 standard ripple effects if applicable. |
| **Transitions** | Use `transition: all 0.2s cubic-bezier(0.2, 0, 0, 1)`. Avoid linear transitions; use easing functions that mimic physical momentum. |
| **Loading States** | Use skeleton screens with shimmer effects (`linear-gradient` with background animation) instead of standard spinners. |

---

## 4. Visual Excellence & Aesthetics

| Trend/Technique | Implementation |
|-----------------|----------------|
| **Glassmorphism** | Combine `backdrop-filter: blur(12px)`, translucent background colors (e.g., `rgba(255,255,255,0.1)`), and a subtle `border: 1px solid rgba(255,255,255,0.2)`. |
| **Gradients** | Use smooth, multi-stop gradients or mesh gradients. Avoid harsh 2-color linear gradients. |
| **Dark Mode** | Desaturate primary colors for dark mode. Use dark gray (not pure black `#000`) for backgrounds to reduce eye strain and allow elevation layers to be visible. |

---

## 5. CSS Anti-Patterns (DON'T)

| ❌ Pattern | ✅ Fix |
|-----------|-------|
| Deeply nested selectors (`.card .header h2 span`) | Flatten selectors. Use BEM or utility classes. |
| `!important` | Fix specificity issues by reorganizing CSS or using `:where()` / `:is()`. |
| Magic Numbers (`margin-top: 37px`) | Use spacing scale variables (`var(--spacing-md)`). |
| Fixed widths (`width: 500px`) | Use `max-width` with percentages or `fit-content` for responsive flow. |
| Pure black (`#000000`) text | Use `#1f1f1f` or `var(--md-sys-color-on-surface)` for better readability. |

---

> **Remember:** A premium CSS implementation is not just about making it look "good". It's about accessibility, performance, systematic design (M3), and creating a responsive, fluid user experience.
