import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Renda Uber", layout="centered")

st.title("📊 Controle de Renda - Uber")

# Inicialização do DataFrame
if "dados" not in st.session_state:
    st.session_state.dados = pd.DataFrame(columns=[
        "Data", "Km Rodado", "Uber (R$)", "99 (R$)", "Outros (R$)", "Gorjeta (R$)",
        "Combustível (R$)", "Aluguel (R$)", "Faturamento Bruto (R$)", "Custo Total (R$)", "Lucro Líquido (R$)"
    ])

# Entrada de dados
data = st.date_input("Data", value=datetime.today())
km = st.number_input("Km rodado no dia", min_value=0.0, step=1.0)
uber = st.number_input("Faturamento Uber (R$)", min_value=0.0, step=1.0)
nove_nove = st.number_input("Faturamento 99 (R$)", min_value=0.0, step=1.0)
outros = st.number_input("Outros ganhos (R$)", min_value=0.0, step=1.0)
gorjeta = st.number_input("Gorjetas (R$)", min_value=0.0, step=1.0)
combustivel = st.number_input("Combustível do dia (R$)", min_value=0.0, step=1.0)
aluguel = st.number_input("Aluguel proporcional (R$)", min_value=0.0, step=1.0)

if st.button("Salvar dados do dia"):
    faturamento_bruto = uber + nove_nove + outros + gorjeta
    custo_total = combustivel + aluguel
    lucro_liquido = faturamento_bruto - custo_total

    nova_linha = {
        "Data": data.strftime("%d/%m/%Y"),
        "Km Rodado": km,
        "Uber (R$)": uber,
        "99 (R$)": nove_nove,
        "Outros (R$)": outros,
        "Gorjeta (R$)": gorjeta,
        "Combustível (R$)": combustivel,
        "Aluguel (R$)": aluguel,
        "Faturamento Bruto (R$)": faturamento_bruto,
        "Custo Total (R$)": custo_total,
        "Lucro Líquido (R$)": lucro_liquido
    }

    st.session_state.dados = pd.concat([st.session_state.dados, pd.DataFrame([nova_linha])], ignore_index=True)
    st.success("✅ Dados salvos com sucesso!")

# Exibição da tabela
dataframe = st.session_state.dados
if not dataframe.empty:
    st.subheader("📅 Histórico de Dados")
    st.dataframe(dataframe, use_container_width=True)

    st.subheader("📈 Lucro Acumulado")
    st.metric("Lucro líquido total (R$)", f"{dataframe['Lucro Líquido (R$)'].sum():.2f}")
    st.line_chart(dataframe.set_index("Data")["Lucro Líquido (R$)"])

    # Botão para baixar os dados
    csv = dataframe.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Baixar CSV", data=csv, file_name="renda_uber.csv", mime="text/csv")
