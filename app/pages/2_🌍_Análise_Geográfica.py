import streamlit as st
import plotly.express as px
import pandas as pd
import folium
import time
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import streamlit_shadcn_ui as ui

# Define o layout da página
st.set_page_config(
    page_title="Analise Geográfica",
    page_icon="🌍", 
    initial_sidebar_state="expanded",
    layout="wide"
)

# Carregar os dados do estado da sessão
df = st.session_state["data"]
df = df.loc[df['CIDADE'] == "GUARULHOS"]

# Setar título
st.markdown("""
    <style>
        .rounded-title {
            text-align: center; 
            font-size: 40px;
        }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='rounded-title'>Análise Geográfica</h1><br>", unsafe_allow_html=True)

# ------------------------------------------------------------ CONFIGURAÇÕES DE FILTROS ---------------------------------------- # 

# Setar título
st.write('Os filtros se aplicam a todos os gráficos da página.')

# Adicionar um seletor de ano, mês, tipo de veículo e marca para furtos acima do gráfico
col1, col2, col3 = st.columns(3)
anos_disponiveis_furtos = [2023, 2024]
meses_disponiveis = ["Todos os Meses", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
tipo_ocorrencia = ['Todas as Ocorrências'] + df['DESCR_OCORRENCIA_VEICULO'].unique().tolist()
tipos_veiculos = ['Todos os Tipos'] + df['DESCR_TIPO_VEICULO'].unique().tolist()
marcas = ['Todas as Marcas'] + df['DESCR_MARCA_VEICULO'].unique().tolist()

# Selectbox 
with col1:
    ano_selecionado = st.selectbox('Ano', anos_disponiveis_furtos)
    bairro_selecionado = st.selectbox('Selecionar Bairro', ['Todos os Bairros'] + df['BAIRRO'].unique().tolist())
with col2:
    mes_selecionado = st.selectbox('Mês', meses_disponiveis)
    tipo_veiculo_selecionado = st.selectbox('Tipo Veículo', tipos_veiculos)
with col3:
    tipo_selecionado = st.selectbox('Tipo Ocorrência', tipo_ocorrencia)
    marca_selecionada = st.selectbox('Marca/Modelo', marcas)


# Filtrar os dados pelo ano, mês selecionado, tipo de ocorrência, tipo de veículo e marca
df['DATA_OCORRENCIA_BO'] = pd.to_datetime(df['DATA_OCORRENCIA_BO'])
df_atual = df[df['DATA_OCORRENCIA_BO'].dt.year == ano_selecionado]

if mes_selecionado != "Todos os Meses":
    mes_index = meses_disponiveis.index(mes_selecionado)
    df_atual = df_atual[df_atual['DATA_OCORRENCIA_BO'].dt.month == mes_index]

if tipo_selecionado != 'Todas as Ocorrências':
    df_atual = df_atual[df_atual['DESCR_OCORRENCIA_VEICULO'] == tipo_selecionado]

if bairro_selecionado != 'Todos os Bairros':
    df_atual = df_atual[df_atual['BAIRRO'] == bairro_selecionado]

if tipo_veiculo_selecionado != 'Todos os Tipos':
    df_atual = df_atual[df_atual['DESCR_TIPO_VEICULO'] == tipo_veiculo_selecionado]

if marca_selecionada != 'Todas as Marcas':
    df_atual = df_atual[df_atual['DESCR_MARCA_VEICULO'] == marca_selecionada]

# Calcular o delta percentual comparado ao mesmo período do ano anterior
if ano_selecionado == 2023:
    delta = None
else:
    df_anterior = df[df['DATA_OCORRENCIA_BO'].dt.year == (ano_selecionado - 1)]
    if mes_selecionado != "Todos os Meses":
        df_anterior = df_anterior[df_anterior['DATA_OCORRENCIA_BO'].dt.month == mes_index]

    if tipo_selecionado != 'Todas as Ocorrências':
        df_anterior = df_anterior[df_anterior['DESCR_OCORRENCIA_VEICULO'] == tipo_selecionado]

    if bairro_selecionado != 'Todos os Bairros':
        df_anterior = df_anterior[df_anterior['BAIRRO'] == bairro_selecionado]

    if tipo_veiculo_selecionado != 'Todos os Tipos':
        df_anterior = df_anterior[df_anterior['DESCR_TIPO_VEICULO'] == tipo_veiculo_selecionado]

    if marca_selecionada != 'Todas as Marcas':
        df_anterior = df_anterior[df_anterior['DESCR_MARCA_VEICULO'] == marca_selecionada]

    total_atual = len(df_atual)
    total_anterior = len(df_anterior)

    if total_anterior > 0:
        delta = ((total_atual - total_anterior) / total_anterior) * 100
    else:
        delta = None

# ------------------------------------------------------------ CONFIGURAÇÕES DE CARDS ---------------------------------------- # 
if delta != None:
    st.write(f":red[Dados de 2024 até {df['DATA_OCORRENCIA_BO'].max().strftime('%d-%m-%Y')}]", unsafe_allow_html=True)
    text = "Comparado ao mesmo preiodo do ano Anterior"
else:
    ""

st.header('Distribuição de Ocorrências por Bairro', divider='rainbow')

col1 = st.columns(3)
with col1[0]:
    st.metric(
        label=f"Total de Ocorrências | {tipo_selecionado}", 
        value=len(df_atual), 
        delta=f"{delta:.2f}% {text}"  if isinstance(delta, float) else delta  ,
        delta_color="inverse"
    )

# ------------------------------------------------------------ CONFIGURAÇÕES DO GRAFICOS ---------------------------------------- # 
# Calcula contagem por bairro
furtos_por_bairro = df_atual['BAIRRO'].value_counts().head(20).reset_index()
furtos_por_bairro.columns = ['BAIRRO', 'NUMERO_DE_FURTOS']
furtos_por_bairro['BAIRRO'] = furtos_por_bairro['BAIRRO'].replace("nan", "NÃO INFORMADO")

# # título do gráfico com base nos filtros
# titulo_grafico = f'Ocorrências de Veículos em {ano_selecionado} - {mes_selecionado}'
# if tipo_selecionado != 'Todas as Ocorrências':
#     titulo_grafico += f' | Tipo: {tipo_selecionado}'
# if tipo_veiculo_selecionado != 'Todos os Tipos':
#     titulo_grafico += f' | Tipo de Veículo: {tipo_veiculo_selecionado}'
# if marca_selecionada != 'Todas as Marcas':
#     titulo_grafico += f' | Marca/Modelo: {marca_selecionada}'
# if bairro_selecionado != 'Todos os Bairros':
#     titulo_grafico += f' | Bairro: {bairro_selecionado}'

if mes_selecionado == 'Todos os Meses':
    title = f'Top 20 Bairros com mais Ocorrências em {ano_selecionado}'
else:
    title = f'Top 20 Bairros com mais Ocorrências em {mes_selecionado} de {ano_selecionado}'

# Plotar o gráfico com Plotly para furtos
fig_furtos = px.bar(
    furtos_por_bairro,
    x='BAIRRO',
    y='NUMERO_DE_FURTOS',
    title=title,
    labels={'BAIRRO': 'Bairro', 'NUMERO_DE_FURTOS': 'Número de Ocorrências'},
    color='NUMERO_DE_FURTOS',
    color_continuous_scale='bluered',
    text='NUMERO_DE_FURTOS'
)

fig_furtos.update_layout(
    width=1700,
    height=600,
    title_x=0.2,
    xaxis_title='Bairro',
    yaxis_title='Número de Ocorrências',
    title_font=dict(size=26)
)

# Ajustar a posição dos rótulos dos valores para furtos
fig_furtos.update_traces(texttemplate='%{text}', textposition='outside')

# Exibir o gráfico no Streamlit para furtos
st.plotly_chart(fig_furtos)

# ------------------------------------------------------------ MAPA ----------------------------------------#

# Função para criar e atualizar 
def criar_mapa(df):
    st.header('Mapa de Ocorrências na cidade de Guarulhos-SP',divider='rainbow')
    st.write("Click para expandir as ocorrências. Ao expandir click no ícone do carro para ver informações.")

    with st.spinner('Aguarde, carregando...'):
        time.sleep(40)

    # Setando configurações iniciais do mapa
    mapa = folium.Map(location=[-23.42952840511497, -46.476692195126226], zoom_start=12, tiles='OpenStreetMap', alpha=0)
    df_local_roubos = df.copy()
    df_local_roubos = df_local_roubos.dropna()
    df_local_roubos['DATA_OCORRENCIA_BO'] = df_local_roubos['DATA_OCORRENCIA_BO'].dt.date

    # Atribuindo nome do marcador
    cluster = MarkerCluster(name='Carros Roubados')

    for _, row in df_local_roubos.iterrows():
        popup_html = f"""
            <b>TIPO VEICULO:</b> {row['DESCR_TIPO_VEICULO']}<br>
            <b>MODELO:</b> {row['DESCR_MARCA_VEICULO']}<br>
            <b>PLACA:</b> {row['PLACA_VEICULO']}<br>
            <b>TIPO OCORRÊNCIA:</b> {row['DESCR_OCORRENCIA_VEICULO']}<br>
            <b>DATA OCORRÊNCIA:</b> {row['DATA_OCORRENCIA_BO']}
        """
        folium.Marker(
            location=[row['LATITUDE'], row['LONGITUDE']],
            popup=folium.Popup(html=popup_html, max_width=300),  # Aumenta o tamanho do popup
            icon=folium.Icon(color='red', prefix='fa', icon='fas fa-car'),
            tooltip=row['BAIRRO']
        ).add_to(cluster)

    cluster.add_to(mapa)

    folium_static(mapa, width=1150, height=600)

# Chamar a função para criar o mapa
criar_mapa(df_atual)
