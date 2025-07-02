import streamlit as st
import pandas as pd
import plotly.express as px

# Carrega os dados
df = pd.read_csv("solicitacoes_pda_powerbi.csv")

# Adicionando logo
st.markdown(
    """
    <div style="text-align: center;">
        <img src="Azul e Branco_.png" width="250">
    </div>
    """,
    unsafe_allow_html=True
)

# Título
st.title("📊 Painel Interativo - Solicitações de PDAs por Cidade e Área")

# Kpis
col1, col2, col3, col4 = st.columns([1.5, 2, 2, 2])

col1.metric("📊 Total de Solicitações", 237)
col2.metric("🏙️ Cidade destaque", "Patos")
col3.metric("📌 PDA mais solicitado", "Engenharia")
col4.metric("📈 Média por cidade", "59.2")

# Filtros
cidades = st.multiselect("Filtrar por cidade:",
                         df["Cidade"].unique(), default=df["Cidade"].unique())
pdas = st.multiselect("Filtrar por área temática (PDA):",
                      df["PDA"].unique(), default=df["PDA"].unique())

# Dados filtrados
df_filtrado = df[df["Cidade"].isin(cidades) & df["PDA"].isin(pdas)]

# Organiza em abas
tab1, tab2, tab3 = st.tabs(
    ["📊 Gráfico por PDA", "🏙️ Gráfico por Cidade", "📋 Dados Completos"])

with tab1:
    st.subheader("📊 Total de Solicitações por PDA")
    grafico_pda = df_filtrado.groupby("PDA", as_index=False)[
        "Solicitações"].sum()
    grafico_pda = grafico_pda.sort_values("Solicitações", ascending=False)
    fig1 = px.bar(grafico_pda, x="PDA", y="Solicitações",
                  color_discrete_sequence=["#636EFA"])
    st.plotly_chart(fig1, use_container_width=True)


with tab2:
    st.subheader("🏙️ Total de Solicitações por Cidade")
    grafico_cidade = df_filtrado.groupby("Cidade", as_index=False)[
        "Solicitações"].sum()
    grafico_cidade = grafico_cidade.sort_values(
        "Solicitações", ascending=False)
    fig2 = px.bar(grafico_cidade, x="Cidade", y="Solicitações",
                  color_discrete_sequence=["#636EFA"])
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.subheader("📋 Tabela de Dados Filtrados")
    st.dataframe(df_filtrado, use_container_width=True)
