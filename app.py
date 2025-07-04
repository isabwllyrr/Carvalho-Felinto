import streamlit as st
import pandas as pd
import plotly.express as px

# Carrega os dados principais
df = pd.read_csv("solicitacoes_pda_consolidadas.csv")

# Função para Top N + "Outros"


def top_n_com_others(df, coluna, valor, n=5):
    df_agg = df.groupby(coluna, as_index=False)[
        valor].sum().sort_values(valor, ascending=False)
    top_n = df_agg.head(n)
    outros = df_agg.iloc[n:]
    outros_sum = outros[valor].sum()
    df_final = pd.concat([top_n, pd.DataFrame(
        {coluna: ['Outros'], valor: [outros_sum]})], ignore_index=True)
    return df_final


# Logo carvalho e felinto + PM
col1, col2 = st.columns(2)

with col1:
    st.image("logo_esquerda_.png", width=200)

with col2:
    st.image("logo_direita_.png", width=200)

st.title("📊 Painel Interativo - Solicitações de PDAs por Cidade e Área")

# Filtros
cidades = st.multiselect("Filtrar por cidade:",
                         df["Cidade"].unique(), default=df["Cidade"].unique())
pdas = st.multiselect("Filtrar por área temática (PDA):",
                      df["PDA"].unique(), default=df["PDA"].unique())

# Dados filtrados
df_filtrado = df[df["Cidade"].isin(cidades) & df["PDA"].isin(pdas)]

# Dicionário com as coordenadas das cidades
coordenadas = {
    'Cidade': ['Patos', 'Campina Grande', 'João Pessoa', 'Guarabira'],
    'Latitude': [-7.0172, -7.2306, -7.1195, -6.8506],
    'Longitude': [-37.2747, -35.8811, -34.8450, -35.4853]
}

# DataFrame com coordenadas
df_coords = pd.DataFrame(coordenadas)

# Merge das coordenadas no dataframe filtrado
df_filtrado = df_filtrado.merge(df_coords, on='Cidade', how='left')

# Abas de navegação
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Gráfico por PDA",
    "🏙️ Gráfico por Cidade",
    "📌 Problemas Mais Recorrentes",
    "🗘️ Mapa das Solicitações",
    "📅 Download"
])

# --- ABA 1: Gráfico por PDA ---
with tab1:
    st.subheader("📊 Total de Solicitações por PDA")
    grafico_pda = df_filtrado.groupby("PDA", as_index=False)[
        "Solicitações"].sum().sort_values("Solicitações", ascending=False)
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

# --- ABA 2: Gráfico por Cidade ---
with tab2:
    st.subheader("🏙️ Total de Solicitações por Cidade")
    grafico_cidade = df_filtrado.groupby("Cidade", as_index=False)[
        "Solicitações"].sum().sort_values("Solicitações", ascending=False)
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

# --- ABA 3: Problemas Mais Recorrentes (com 2 gráficos) ---
with tab3:
    st.subheader("📌 Problemas Mais Recorrentes (Top 10)")

    # Top 10 problemas identificados manualmente
    problemas_top10 = [
        {"Problema": "Baixo efetivo", "Ocorrências": 35},
        {"Problema": "Infraestrutura precária", "Ocorrências": 30},
        {"Problema": "Salário insatisfatório", "Ocorrências": 10},
        {"Problema": "Tecnologia obsoleta", "Ocorrências": 9},
        {"Problema": "Falta de capacitação", "Ocorrências": 8},
        {"Problema": "Falta de viaturas", "Ocorrências": 6},
        {"Problema": "Mobiliário danificado", "Ocorrências": 6},
        {"Problema": "Infiltrações e goteiras", "Ocorrências": 5},
        {"Problema": "Falta de espaço físico", "Ocorrências": 4},
        {"Problema": "Falta de padronização", "Ocorrências": 4},
    ]

    df_top10 = pd.DataFrame(problemas_top10)

    # Gráfico de barras
    fig_top10 = px.bar(
        df_top10,
        x="Ocorrências",
        y="Problema",
        orientation='h',
        color_discrete_sequence=["#EF553B"]
    )
    st.plotly_chart(fig_top10, use_container_width=True)

    # Gráfico de pizza com os top 5
    df_top5 = df_top10.head(5)
    fig_pie = px.pie(
        df_top5,
        values="Ocorrências",
        names="Problema",
        title="Top 5 Problemas - Participação",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# --- ABA 4: Mapa ---
with tab4:
    st.subheader("🗘️ Mapa das Solicitações por Cidade")

    dados_mapa = df_filtrado.groupby(
        ["Cidade", "Latitude", "Longitude"], as_index=False)["Solicitações"].sum()

    fig_mapa = px.scatter_mapbox(
        dados_mapa,
        lat="Latitude",
        lon="Longitude",
        size="Solicitações",
        hover_name="Cidade",
        hover_data={"Solicitações": True,
                    "Latitude": False, "Longitude": False},
        zoom=6,
        size_max=30,
        color_discrete_sequence=["#636EFA"]
    )

    fig_mapa.update_layout(mapbox_style="open-street-map")
    fig_mapa.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    st.plotly_chart(fig_mapa, use_container_width=True)

# --- ABA 5: Download CSV filtrado ---
with tab5:
    st.subheader("📅 Baixar os dados filtrados")
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button("📅 Clique para baixar", csv,
                       "dados_filtrados.csv", "text/csv")
