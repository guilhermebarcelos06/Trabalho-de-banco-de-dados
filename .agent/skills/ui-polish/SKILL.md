---
name: ui-polish
description: >-
  Audit and refine user interfaces to eliminate generic AI aesthetics ("AI slop") and elevate visual polish
  to tier-1 product standards (Linear, Vercel, Stripe, Raycast). Enforces typography hierarchy, optical alignment,
  subtle 1px borders, smooth 150ms–200ms micro-interactions, and a mandatory 8-state UI matrix (skeleton, empty, error, disabled, etc.).
triggers:
  - "melhorar visual"
  - "eliminar ai slop"
  - "refinar interface"
  - "adicionar microinterações"
  - "estilo linear"
  - "estilo vercel"
  - "estados de ui"
  - "skeleton screen"
  - "empty state"
  - "polimento de interface"
---

# UI Polish: Eliminação de AI Slop & Acabamento Nível Tier-1

Esta skill governa o padrão estético, de usabilidade e de microinteração das interfaces. O objetivo é extirpar qualquer aspecto de interface gerada por IA sem critérios ("AI Slop" — gradientes roxos fluorescentes, sombras difusas exageradas, cartões aninhados recursivamente) e elevar o acabamento visual para o padrão de excelência de ferramentas como **Linear, Vercel, Stripe e Raycast**.

---

## 1. Diretrizes de Excelência Visual (Benchmark Tier-1)

### 1.1. Geometria, Bordas e Contraste Sutil
- **Bordas Sutis (Subtle 1px Borders):** Nunca utilize bordas grossas ou cinzas sólidas desarmônicas. Use bordas de `1px` com baixa opacidade:
  - Tema Claro: `border: 1px solid rgba(15, 23, 42, 0.08);`
  - Tema Escuro: `border: 1px solid rgba(255, 255, 255, 0.08);`
- **Profundidade por Superfície (Layering):** Diferencie camadas elevando ou rebaixando o tom de fundo da superfície (`--surface-subtle` vs `--surface-raised`), e não acumulando sombras pretas intensas.
- **Evitar "Card-ception":** Proibido aninhar um cartão com borda e sombra dentro de outro cartão que já possui borda e sombra. Use divisores sutis ou alternância de backgrounds.

### 1.2. Tipografia e Alinhamento Óptico
- **Hierarquia Clara:** Diferencie títulos de parágrafos através de **peso (`font-weight: 500` / `600`)** e **cor semântica (`--foreground-muted`)**, não apenas pelo tamanho da fonte.
- **Kerning e Tracking Intencional:**
  - Títulos grandes (`h1`, `h2`): `letter-spacing: -0.025em;` ou `-0.02em` (reduz espaçamento entre letras em corpos grandes para coesão).
  - Títulos pequenos/uppercase (badges, overlines): `letter-spacing: 0.05em; font-size: 0.75rem; font-weight: 600; text-transform: uppercase;`.
- **Alinhamento Óptico com Ícones:** Ícones ao lado de textos devem ser alinhados verticalmente pela altura-x (x-height), não apenas pelo box geométrico. Use `display: inline-flex; align-items: center; gap: var(--space-2);`.

### 1.3. Microinterações e Física de Movimento
- **Duração Máxima:** Todas as transições de hover, active e foco devem durar entre **150ms e 200ms**. Nunca use animações lentas (300ms–500ms) para estados interativos básicos.
- **Curva de Easing Acelerada:** Use `ease-out` ou curva personalizada suave:
  ```css
  transition: all 180ms cubic-bezier(0.16, 1, 0.3, 1);
  ```
- **Feedback Tátil:**
  - Hover: Leve clareamento/escurecimento de superfície (`brightness(1.05)` ou `--surface-hover`) e sutil transição de borda.
  - Active: Leve escala para baixo (`transform: scale(0.98);`) transmitindo sensação de clique físico.

---

## 2. A Matriz Obrigatória de 8 Estados de UI

Nenhum componente ou tela interativa é considerado concluído sem contemplar explicitamente os 8 estados da matriz:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        MATRIZ DE ESTADOS DE UI                         │
├────────────────────┬───────────────────────────────────────────────────┤
│ 1. Idle / Default  │ Estado padrão em repouso.                         │
│ 2. Hover           │ Realce sutil (150ms ease-out), cursor: pointer.   │
│ 3. Active / Click  │ Leve recuo (scale(0.98)), profundidade de clique. │
│ 4. Focus-Visible   │ Anel de foco nítido com offset (outline/ring).    │
│ 5. Loading / Busy  │ Skeleton shimmer proporcional ou spinner não-bloq.│
│ 6. Empty State     │ Sem dados: ícone, título claro, copy e CTA útil.  │
│ 7. Error State     │ Mensagem descritiva + ação clara de recuperação.  │
│ 8. Disabled        │ Opacidade 0.5, cursor: not-allowed, sem pointer.  │
└────────────────────┴───────────────────────────────────────────────────┘
```

### Exemplo de Skeleton & Shimmer Padrão (Sem AI Slop)
```css
@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

.skeleton {
  background: linear-gradient(
    90deg,
    var(--surface-subtle) 25%,
    var(--border) 50%,
    var(--surface-subtle) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.8s infinite ease-in-out;
  border-radius: var(--radius-sm);
}
```

---

## 3. Checklist Determinístico de Polimento de UI

Execute esta verificação antes de liberar qualquer interface:

- [ ] **Eliminação de AI Slop:** A tela está livre de gradientes roxo/magenta/neon gratuitos em botões, bordas ou títulos?
- [ ] **Sombras Naturais:** Todas as sombras utilizam difusão e opacidade realistas (`rgba(0,0,0,0.06)`) sem manchas escuras borradas cobrindo o conteúdo?
- [ ] **Bordas com Opacidade:** As bordas utilizam `rgba(..., 0.08)` e espessura de `1px`?
- [ ] **Alinhamento e Whitespace:** Existe espaçamento generoso e consistente entre seções (mínimo de 24px a 48px), permitindo que a interface "respire"?
- [ ] **Transições Temporizadas:** Transições interativas estão configuradas entre 150ms e 200ms com curva `ease-out`?
- [ ] **Presença dos 8 Estados:**
  - Existe representação para estado vazio (*Empty State*) com botão de criação primário?
  - Existe tratamento de erro com mensagem de diagnóstico e botão "Tentar novamente"?
  - Existe esqueleto de carregamento (*Skeleton Screen*) espelhando exatamente a geometria dos dados reais?
- [ ] **Focus Ring Acessível:** Todos os controles interativos exibem um anel de foco visível ao navegar com a tecla `Tab`.

---

## 4. Anti-Padrões Explícitos (O que NUNCA fazer)

- ❌ **Gradientes "Cyberpunk / AI Slop":** Botões ou textos com gradiente `linear-gradient(to right, #ec4899, #8b5cf6, #3b82f6)` que gritam estética gerada por IA de 2023.
- ❌ **Cartão dentro de Cartão dentro de Cartão:** Elemento pai com borda + sombra contendo cards filhos com borda + sombra contendo caixas com borda + sombra.
- ❌ **Animações Lentas e Arrasto:** Transições de 400ms ou 500ms em botões ou menus que fazem a interface parecer lenta e travada.
- ❌ **Telas Brancas de Carregamento:** Exibir uma tela em branco ou apenas um loader minúsculo no canto enquanto os dados carregam.
- ❌ **Empty States Mudos:** Tabelas ou listas sem dados exibindo apenas "Nenhum registro" sem explicação, sem ícone e sem ação recomendada.
- ❌ **Sombras Desconectadas da Luz:** `box-shadow: 0 0 25px rgba(0,0,0,0.4)` sem deslocamento no eixo Y e com difusão irreal.
