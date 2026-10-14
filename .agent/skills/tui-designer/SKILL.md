---
name: tui-designer
description: >-
  Architect and design ergonomic, modern Terminal User Interfaces (TUI) and Command Line Interfaces (CLI).
  Enforces multi-pane layouts, sticky status bars with explicit keyboard shortcuts ([q] Quit, [/?] Help, [Tab] Next),
  ANSI/TrueColor dual-mode color schemes (dark/light terminal friendly), non-blocking progress spinners/bars,
  and strict support for --no-color and machine-readable JSON piping.
triggers:
  - "criar tui"
  - "interface de terminal"
  - "cli interativa"
  - "dashboard de terminal"
  - "textual python"
  - "bubble tea go"
  - "rich terminal"
  - "curses"
  - "ergonomia de linha de comando"
---

# TUI Designer: Ergonomia, Painéis & Interfaces de Terminal Modernas

Esta skill governa o design, a usabilidade e a arquitetura técnica de **Interfaces de Usuário em Modo Texto (TUI)** e ferramentas de linha de comando avançadas (CLI) construídas com frameworks como Textual (Python), Bubble Tea (Go), Ink (Node/React), Ratatui (Rust) ou bibliotecas de formatação como Rich/Blessed.

---

## 1. Arquitetura de Layout em Terminal (Panels & Status Bar)

Uma TUI moderna deve ter divisão clara de responsabilidades no viewport:

```
┌────────────────────────────────────────────────────────────────────────┐
│ TOP BAR: Título do App | Contexto / Branch / Sessão       | v1.2.0    │
├──────────────────────────┬─────────────────────────────────────────────┤
│ PAINEL LATERAL (25%)     │ PAINEL PRINCIPAL (75%)                      │
│ - [1] Visão Geral        │ Seleção: [1] Visão Geral                    │
│ - [2] Contas Bancárias   │                                             │
│ - [3] Transações         │ • Clientes Ativos: 45                       │
│ - [4] Auditoria          │ • Volume Movimentado: R$ 850.400,00         │
│ - [5] Configurações      │ • Alertas de Segurança: 0 pendentes         │
│                          │                                             │
│                          │ Pressione [Enter] para expandir detalhes    │
├──────────────────────────┴─────────────────────────────────────────────┤
│ STATUS BAR: [Tab] Mudar Painel | [↑/↓] Navegar | [/?] Ajuda | [q] Sair │
└────────────────────────────────────────────────────────────────────────┘
```

### Regras Estruturais Inegociáveis:
1. **Status Bar Permanente (Bottom Bar):** O rodapé deve sempre listar as teclas de atalho essenciais em formato mnemônico de alto contraste (`[tecla] Ação`).
2. **Ciclo de Saída Limpo:**
   - A tecla `q` ou `Esc` (em telas raiz) e `Ctrl+C` devem restaurar imediatamente o buffer alternativo do terminal (`rmcup` / `leave_alternate_screen`), restaurar a visibilidade do cursor e restaurar os modos canônicos do terminal.
3. **Tratamento de Redimensionamento (`SIGWINCH`):** O layout deve reagir a alterações nas dimensões do terminal (mínimo suportado: 80x24) sem corromper a renderização ou causar travamentos.

---

## 2. Paleta de Cores e Compatibilidade de Terminal

Terminais variam drasticamente entre fundos pretos profundos, fundos brancos (Solarized Light) e esquemas de 16 cores básicas.

### 2.1. Níveis de Cor e Degradação Elegante
Sua TUI deve detectar as capacidades do terminal e degradar de forma limpa:
- **Nível 3 (TrueColor / 24-bit RGB):** Utilizado se `COLORTERM=truecolor` ou `COLORTERM=24bit`.
- **Nível 2 (ANSI 256 cores):** Mapeamento para índices da tabela de 256 cores xterm.
- **Nível 1 (ANSI 16 cores básicas):** Utilizar apenas códigos padrão (`red`, `green`, `yellow`, `blue`, etc.) com atributos `bold` ou `dim`.
- **Nível 0 (Monocromático):** Somente texto, sublinhado e inverso de vídeo.

### 2.2. Respeito Mandatório ao Padrão `NO_COLOR`
Se a variável de ambiente `NO_COLOR` estiver presente (mesmo que com valor vazio ou `1`) ou se o parâmetro `--no-color` for fornecido via CLI:
- **Desative imediatamente todas as sequências de escape ANSI de cor.**
- Utilize apenas caracteres e formatações de texto legíveis.

### 2.3. Detecção de TTY e Tubulação (Pipes)
Se `stdout` não for um terminal interativo (`!sys.stdout.isatty()` ou teste de pipe `ls | ...`):
- A TUI não deve tentar renderizar sequências de controle de tela nem entrar em modo tela-cheia (fullscreen).
- Deve emitir saída legível pura em texto ou JSON estruturado (`--json` por padrão ou detecção automática).

---

## 3. Indicadores de Progresso e Operações Não-Bloqueantes

1. **Spinners para Operações Indeterminadas:**
   - Use sequências UTF-8 suaves: `⠋ ⠙ ⠹ ⠸ ⠼ ⠴ ⠦ ⠧ ⠇ ⠏`
   - O spinner deve rodar em uma thread assíncrona ou co-rotina, **nunca bloqueando o processamento principal**.
2. **Barras de Progresso Determinísticas:**
   - Para transferências, uploads ou migrações de dados, mostre porcentagem, velocidade e tempo restante estimado:
     ```
     Sincronizando banco: [██████████████████░░░░░░] 75% | 1.200/1.600 reg | 450 reg/s | ETA: 1s
     ```

---

## 4. Checklist Determinístico de Qualidade de TUI/CLI

Execute esta auditoria antes de liberar qualquer CLI/TUI:

- [ ] **Restauração de Terminal na Saída:** Ao finalizar (seja por `q`, `Ctrl+C` ou erro não tratado), o cursor do mouse e do texto voltam a ficar visíveis e o prompt normal do bash/zsh é restaurado sem resíduos na tela?
- [ ] **Atalhos na Status Bar:** A barra inferior exibe no mínimo:
  - `[q] Sair`
  - `[/?] Ajuda`
  - `[Tab]` ou `[↑/↓]` para alternar foco ou navegar itens?
- [ ] **Dual-Theme Friendly:** Cores de texto não usam cinza escuro ou preto que ficam invisíveis em terminais com fundo escuro, nem usam branco brilhante que fica invisível em terminais com fundo claro?
- [ ] **Suporte a `NO_COLOR` e `--no-color`:** A aplicação funciona sem emitir códigos ANSI quando `NO_COLOR=1` é exportado no terminal?
- [ ] **Compatibilidade com Redimensionamento:** Redimensionar a janela do terminal ajusta as caixas automaticamente sem jogar linhas quebradas para baixo?
- [ ] **Saída em Modo Pipe / JSON:** Executar o comando redirecionando para um arquivo (`app > output.txt`) desativa menus interativos e emite saída limpa ou serializada?

---

## 5. Anti-Padrões Explícitos (O que NUNCA fazer)

- ❌ **Cursor Invisível Permanente:** Ocultar o cursor do terminal no início da aplicação (`\e[?25l`) e esquecer de restaurá-lo no tratamento de exceção (`try ... finally: show_cursor()`), deixando o terminal do usuário quebrado.
- ❌ **Bloquear o Event Loop com I/O Síncrono:** Executar uma query de banco de dados pesada ou request HTTP direto na thread da TUI, congelando a interface e ignorando o teclado.
- ❌ **Cores Hardcoded Sem Checar Contraste de Fundo:** Imprimir texto em amarelo claro puro sem background ou preto puro em terminais onde a cor de fundo não é garantida.
- ❌ **Ignorar Sinais de Interrupção (`SIGINT`):** Capturar `KeyboardInterrupt` e não encerrar o programa, deixando o usuário preso sem conseguir dar `Ctrl+C`.
- ❌ **Menus Interativos em Scripts Automatizados:** Tentar abrir uma TUI quando o comando foi executado em ambiente CI/CD ou dentro de um cron job sem terminal anexado.
