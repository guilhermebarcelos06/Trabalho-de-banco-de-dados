---
name: design-system-architect
description: >-
  Define, maintain, and audit semantic design tokens (colors, fluid typography, 4px/8px spacing scales, border radii, shadows/elevation, and dark/light themes).
  Enforces zero-hardcoded-values rules, ensuring all components consume semantic CSS variables or centralized Tailwind tokens.
triggers:
  - "criar design tokens"
  - "definir paleta de cores"
  - "configurar temas light/dark"
  - "tipografia fluida"
  - "escala de espaçamento"
  - "remover valores hardcoded"
  - "design system"
  - "tokens semânticos"
  - "variáveis css de tema"
---

# Design System Architect

Esta skill estabelece e governa a infraestrutura de **Design Tokens Semânticos**, garantindo que nenhum valor visual (cor hexadecimal, pixel arbitrário de espaçamento, raio de borda ou sombra) seja codificado de forma estática nos componentes. Tudo deve fluir de uma arquitetura centralizada em três camadas.

---

## 1. Arquitetura de Tokens em 3 Camadas

Para manter manutenibilidade e escalabilidade, todo token deve respeitar a hierarquia:

```
[ Camada 1: Primitivos / Globais ]  -> Valores brutos (ex: blue-500: #3b82f6, space-4: 16px)
             │
             ▼
[ Camada 2: Semânticos / Contexto ] -> Papéis de UI (ex: --primary, --surface-raised, --border-subtle)
             │
             ▼
[ Camada 3: Componente ]            -> Elementos específicos (ex: --btn-bg: var(--primary))
```

> **Regra Fundamental:** Os componentes de interface **NUNCA** acessam a Camada 1 diretamente. Eles consomem exclusivamente a **Camada 2 (Semântica)** ou a **Camada 3 (Componente)**.

---

## 2. Dicionário Canônico de Tokens Semânticos

Toda aplicação deve definir a seguinte estrutura mínima no seu arquivo central de estilos (ex: `tokens.css` ou `globals.css`):

```css
:root {
  /* ==========================================================================
     1. Superfícies e Fundos (Surfaces)
     ========================================================================== */
  --surface: #ffffff;
  --surface-subtle: #f8fafc;
  --surface-raised: #ffffff;
  --surface-overlay: #ffffff;
  --surface-sunken: #f1f5f9;

  /* ==========================================================================
     2. Tipografia e Cores de Frente (Foregrounds)
     ========================================================================== */
  --foreground: #0f172a;
  --foreground-muted: #64748b;
  --foreground-subtle: #94a3b8;
  --foreground-inverse: #ffffff;

  /* ==========================================================================
     3. Cores de Destaque e Ação (Brand & Accent)
     ========================================================================== */
  --primary: #2563eb;
  --primary-hover: #1d4ed8;
  --primary-active: #1e40af;
  --primary-foreground: #ffffff;

  --accent: #f1f5f9;
  --accent-foreground: #0f172a;

  /* ==========================================================================
     4. Estados Semânticos (Feedback)
     ========================================================================== */
  --destructive: #dc2626;
  --destructive-hover: #b91c1c;
  --destructive-foreground: #ffffff;

  --success: #16a34a;
  --success-foreground: #ffffff;

  --warning: #d97706;
  --warning-foreground: #ffffff;

  --info: #0284c7;
  --info-foreground: #ffffff;

  /* ==========================================================================
     5. Bordas, Divisores e Foco (Borders & Focus)
     ========================================================================== */
  --border: rgba(15, 23, 42, 0.08);
  --border-subtle: rgba(15, 23, 42, 0.04);
  --border-strong: rgba(15, 23, 42, 0.16);

  --ring: #2563eb;
  --ring-offset: #ffffff;

  /* ==========================================================================
     6. Raios de Borda (Radii)
     ========================================================================== */
  --radius-xs: 4px;
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-full: 9999px;

  /* ==========================================================================
     7. Elevação e Sombras (Elevations)
     ========================================================================== */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.07), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -4px rgba(0, 0, 0, 0.04);
  --shadow-focus: 0 0 0 2px var(--ring-offset), 0 0 0 4px var(--ring);
}

/* ==========================================================================
   Tema Escuro (Dark Mode)
   ========================================================================== */
[data-theme="dark"],
.dark {
  --surface: #090d16;
  --surface-subtle: #0f172a;
  --surface-raised: #1e293b;
  --surface-overlay: #1e293b;
  --surface-sunken: #020617;

  --foreground: #f8fafc;
  --foreground-muted: #94a3b8;
  --foreground-subtle: #64748b;
  --foreground-inverse: #0f172a;

  --primary: #3b82f6;
  --primary-hover: #60a5fa;
  --primary-active: #2563eb;
  --primary-foreground: #ffffff;

  --accent: #1e293b;
  --accent-foreground: #f8fafc;

  --destructive: #ef4444;
  --destructive-hover: #f87171;
  --destructive-foreground: #ffffff;

  --success: #22c55e;
  --success-foreground: #ffffff;

  --warning: #f59e0b;
  --warning-foreground: #000000;

  --border: rgba(255, 255, 255, 0.08);
  --border-subtle: rgba(255, 255, 255, 0.04);
  --border-strong: rgba(255, 255, 255, 0.16);

  --ring: #60a5fa;
  --ring-offset: #090d16;

  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.4);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.5), 0 2px 4px -2px rgba(0, 0, 0, 0.4);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.6), 0 4px 6px -4px rgba(0, 0, 0, 0.4);
}
```

---

## 3. Escala de Espaçamento Modular (Grid de 4px / 8px)

Nenhum valor de espaçamento fora desta escala é permitido:

| Token / Step | Valor em Pixels | Valor em REM | Uso Típico |
| :--- | :--- | :--- | :--- |
| `space-1` | 4px | 0.25rem | Gaps mínimos, badges, micro-ícones |
| `space-2` | 8px | 0.5rem | Padding interno de inputs, botões compactos, gap de tags |
| `space-3` | 12px | 0.75rem | Padding vertical de botões padrão, espaçamento entre itens compactos |
| `space-4` | 16px | 1.0rem | Padding padrão de cards, margens de formulário |
| `space-5` | 20px | 1.25rem | Gaps de seções intermediárias |
| `space-6` | 24px | 1.5rem | Espaçamento entre cartões, paddings amplos |
| `space-8` | 32px | 2.0rem | Divisão entre grupos de conteúdo |
| `space-10` | 40px | 2.5rem | Margem superior de títulos principais |
| `space-12` | 48px | 3.0rem | Respiro entre seções de página |
| `space-16` | 64px | 4.0rem | Seções hero e rodapés |

---

## 4. Tipografia Fluida com Razão Modular

Evite alterar tamanhos de fonte exclusivamente por media queries fixas. Utilize funções de interpolação fluida (`clamp()`):

```css
:root {
  /* Escala tipográfica fluida: MinViewport=375px (23.4rem) | MaxViewport=1440px (90rem) */
  --font-size-xs: clamp(0.75rem, 0.73rem + 0.1vw, 0.8125rem);
  --font-size-sm: clamp(0.875rem, 0.85rem + 0.12vw, 0.9375rem);
  --font-size-base: clamp(1rem, 0.96rem + 0.18vw, 1.125rem);
  --font-size-lg: clamp(1.125rem, 1.07rem + 0.25vw, 1.25rem);
  --font-size-xl: clamp(1.25rem, 1.16rem + 0.4vw, 1.5rem);
  --font-size-2xl: clamp(1.5rem, 1.35rem + 0.65vw, 1.875rem);
  --font-size-3xl: clamp(1.875rem, 1.65rem + 1.0vw, 2.375rem);
  --font-size-4xl: clamp(2.25rem, 1.95rem + 1.4vw, 3.0rem);

  /* Alturas de Linha Relativas */
  --line-height-tight: 1.15;
  --line-height-snug: 1.3;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.65;
}
```

---

## 5. Checklist Determinístico de Verificação

Antes de aprovar qualquer alteração de estilo ou componente:

- [ ] **Zero Hardcoded Colors:** Nenhum arquivo de componente (`.tsx`, `.vue`, `.html`, `.css`) contém `#hex`, `rgb(...)` ou `hsl(...)` diretamente nos seletores de componente.
- [ ] **Alinhamento ao Grid de 4px/8px:** Todas as propriedades `padding`, `margin`, `gap`, `top`, `left`, `bottom`, `right` utilizam valores da escala oficial (múltiplos de 4px).
- [ ] **Paridade Light/Dark:** Todos os tokens semânticos declarados no escopo claro possuem mapeamento contrastante e legível no escopo escuro.
- [ ] **Bordas Semânticas com Opacidade:** Bordas usam variáveis com alfa controlado (`rgba(..., 0.08)`), evitando bordas cinza sólidas que poluem a tela.
- [ ] **Centralização em Tailwind/CSS:** Se o projeto utiliza Tailwind, as cores do `tailwind.config.js` apontam para as variáveis CSS semânticas (`colors: { surface: 'var(--surface)', ... }`).

---

## 6. Anti-Padrões Explícitos (O que NUNCA fazer)

- ❌ **Cores Hardcoded Inline:** `style="background: #3b82f6"` ou `bg-[#3b82f6]` espalhados pelo código.
- ❌ **Pixels Arbitrários em Espaçamentos:** `padding: 13px; margin-top: 17px; gap: 7px;`.
- ❌ **Dependência Direta de Tons Numéricos:** Usar `text-gray-800` em um botão que fica invisível se a tela for para o modo dark.
- ❌ **Inversão Simples com Invert Filter:** Usar `filter: invert(1)` para simular dark mode em vez de mapear tokens semânticos.
- ❌ **Raios de Borda Descoordenados:** Usar `border-radius: 5px` em um botão, `12px` no input ao lado e `30px` no card, quebrando a harmonia visual.
