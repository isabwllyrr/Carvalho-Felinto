import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

<<<<<<< HEAD
st.set_page_config(layout="wide")

# Leitura dos dados
df = pd.read_csv("solicitacoes_pda_consolidadas.csv", encoding="utf-8")

# Filtros
=======
# Layout horizontal (widescreen)
st.set_page_config(layout="wide")

# Upload do arquivo CSV
uploaded_file = st.sidebar.file_uploader(
    "📂 Envie o arquivo de dados (.csv)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.sidebar.warning("⚠️ Por favor, envie o arquivo para continuar.")
    st.stop()

# Função auxiliar para Top N + "Outros"


def top_n_com_others(df, coluna, valor, n=5):
    df_agg = df.groupby(coluna, as_index=False)[
        valor].sum().sort_values(valor, ascending=False)
    if len(df_agg) > n:
        top_n = df_agg.head(n)
        outros_sum = df_agg.iloc[n:][valor].sum()
        outros = pd.DataFrame({coluna: ['Outros'], valor: [outros_sum]})
        df_final = pd.concat([top_n, outros], ignore_index=True)
    else:
        df_final = df_agg
    return df_final


# Filtros na sidebar
>>>>>>> fb32da7459753c169e8356edbfa578040f441bf4
st.sidebar.markdown("### 🎯 Filtros")
cidades = st.sidebar.multiselect(
    "Cidade:", df["Cidade"].unique(), default=df["Cidade"].unique())
pdas = st.sidebar.multiselect(
    "Área temática (PDA):", df["PDA"].unique(), default=df["PDA"].unique())
<<<<<<< HEAD
df_filtrado = df[df["Cidade"].isin(cidades) & df["PDA"].isin(pdas)]

# Coordenadas
=======

# Aplicando filtros
df_filtrado = df[df["Cidade"].isin(cidades) & df["PDA"].isin(pdas)]

# Adicionando coordenadas das cidades
>>>>>>> fb32da7459753c169e8356edbfa578040f441bf4
df_coords = pd.DataFrame({
    'Cidade': ['Patos', 'Campina Grande', 'João Pessoa', 'Guarabira'],
    'Latitude': [-7.0172, -7.2306, -7.1195, -6.8506],
    'Longitude': [-37.2747, -35.8811, -34.8450, -35.4853]
})
df_filtrado = df_filtrado.merge(df_coords, on='Cidade', how='left')

<<<<<<< HEAD
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
=======
# Cabeçalho central com logos
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    logo_esq, logo_dir = st.columns([1, 1])
    with logo_esq:
        st.image("logo_esquerda_.png", width=250)
    with logo_dir:
        st.image("logo_direita_.png", width=150)

st.title("📊 Painel Interativo - Solicitações de PDAs por Cidade e Área")

# Abas
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Gráfico por PDA",
    "🌇️ Gráfico por Cidade",
    "📌 Problemas Mais Recorrentes",
    "🗸️ Mapa das Solicitações",
    "🗕️ Download"
])

# === ABA 1 ===
with tab1:
    st.subheader("📊 Total de Solicitações por PDA")
    grafico_pda = df_filtrado.groupby("PDA", as_index=False)[
        "Solicitações"].sum().sort_values("Solicitações", ascending=False)
    total_pda = grafico_pda["Solicitações"].sum()
    grafico_pda["Percentual"] = grafico_pda["Solicitações"] / total_pda * 100
    texto_pda = [f"{v:,}".replace(',', '.') + f" ({p:.1f}%)".replace('.', ',')
                 for v, p in zip(grafico_pda["Solicitações"], grafico_pda["Percentual"])]

    fig1 = px.bar(grafico_pda, x="PDA", y="Solicitações",
                  color_discrete_sequence=["#1F4E79"],
                  text=texto_pda)
    fig1.update_traces(textposition='outside',
                       textfont=dict(color='black', size=14, family='Arial Black'))
    fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                       paper_bgcolor='rgba(0,0,0,0)',
                       showlegend=False,
                       font=dict(color='black'),
                       xaxis=dict(showgrid=False),
                       yaxis=dict(showgrid=False))
    st.plotly_chart(fig1, use_container_width=True)

    grafico_pda_top5 = top_n_com_others(
        df_filtrado, "PDA", "Solicitações", n=5)
    fig_donut = px.pie(grafico_pda_top5, values='Solicitações', names='PDA', hole=0.5,
                       color_discrete_sequence=["#A0A0A0", "#555555", "#1F4E79", "#7B8DAB", "#B0BEC5"])
    fig_donut.update_traces(textposition='outside',
                            textfont=dict(color='black', size=14, family='Arial Black'))
    fig_donut.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='black'),
                            showlegend=True)
    st.plotly_chart(fig_donut, use_container_width=True)

# === ABA 2 ===
with tab2:
    st.subheader("🌇️ Total de Solicitações por Cidade")
    grafico_cidade = df_filtrado.groupby("Cidade", as_index=False)[
        "Solicitações"].sum().sort_values("Solicitações", ascending=False)
    total_cidade = grafico_cidade["Solicitações"].sum()
    grafico_cidade["Percentual"] = grafico_cidade["Solicitações"] / \
        total_cidade * 100
    texto_cidade = [f"{v:,}".replace(',', '.') + f" ({p:.1f}%)".replace('.', ',')
                    for v, p in zip(grafico_cidade["Solicitações"], grafico_cidade["Percentual"])]

    fig2 = px.bar(grafico_cidade, x="Cidade", y="Solicitações",
                  color_discrete_sequence=["#1F4E79"],
                  text=texto_cidade)
    fig2.update_traces(textposition='outside',
                       textfont=dict(color='black', size=14, family='Arial Black'))
    fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                       paper_bgcolor='rgba(0,0,0,0)',
                       showlegend=False,
                       font=dict(color='black'),
                       xaxis=dict(showgrid=False),
                       yaxis=dict(showgrid=False))
    st.plotly_chart(fig2, use_container_width=True)

    grafico_cidade_top4 = top_n_com_others(
        df_filtrado, "Cidade", "Solicitações", n=4)
    fig_donut_cidade = px.pie(grafico_cidade_top4, values='Solicitações', names='Cidade', hole=0.5,
                              color_discrete_sequence=["#A0A0A0", "#555555", "#1F4E79", "#7B8DAB"])
    fig_donut_cidade.update_traces(textposition='outside',
                                   textfont=dict(color='black', size=14, family='Arial Black'))
    fig_donut_cidade.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                                   paper_bgcolor='rgba(0,0,0,0)',
                                   font=dict(color='black'),
                                   showlegend=True)
    st.plotly_chart(fig_donut_cidade, use_container_width=True)

# === ABA 3 ===
with tab3:
    st.subheader("📌 Problemas Mais Recorrentes (Top 10)")
>>>>>>> fb32da7459753c169e8356edbfa578040f441bf4
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
<<<<<<< HEAD
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
=======
    df_top10 = pd.DataFrame(problemas_top10)
    total = df_top10["Ocorrências"].sum()
    df_top10["Percentual"] = df_top10["Ocorrências"] / total * 100
    texto_top10 = [f"{v} ({p:.1f}%)".replace('.', ',') for v, p in zip(
        df_top10["Ocorrências"], df_top10["Percentual"])]

    fig_top10 = px.bar(df_top10, x="Ocorrências", y="Problema", orientation='h',
                       color_discrete_sequence=["#1F4E79"],
                       text=texto_top10)
    fig_top10.update_traces(textposition='outside',
                            textfont=dict(color='black', size=14, family='Arial Black'))
    fig_top10.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='black'),
                            xaxis=dict(showgrid=False),
                            yaxis=dict(showgrid=False),
                            xaxis_title=None,
                            yaxis_title=None)
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

# === ABA 4 ===
with tab4:
    st.subheader("🗸️ Mapa das Solicitações por Cidade")
    dados_mapa = df_filtrado.groupby(
        ["Cidade", "Latitude", "Longitude"], as_index=False)["Solicitações"].sum()
    fig_mapa = px.scatter_mapbox(dados_mapa, lat="Latitude", lon="Longitude",
                                 size="Solicitações", size_max=30,
                                 hover_name="Cidade",
                                 hover_data={"Solicitações": True,
                                             "Latitude": False, "Longitude": False},
                                 zoom=6,
                                 color_discrete_sequence=["#1F4E79"])
    fig_mapa.update_layout(mapbox_style="open-street-map",
                           margin={"r": 0, "t": 0, "l": 0, "b": 0})
    st.plotly_chart(fig_mapa, use_container_width=True)

    st.markdown("""
    <div style='padding: 10px; background-color: #F5F5F5; border-radius: 10px; font-size: 16px'>
        O mapa acima ilustra a distribuição geográfica das <b>solicitações por cidade</b>, onde o tamanho dos círculos representa o volume de registros em cada localidade.
        <br><br>
        <b>Patos</b> se destaca como o município com o maior número de solicitações (<b>89 no total</b>), evidenciando uma demanda significativamente maior em relação às demais cidades.
        <br><br>
        Veja abaixo os números por cidade:
        <ul>
            <li><b>Patos:</b> 89 solicitações</li>
            <li><b>Campina Grande:</b> 74 solicitações</li>
            <li><b>João Pessoa:</b> 40 solicitações</li>
            <li><b>Guarabira:</b> 34 solicitações</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# === ABA 5 ===
with tab5:
    st.subheader("🗕️ Baixar os dados filtrados")
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button("🗕️ Clique para baixar", csv,
                       "dados_filtrados.csv", "text/csv")
>>>>>>> fb32da7459753c169e8356edbfa578040f441bf4
