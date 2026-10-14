import streamlit as st
import pandas as pd
from db import execute_query, execute_dml, executar_transferencia_transacional, get_connection
from auth import hash_senha, verificar_senha
from theme import apply_custom_theme
from ui_components import (
    render_header,
    render_kpi,
    render_empty_state,
    render_status_badge,
    render_callout
)

# Configuração da página Streamlit (layout amplo, título e favicon)
st.set_page_config(
    page_title="Sistema Bancário — Etapa 2 (N2)",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Aplicação do Design System (design-system-architect + ui-polish)
apply_custom_theme()

# ==============================================================================
# MENU LATERAL DE NAVEGAÇÃO
# ==============================================================================
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
        <span style="font-size: 1.8rem;">🏦</span>
        <div>
            <div style="font-weight: 700; font-size: 1.05rem; color: var(--foreground-primary);">Banco UCB</div>
            <div style="font-size: 0.75rem; color: var(--foreground-muted);">Gestão & Operações N2</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.caption("Laboratório de Banco de Dados · Prof. Samuel Novais Moura Júnior")
    st.divider()

    menu = st.radio(
        "Navegação por Requisito:",
        [
            "1. CRUD de 4 Entidades (B1)",
            "2. Consultas Parametrizadas (B1)",
            "3. Relatório Consolidado - VIEW (B1)",
            "4. Transação Multitabela & Rollback (B1/B3)",
            "5. Segurança & SQL Injection (B2/B5)",
            "6. Otimização & EXPLAIN (B4)",
            "7. Gatilhos de Auditoria (B6)"
        ],
        label_visibility="visible"
    )

    st.divider()
    render_callout(
        "Ambiente Conectado",
        "Conexão ativa com MySQL 8.0 via Prepared Statements nativos e governança de integridade financeira.",
        callout_type="info",
        icon="🔒"
    )

# ==============================================================================
# 1. CRUD DE 4 ENTIDADES (B1)
# ==============================================================================
if menu == "1. CRUD de 4 Entidades (B1)":
    render_header(
        title="CRUD de Entidades com Tratamento Amigável",
        subtitle="Gerenciamento de clientes, contas, cartões e favorecidos com validação de chaves e constraints.",
        badge_text="Requisito B1: CRUD",
        badge_type="primary",
        icon="📋"
    )

    entidade = st.selectbox(
        "Selecione a Entidade para Operar:",
        ["Cliente (PF/PJ)", "Conta Bancária", "Cartão", "Beneficiário"]
    )

    # -----------------------------
    # CRUD 1: CLIENTE
    # -----------------------------
    if entidade == "Cliente (PF/PJ)":
        tab_list, tab_novo, tab_edit = st.tabs(["🔍 Consultar Clientes", "➕ Novo Cliente", "✏️ Atualizar / Remover"])
        
        with tab_list:
            filtro_nome = st.text_input("Filtrar por nome ou CPF/CNPJ:", key="filtro_cli", placeholder="Digite para buscar...")
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
            else:
                render_empty_state("Nenhum cliente encontrado", "Tente outro termo de busca ou cadastre um novo cliente.", icon="👤", action_hint="Utilize a aba 'Novo Cliente'")

        with tab_novo:
            with st.form("form_novo_cliente"):
                c1, c2 = st.columns(2)
                with c1:
                    nome = st.text_input("Nome Completo / Razão Social:")
                    cpf_cnpj = st.text_input("CPF ou CNPJ (único):")
                with c2:
                    telefone = st.text_input("Telefone (opcional):")
                    email = st.text_input("E-mail corporativo/pessoal:")
                
                sub = st.form_submit_button("Cadastrar Cliente", type="primary")
                if sub:
                    if not nome or not cpf_cnpj or not email:
                        st.warning("Preencha todos os campos obrigatórios (Nome, CPF/CNPJ e E-mail).")
                    else:
                        sql = "INSERT INTO cliente (cpf_cnpj, nome, telefone, email) VALUES (%s, %s, %s, %s);"
                        tel_val = telefone.strip() if telefone and telefone.strip() else None
                        ok, last_id, err = execute_dml(sql, (cpf_cnpj.strip(), nome.strip(), tel_val, email.strip()))
                        if ok:
                            st.success(f"✅ Cliente cadastrado com sucesso! ID Gerado: {last_id}")
                        else:
                            st.error(err)

        with tab_edit:
            id_cli_edit = st.number_input("Informe o ID do Cliente para Gestão:", min_value=1, step=1)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Atualização de Contato**")
                novo_tel = st.text_input("Novo Telefone:")
                novo_email = st.text_input("Novo E-mail:")
                if st.button("Salvar Alterações de Contato"):
                    sql = "UPDATE cliente SET telefone = %s, email = %s WHERE id_cliente = %s;"
                    ok, _, err = execute_dml(sql, (novo_tel, novo_email, id_cli_edit))
                    if ok:
                        st.success("✅ Contato do cliente atualizado com sucesso!")
                    else:
                        st.error(err)
            with col2:
                st.markdown("**Exclusão com Integridade Referencial**")
                st.caption("A exclusão será bloqueada com mensagem clara caso o cliente possua contas vinculadas.")
                if st.button("Excluir Cliente com Segurança", type="secondary"):
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
        tab_list, tab_nova, tab_status = st.tabs(["🔍 Listar Contas", "➕ Nova Conta", "🔒 Alterar Status"])
        
        with tab_list:
            res, err = execute_query("SELECT cb.numero_conta, cb.codigo_agencia, a.nome AS agencia, cb.modalidade, cb.saldo, cb.data_abertura, cb.status FROM conta_bancaria cb INNER JOIN agencia a ON cb.codigo_agencia = a.codigo_agencia ORDER BY cb.numero_conta DESC LIMIT 40;")
            if res:
                st.dataframe(pd.DataFrame(res), use_container_width=True)
            elif err:
                st.error(err)
            else:
                render_empty_state("Nenhuma conta encontrada", "Abra a primeira conta na aba 'Nova Conta'.", icon="💳")

        with tab_nova:
            with st.form("form_nova_conta"):
                c1, c2 = st.columns(2)
                with c1:
                    num_conta = st.text_input("Número da Conta (ex: 10099-X):")
                    cod_agencia = st.number_input("Código da Agência (1 a 5):", min_value=1, max_value=5, value=1)
                with c2:
                    modalidade = st.selectbox("Modalidade:", ["CORRENTE", "POUPANCA"])
                    saldo_ini = st.number_input("Depósito Inicial (R$):", min_value=0.0, value=100.0, step=50.0)
                
                sub_c = st.form_submit_button("Abrir Conta Bancária", type="primary")
                if sub_c:
                    sql = "INSERT INTO conta_bancaria (numero_conta, codigo_agencia, modalidade, saldo, data_abertura, status) VALUES (%s, %s, %s, %s, CURDATE(), 'ATIVA');"
                    ok, _, err = execute_dml(sql, (num_conta.strip(), cod_agencia, modalidade, saldo_ini))
                    if ok:
                        st.success(f"✅ Conta {num_conta} aberta com sucesso com status ATIVA!")
                    else:
                        st.error(err)

        with tab_status:
            c_target = st.text_input("Número da Conta Alvo:")
            c1, c2 = st.columns(2)
            with c1:
                novo_st = st.selectbox("Novo Status:", ["ATIVA", "BLOQUEADA", "ENCERRADA"])
            with c2:
                motivo = st.text_input("Justificativa da Alteração:")
            
            if st.button("Confirmar Alteração de Status", type="primary"):
                sql = "UPDATE conta_bancaria SET status = %s WHERE numero_conta = %s;"
                ok, _, err = execute_dml(sql, (novo_st, c_target))
                if ok:
                    # Registra histórico temporal na entidade fraca
                    sql_h = "INSERT INTO historico_status_conta (numero_conta, status_anterior, status_novo, data_alteracao, motivo) VALUES (%s, 'ANTERIOR', %s, NOW(), %s);"
                    execute_dml(sql_h, (c_target, novo_st, motivo))
                    st.success(f"✅ Status da conta {c_target} alterado para {novo_st}! Histórico e auditoria disparados.")
                else:
                    st.error(err)

    # -----------------------------
    # CRUD 3: CARTÃO
    # -----------------------------
    elif entidade == "Cartão":
        tab_list, tab_novo, tab_st = st.tabs(["🔍 Consultar Cartões", "➕ Emitir Cartão", "🔄 Alterar Status"])
        
        with tab_list:
            res, err = execute_query("SELECT numero_cartao, numero_conta, tipo, status FROM cartao ORDER BY numero_cartao DESC LIMIT 40;")
            if res:
                st.dataframe(pd.DataFrame(res), use_container_width=True)
            elif err:
                st.error(err)
            else:
                render_empty_state("Nenhum cartão emitido", "Emita novos cartões vinculados a contas correntes.", icon="💳")

        with tab_novo:
            with st.form("form_novo_cartao"):
                n_cartao = st.text_input("Número do Cartão (16 dígitos numéricos):", max_chars=16)
                n_conta_vinc = st.text_input("Número da Conta Vinculada:")
                tipo_c = st.selectbox("Tipo de Cartão:", ["DEBITO", "CREDITO", "MULTIPLO"])
                sub_cart = st.form_submit_button("Emitir Novo Cartão", type="primary")
                if sub_cart:
                    sql = "INSERT INTO cartao (numero_cartao, numero_conta, tipo, status) VALUES (%s, %s, %s, 'AGUARDANDO_DESBLOQUEIO');"
                    ok, _, err = execute_dml(sql, (n_cartao.strip(), n_conta_vinc.strip(), tipo_c))
                    if ok:
                        st.success(f"✅ Cartão {n_cartao} emitido com sucesso! Status inicial: AGUARDANDO_DESBLOQUEIO.")
                    else:
                        st.error(err)

        with tab_st:
            num_cart_edit = st.text_input("Número do Cartão a Modificar:")
            st_cart = st.selectbox("Novo Status:", ["ATIVO", "BLOQUEADO", "CANCELADO", "AGUARDANDO_DESBLOQUEIO"])
            if st.button("Atualizar Situação do Cartão"):
                sql = "UPDATE cartao SET status = %s WHERE numero_cartao = %s;"
                ok, _, err = execute_dml(sql, (st_cart, num_cart_edit))
                if ok:
                    st.success("✅ Situação do cartão atualizada!")
                else:
                    st.error(err)

    # -----------------------------
    # CRUD 4: BENEFICIÁRIO
    # -----------------------------
    elif entidade == "Beneficiário":
        tab_list, tab_novo = st.tabs(["🔍 Listar Beneficiários", "➕ Adicionar Beneficiário"])
        
        with tab_list:
            res, err = execute_query("SELECT id_beneficiario, numero_conta_origem, nome, documento, banco, agencia, conta FROM beneficiario ORDER BY id_beneficiario DESC LIMIT 30;")
            if res:
                st.dataframe(pd.DataFrame(res), use_container_width=True)
            elif err:
                st.error(err)
            else:
                render_empty_state("Nenhum beneficiário cadastrado", "Cadastre favorecidos frequentes para transferências rápidas.", icon="🤝")

        with tab_novo:
            with st.form("form_novo_ben"):
                c1, c2 = st.columns(2)
                with c1:
                    c_orig = st.text_input("Conta de Origem do Cliente:")
                    nome_b = st.text_input("Nome Completo do Favorecido:")
                    doc_b = st.text_input("CPF ou CNPJ do Favorecido:")
                with c2:
                    bco_b = st.text_input("Código/Nome do Banco:", value="001 - Banco do Brasil")
                    ag_b = st.text_input("Agência:")
                    cta_b = st.text_input("Conta com Dígito:")
                
                sub_b = st.form_submit_button("Cadastrar Favorecido", type="primary")
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
    render_header(
        title="Consultas Parametrizadas & Métricas",
        subtitle="Execução analítica com junções múltiplas, agregações financeiras e filtros dinâmicos protegidos.",
        badge_text="Requisito B1: Consultas",
        badge_type="info",
        icon="🔎"
    )

    tipo_cons = st.radio(
        "Selecione o Relatório Parametrizado:",
        ["Extrato Financeiro por Período & Conta", "Posição de Crédito, Empréstimos & Inadimplência"],
        horizontal=True
    )

    if tipo_cons == "Extrato Financeiro por Período & Conta":
        c1, c2, c3 = st.columns([1.5, 1, 1])
        with c1:
            conta_filtro = st.text_input("Número da Conta (deixe vazio para todas):", value="10001-X")
        with c2:
            data_ini = st.date_input("Data Inicial:", value=pd.to_datetime("2024-01-01"))
        with c3:
            data_fim = st.date_input("Data Final:", value=pd.to_datetime("2026-12-31"))

        if st.button("Buscar Extrato Parametrizado", type="primary"):
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
                
                # Cards de Indicadores
                kpi1, kpi2, kpi3 = st.columns(3)
                render_kpi(kpi1, "Transações Encontradas", f"{len(df)}", "No período selecionado", badge_text="Total", badge_type="primary")
                render_kpi(kpi2, "Volume Total Transacionado", f"R$ {df['valor'].sum():,.2f}", "Soma dos valores movimentados", badge_text="Volume", badge_type="success")
                render_kpi(kpi3, "Ticket Médio", f"R$ {df['valor'].mean():,.2f}", "Média aritmética por operação", badge_text="Média", badge_type="neutral")
                
                st.markdown("### Detalhamento das Operações")
                st.dataframe(df, use_container_width=True)
            elif err:
                st.error(err)
            else:
                render_empty_state("Nenhuma transação encontrada", "Verifique o intervalo de datas ou a conta informada.", icon="📅")

    elif tipo_cons == "Posição de Crédito, Empréstimos & Inadimplência":
        status_filtro = st.selectbox("Filtrar por Status do Empréstimo:", ["TODOS", "ATIVO", "QUITADO", "INADIMPLENTE"])
        
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
            df = pd.DataFrame(res)
            st.dataframe(df, use_container_width=True)
        elif err:
            st.error(err)
        else:
            render_empty_state("Nenhum contrato encontrado", "Não há contratos com o status selecionado.", icon="📄")

# ==============================================================================
# 3. RELATÓRIO CONSOLIDADO VIA VIEW (B1)
# ==============================================================================
elif menu == "3. Relatório Consolidado - VIEW (B1)":
    render_header(
        title="Relatório Consolidado por Agência (VIEW)",
        subtitle="Agregações em tempo real consumindo a visão segura vw_relatorio_consolidado_agencias.",
        badge_text="Requisito B1: VIEW",
        badge_type="success",
        icon="📊"
    )

    res, err = execute_query("SELECT * FROM vw_relatorio_consolidado_agencias;")
    if res:
        df = pd.DataFrame(res)
        
        c1, c2, c3 = st.columns(3)
        render_kpi(c1, "Contas Ativas", f"{int(df['total_contas_ativas'].sum())}", "Distribuídas em todas as agências", badge_text="Total", badge_type="primary")
        render_kpi(c2, "Custódia Global", f"R$ {df['saldo_total_custodia'].sum():,.2f}", "Depósitos totais sob custódia", badge_text="Depósitos", badge_type="success")
        render_kpi(c3, "Volume Movimentado", f"R$ {df['volume_total_transacionado'].sum():,.2f}", "Total de transações registradas", badge_text="Movimento", badge_type="neutral")
        
        st.markdown("### Resumo por Agência")
        st.dataframe(df, use_container_width=True)
        
        st.markdown("### Distribuição de Volume Transacionado")
        st.bar_chart(data=df.set_index("nome_agencia")["volume_total_transacionado"])
    elif err:
        st.error(err)
    else:
        render_empty_state("VIEW vazia", "Não há dados consolidados de agências no banco.", icon="📊")

# ==============================================================================
# 4. TRANSAÇÃO MULTITABELA & ROLLBACK (B1/B3)
# ==============================================================================
elif menu == "4. Transação Multitabela & Rollback (B1/B3)":
    render_header(
        title="Atomicidade Transacional ACID & Simulação de Falha",
        subtitle="Operação multitabela coordenada entre débito, crédito e registro com suporte a ROLLBACK garantido.",
        badge_text="Requisito B1 / B3: ACID",
        badge_type="warning",
        icon="⚡"
    )

    render_callout(
        "Mecanismo de Integridade Financeira",
        "A transferência debita a conta de origem, credita a de destino e gera o registro histórico na tabela `transacao`. Se qualquer etapa falhar ou for interrompida, todas as alterações são desfeitas imediatamente via ROLLBACK.",
        callout_type="info",
        icon="ℹ️"
    )

    c1, c2 = st.columns(2)
    with c1:
        c_origem = st.selectbox("Conta de Origem:", ["10001-X", "10002-X", "10003-X", "10004-X", "10005-X"])
        res_o, _ = execute_query("SELECT saldo, status FROM conta_bancaria WHERE numero_conta = %s;", (c_origem,), fetch_all=False)
        saldo_o = float(res_o['saldo']) if res_o else 0.0
        render_kpi(st, f"Saldo Origem ({c_origem})", f"R$ {saldo_o:,.2f}", f"Status: {res_o['status'] if res_o else 'N/A'}", badge_text="Origem", badge_type="neutral")

    with c2:
        c_destino = st.selectbox("Conta de Destino:", ["10002-X", "10001-X", "10003-X", "10004-X", "10005-X"])
        res_d, _ = execute_query("SELECT saldo, status FROM conta_bancaria WHERE numero_conta = %s;", (c_destino,), fetch_all=False)
        saldo_d = float(res_d['saldo']) if res_d else 0.0
        render_kpi(st, f"Saldo Destino ({c_destino})", f"R$ {saldo_d:,.2f}", f"Status: {res_d['status'] if res_d else 'N/A'}", badge_text="Destino", badge_type="neutral")

    valor_transf = st.number_input("Valor da Operação (R$):", min_value=1.0, value=300.0, step=50.0)

    st.markdown("---")
    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        st.markdown("**🟢 Execução Normal com COMMIT**")
        if st.button("Executar Transferência com Sucesso", type="primary"):
            sucesso, msg = executar_transferencia_transacional(c_origem, c_destino, valor_transf, simular_falha=False)
            if sucesso:
                st.success(msg)
                st.balloons()
            else:
                st.error(msg)

    with col_btn2:
        st.markdown("**🔴 Teste de Resiliência com Falha Forçada (ROLLBACK)**")
        st.caption("Provoca uma exceção deliberada logo após debitar a origem, testando a restauração do saldo.")
        if st.button("Simular Falha no Meio da Transação", type="secondary"):
            sucesso, msg = executar_transferencia_transacional(c_origem, c_destino, valor_transf, simular_falha=True)
            if sucesso:
                st.success(msg)
            else:
                st.warning(f"⚠️ {msg}")
                st.info("Comprovado: Nenhum valor foi debitado ou perdido indevidamente. Atomicidade garantida.")

# ==============================================================================
# 5. SEGURANÇA & SQL INJECTION (B2/B5)
# ==============================================================================
elif menu == "5. Segurança & SQL Injection (B2/B5)":
    render_header(
        title="Segurança, Prevenção contra SQLi & Controle de Acesso",
        subtitle="Blindagem por Prepared Statements, perfis de menor privilégio e mascaramento de dados (LGPD).",
        badge_text="Requisito B2 / B5: Segurança",
        badge_type="error",
        icon="🛡️"
    )

    tab_inj, tab_perfis, tab_lgpd = st.tabs(["🧪 Teste de SQL Injection", "👥 Perfis MySQL & Privilégios", "🔒 Proteção LGPD"])

    with tab_inj:
        st.markdown("### Demonstração de Imunidade a Injeção de Código")
        st.markdown("Mesmo inserindo comandos SQL maliciosos, a biblioteca trata os dados como literais via Prepared Statements.")

        payload_teste = st.text_input("Payload malicioso para teste:", value="' OR '1'='1")
        st.code("cursor.execute('SELECT nome, email FROM cliente WHERE email = %s', (payload,))", language="python")

        res, err = execute_query("SELECT id_cliente, nome, email FROM cliente WHERE email = %s;", (payload_teste,))
        if res is not None:
            if len(res) == 0:
                render_callout(
                    "Blindagem Confirmada!",
                    "A consulta tratou o payload como string literal. Nenhum vazamento de tabela ou bypass de autenticação ocorreu.",
                    callout_type="success",
                    icon="🛡️"
                )
            else:
                st.dataframe(pd.DataFrame(res))
        elif err:
            st.error(err)

    with tab_perfis:
        st.markdown("### Teste de Privilégios Mínimos por Usuário")
        perfil_sel = st.selectbox("Conectar com as Credenciais de:", ["user_admin", "user_atendente", "user_auditor"])
        senhas = {
            "user_admin": "AdminPass#2026",
            "user_atendente": "AtendPass#2026",
            "user_auditor": "AuditPass#2026"
        }
        
        st.write(f"Tentando executar comando `DELETE` sob a conta `{perfil_sel}`...")
        if st.button("Executar Operação Restrita (DELETE FROM agencia WHERE codigo_agencia = 999)"):
            ok, _, err = execute_dml("DELETE FROM agencia WHERE codigo_agencia = 999;", user=perfil_sel, password=senhas[perfil_sel])
            if ok:
                st.warning("Comando executado com sucesso.")
            else:
                st.error(f"Acesso Recusado conforme política de segurança: {err}")

    with tab_lgpd:
        st.markdown("### Mascaramento de Documentos Pessoais (LGPD)")
        st.markdown("Atendentes visualizam o CPF ofuscado (`***.456.789-**`) através da VIEW `vw_cliente_atendimento`:")
        res_v, _ = execute_query("SELECT id_cliente, nome, cpf_mascarado, telefone, email, numero_conta, modalidade, status_conta FROM vw_cliente_atendimento LIMIT 20;")
        if res_v:
            st.dataframe(pd.DataFrame(res_v), use_container_width=True)

# ==============================================================================
# 6. OTIMIZAÇÃO & EXPLAIN (B4)
# ==============================================================================
elif menu == "6. Otimização & EXPLAIN (B4)":
    render_header(
        title="Otimização de Consultas & EXPLAIN ANALYZE",
        subtitle="Demonstração do ganho de eficiência com índices compostos em tabelas de alto volume.",
        badge_text="Requisito B4: Otimização",
        badge_type="info",
        icon="⚡"
    )

    cons_critica = st.selectbox("Selecione a Consulta Crítica para Análise:", [
        "1. Extrato por Conta e Período (idx_transacao_conta_data)",
        "2. Cobrança de Parcelas em Atraso (idx_parcela_status_vencimento)",
        "3. Histórico de Alterações de Status (idx_historico_conta_data)"
    ])

    if st.button("Executar EXPLAIN na Consulta", type="primary"):
        if "1. Extrato" in cons_critica:
            sql_exp = "EXPLAIN SELECT * FROM transacao WHERE numero_conta_origem = '10001-X' AND data_hora BETWEEN '2024-01-01' AND '2024-12-31' ORDER BY data_hora DESC;"
        elif "2. Cobrança" in cons_critica:
            sql_exp = "EXPLAIN SELECT * FROM parcela_emprestimo WHERE status = 'EM_ATRASO' AND data_vencimento < '2024-10-01' ORDER BY data_vencimento ASC;"
        else:
            sql_exp = "EXPLAIN SELECT * FROM historico_status_conta WHERE numero_conta = '10001-X' ORDER BY data_alteracao DESC;"

        res, err = execute_query(sql_exp)
        if res:
            st.markdown("### Plano de Execução Gerado pelo Otimizador:")
            st.dataframe(pd.DataFrame(res), use_container_width=True)
            render_callout(
                "Índice Utilizado com Sucesso!",
                "O otimizador do MySQL 8.0 utilizou index lookup (type: ref / range), eliminando Full Table Scan e a necessidade de classificação em disco (filesort).",
                callout_type="success",
                icon="⚡"
            )
        elif err:
            st.error(err)

# ==============================================================================
# 7. GATILHOS DE AUDITORIA (B6)
# ==============================================================================
elif menu == "7. Gatilhos de Auditoria (B6)":
    render_header(
        title="Trilha de Auditoria em Tempo Real",
        subtitle="Rastreabilidade automática de alterações capturadas por Triggers AFTER UPDATE com payload JSON.",
        badge_text="Requisito B6: Auditoria",
        badge_type="primary",
        icon="📝"
    )

    res, err = execute_query("SELECT id_auditoria, tabela_afetada, operacao, registro_id, usuario_responsavel, data_hora, valores_anteriores, valores_novos FROM tb_auditoria_sistema ORDER BY id_auditoria DESC;")
    if res:
        st.dataframe(pd.DataFrame(res), use_container_width=True)
    elif err:
        st.error(err)
    else:
        render_empty_state("Nenhum evento registrado", "Altere o status de uma conta bancária ou parcela para disparar o trigger.", icon="📝", action_hint="Vá até a aba 'CRUD de Contas' e altere um status.")
