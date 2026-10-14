---
name: component-builder
description: >-
  Build modular, compound, and reusable UI components. Enforces strict separation of state/headless logic
  from visual presentation, accessible primitives (Radix UI, React Aria, Base UI, modern native HTML dialog/popover),
  type-safe variants (CVA / Tailwind Variants), and robust mobile-first responsiveness.
triggers:
  - "criar componente"
  - "refatorar componente de ui"
  - "construir botão reutilizável"
  - "modal acessível"
  - "compound components"
  - "variantes de componente"
  - "cva"
  - "tailwind variants"
  - "headless ui"
---

# Component Builder: Arquitetura Modular & Variantes Tipadas

Esta skill estabelece a metodologia de engenharia para o desenvolvimento de componentes de interface que sejam altamente desacoplados, resilientes, composíveis e 100% acessíveis por padrão.

---

## 1. Princípios Estruturais de Design de Componentes

### 1.1. Separação Estrita de Camadas (Headless vs. Visual)
Todo componente interativo não-trivial deve separar claramente:
1. **Camada de Comportamento / Lógica (Headless):** Gerencia estado aberto/fechado, seleção, índices ativos, foco de teclado e eventos ARIA.
2. **Camada de Apresentação (View / Slot):** Recebe o estado via props/context e aplica classes utilitárias ou estilos encapsulados.

```
┌────────────────────────────────────────────────────────┐
│             COMPONENTE COMPOSTO / EXPORT               │
├──────────────────────────┬─────────────────────────────┤
│ Comportamento (Headless) │ Radix / React Aria / Hooks  │
│ Variantes e Estilo       │ CVA / Tailwind Variants     │
│ Composição de Slots      │ Root, Trigger, Content, Item│
└──────────────────────────┴─────────────────────────────┘
```

### 1.2. Primitivas Acessíveis em Vez de Reinvenções
Nunca crie componentes complexos a partir de `divs` com listeners manuais de clique:
- Modais e Diálogos ➔ Use `<dialog>` nativo moderno ou `@radix-ui/react-dialog`.
- Popovers e Dropdowns ➔ Use API nativa de `popover` ou `@radix-ui/react-popover`.
- Menus e Selects ➔ Use primitivas que já implementem a especificação WAI-ARIA com navegação por setas do teclado.

### 1.3. Padrão de Variantes Tipadas (CVA - Class Variance Authority)
Defina todas as permutações visuais através de matrizes declarativas tipadas:

```typescript
import { cva, type VariantProps } from 'class-variance-authority';

export const buttonVariants = cva(
  // Estilos Base (Aplicados a todas as instâncias)
  'inline-flex items-center justify-center font-medium transition-all duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 select-none active:scale-[0.98]',
  {
    variants: {
      variant: {
        primary: 'bg-primary text-primary-foreground hover:bg-primary-hover shadow-sm',
        secondary: 'bg-surface-raised text-foreground border border-border hover:bg-surface-subtle shadow-sm',
        destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive-hover shadow-sm',
        ghost: 'text-foreground hover:bg-surface-subtle',
        link: 'text-primary underline-offset-4 hover:underline p-0 h-auto'
      },
      size: {
        sm: 'h-8 px-3 text-xs rounded-sm gap-1.5',
        md: 'h-10 px-4 text-sm rounded-md gap-2',
        lg: 'h-12 px-6 text-base rounded-lg gap-2.5',
        icon: 'h-10 w-10 p-0 rounded-md'
      }
    },
    defaultVariants: {
      variant: 'primary',
      size: 'md'
    }
  }
);
```

---

## 2. Padrão de Componentes Compostos (Compound Components)

Componentes ricos devem oferecer flexibilidade através de subcomponentes exportados em conjunto, permitindo ao consumidor customizar a ordem do layout sem criar centenas de "props booleanas":

```tsx
// Exemplo canônico de Card Composto
export function Card({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("rounded-lg border border-border bg-surface text-foreground shadow-sm", className)} {...props} />;
}

export function CardHeader({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("flex flex-col space-y-1.5 p-6", className)} {...props} />;
}

export function CardTitle({ className, ...props }: React.HTMLAttributes<HTMLHeadingElement>) {
  return <h3 className={cn("font-semibold leading-none tracking-tight text-lg", className)} {...props} />;
}

export function CardDescription({ className, ...props }: React.HTMLAttributes<HTMLParagraphElement>) {
  return <p className={cn("text-sm text-foreground-muted", className)} {...props} />;
}

export function CardContent({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("p-6 pt-0", className)} {...props} />;
}

export function CardFooter({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("flex items-center p-6 pt-0 gap-3", className)} {...props} />;
}
```

---

## 3. Diretrizes de Responsividade Mobile-First

1. **Larguras Fluídas e Flexíveis:** Proibido o uso de larguras fixas em pixels (`w-[500px]`, `width: 600px`). Utilize `max-w-*`, `w-full`, ou containers flex/grid.
2. **Touch Targets Conformes:** Em resoluções móveis ou interfaces sensíveis ao toque, todo elemento interativo deve possuir uma área clicável mínima de **44x44px** (ou padding compensatório).
3. **Quebras de Layout Controladas:** O layout base deve ser sempre testado e funcional na largura mínima padrão da indústria: **320px**.

---

## 4. Checklist Determinístico de Verificação

Antes de aprovar ou entregar um novo componente:

- [ ] **Polimorfismo e Prop Forwarding:** O componente aceita `ref` (`forwardRef` no React ou equivalente no framework utilizado) e repassa `...rest` props para a tag HTML raiz?
- [ ] **Variantes Declarativas Tipadas:** Todas as permutações de tamanho, cor e comportamento estão catalogadas em uma matriz tipada (ex: CVA / Tailwind Variants)?
- [ ] **Respeito aos Princípios Headless:** Componentes modais, suspensos ou de menu delegam eventos de teclado e controle de foco a primitivas estabelecidas?
- [ ] **Resistência a Overflow:** O componente foi testado com textos extremamente longos (respeitando `truncate`, `break-words` ou ellipsis sem quebrar a geometria pai)?
- [ ] **Sem Efeitos Colaterais Globais:** As classes ou estilos do componente não vazam para fora do seu escopo nem alteram tags genéricas globais.

---

## 5. Anti-Padrões Explícitos (O que NUNCA fazer)

- ❌ **"Mega-Componentes" com Prop Drilling:** Um componente monólito de 800 linhas que recebe 40 props do tipo `hasHeader`, `isCompact`, `showFooter`, `customIconStyle`, tornando a manutenção impraticável.
- ❌ **Divs Falsas Clicáveis:** `<div onClick={handleClick}>Excluir</div>` sem `role="button"`, sem `tabIndex={0}`, e sem suporte a `Enter`/`Space`.
- ❌ **Bloqueio de Classes do Usuário:** Impedir que o consumidor do componente customize classes através da prop `className` combinada com `clsx` / `tailwind-merge`.
- ❌ **Layouts Hardcoded Quebráveis em Mobile:** Utilizar `width: 720px; position: absolute;` sem breakpoints responsivos.
- ❌ **Mistura de Fetching de Dados e View:** Componente de botão ou card fazendo requisições `fetch()` internamente em vez de receber dados ou callbacks por props.
