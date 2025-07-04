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
    st.image("logo_direita_.png", width=200)

with col2:
    st.image("logo_esquerda_.png", width=200)

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

# Aba
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Gráfico por PDA",
    "🏙️ Gráfico por Cidade",
    "📋 Dados Completos",
    "🧭 Problemas por Cidade e Área",
    "📌 Problemas Mais Recorrentes",
    "📥 Download",
    "🗺️ Mapa das Solicitações"
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

# --- ABA 3: Tabela de dados ---
with tab3:
    st.subheader("📋 Tabela de Dados Filtrados")
    st.dataframe(df_filtrado, use_container_width=True)

# --- PROBLEMAS MANUAIS POR CIDADE/PDA ---
problemas = [
    {"Cidade": "Patos", "PDA": "Gestão de Pessoas",
        "Problema": "Efetivo escasso, insatisfação com salários, falta de motivação, ausência de capacitação"},
    {"Cidade": "Patos", "PDA": "Engenharia",
        "Problema": "Alojamento precário, sede sem estrutura, infiltrações, instalações elétricas ruins, sem espaço para práticas esportivas"},
    {"Cidade": "Patos", "PDA": "Tecnologia da Informação",
        "Problema": "Necessidade de novos computadores e impressoras, novos recursos tecnológicos para maximizar a produtividade"},
    {"Cidade": "Patos", "PDA": "Saúde",
        "Problema": "Ampliação dos serviços de saúde para o PM e sua família, serviço de acolhimento psicoterapêutico"},
    {"Cidade": "Patos", "PDA": "Materiais e Patrimônio",
        "Problema": "Falta de mobiliário adequado e manutenção predial"},

    {"Cidade": "Campina Grande", "PDA": "Gestão de Pessoas",
        "Problema": "Baixo salário, sobrecarga de trabalho, idade avançada dos efetivos"},
    {"Cidade": "Campina Grande", "PDA": "Engenharia",
        "Problema": "Necessidade de construção de unidade, infiltrações, manutenção predial"},
    {"Cidade": "Campina Grande", "PDA": "Tecnologia da Informação",
        "Problema": "Equipamentos obsoletos e falta de TI"},
    {"Cidade": "Campina Grande", "PDA": "Saúde",
        "Problema": "Falta de estrutura adequada para atendimento médico"},
    {"Cidade": "Campina Grande", "PDA": "Materiais e Patrimônio",
        "Problema": "Defasagem no controle de patrimônio e estoque"},

    {"Cidade": "João Pessoa", "PDA": "Gestão de Pessoas",
        "Problema": "Déficit de efetivo, redistribuição necessária, ausência de incentivo"},
    {"Cidade": "João Pessoa", "PDA": "Engenharia",
        "Problema": "Reformas urgentes, infiltrações, construção de alojamento e presídio"},
    {"Cidade": "João Pessoa", "PDA": "Tecnologia da Informação",
        "Problema": "Falta de suporte técnico e equipamentos desatualizados"},
    {"Cidade": "João Pessoa", "PDA": "Processos e Normas",
        "Problema": "Necessidade de atualização e padronização de normas internas"},
    {"Cidade": "João Pessoa", "PDA": "Materiais e Patrimônio",
        "Problema": "Infraestrutura inadequada e controle patrimonial falho"},

    {"Cidade": "Guarabira", "PDA": "Gestão de Pessoas",
        "Problema": "Falta de efetivo, ausência de plano de carreira e motivação baixa"},
    {"Cidade": "Guarabira", "PDA": "Engenharia",
        "Problema": "Falta de manutenção predial, infiltrações, sede com problemas estruturais"},
    {"Cidade": "Guarabira", "PDA": "Tecnologia da Informação",
        "Problema": "Carência de computadores e rede instável"},
    {"Cidade": "Guarabira", "PDA": "Processos e Normas",
        "Problema": "Desorganização documental e ausência de fluxos claros"},
    {"Cidade": "Guarabira", "PDA": "Materiais e Patrimônio",
        "Problema": "Móveis deteriorados, controle ineficaz de estoque"},
]

df_problemas = pd.DataFrame(problemas)

# --- ABA 4: Problemas por Cidade e Área ---
with tab4:
    st.subheader("🧭 Problemas por Cidade e Área")

    with st.container(border=True):
        st.markdown("### 🎯 Filtros")
        cidades_prob = st.multiselect("Selecione a cidade:", df_problemas["Cidade"].unique(
        ), default=df_problemas["Cidade"].unique())
        pdas_prob = st.multiselect("Selecione a área temática (PDA):", df_problemas["PDA"].unique(
        ), default=df_problemas["PDA"].unique())

        df_prob_filtrado = df_problemas[df_problemas["Cidade"].isin(
            cidades_prob) & df_problemas["PDA"].isin(pdas_prob)]

    with st.container(border=True):
        st.markdown("### 📋 Tabela de Problemas")
        st.data_editor(df_prob_filtrado, use_container_width=True,
                       disabled=True, height=400)

# --- ABA 5: Problemas Mais Recorrentes ---
with tab5:
    st.subheader("📌 Problemas Mais Recorrentes")
    todas = df_problemas["Problema"].str.lower().str.split(", ")
    plano = pd.Series([item for sublist in todas for item in sublist])
    top = plano.value_counts().reset_index()
    top.columns = ["Problema recorrente", "Ocorrências"]
    st.dataframe(top, use_container_width=True)

# --- ABA 6: Download CSV filtrado ---
with tab6:
    st.subheader("📥 Baixar os dados filtrados")
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Clique para baixar", csv,
                       "dados_filtrados.csv", "text/csv")

with tab7:
    st.subheader("🗺️ Mapa das Solicitações por Cidade")

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
