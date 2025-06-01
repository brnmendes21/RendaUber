import streamlit as st import pandas as pd from datetime import datetime

st.set_page_config(page_title="Renda Uber", layout="wide") st.title("🚗 Painel de Controle - Renda Uber")

Inicialização dos dados

if "dados" not in st.session_state: st.session_state.dados = pd.DataFrame(columns=[ "Data", "KM Final do Dia", "KM Inicial do Dia", "KM Rodado", "Uber (R$)", "99 (R$)", "Outros (R$)", "Gorjeta (R$)", "Combustível (R$)", "Aluguel (R$)", "Outros Gastos (R$)", "Faturamento Bruto (R$)", "Custo Total (R$)", "Lucro Líquido (R$)" ])

Navegação por abas

aba = st.sidebar.radio("Selecione a aba:", ["Registrar Dia", "Gastos", "Relatórios"])

if aba == "Registrar Dia": st.header("📅 Registro Diário")

data = st.date_input("Data", value=datetime.today())
km_final = st.number_input("KM do painel (final do dia)", min_value=0.0, step=1.0)
km_inicial = st.session_state.dados["KM Final do Dia"].iloc[-1] if not st.session_state.dados.empty else 0.0
km_rodado = km_final - km_inicial
st.markdown(f"**KM Inicial automático:** {km_inicial:.1f} km")
st.markdown(f"**KM Rodado calculado:** {km_rodado:.1f} km")

col1, col2, col3 = st.columns(3)
with col1:
    uber = st.number_input("Uber (R$)", min_value=0.0, step=1.0)
with col2:
    nove_nove = st.number_input("99 (R$)", min_value=0.0, step=1.0)
with col3:
    outros = st.number_input("Outros ganhos (R$)", min_value=0.0, step=1.0)

gorjeta = st.number_input("Gorjetas (R$)", min_value=0.0, step=1.0)
combustivel = st.number_input("Gasto com Combustível (R$)", min_value=0.0, step=1.0)
aluguel = st.number_input("Gasto com Aluguel (R$)", min_value=0.0, step=1.0)
outros_gastos = st.number_input("Outros Gastos (R$)", min_value=0.0, step=1.0)

if st.button("Salvar Dia"):
    faturamento_bruto = uber + nove_nove + outros + gorjeta
    custo_total = combustivel + aluguel + outros_gastos
    lucro_liquido = faturamento_bruto - custo_total

    nova_linha = {
        "Data": data.strftime("%d/%m/%Y"),
        "KM Final do Dia": km_final,
        "KM Inicial do Dia": km_inicial,
        "KM Rodado": km_rodado,
        "Uber (R$)": uber,
        "99 (R$)": nove_nove,
        "Outros (R$)": outros,
        "Gorjeta (R$)": gorjeta,
        "Combustível (R$)": combustivel,
        "Aluguel (R$)": aluguel,
        "Outros Gastos (R$)": outros_gastos,
        "Faturamento Bruto (R$)": faturamento_bruto,
        "Custo Total (R$)": custo_total,
        "Lucro Líquido (R$)": lucro_liquido
    }

    st.session_state.dados = pd.concat([st.session_state.dados, pd.DataFrame([nova_linha])], ignore_index=True)
    st.success("✅ Dados salvos com sucesso!")

elif aba == "Gastos": st.header("📂 Gastos Detalhados") tipo_gasto = st.selectbox("Categoria de Gasto", ["Combustível", "Aluguel", "Outros"]) total = 0

if tipo_gasto == "Combustível":
    total = st.session_state.dados["Combustível (R$)"].sum()
elif tipo_gasto == "Aluguel":
    total = st.session_state.dados["Aluguel (R$)"].sum()
else:
    total = st.session_state.dados["Outros Gastos (R$)"].sum()

st.metric(f"Total gasto com {tipo_gasto}", f"R$ {total:.2f}")

elif aba == "Relatórios": st.header("📊 Relatórios e Progresso") df = st.session_state.dados

if not df.empty:
    col1, col2, col3 = st.columns(3)
    col1.metric("Lucro líquido total", f"R$ {df['Lucro Líquido (R$)'].sum():.2f}")
    col2.metric("Faturamento bruto", f"R$ {df['Faturamento Bruto (R$)'].sum():.2f}")
    col3.metric("Total gasto", f"R$ {df['Custo Total (R$)'].sum():.2f}")

    # Gráfico de pizza
    st.subheader("📎 Distribuição de Custos")
    pie_data = pd.DataFrame({
        'Categoria': ['Lucro', 'Combustível', 'Aluguel', 'Outros'],
        'Valor': [
            df['Lucro Líquido (R$)'].sum(),
            df['Combustível (R$)'].sum(),
            df['Aluguel (R$)'].sum(),
            df['Outros Gastos (R$)'].sum()
        ]
    })
    st.plotly_chart({
        "data": [{
            "type": "pie",
            "labels": pie_data['Categoria'],
            "values": pie_data['Valor'],
            "hole": 0.4
        }]
    })

    st.subheader("📅 Histórico Completo")
    st.dataframe(df, use_container_width=True)

    # Botão para baixar os dados
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Baixar CSV", data=csv, file_name="renda_uber.csv", mime="text/csv")
else:
    st.info("Nenhum dado registrado ainda.")

