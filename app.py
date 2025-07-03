import streamlit as st
import pandas as pd
import plotly.express as px

# Carrega os dados
df = pd.read_csv("solicitacoes_pda_consolidadas.csv")

# Função para top n + "Outros"


def top_n_com_others(df, coluna, valor, n=5):
    # Agrupa e ordena
    df_agg = df.groupby(coluna, as_index=False)[valor].sum()
    df_agg = df_agg.sort_values(valor, ascending=False)

    # Seleciona top n
    top_n = df_agg.head(n)
    outros = df_agg.iloc[n:]

    # Soma o resto como "Outros"
    outros_sum = outros[valor].sum()

    # Cria novo dataframe incluindo "Outros"
    df_final = pd.concat([top_n, pd.DataFrame(
        {coluna: ['Outros'], valor: [outros_sum]})], ignore_index=True)
    return df_final


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

    st.subheader("🍩 Participação percentual Top 5 por PDA")
    grafico_pda_top5 = top_n_com_others(
        df_filtrado, "PDA", "Solicitações", n=5)
    fig_donut = px.pie(
        grafico_pda_top5,
        values='Solicitações',
        names='PDA',
        hole=0.5,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig_donut, use_container_width=True)

with tab2:
    st.subheader("🏙️ Total de Solicitações por Cidade")
    grafico_cidade = df_filtrado.groupby("Cidade", as_index=False)[
        "Solicitações"].sum()
    grafico_cidade = grafico_cidade.sort_values(
        "Solicitações", ascending=False)
    fig2 = px.bar(grafico_cidade, x="Cidade", y="Solicitações",
                  color_discrete_sequence=["#636EFA"])
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("🍩 Participação percentual por Cidade")
    grafico_cidade_top4 = top_n_com_others(
        df_filtrado, "Cidade", "Solicitações", n=4)
    fig_donut_cidade = px.pie(
        grafico_cidade_top4,
        values='Solicitações',
        names='Cidade',
        hole=0.5,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig_donut_cidade, use_container_width=True)

with tab3:
    st.subheader("📋 Tabela de Dados Filtrados")
    st.dataframe(df_filtrado, use_container_width=True)
