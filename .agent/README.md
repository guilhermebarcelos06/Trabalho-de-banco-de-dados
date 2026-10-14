# Pacote de Design Skills para Agentes de IA

Este diretório contém o pacote de 6 **Design Skills** especializadas para arquitetura de design systems, polimento estético de nível internacional, engenharia de componentes modulares, auditoria de acessibilidade WCAG 2.2, prototipação rápida em ASCII e ergonomia de interfaces de terminal (TUI).

---

## 📁 Estrutura de Arquivos

```text
.agent/
├── README.md
└── skills/
    ├── design-system-architect/
    │   └── SKILL.md
    ├── ui-polish/
    │   └── SKILL.md
    ├── component-builder/
    │   └── SKILL.md
    ├── a11y-auditor/
    │   └── SKILL.md
    ├── ascii-wireframer/
    │   └── SKILL.md
    └── tui-designer/
        └── SKILL.md
```

Todas as skills também estão instaladas no escopo global em `~/.gemini/config/skills/`, tornando-as disponíveis em qualquer outro projeto executado nesta máquina.

---

## 🚀 Como Invocar Cada Skill (Exemplos Práticos)

### 1. `design-system-architect`
- **Exemplo de Prompt:**
  > *"Atue com a skill design-system-architect para definir as variáveis CSS semânticas de tema claro e escuro para o nosso aplicativo bancário, garantindo escala de 4px/8px e zero cores hexadecimais soltas nos componentes."*

### 2. `ui-polish`
- **Exemplo de Prompt:**
  > *"Use a skill ui-polish para refinar a interface da tela de transações bancárias. Remova qualquer aspecto de IA genérica, aplique bordas sutis de 1px com transparência, microinterações de 180ms ease-out e implemente os estados de skeleton, vazio e erro."*

### 3. `component-builder`
- **Exemplo de Prompt:**
  > *"Utilize a skill component-builder para criar um componente de Modal de Transferência com variantes CVA tipadas, suporte a fechamento por Escape e foco automático acessível usando primitivas nativas."*

### 4. `a11y-auditor`
- **Exemplo de Prompt:**
  > *"Execute a skill a11y-auditor para auditar nosso formulário de cadastro de contas correntes contra WCAG 2.2 AA. Verifique contraste de cores mínimo de 4.5:1, etiquetas nos campos e navegação completa por teclado."*

### 5. `ascii-wireframer`
- **Exemplo de Prompt:**
  > *"Com a skill ascii-wireframer, esboce um wireframe de terminal usando caracteres Unicode box-drawing mostrando o layout Desktop e Mobile da nova tela de extrato de empréstimos, com o mapa de navegação entre telas."*

### 6. `tui-designer`
- **Exemplo de Prompt:**
  > *"Aplique a skill tui-designer para projetar uma CLI interativa em Python Textual com divisão em 2 painéis, barra de status no rodapé com atalhos de teclado ([q] Sair, [Tab] Próximo) e suporte a `--no-color`."*
