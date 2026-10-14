---
name: ascii-wireframer
description: >-
  Rapidly prototype terminal-based and web layouts, block hierarchies, and user interaction flows using
  Unicode box-drawing characters (┌─┐│└┘├┤┬┴┼). Generates pixel-aligned ASCII wireframes, responsive screen comparisons
  (Desktop 80-col vs Mobile 36-col), and step-by-step screen navigation maps before writing production code.
triggers:
  - "criar wireframe"
  - "prototipar layout no terminal"
  - "rascunho de tela em ascii"
  - "fluxo de navegação"
  - "wireframe unicode"
  - "planejar layout visual"
  - "esboço de interface"
---

# ASCII Wireframer: Prototipação em Terminal com Box-Drawing

Esta skill permite ao agente desenhar e validar rapidamente a arquitetura de informação, distribuição de blocos visuais, controles interativos e mapas de navegação entre telas diretamente em formato de texto/Markdown, antes de despender tempo escrevendo código CSS, HTML ou componentes.

---

## 1. Conjunto Canônico de Caracteres Unicode Box-Drawing

Para manter precisão milimétrica e renderização consistente em qualquer fonte monospaçada moderna:

### Linhas Simples (Estruturas e Containers)
- Cantos: `┌` (superior esquerdo), `┐` (superior direito), `└` (inferior esquerdo), `┘` (inferior direito)
- Linhas: `─` (horizontal), `│` (vertical)
- Junções e Divisores: `├` (T para a direita), `┤` (T para a esquerda), `┬` (T para baixo), `┴` (T para cima), `┼` (cruzamento central)

### Linhas Arredondadas (Cards e Modais Modernos)
- Cantos: `╭` (superior esquerdo), `╮` (superior direito), `╰` (inferior esquerdo), `╯` (inferior direito)

### Linhas Duplas (Janelas Principais e Cabeçalhos Críticos)
- Cantos e Linhas: `╔` `╗` `╚` `╝` `═` `║` `╠` `╣` `╦` `╩` `╬`

### Preenchimentos, Seleções e Estados
- Selecionado / Ativo: `[x]` ou `(•)` ou `█`
- Desmarcado / Vazio: `[ ]` ou `( )` ou `░`
- Botão Primário: `[▶ Confirmar ]` ou `[ Salvar ]*`
- Botão Secundário: `[ Cancelar ]`
- Setas de Fluxo: `──▶` ou `◀──` ou `▼` ou `▲`

---

## 2. Template Padrão de Especificação de Wireframe

Todo wireframe gerado deve conter as 4 seções:

```markdown
### 1. Metadados da Tela
- **Nome da Tela:** Dashboard Financeiro do Cliente
- **Resolução Alvo:** Desktop (80 colunas) & Mobile (36 colunas)
- **Objetivo Principal:** Exibir saldo consolidado, últimas 5 transações e botão rápido de transferência.

### 2. Wireframe Desktop (80 Colunas)
┌──────────────────────────────────────────────────────────────────────────────┐
│ [Logo Banco]        Extrato   Contas   Transferências   [Perfil / Sair]      │
├──────────────────────────────────────────────────────────────────────────────┤
│ Olá, Guilherme Barcelos                            Status: Conta Corrente Ativa │
│                                                                              │
│ ┌───────────────────────────┐ ┌────────────────────────────────────────────┐ │
│ │ Saldo em Conta            │ │ Ações Rápidas                              │ │
│ │ R$ 14.850,22              │ │ [▶ Nova Transferência ]  [ Extrato PDF ]   │ │
│ │ Última sinc: 14/10 22:15  │ │ [ Pagar Boleto ]         [ Bloquear Cartão]│ │
│ └───────────────────────────┘ └────────────────────────────────────────────┘ │
│                                                                              │
│ ┌──────────────────────────────────────────────────────────────────────────┐ │
│ │ Últimas Transações                                     [ Ver todas (120) ]│ │
│ ├───────────────────────┬──────────────┬───────────────┬───────────────────┤ │
│ │ Descrição             │ Data/Hora    │ Tipo          │ Valor (R$)        │ │
│ ├───────────────────────┼──────────────┼───────────────┼───────────────────┤ │
│ │ PIX Recebido - Carlos │ 14/10 21:04  │ Crédito       │ + R$ 350,00       │ │
│ │ Supermercado Pão Bom  │ 14/10 18:32  │ Débito        │ - R$ 142,50       │ │
│ │ Posto Shell Combust.  │ 13/10 09:12  │ Débito        │ - R$ 220,00       │ │
│ └───────────────────────┴──────────────┴───────────────┴───────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────┘

### 3. Wireframe Mobile (36 Colunas)
┌──────────────────────────────────┐
│ [=] Meu Banco           [User]   │
├──────────────────────────────────┤
│ Saldo Disponível                 │
│ R$ 14.850,22                     │
│                                  │
│ [▶ Transferir ]  [ Pagar Conta ] │
│                                  │
│ ╭────────────────────────────────╮
│ │ Últimas Transações             │
│ │ ────────────────────────────── │
│ │ PIX Carlos       + R$ 350,00   │
│ │ Supermercado     - R$ 142,50   │
│ │ Posto Shell      - R$ 220,00   │
│ ╰────────────────────────────────╯
│                                  │
│ [q] Sair | [Home] [Extrato] [Menu│
└──────────────────────────────────┘

### 4. Mapa de Navegação Entre Telas
┌─────────────────┐       [ Botão: Nova Transf. ]       ┌──────────────────┐
│ Dashboard Inicial│ ─────────────────────────────────▶ │ Modal/Tela Transf│
└─────────────────┘                                     └──────────────────┘
         │                                                        │
         │ [ Botão: Extrato PDF ]                                 │ [ Sucesso ]
         ▼                                                        ▼
┌─────────────────┐                                     ┌──────────────────┐
│ Visualizador PDF│                                     │ Recibo com Autent│
└─────────────────┘                                     └──────────────────┘
```

---

## 3. Checklist Determinístico de Validação de Wireframe

Antes de apresentar um wireframe de tela ao usuário:

- [ ] **Alinhamento Monospaçado Estrito:** O wireframe foi renderizado dentro de um bloco de código Markdown com três crases (```` ```text ````) e todas as colunas fecham perfeitamente sem desalinhamentos?
- [ ] **Consistência de Caracteres Box-Drawing:** Não há caracteres soltos (`+---`, `|`) misturados aleatoriamente com caracteres Unicode (`┌─┐`)?
- [ ] **Identificação de Controles:** Os elementos interativos possuem marcadores claros:
  - Botões entre colchetes: `[ Botão ]`
  - Campos de texto / Inputs: `[ Digite seu e-mail...   ]`
  - Checkboxes: `[ ]` ou `[x]`
  - Radio buttons: `( )` ou `(•)`
- [ ] **Visão de Responsividade:** Se a interface for web, o wireframe fornece tanto a visualização em formato Desktop quanto a visualização em formato Mobile (layout empilhado)?
- [ ] **Legenda de Navegação:** O mapa de setas (`──▶`) deixa explícito para onde cada clique ou ação do usuário transporta a tela?

---

## 4. Anti-Padrões Explícitos (O que NUNCA fazer)

- ❌ **Mistura Desalinhada de ASCII e Unicode:** Desenhar cantos com `+` e linhas com `═`, resultando em caixas tortas no terminal.
- ❌ **Caixas Abertas sem Fechamento:** Deixar linhas verticais sem fechar o canto inferior correspondente.
- ❌ **Texto que Estoura a Largura da Moldura:** Textos longos que empurram os caracteres de fechamento `│` para a direita, entortando a tabela.
- ❌ **Wireframes Sem Ações Explícitas:** Desenhar apenas caixas vazias sem indicar botões, rótulos de campos ou fluxo de decisão.
- ❌ **Ignorar a Resolução do Terminal:** Desenhar layouts com mais de 100 caracteres de largura sem quebrar em blocos verticais, gerando quebra automática e ilegível no terminal.
