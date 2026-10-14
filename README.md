# 🏦 Sistema de Gestão de Contas e Operações Bancárias

> **Instituição:** Universidade Católica de Brasília (UCB)  
> **Curso:** Bacharelado em Engenharia de Software  
> **Disciplina:** Laboratório de Banco de Dados — GPE17M40083  
> **Professor:** Samuel Novais Moura Júnior  
> **Semestre:** 2026/2  
> **SGBD Utilizado:** MySQL 8.0  
> **Interface da Aplicação:** Python 3 + Streamlit  

---

## 👥 Integrantes da Equipe
- **Gabriel Almeida Silva Netto**
- **Gabriel Reis**
- **Gabriel Lima Leite**
- **Celiandro Borges Mazarro**
- **Caio Gasparin**
- **Eduardo**
- **Guilherme Barcelos**

---

## 📌 Visão Geral do Projeto
Este repositório contém a entrega completa e integrada da disciplina, contemplando:
1. **Etapa 1 Revisada**: Modelagem conceitual revisada (notação Crow's Foot unificada com cardinalidades mín/máx explícitas), modelo lógico normalizado na 3FN com prova formal de dependências funcionais, scripts DDL com restrições e checks completos, e carga com casos de contorno.
2. **Etapa 2 (N2 - Operação, Interface e Desempenho)**:
   - **Aplicação Web Interativa (Streamlit)** com 4 CRUDs, 2 consultas parametrizadas, relatório analítico alimentado por VIEW e operação transacional de transferência bancária.
   - **Transação e Concorrência**: Demonstração de atomicidade com botão de falha proposital (Rollback forçado) e experimento automatizado com duas sessões simultâneas e lock de linha (`SELECT ... FOR UPDATE`).
   - **Otimização de Consultas**: Estudo de desempenho com `EXPLAIN ANALYZE` sobre mais de 10.000 registros, comprovando o ganho de 92% com índices compostos.
   - **Segurança e Perfis**: 3 usuários MySQL nativos (`user_admin`, `user_atendente`, `user_auditor`) com `GRANT`/`REVOKE`, visão restritiva com mascaramento de CPF (`vw_cliente_atendimento`) e senhas criptografadas com `bcrypt`.
   - **Auditoria**: Tabela dedicada e 2 gatilhos capturando valores anteriores e novos em JSON.

---

## 📂 Estrutura do Repositório

```text
banco/
├── app/
│   ├── app.py                     # Aplicação Web Streamlit (Interface B1 a B6)
│   ├── db.py                      # Camada de dados (Prepared Statements + Erros amigáveis)
│   └── auth.py                    # Criptografia de senhas (bcrypt com salt)
├── docs/
│   ├── modelo_er.md               # MER Conceitual revisado (Crow's Foot e cardinalidades mín/máx)
│   ├── modelo_logico.md           # Esquema lógico (PKs/FKs), justificativas e prova formal 3FN
│   ├── dicionario_dados.md        # Dicionário de dados conceitual
│   ├── plano_etapa2.md            # Plano detalhado de execução e conformidade
│   └── relatorio_etapa2.md        # Relatório técnico final completo (Etapa 1 + 2 + IA + Roteiro)
├── scripts/
│   ├── gerar_cargas_completas.py  # Gerador da carga oficial (40+ entidades e 100+ transações)
│   ├── gerador_carga_alta.py      # Gerador de 10.000+ transações para o benchmark EXPLAIN
│   └── experimento_concorrencia.py # Experimento prático de concorrência com 2 sessões
├── sql/
│   ├── 01_ddl.sql                 # Script físico DDL revisado (sem CASCADE financeiro)
│   ├── 02_Cargas.sql              # Script de carga inicial com casos de contorno
│   ├── 03_consultas.sql           # As 15 consultas exigidas com perguntas de negócio
│   ├── 04_etapa2_seguranca_auditoria.sql # Tabela de auditoria, 2 triggers, 2 views e 3 perfis
│   └── 05_etapa2_otimizacao_indices.sql  # 3 índices compostos para o benchmark
├── docker-compose.yml             # Orquestração do MySQL 8.0 oficial
├── requirements.txt               # Dependências Python
├── .env.example                   # Modelo de variáveis de ambiente
├── .gitignore                     # Proteção contra vazamento de credenciais
└── README.md                      # Documentação de entrada do repositório
```

---

## 🚀 Como Executar em Máquina Limpa

### 1. Pré-requisitos
- [Docker](https://docs.docker.com/get-docker/) e [Docker Compose](https://docs.docker.com/compose/)
- [Python 3.10+](https://www.python.org/)

### 2. Inicialização do Banco de Dados (MySQL 8.0)
```bash
# Clone o repositório
git clone https://github.com/FlashTR5/Sistema-de-Gestao-de-Contas-e-Operacoes-Bancarias.git
cd Sistema-de-Gestao-de-Contas-e-Operacoes-Bancarias

# Copie o arquivo de variáveis de ambiente
cp .env.example .env

# Suba o container do MySQL 8.0
docker compose up -d

# Aguarde 10 segundos para a inicialização e execute os scripts SQL na ordem:
docker exec -i mysql-banco mysql -uroot -pbanco_secret sistema_bancario < sql/01_ddl.sql
docker exec -i mysql-banco mysql -uroot -pbanco_secret sistema_bancario < sql/02_Cargas.sql
docker exec -i mysql-banco mysql -uroot -pbanco_secret sistema_bancario < sql/04_etapa2_seguranca_auditoria.sql
docker exec -i mysql-banco mysql -uroot -pbanco_secret sistema_bancario < sql/05_etapa2_otimizacao_indices.sql
```

### 3. Execução da Aplicação Web
```bash
# Crie e ative o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate   # No Windows: .venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Inicie a aplicação
streamlit run app/app.py
```
Acesse no seu navegador: **`http://localhost:8501`**

---

## 🧪 Testes e Validação Técnica

### Teste de Carga Alta e EXPLAIN (B4)
```bash
# Injeta 10.000 transações sintéticas para os testes de plano de execução
python3 scripts/gerador_carga_alta.py
```

### Experimento de Concorrência com 2 Sessões (B3)
```bash
# Executa duas threads simultâneas disputando a mesma conta com row lock
python3 scripts/experimento_concorrencia.py
```

---

## 📋 Checklist Oficial da Etapa 2 (Anexo C)
- [x] A aplicação sobe em máquina limpa seguindo as instruções do README.
- [x] Os quatro CRUDs, as duas consultas parametrizadas e o relatório funcionam.
- [x] Nenhuma consulta é montada por concatenação de string.
- [x] As credenciais do banco não estão versionadas.
- [x] A operação transacional foi testada nos dois desfechos: sucesso e falha.
- [x] O experimento de concorrência está documentado com o que foi observado.
- [x] Os três estudos de EXPLAIN trazem plano antes, índice, plano depois e tempo.
- [x] Os três perfis de acesso foram criados e testados com login real.
- [x] As senhas da aplicação estão armazenadas com hash e sal.
- [x] Os dois gatilhos de auditoria registram autor, data e valores.
- [x] O plano de backup está descrito com frequência e estratégia de retenção.
- [x] As correções apontadas na devolutiva da Etapa 1 foram incorporadas.
- [x] O ambiente de demonstração está preparado: banco povoado e duas sessões abertas.
- [x] A seção de declaração de uso de IA está preenchida.
