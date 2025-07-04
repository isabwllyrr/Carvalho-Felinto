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

    if outros_sum > 0:
        df_final = pd.concat([top_n, pd.DataFrame(
            {coluna: ['Outros'], valor: [outros_sum]})], ignore_index=True)
    else:
        df_final = top_n

    return df_final


# Logo carvalho e felinto + PM
col1, col2 = st.columns(2)
with col1:
    st.image("logo_esquerda_.png", width=200)
with col2:
    st.image("logo_direita_.png", width=150)

st.title("📊 Painel Interativo - Solicitações de PDAs por Cidade e Área")

# Filtros
cidades = st.multiselect("Filtrar por cidade:",
                         df["Cidade"].unique(), default=df["Cidade"].unique())
pdas = st.multiselect("Filtrar por área temática (PDA):",
                      df["PDA"].unique(), default=df["PDA"].unique())

# Dados filtrados
df_filtrado = df[df["Cidade"].isin(cidades) & df["PDA"].isin(pdas)]

# Coordenadas manuais
df_coords = pd.DataFrame({
    'Cidade': ['Patos', 'Campina Grande', 'João Pessoa', 'Guarabira'],
    'Latitude': [-7.0172, -7.2306, -7.1195, -6.8506],
    'Longitude': [-37.2747, -35.8811, -34.8450, -35.4853]
})
df_filtrado = df_filtrado.merge(df_coords, on='Cidade', how='left')

# Abas de navegação
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Gráfico por PDA",
    "🌇️ Gráfico por Cidade",
    "📌 Problemas Mais Recorrentes",
    "🗸️ Mapa das Solicitações",
    "🗕️ Download"
])

# --- ABA 1 ---
with tab1:
    st.subheader("📊 Total de Solicitações por PDA")
    grafico_pda = df_filtrado.groupby("PDA", as_index=False)[
        "Solicitações"].sum().sort_values("Solicitações", ascending=False)
    fig1 = px.bar(grafico_pda, x="PDA", y="Solicitações",
                  color_discrete_sequence=["#1F4E79"])
    fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                       paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("🍩 Participação percentual Top 5 por PDA")
    grafico_pda_top5 = top_n_com_others(
        df_filtrado, "PDA", "Solicitações", n=5)
    fig_donut = px.pie(grafico_pda_top5, values='Solicitações', names='PDA', hole=0.5,
                       color_discrete_sequence=["#A0A0A0", "#555555", "#1F4E79", "#7B8DAB", "#B0BEC5"])
    fig_donut.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_donut, use_container_width=True)

# --- ABA 2 ---
with tab2:
    st.subheader("🌇️ Total de Solicitações por Cidade")
    grafico_cidade = df_filtrado.groupby("Cidade", as_index=False)[
        "Solicitações"].sum().sort_values("Solicitações", ascending=False)
    fig2 = px.bar(grafico_cidade, x="Cidade", y="Solicitações",
                  color_discrete_sequence=["#1F4E79"])
    fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                       paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("🍩 Participação percentual por Cidade")
    grafico_cidade_top4 = top_n_com_others(
        df_filtrado, "Cidade", "Solicitações", n=4)
    fig_donut_cidade = px.pie(grafico_cidade_top4, values='Solicitações', names='Cidade', hole=0.5,
                              color_discrete_sequence=["#A0A0A0", "#555555", "#1F4E79", "#7B8DAB"])
    fig_donut_cidade.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_donut_cidade, use_container_width=True)


# --- ABA 3: Problemas Mais Recorrentes ---
with tab3:
    st.subheader("📌 Problemas Mais Recorrentes (Top 10)")

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

    fig_top10 = px.bar(
        df_top10,
        x="Ocorrências",
        y="Problema",
        orientation='h',
        color_discrete_sequence=["#1F4E79"],  # azul escuro neutro
    )

    fig_top10.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title=None,
        yaxis_title=None,
    )

    st.plotly_chart(fig_top10, use_container_width=True)

    st.markdown("""
    <div style='padding: 10px; background-color: #F5F5F5; border-radius: 10px; font-size: 16px'>
        Os dados acima refletem os <b>principais problemas enfrentados pelas cidades</b> com base nas áreas temáticas priorizadas (PDAs).
        <br><br>
        <b>Baixo efetivo</b> e <b>infraestrutura precária</b> são, disparadamente, os problemas mais mencionados, representando juntos mais de 60% das ocorrências.
        <br><br>
        Esses indicadores podem auxiliar na <b>priorização de investimentos e políticas públicas</b> mais eficientes, voltadas para as reais demandas operacionais.
    </div>
    """, unsafe_allow_html=True)
# --- ABA 4 ---
with tab4:
    st.subheader("🗸️ Mapa das Solicitações por Cidade")
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
        color_discrete_sequence=["#1F4E79"]
    )
    fig_mapa.update_layout(mapbox_style="open-street-map")
    fig_mapa.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    st.plotly_chart(fig_mapa, use_container_width=True)

# --- ABA 5 ---
with tab5:
    st.subheader("🗕️ Baixar os dados filtrados")
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button("🗕️ Clique para baixar", csv,
                       "dados_filtrados.csv", "text/csv")
