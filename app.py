import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

st.set_page_config(layout="wide")

# Leitura dos dados
df = pd.read_csv("solicitacoes_pda_consolidadas.csv", encoding="utf-8")

# Filtros
st.sidebar.markdown("### 🎯 Filtros")
cidades = st.sidebar.multiselect(
    "Cidade:", df["Cidade"].unique(), default=df["Cidade"].unique())
pdas = st.sidebar.multiselect(
    "Área temática (PDA):", df["PDA"].unique(), default=df["PDA"].unique())
df_filtrado = df[df["Cidade"].isin(cidades) & df["PDA"].isin(pdas)]

# Coordenadas
df_coords = pd.DataFrame({
    'Cidade': ['Patos', 'Campina Grande', 'João Pessoa', 'Guarabira'],
    'Latitude': [-7.0172, -7.2306, -7.1195, -6.8506],
    'Longitude': [-37.2747, -35.8811, -34.8450, -35.4853]
})
df_filtrado = df_filtrado.merge(df_coords, on='Cidade', how='left')

# Carrega as imagens
logo_esquerda = Image.open("logo_esquerda_.png")
logo_direita = Image.open("logo_direita_.png")

# Cria colunas proporcionais e centraliza as logos na coluna do meio
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    col_logo1, col_logo2 = st.columns([1, 1])
    with col_logo1:
        st.image(logo_esquerda, width=350)
    with col_logo2:
        st.image(logo_direita, width=180)

# Título centralizado
st.markdown("<h2 style='text-align: center;'>Painel de Demandas Prioritárias - Cidades e PDAs</h2>",
            unsafe_allow_html=True)


# Cartões
total = df_filtrado["Solicitações"].sum()
cidade_top = df_filtrado.groupby("Cidade")["Solicitações"].sum().idxmax()
pda_top = df_filtrado.groupby("PDA")["Solicitações"].sum().idxmax()

col_card1, col_card2, col_card3 = st.columns(3)
with col_card1:
    st.markdown(f"""
        <div style='background-color:#1F4E79; padding:20px; border-radius:10px; text-align:center; color:white;'>
            <h1 style='font-size:28px; margin:0;'>{total}</h1>
            <p>Total de Solicitações</p>
        </div>
    """, unsafe_allow_html=True)
with col_card2:
    st.markdown(f"""
        <div style='background-color:#7B8DAB; padding:20px; border-radius:10px; text-align:center; color:white;'>
            <h1 style='font-size:28px; margin:0;'>{cidade_top}</h1>
            <p>Cidade com mais solicitações</p>
        </div>
    """, unsafe_allow_html=True)
with col_card3:
    st.markdown(f"""
        <div style='background-color:#A0A0A0; padding:20px; border-radius:10px; text-align:center; color:white;'>
            <h1 style='font-size:28px; margin:0;'>{pda_top}</h1>
            <p>PDA mais solicitado</p>
        </div>
    """, unsafe_allow_html=True)

# Gráficos linha 1
col1, col2 = st.columns(2)

with col1:
    df_pda = df_filtrado.groupby("PDA", as_index=False)[
        "Solicitações"].sum().sort_values("Solicitações", ascending=False)
    total_pda = df_pda["Solicitações"].sum()
    df_pda["%"] = df_pda["Solicitações"] / total_pda * 100
    df_pda["label"] = df_pda["%"].apply(lambda x: f"<b>{x:.1f}%</b>")

    fig_pda = px.bar(df_pda, x="PDA", y="Solicitações",
                     text="label", color_discrete_sequence=["#1F4E79"])
    fig_pda.update_traces(textposition='outside', textfont=dict(
        size=16, color='black', family='Arial Black'))
    fig_pda.update_layout(title="Solicitações por PDA",
                          showlegend=False, margin=dict(t=40))
    st.plotly_chart(fig_pda, use_container_width=True)

with col2:
    df_cidade = df_filtrado.groupby("Cidade", as_index=False)[
        "Solicitações"].sum()
    total_cidade = df_cidade["Solicitações"].sum()
    df_cidade["%"] = df_cidade["Solicitações"] / total_cidade * 100

    fig_cidade = px.pie(df_cidade, names="Cidade", values="Solicitações",
                        hole=0.5,
                        color_discrete_sequence=["#1F4E79", "#7B8DAB", "#A0A0A0", "#555555"])
    fig_cidade.update_traces(textposition='outside', textfont=dict(
        size=16, color="black", family="Arial Black"))
    fig_cidade.update_layout(title="Distribuição por Cidade")
    st.plotly_chart(fig_cidade, use_container_width=True)

# Gráficos linha 2
col3, col4 = st.columns(2)
with col3:
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
        {"Problema": "Falta de padronização", "Ocorrências": 4}
    ]
    df_prob = pd.DataFrame(problemas_top10)
    total_prob = df_prob["Ocorrências"].sum()
    df_prob["%"] = df_prob["Ocorrências"] / total_prob * 100
    df_prob["label"] = df_prob["%"].apply(lambda x: f"<b>{x:.1f}%</b>")

    fig_prob = px.bar(df_prob, x="Ocorrências", y="Problema", orientation="h", text="label",
                      color_discrete_sequence=["#1F4E79"])
    fig_prob.update_traces(textposition='outside', textfont=dict(
        size=16, color="black", family='Arial Black'))
    fig_prob.update_layout(title="Top 10 Problemas", showlegend=False)
    st.plotly_chart(fig_prob, use_container_width=True)

with col4:
    dados_mapa = df_filtrado.groupby(
        ["Cidade", "Latitude", "Longitude"], as_index=False)["Solicitações"].sum()
    fig_mapa = px.scatter_mapbox(dados_mapa, lat="Latitude", lon="Longitude", size="Solicitações",
                                 color="Cidade", size_max=30, zoom=6,
                                 color_discrete_sequence=["#1F4E79", "#7B8DAB", "#A0A0A0", "#555555"])
    fig_mapa.update_layout(mapbox_style="carto-positron",
                           margin={"r": 0, "t": 30, "l": 0, "b": 0})
    fig_mapa.update_layout(title="Mapa de Solicitações")
    st.plotly_chart(fig_mapa, use_container_width=True)

# Download
st.markdown("---")
st.download_button("🗕 Baixar dados filtrados", df_filtrado.to_csv(index=False).encode("utf-8"),
                   file_name="dados_filtrados.csv", mime="text/csv")
