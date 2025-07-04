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
        "Problema": "Efetivo escasso, insatisfação com salários, falta de motivação, ausência de capacitação, criação de ajuda de custo, treinamento com material bélico, dificuldade em atender as diversas modalidades de policiamento, limpeza e água para consumo dos policiais"},
    {"Cidade": "Patos", "PDA": "Engenharia",
        "Problema": "Alojamento precário, sede sem estrutura, infiltrações, instalações elétricas ruins, sem espaço para práticas esportivas, construção de pátios para depósitos de veículos, manutenção de material, pavimentação, criação de secretaria"},
    {"Cidade": "Patos", "PDA": "Tecnologia da Informação",
        "Problema": "Necessidade de novos computadores, impressoras novas, novos recursos tecnológicos para maximizar a produtividade"},
    {"Cidade": "Patos", "PDA": "Saúde",
        "Problema": "Ampliação dos serviços de saúde para o PM e sua família, serviço de acolhimento psicoterapêutico"},
    {"Cidade": "Patos", "PDA": "Materiais e Patrimônio",
        "Problema": "Falta de mobiliário adequado, viaturas com xadrez. ar-condicionado, motocicletas para mobilidade nas fiscalizações"},

    {"Cidade": "Campina Grande", "PDA": "Gestão de Pessoas",
        "Problema": "insatisfação com salários, efetivo escasso, grande demanda de serviços, investir em planos de carreira, idade avançada dos efetivos, treinamento com material bélico, permitir que os PM´s formados em direito assessorem os militares que respondem judicialmente, terceirizar serviço de limpeza, implementar formação contínua para os soldados, verba para custeio de despesas mensais recorrentes"},
    {"Cidade": "Campina Grande", "PDA": "Engenharia",
        "Problema": "sede sem estrutura, construção de uma nova unidade que comporte a força tática, calçamento e asfaltamento dos estacionamentos, infiltrações, falta de reboque para condução de veículos apreendidos, coletes com apetrechos pagos pelo estado, sem espaço para atividades físicas, criação de um canil"},
    {"Cidade": "Campina Grande", "PDA": "Tecnologia da Informação",
        "Problema": "Necessidade de novos computadores, dados migrados incompletos"},
    {"Cidade": "Campina Grande", "PDA": "Saúde",
        "Problema": "Falta de estrutura adequada para atendimento médico"},
    {"Cidade": "Campina Grande", "PDA": "Materiais e Patrimônio",
        "Problema": "viaturas com xadrez, falta de utensílios eletrodométiscos, kit de aquisição APH, novos móveis, caminhão prancha"},

    {"Cidade": "João Pessoa", "PDA": "Gestão de Pessoas",
        "Problema": "Terceirizar serviços de limpeza, mais coordenadores da integração comunitária, ampliação da terceirização dos seviços gerais, ausência de capacitação, treinamento com material bélico, efetivo escasso, valorização de repressão afetando as prioridades da gestão, colocar os oficiais do CFO em comando, insuficiência de recursos extras, falta de motivação, plano de estruturação das mulheres, redistribuição dos oficiais de maneira estratégica"},
    {"Cidade": "João Pessoa", "PDA": "Engenharia",
        "Problema": "Construção do presídio militar, restauração dos muros dos batalhões, construção de um hospital da PM, construção de um colégio militar no sertão, infiltrações, paredes mofadas, alojamento precário, construção de mais salas, construção de coberturas para proteção de viatura, pinturas dos setores dos batalhões, reforma nos banheiros, construção de alojamentos femininos"},
    {"Cidade": "João Pessoa", "PDA": "Tecnologia da Informação",
        "Problema": "Necessidade de novos computadores, computadores obsoletos, impressoras novas"},
    {"Cidade": "João Pessoa", "PDA": "Processos e Normas",
        "Problema": "Aplicação de rotinas de policiamento, projeto para regulamenação de carga horária, transparência no processo de planejamento das criações de batalhões"},
    {"Cidade": "João Pessoa", "PDA": "Materiais e Patrimônio",
        "Problema": "Viaturas com xadrez, blindagem das viaturas, investir em pneus que não estourem, viaturas focadas em áreas rurais, novos móveis"},

    {"Cidade": "Guarabira", "PDA": "Gestão de Pessoas",
        "Problema": "Efetivo escasso, preparação de programa que vise orientar e preparar psicologicamente o militar que está indo para reserva, oficiais de curso não tem garantia de atingir a plenitude, treinamento com material bélico"},
    {"Cidade": "Guarabira", "PDA": "Engenharia",
        "Problema": "Sem espaço para atividades físicas, sede sem estrutura, construção de stand de tiro, construção de alojamentos femininos, contratação do serviço de manutenção diária, alojamento precário"},
    {"Cidade": "Guarabira", "PDA": "Tecnologia da Informação",
        "Problema": "Aquisição de armazenamento em nuvem, necessidade de novos computadores, sistema integrado de informações, sistema de armaria eletrônico"},
    {"Cidade": "Guarabira", "PDA": "Processos e Normas",
        "Problema": "Avaço no arcabouço legislativo, reformulação no processo gerencial e decisório, melhorar a definição de atribuição dos oficiais, ampliar o setor de manutenção, implementar uma operação em conjunto com outros órgãos operativos"},
    {"Cidade": "Guarabira", "PDA": "Materiais e Patrimônio",
        "Problema": "Novos móveis, aquisição de materiais para o setor administrativo, viaturas com xadrez, solicitação de datashow, tela de projeção, caixa de som acústica, microfone sem fio"},
    {"Cidade": "Guarabira", "PDA": "Saúde",
        "Problema": "Plano de saúde que seja atendido em todo o Estado"},
    {"Cidade": "Guarabira", "PDA": "Material Bélico",
        "Problema": "Necessidade de mais munição dos cal"}
]

df_problemas = pd.DataFrame(problemas)

# --- ABA 4: Problemas por Cidade e Área ---
with tab4:
    st.subheader("🧭 Problemas por Cidade e Área")

    cidades_unicas = df_problemas["Cidade"].unique()

    for cidade in cidades_unicas:
        st.markdown(f"### 📍 {cidade}")
        df_cidade = df_problemas[df_problemas["Cidade"] == cidade]

        for _, linha in df_cidade.iterrows():
            st.markdown(f"""
            <div style="background-color:#f0f2f6; padding: 12px; border-radius: 10px; margin-bottom:10px;">
                <strong>🗂️ {linha['PDA']}</strong><br>
                {linha['Problema']}
            </div>
            """, unsafe_allow_html=True)


# --- ABA 5: Problemas Mais Recorrentes ---
with tab5:
    st.subheader("📌 Problemas Mais Recorrentes")

    # Divide os problemas em frases separadas
    todas = df_problemas["Problema"].str.lower().str.split(", ")
    plano = pd.Series([item.strip() for sublist in todas for item in sublist])
    top = plano.value_counts().reset_index()
    top.columns = ["Problema recorrente", "Ocorrências"]

    for _, row in top.iterrows():
        st.markdown(f"""
        <div style="background-color:#e6f7ff; padding: 10px; border-left: 6px solid #1890ff; margin-bottom:8px; border-radius:5px">
            <strong>🔹 {row['Problema recorrente'].capitalize()}</strong><br>
            Ocorrências: {row['Ocorrências']}
        </div>
        """, unsafe_allow_html=True)

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
