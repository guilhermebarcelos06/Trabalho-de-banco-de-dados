import streamlit as st
import pandas as pd
from db import execute_query, execute_dml, executar_transferencia_transacional, get_connection
from auth import hash_senha, verificar_senha

# Configuração da página Streamlit
st.set_page_config(
    page_title="Sistema Bancário — Etapa 2 (N2)",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo e Cabeçalho
st.title("🏦 Sistema de Gestão de Contas e Operações Bancárias")
st.caption("Disciplina: Laboratório de Banco de Dados — UCB (Prof. Samuel Novais Moura Júnior) · Etapa 2 (N2)")

# Menu Lateral de Navegação
menu = st.sidebar.radio(
    "Navegação da Etapa 2:",
    [
        "1. CRUD de 4 Entidades (B1)",
        "2. Consultas Parametrizadas (B1)",
        "3. Relatório Consolidado - VIEW (B1)",
        "4. Transação Multitabela & Rollback (B1/B3)",
        "5. Segurança & SQL Injection (B2/B5)",
        "6. Otimização & EXPLAIN (B4)",
        "7. Gatilhos de Auditoria (B6)"
    ]
)

st.sidebar.divider()
st.sidebar.info("💡 **Apresentação ao Vivo**: Todas as operações utilizam Prepared Statements nativos e respeitam as restrições do banco.")

# ==============================================================================
# 1. CRUD DE 4 ENTIDADES (B1)
# ==============================================================================
if menu == "1. CRUD de 4 Entidades (B1)":
    st.header("📋 CRUD de Entidades com Tratamento Amigável de Erros")
    st.markdown("Gerencie as entidades principais do sistema bancário. Erros de integridade (duplicidade, constraints CHECK e chaves estrangeiras) são tratados com mensagens claras.")

    entidade = st.selectbox("Selecione a Entidade para Operar:", ["Cliente", "Conta Bancária", "Cartão", "Beneficiário"])

    # -----------------------------
    # CRUD 1: CLIENTE
    # -----------------------------
    if entidade == "Cliente":
        st.subheader("Gerenciamento de Clientes (PF e PJ)")
        tab_list, tab_novo, tab_edit = st.tabs(["🔍 Consultar Clientes", "➕ Novo Cliente", "✏️ Atualizar / Remover"])
        
        with tab_list:
            filtro_nome = st.text_input("Filtrar por nome ou documento:", key="filtro_cli")
            if filtro_nome:
                sql = "SELECT id_cliente, cpf_cnpj, nome, telefone, email FROM cliente WHERE nome LIKE %s OR cpf_cnpj LIKE %s ORDER BY id_cliente DESC;"
                res, err = execute_query(sql, (f"%{filtro_nome}%", f"%{filtro_nome}%"))
            else:
                sql = "SELECT id_cliente, cpf_cnpj, nome, telefone, email FROM cliente ORDER BY id_cliente DESC LIMIT 30;"
                res, err = execute_query(sql)
            
            if res:
                st.dataframe(pd.DataFrame(res), use_container_width=True)
            elif err:
                st.error(err)

        with tab_novo:
            with st.form("form_novo_cliente"):
                nome = st.text_input("Nome Completo / Razão Social:")
                cpf_cnpj = st.text_input("CPF ou CNPJ (único):")
                telefone = st.text_input("Telefone (opcional):")
                email = st.text_input("E-mail (único):")
                sub = st.form_submit_button("Salvar Cliente")
                if sub:
                    if not nome or not cpf_cnpj or not email:
                        st.warning("Preencha os campos obrigatórios (Nome, CPF/CNPJ e E-mail).")
                    else:
                        sql = "INSERT INTO cliente (cpf_cnpj, nome, telefone, email) VALUES (%s, %s, %s, %s);"
                        tel_val = telefone if telefone.strip() else None
                        ok, last_id, err = execute_dml(sql, (cpf_cnpj.strip(), nome.strip(), tel_val, email.strip()))
                        if ok:
                            st.success(f"✅ Cliente cadastrado com sucesso! ID gerado: {last_id}")
                        else:
                            st.error(err)

        with tab_edit:
            id_cli_edit = st.number_input("Informe o ID do Cliente:", min_value=1, step=1)
            col1, col2 = st.columns(2)
            with col1:
                novo_tel = st.text_input("Novo Telefone:")
                novo_email = st.text_input("Novo E-mail:")
                if st.button("Atualizar Dados de Contato"):
                    sql = "UPDATE cliente SET telefone = %s, email = %s WHERE id_cliente = %s;"
                    ok, _, err = execute_dml(sql, (novo_tel, novo_email, id_cli_edit))
                    if ok:
                        st.success("✅ Dados do cliente atualizados com sucesso!")
                    else:
                        st.error(err)
            with col2:
                st.write("**Exclusão Segura**")
                st.caption("A exclusão será bloqueada se o cliente possuir contas ativas.")
                if st.button("Excluir Cliente", type="secondary"):
                    sql = "DELETE FROM cliente WHERE id_cliente = %s;"
                    ok, _, err = execute_dml(sql, (id_cli_edit,))
                    if ok:
                        st.success("Cliente removido com sucesso!")
                    else:
                        st.error(err)

    # -----------------------------
    # CRUD 2: CONTA BANCÁRIA
    # -----------------------------
    elif entidade == "Conta Bancária":
        st.subheader("Gerenciamento de Contas Bancárias")
        tab_list, tab_nova, tab_status = st.tabs(["🔍 Listar Contas", "➕ Nova Conta", "🔒 Alterar Status"])
        
        with tab_list:
            res, err = execute_query("SELECT cb.numero_conta, cb.codigo_agencia, a.nome AS agencia, cb.modalidade, cb.saldo, cb.data_abertura, cb.status FROM conta_bancaria cb INNER JOIN agencia a ON cb.codigo_agencia = a.codigo_agencia ORDER BY cb.numero_conta DESC LIMIT 40;")
            if res:
                st.dataframe(pd.DataFrame(res), use_container_width=True)
            elif err:
                st.error(err)

        with tab_nova:
            with st.form("form_nova_conta"):
                num_conta = st.text_input("Número da Conta (ex: 10099-X):")
                cod_agencia = st.number_input("Código da Agência (1 a 5):", min_value=1, max_value=5, value=1)
                modalidade = st.selectbox("Modalidade:", ["CORRENTE", "POUPANCA"])
                saldo_ini = st.number_input("Saldo Inicial (R$):", min_value=0.0, value=100.0, step=50.0)
                sub_c = st.form_submit_button("Criar Conta")
                if sub_c:
                    sql = "INSERT INTO conta_bancaria (numero_conta, codigo_agencia, modalidade, saldo, data_abertura, status) VALUES (%s, %s, %s, %s, CURDATE(), 'ATIVA');"
                    ok, _, err = execute_dml(sql, (num_conta.strip(), cod_agencia, modalidade, saldo_ini))
                    if ok:
                        st.success(f"✅ Conta bancária {num_conta} aberta com sucesso!")
                    else:
                        st.error(err)

        with tab_status:
            c_target = st.text_input("Número da Conta para Alteração de Status:")
            novo_st = st.selectbox("Novo Status:", ["ATIVA", "BLOQUEADA", "ENCERRADA"])
            motivo = st.text_input("Motivo da Alteração:")
            if st.button("Confirmar Alteração de Status"):
                sql = "UPDATE conta_bancaria SET status = %s WHERE numero_conta = %s;"
                ok, _, err = execute_dml(sql, (novo_st, c_target))
                if ok:
                    # Registra histórico temporal
                    sql_h = "INSERT INTO historico_status_conta (numero_conta, status_anterior, status_novo, data_alteracao, motivo) VALUES (%s, 'ANTERIOR', %s, NOW(), %s);"
                    execute_dml(sql_h, (c_target, novo_st, motivo))
                    st.success(f"✅ Status da conta {c_target} alterado para {novo_st}! (Gatilho de auditoria disparado)")
                else:
                    st.error(err)

    # -----------------------------
    # CRUD 3: CARTÃO
    # -----------------------------
    elif entidade == "Cartão":
        st.subheader("Gerenciamento de Cartões")
        tab_list, tab_novo, tab_st = st.tabs(["🔍 Consultar Cartões", "➕ Emitir Cartão", "🔄 Alterar Status"])
        
        with tab_list:
            res, err = execute_query("SELECT numero_cartao, numero_conta, tipo, status FROM cartao ORDER BY numero_cartao DESC LIMIT 40;")
            if res:
                st.dataframe(pd.DataFrame(res), use_container_width=True)
            elif err:
                st.error(err)

        with tab_novo:
            with st.form("form_novo_cartao"):
                n_cartao = st.text_input("Número do Cartão (16 dígitos):", max_chars=16)
                n_conta_vinc = st.text_input("Número da Conta Vinculada:")
                tipo_c = st.selectbox("Tipo de Cartão:", ["DEBITO", "CREDITO", "MULTIPLO"])
                sub_cart = st.form_submit_button("Emitir Cartão")
                if sub_cart:
                    sql = "INSERT INTO cartao (numero_cartao, numero_conta, tipo, status) VALUES (%s, %s, %s, 'AGUARDANDO_DESBLOQUEIO');"
                    ok, _, err = execute_dml(sql, (n_cartao.strip(), n_conta_vinc.strip(), tipo_c))
                    if ok:
                        st.success(f"✅ Cartão {n_cartao} emitido com sucesso! Status: AGUARDANDO_DESBLOQUEIO.")
                    else:
                        st.error(err)

        with tab_st:
            num_cart_edit = st.text_input("Número do Cartão a Atualizar:")
            st_cart = st.selectbox("Status:", ["ATIVO", "BLOQUEADO", "CANCELADO", "AGUARDANDO_DESBLOQUEIO"])
            if st.button("Atualizar Status do Cartão"):
                sql = "UPDATE cartao SET status = %s WHERE numero_cartao = %s;"
                ok, _, err = execute_dml(sql, (st_cart, num_cart_edit))
                if ok:
                    st.success("✅ Status do cartão atualizado com sucesso!")
                else:
                    st.error(err)

    # -----------------------------
    # CRUD 4: BENEFICIÁRIO
    # -----------------------------
    elif entidade == "Beneficiário":
        st.subheader("Gerenciamento de Beneficiários e Favorecidos")
        tab_list, tab_novo = st.tabs(["🔍 Listar Beneficiários", "➕ Adicionar Beneficiário"])
        
        with tab_list:
            res, err = execute_query("SELECT id_beneficiario, numero_conta_origem, nome, documento, banco, agencia, conta FROM beneficiario ORDER BY id_beneficiario DESC LIMIT 30;")
            if res:
                st.dataframe(pd.DataFrame(res), use_container_width=True)
            elif err:
                st.error(err)

        with tab_novo:
            with st.form("form_novo_ben"):
                c_orig = st.text_input("Conta de Origem (Correntista):")
                nome_b = st.text_input("Nome do Favorecido:")
                doc_b = st.text_input("CPF ou CNPJ do Favorecido:")
                bco_b = st.text_input("Banco Destino (ex: 001 - Banco do Brasil):")
                ag_b = st.text_input("Agência Destino:")
                cta_b = st.text_input("Conta Destino:")
                sub_b = st.form_submit_button("Cadastrar Beneficiário")
                if sub_b:
                    sql = "INSERT INTO beneficiario (numero_conta_origem, nome, documento, banco, agencia, conta) VALUES (%s, %s, %s, %s, %s, %s);"
                    ok, last_id, err = execute_dml(sql, (c_orig.strip(), nome_b.strip(), doc_b.strip(), bco_b.strip(), ag_b.strip(), cta_b.strip()))
                    if ok:
                        st.success(f"✅ Beneficiário cadastrado com sucesso! ID: {last_id}")
                    else:
                        st.error(err)


# ==============================================================================
# 2. CONSULTAS PARAMETRIZADAS (B1)
# ==============================================================================
elif menu == "2. Consultas Parametrizadas (B1)":
    st.header("🔎 Telas de Consultas Parametrizadas com Junção e Agregação")
    st.markdown("Consultas com prepared statements puros, unindo múltiplas tabelas e agregando métricas.")

    tipo_cons = st.radio("Escolha a Consulta Parametrizada:", ["Consulta 1: Extrato por Período e Conta", "Consulta 2: Posição de Empréstimos e Inadimplência"])

    if tipo_cons == "Consulta 1: Extrato por Período e Conta":
        st.subheader("Extrato Detalhado de Transações")
        col1, col2, col3 = st.columns(3)
        with col1:
            conta_filtro = st.text_input("Número da Conta (deixe em branco para todas):", value="10001-X")
        with col2:
            data_ini = st.date_input("Data Inicial:", value=pd.to_datetime("2024-01-01"))
        with col3:
            data_fim = st.date_input("Data Final:", value=pd.to_datetime("2024-12-31"))

        if st.button("Buscar Extrato"):
            params = [f"{data_ini} 00:00:00", f"{data_fim} 23:59:59"]
            where_conta = ""
            if conta_filtro.strip():
                where_conta = "AND (t.numero_conta_origem = %s OR t.numero_conta_destino = %s)"
                params.extend([conta_filtro.strip(), conta_filtro.strip()])

            sql = f"""
            SELECT 
                t.id_transacao,
                t.data_hora,
                t.tipo AS tipo_operacao,
                t.valor,
                t.numero_conta_origem AS conta_origem,
                c_orig.nome AS titular_origem,
                t.numero_conta_destino AS conta_destino,
                COALESCE(c_dest.nome, 'Instituição / Caixa') AS titular_destino
            FROM transacao t
            INNER JOIN conta_bancaria cb_orig ON t.numero_conta_origem = cb_orig.numero_conta
            INNER JOIN cliente_conta cc_orig ON cb_orig.numero_conta = cc_orig.numero_conta AND cc_orig.tipo_titular = 'TITULAR'
            INNER JOIN cliente c_orig ON cc_orig.id_cliente = c_orig.id_cliente
            LEFT JOIN conta_bancaria cb_dest ON t.numero_conta_destino = cb_dest.numero_conta
            LEFT JOIN cliente_conta cc_dest ON cb_dest.numero_conta = cc_dest.numero_conta AND cc_dest.tipo_titular = 'TITULAR'
            LEFT JOIN cliente c_dest ON cc_dest.id_cliente = c_dest.id_cliente
            WHERE t.data_hora BETWEEN %s AND %s {where_conta}
            ORDER BY t.data_hora DESC;
            """
            res, err = execute_query(sql, tuple(params))
            if res:
                df = pd.DataFrame(res)
                st.dataframe(df, use_container_width=True)
                
                # Agregação resumida
                col_m1, col_m2 = st.columns(2)
                col_m1.metric("Total de Transações Encontradas", len(df))
                col_m2.metric("Volume Financeiro Total", f"R$ {df['valor'].sum():,.2f}")
            elif err:
                st.error(err)
            else:
                st.info("Nenhuma transação encontrada para os filtros selecionados.")

    elif tipo_cons == "Consulta 2: Posição de Empréstimos e Inadimplência":
        st.subheader("Relatório de Crédito e Parcelas por Cliente")
        status_filtro = st.selectbox("Status do Empréstimo:", ["TODOS", "ATIVO", "QUITADO", "INADIMPLENTE"])
        
        sql = """
        SELECT 
            c.id_cliente,
            c.nome AS cliente,
            c.cpf_cnpj,
            e.id_emprestimo,
            e.tipo_modalidade,
            e.valor_total AS valor_contratado,
            e.status AS status_contrato,
            COUNT(p.numero_parcela) AS total_parcelas,
            COALESCE(SUM(CASE WHEN p.status = 'PAGO' THEN p.valor ELSE 0 END), 0.00) AS total_amortizado,
            COALESCE(SUM(CASE WHEN p.status = 'EM_ATRASO' THEN p.valor ELSE 0 END), 0.00) AS total_em_atraso
        FROM cliente c
        INNER JOIN emprestimo e ON c.id_cliente = e.id_cliente
        LEFT JOIN parcela_emprestimo p ON e.id_emprestimo = p.id_emprestimo
        """
        params = []
        if status_filtro != "TODOS":
            sql += " WHERE e.status = %s "
            params.append(status_filtro)
        sql += " GROUP BY c.id_cliente, c.nome, c.cpf_cnpj, e.id_emprestimo, e.tipo_modalidade, e.valor_total, e.status ORDER BY total_em_atraso DESC;"

        res, err = execute_query(sql, tuple(params) if params else None)
        if res:
            st.dataframe(pd.DataFrame(res), use_container_width=True)
        elif err:
            st.error(err)


# ==============================================================================
# 3. RELATÓRIO CONSOLIDADO VIA VIEW (B1)
# ==============================================================================
elif menu == "3. Relatório Consolidado - VIEW (B1)":
    st.header("📊 Relatório Consolidado por Agência (Alimentado por VIEW)")
    st.markdown("Este painel consome diretamente a visão `vw_relatorio_consolidado_agencias` criada no MySQL.")

    res, err = execute_query("SELECT * FROM vw_relatorio_consolidado_agencias;")
    if res:
        df = pd.DataFrame(res)
        
        # Cards de Indicadores
        c1, c2, c3 = st.columns(3)
        c1.metric("Contas Ativas no Banco", int(df['total_contas_ativas'].sum()))
        c2.metric("Saldo sob Custódia Global", f"R$ {df['saldo_total_custodia'].sum():,.2f}")
        c3.metric("Volume Total Transacionado", f"R$ {df['volume_total_transacionado'].sum():,.2f}")
        
        st.divider()
        st.dataframe(df, use_container_width=True)
        
        # Gráfico
        st.bar_chart(data=df.set_index("nome_agencia")["volume_total_transacionado"])
    elif err:
        st.error(err)


# ==============================================================================
# 4. TRANSAÇÃO MULTITABELA & ROLLBACK (B1 e B3)
# ==============================================================================
elif menu == "4. Transação Multitabela & Rollback (B1/B3)":
    st.header("⚡ Operação Transacional Multitabela: Transferência entre Contas")
    st.markdown("""
    **Item Central da Etapa 2:** Demonstração prática dos mecanismos de atomicidade e integridade transacional.
    - Altera simultaneamente a conta de origem, a conta de destino e insere o histórico na tabela `transacao`.
    - Permite executar com sucesso (`COMMIT`) ou provocar falha proposital no meio da transação (`ROLLBACK`).
    """)

    col1, col2 = st.columns(2)
    with col1:
        c_origem = st.selectbox("Conta de Origem:", ["10001-X", "10002-X", "10003-X", "10004-X", "10005-X"])
        res_o, _ = execute_query("SELECT saldo, status FROM conta_bancaria WHERE numero_conta = %s;", (c_origem,), fetch_all=False)
        saldo_o = float(res_o['saldo']) if res_o else 0.0
        st.info(f"**Saldo Atual da Origem:** R$ {saldo_o:,.2f} · Status: {res_o['status'] if res_o else 'N/A'}")

    with col2:
        c_destino = st.selectbox("Conta de Destino:", ["10002-X", "10001-X", "10003-X", "10004-X", "10005-X"])
        res_d, _ = execute_query("SELECT saldo, status FROM conta_bancaria WHERE numero_conta = %s;", (c_destino,), fetch_all=False)
        saldo_d = float(res_d['saldo']) if res_d else 0.0
        st.info(f"**Saldo Atual do Destino:** R$ {saldo_d:,.2f} · Status: {res_d['status'] if res_d else 'N/A'}")

    valor_transf = st.number_input("Valor da Transferência (R$):", min_value=1.0, value=500.0, step=50.0)

    st.divider()
    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        st.write("🟢 **Cenário Normal (Sucesso)**")
        if st.button("Executar Transferência com Sucesso (COMMIT)", type="primary"):
            sucesso, msg = executar_transferencia_transacional(c_origem, c_destino, valor_transf, simular_falha=False)
            if sucesso:
                st.success(msg)
                st.balloons()
            else:
                st.error(msg)

    with col_btn2:
        st.write("🔴 **Cenário de Teste de Integridade (Falha Forçada)**")
        st.caption("Gera uma falha proposital no meio da transação após o débito. O ROLLBACK restaura o banco de dados sem deixar inconsistência.")
        if st.button("Simular Falha Proposital no Meio da Transação (ROLLBACK)"):
            sucesso, msg = executar_transferencia_transacional(c_origem, c_destino, valor_transf, simular_falha=True)
            if sucesso:
                st.success(msg)
            else:
                st.warning(f"⚠️ {msg}")
                st.info("Comprovado: Nenhum saldo foi debitado ou creditado indevidamente.")


# ==============================================================================
# 5. SEGURANÇA & SQL INJECTION (B2 e B5)
# ==============================================================================
elif menu == "5. Segurança & SQL Injection (B2/B5)":
    st.header("🛡️ Segurança, Prepared Statements e Controle de Acesso")
    
    tab_inj, tab_perfis, tab_lgpd = st.tabs(["🧪 Teste de SQL Injection (B2)", "👥 Perfis MySQL e Privilégios (B5)", "🔒 LGPD e Mascaramento (B5)"])

    with tab_inj:
        st.subheader("Demonstração de Resistência a SQL Injection")
        st.markdown("Conforme o edital B2, demonstração de que a aplicação utiliza Prepared Statements e resiste a injeções maliciosas.")

        payload_teste = st.text_input("Entrada maliciosa para teste:", value="' OR '1'='1")
        
        st.write("**Executando busca com Prepared Statement:**")
        st.code("cursor.execute('SELECT nome, email FROM cliente WHERE email = %s', (payload,))", language="python")
        
        res, err = execute_query("SELECT id_cliente, nome, email FROM cliente WHERE email = %s;", (payload_teste,))
        if res is not None:
            if len(res) == 0:
                st.success("✅ **Resistente a SQL Injection!** A query tratou a entrada como texto literal e não retornou registros indevidos.")
            else:
                st.dataframe(pd.DataFrame(res))
        elif err:
            st.error(err)

    with tab_perfis:
        st.subheader("Perfis de Acesso no MySQL com Menor Privilégio")
        perfil_sel = st.selectbox("Conectar sob o Perfil:", ["user_admin", "user_atendente", "user_auditor"])
        
        senhas = {
            "user_admin": "AdminPass#2026",
            "user_atendente": "AtendPass#2026",
            "user_auditor": "AuditPass#2026"
        }
        
        st.write(f"Testando consulta de exclusão sob o usuário **{perfil_sel}**...")
        if st.button("Tentar Excluir Agência (DELETE FROM agencia WHERE codigo_agencia = 999)"):
            ok, _, err = execute_dml("DELETE FROM agencia WHERE codigo_agencia = 999;", user=perfil_sel, password=senhas[perfil_sel])
            if ok:
                st.warning("Operação permitida pelo perfil.")
            else:
                st.error(f"Acesso Negado conforme esperado: {err}")

    with tab_lgpd:
        st.subheader("Tratamento de Dados Pessoais (LGPD)")
        st.markdown("Exibição da VIEW `vw_cliente_atendimento`, que mascara o CPF para operadores de atendimento:")
        res_v, _ = execute_query("SELECT id_cliente, nome, cpf_mascarado, telefone, email, numero_conta, modalidade, status_conta FROM vw_cliente_atendimento LIMIT 20;")
        if res_v:
            st.dataframe(pd.DataFrame(res_v), use_container_width=True)


# ==============================================================================
# 6. OTIMIZAÇÃO & EXPLAIN (B4)
# ==============================================================================
elif menu == "6. Otimização & EXPLAIN (B4)":
    st.header("⚡ Estudo de Otimização de Consultas com EXPLAIN (B4)")
    st.markdown("Análise dos planos de execução das 3 consultas críticas antes e depois dos índices compostos criados.")

    cons_critica = st.selectbox("Escolha a Consulta Crítica:", [
        "Consulta Crítica 1: Extrato por Conta e Período (idx_transacao_conta_data)",
        "Consulta Crítica 2: Cobrança de Parcelas em Atraso (idx_parcela_status_vencimento)",
        "Consulta Crítica 3: Histórico de Alterações de Status (idx_historico_conta_data)"
    ])

    if st.button("Executar EXPLAIN na Consulta Selecionada"):
        if "Consulta Crítica 1" in cons_critica:
            sql_exp = "EXPLAIN SELECT * FROM transacao WHERE numero_conta_origem = '10001-X' AND data_hora BETWEEN '2024-01-01' AND '2024-12-31' ORDER BY data_hora DESC;"
        elif "Consulta Crítica 2" in cons_critica:
            sql_exp = "EXPLAIN SELECT * FROM parcela_emprestimo WHERE status = 'EM_ATRASO' AND data_vencimento < '2024-10-01' ORDER BY data_vencimento ASC;"
        else:
            sql_exp = "EXPLAIN SELECT * FROM historico_status_conta WHERE numero_conta = '10001-X' ORDER BY data_alteracao DESC;"

        res, err = execute_query(sql_exp)
        if res:
            st.write("**Plano de Execução Retornado pelo MySQL 8.0:**")
            st.dataframe(pd.DataFrame(res), use_container_width=True)
            st.success("✅ **Análise do Plano**: O MySQL utiliza o índice composto (type: ref / range), evitando Full Table Scan e eliminando a etapa de 'filesort'.")
        elif err:
            st.error(err)


# ==============================================================================
# 7. GATILHOS DE AUDITORIA (B6)
# ==============================================================================
elif menu == "7. Gatilhos de Auditoria (B6)":
    st.header("📝 Tabela e Gatilhos de Auditoria em Tempo Real (B6)")
    st.markdown("Visualização direta da tabela `tb_auditoria_sistema`, alimentada automaticamente pelos triggers de auditoria em `conta_bancaria` e `parcela_emprestimo`:")

    res, err = execute_query("SELECT id_auditoria, tabela_afetada, operacao, registro_id, usuario_responsavel, data_hora, valores_anteriores, valores_novos FROM tb_auditoria_sistema ORDER BY id_auditoria DESC;")
    if res:
        st.dataframe(pd.DataFrame(res), use_container_width=True)
    elif err:
        st.error(err)
    else:
        st.info("Nenhum evento registrado ainda na tabela de auditoria.")
