---
name: a11y-auditor
description: >-
  Audit and enforce accessibility standards according to WCAG 2.2 AA and AAA specifications.
  Verifies semantic HTML landmarks, strict keyboard navigation, high-visibility focus rings (focus-visible),
  minimalistic and compliant ARIA usage, accessible form labels, prefers-reduced-motion queries, and 4.5:1 color contrast.
triggers:
  - "auditar acessibilidade"
  - "wcag 2.2"
  - "navegação por teclado"
  - "contraste de cores"
  - "leitores de tela"
  - "atributos aria"
  - "focus visible"
  - "a11y"
  - "acessibilidade web"
---

# A11y Auditor: Conformidade WCAG 2.2 AA/AAA & Acessibilidade Total

Esta skill estabelece os critérios determinísticos de auditoria e correção de acessibilidade digital, assegurando que todas as interfaces possam ser operadas plenamente por pessoas usuárias de tecnologias assistivas (leitores de tela, navegação por teclado, comandos de voz e ajustes de contraste/movimento).

---

## 1. Fundamentos e Regras Inegociáveis da WCAG 2.2

### 1.1. Estrutura Semântica de Landmarks
Uma aplicação acessível deve possuir marcos semânticos nativos para permitir que leitores de tela pulem direto para seções relevantes:
- `<header>`: Cabeçalho global ou de seção principal.
- `<nav>`: Blocos de navegação primária ou paginação (sempre acompanhados de `aria-label="Navegação Principal"` quando houver mais de um).
- `<main>`: O conteúdo principal da página (deve existir exatamente **um** por página).
- `<aside>`: Conteúdo complementar ou barra lateral de suporte.
- `<footer>`: Rodapé da aplicação com links institucionais e direitos autorais.

### 1.2. A Primeira Regra do ARIA (W3C)
> *"Se você puder usar um elemento HTML nativo com a semântica e o comportamento já incorporados em vez de redirecionar um elemento genérico usando ARIA, faça isso."*

- Use `<button>` em vez de `<div role="button">`.
- Use `<a href="...">` para navegação entre rotas em vez de `<button>` que dispara redirecionamento de URL.
- Use `<dialog>` em vez de `<div role="dialog">`.
- **ARIA adiciona semântica para leitores de tela; ele NÃO adiciona comportamento no teclado!** Adicionar `role="button"` em uma `div` não faz a tecla `Enter` ou `Space` disparar o evento.

### 1.3. Hierarquia Rígida de Títulos (Headings)
- Cada página deve ter exatamente **um único `<h1>`** representando o tópico principal da tela.
- **Proibido pular níveis hierárquicos:** Nunca transite de `<h1>` diretamente para `<h3>` ou `<h4>`. A sequência deve ser `h1 -> h2 -> h3`.

---

## 2. Contraste de Cores e Tipografia Acessível

Para conformidade **WCAG 2.2 Nível AA**:
- **Texto Normal (< 18pt ou < 24px normal / < 14pt ou < 18.66px negrito):** Razão mínima de contraste de **4.5:1** contra o fundo.
- **Texto Grande (≥ 18pt / ≥ 24px normal ou ≥ 14pt / ≥ 18.66px negrito):** Razão mínima de contraste de **3.0:1**.
- **Componentes de Interface Gráfica e Estados (Bordas de Input, Ícones Ativos):** Razão mínima de contraste de **3.0:1** contra superfícies adjacentes.
- **Nível AAA (Excelência):** Razão mínima de **7.0:1** para texto normal e **4.5:1** para texto grande.

### Fórmula de Verificação Rápida de Luminância Relativa
Dado a luminância relativa $L_1$ da cor mais clara e $L_2$ da mais escura:
$$\text{Contraste} = \frac{L_1 + 0.05}{L_2 + 0.05}$$

---

## 3. Navegação Completa via Teclado e Estados de Foco

1. **Visibilidade Obrigatória de Foco (`:focus-visible`):**
   - Sob hipótese alguma remova o anel de foco com `outline: none` sem substituí-lo por um indicador de espessura e contraste equivalentes ou superiores.
   - Padrão recomendado:
     ```css
     :focus-visible {
       outline: 2px solid var(--ring);
       outline-offset: 2px;
     }
     ```
2. **Ordem de Tabulação Natural:**
   - A ordem de foco deve acompanhar o fluxo visual e de leitura da esquerda para a direita, de cima para baixo.
   - **Proibição de `tabindex > 0`:** Nunca utilize índices positivos (`tabindex="1"`, `tabindex="2"`). Use exclusivamente `tabindex="0"` (para incluir elemento no fluxo natural) ou `tabindex="-1"` (para foco programático via script).
3. **Skip Links (Links para Pular para o Conteúdo):**
   - Toda página com cabeçalho ou menu extenso deve fornecer um link inicial oculto visualmente que se torna visível ao pressionar `Tab`:
     ```html
     <a href="#conteudo-principal" class="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-50 focus:p-3 focus:bg-primary focus:text-white">
       Pular para o conteúdo principal
     </a>
     ```

---

## 4. Acessibilidade Sensorial & Movimento Reduzido

Toda animação decorativa ou transição de tela deve respeitar a preferência de sistema do usuário por redução de movimento:

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

---

## 5. Checklist Determinístico de Auditoria de Acessibilidade

Antes de considerar uma interface aprovada em acessibilidade:

- [ ] **Rótulos em Formulários:** Todo campo de entrada (`<input>`, `<select>`, `<textarea>`) possui uma tag `<label>` explicitamente ligada via atributo `for="id_do_campo"` ou `aria-label` descritivo?
- [ ] **Botões Apenas de Ícone:** Todo botão que renderiza apenas um ícone gráfico possui atributo `aria-label="Descrição da ação"` ou elemento de texto com classe `.sr-only`?
- [ ] **Imagens com Texto Alternativo:** Todas as imagens possuem o atributo `alt` preenchido contextualmente? (Imagens puramente decorativas devem conter explicitamente `alt=""` e `aria-hidden="true"`).
- [ ] **Focus Rings Não Destruídos:** Foi feita uma busca por `outline: 0`, `outline: none` ou `ring-0` no CSS para garantir que nenhum foco foi suprimido sem reposição?
- [ ] **Ausência de `tabindex` Positivo:** Nenhum arquivo contém `tabindex="1"`, `tabindex="2"` ou números maiores que zero?
- [ ] **Contraste Mínimo 4.5:1 Verificado:** Todas as cores de texto atendem ao teste matemático de contraste contra seu respectivo background?
- [ ] **Navegação Exclusiva por Teclado:** É possível navegar por toda a tela, abrir modais, preencher formulários, acionar selects e fechar diálogos (via tecla `Esc`) sem tocar no mouse?

---

## 6. Anti-Padrões Explícitos (O que NUNCA fazer)

- ❌ **`outline: none` Solto:** Resetar o foco do navegador sem criar um anel de foco customizado de alto contraste.
- ❌ **Divs Clicáveis Sem Semântica:** `<div onclick="...">` sem propriedades de teclado, impedindo qualquer usuário cego ou motor de interagir.
- ❌ **Erros de Formulário Identificados Só por Borda Vermelha:** Pintar a borda de vermelho sem exibir uma mensagem textual de erro ligada ao campo por `aria-describedby="erro-id"`.
- ❌ **Texto com Baixo Contraste ("Modinha Cinza Claro"):** Usar texto `#a1a1aa` sobre fundo `#ffffff` (contraste 2.3:1, violando gravemente a WCAG).
- ❌ **Atributo `title` como Substituto de Rótulo:** Usar `<button title="Salvar">` achando que isso substitui um `aria-label` confiável para leitores de tela.
