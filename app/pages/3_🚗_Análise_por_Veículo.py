import streamlit as st
import plotly.express as px
import pandas as pd

# Define o layout da página
st.set_page_config(
    page_title="Análise por Veículos",
    page_icon="🚗", 
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

st.markdown("<h1 class='rounded-title'>Análise de Ocorrência por Veículos</h1><br>", unsafe_allow_html=True)

# ------------------------------------------------------------ CONFIGURAÇÕES DE FILTROS ---------------------------------------- # 
anos_disponiveis_furtos = [2023, 2024]
tipos_veiculos = ['Todos os Tipos'] + df['DESCR_TIPO_VEICULO'].unique().tolist()
marcas = ['Todas as Marcas'] + df['DESCR_MARCA_VEICULO'].unique().tolist()
meses_disponiveis = ["Todos os Meses", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
tipo_ocorrencia = ['Todas as Ocorrências'] + df['DESCR_OCORRENCIA_VEICULO'].unique().tolist()

# Setar título
st.write('Os filtros se aplicam a todos os gráficos da página.')

# Layout dos filtros
col1, col2, col3 = st.columns(3)

# Selectbox para o ano e bairro
with col1:
    ano_selecionado = st.selectbox('Ano', anos_disponiveis_furtos)
    bairro_selecionado = st.selectbox('Selecionar Bairro', ['Todos os Bairros'] + df['BAIRRO'].unique().tolist())

# Selectbox para mês e tipo de veículo
with col2:
    mes_selecionado = st.selectbox('Mês', meses_disponiveis)
    tipo_veiculo_selecionado = st.selectbox('Tipo Veículo', tipos_veiculos)

# Selectbox para tipo de ocorrência e marca
with col3:
    tipo_selecionado = st.selectbox('Tipo Ocorrência', tipo_ocorrencia)
    marca_selecionada = st.selectbox('Marca/Modelo', marcas)


# Filtrar os dados com base nos filtros selecionados
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

st.header('Analises de Ocorrências', divider='rainbow')

st.metric(
    label=f"Total de Ocorrências | {tipo_selecionado}", 
    value=len(df_atual), 
    delta=f"{delta:.2f}% {text}"  if isinstance(delta, float) else delta  ,
    delta_color="inverse"
)

# ------------------------------------------------------------ CONFIGURAÇÕES DO GRAFICO (Distribuição de Ocorrências por Tipo de Veículos) ---------------------------------------- # 

# # Construção do título do gráfico
# titulo_grafico = f'Ocorrências de Veículos em {mes_selecionado} de {ano_selecionado}'
# if tipo_selecionado != 'Todas as Ocorrências':
#     titulo_grafico += f' | Tipo: {tipo_selecionado}'
# if tipo_veiculo_selecionado != 'Todos os Tipos':
#     titulo_grafico += f' | Tipo de Veículo: {tipo_veiculo_selecionado}'
# if marca_selecionada != 'Todas as Marcas':
#     titulo_grafico += f' | Marca: {marca_selecionada}'
# if bairro_selecionado != 'Todos os Bairros':
#     titulo_grafico += f' | Bairro: {bairro_selecionado}'

col1, col2 = st.columns([2, 2])

with col1:

    # ------------------------------------------------------------------------- Ocorrências por Tipo de Veículo --------------------------- #

    # Cálculo de ocorrências por tipo de veículo
    furtos_por_tipos_veiculos = df_atual['DESCR_TIPO_VEICULO'].value_counts().head(30).reset_index()
    furtos_por_tipos_veiculos.columns = ['DESCR_TIPO_VEICULO', 'NUMERO_DE_FURTOS']

    if mes_selecionado == 'Todos os Meses':
        title = f'Ocorrências por Tipo de Veículo em {ano_selecionado}'
    else:
        title = f'Ocorrências por Tipo de Veículo em {mes_selecionado} de {ano_selecionado}'

    # Plotar o gráfico de barras com Plotly (barras horizontais)
    fig_furtos_tipo_veiculo = px.bar(
        furtos_por_tipos_veiculos,
        x='NUMERO_DE_FURTOS',  
        y='DESCR_TIPO_VEICULO', 
        title=title,
        labels={'DESCR_TIPO_VEICULO': 'Tipo de Veículo', 'NUMERO_DE_FURTOS': 'Número de Ocorrências'},
        color='NUMERO_DE_FURTOS', 
        color_continuous_scale='bluered',  
        text='NUMERO_DE_FURTOS',  
        orientation='h'
    )

    fig_furtos_tipo_veiculo.update_layout(
        width=1500,
        height=600,
        xaxis_title='Número de Ocorrências',
        yaxis_title='Tipo de Veículo',
        title_font=dict(size=18),
        xaxis_tickangle=0,  
        xaxis_tickmode='array', 
        yaxis={'categoryorder':'total ascending'}  
    )

    fig_furtos_tipo_veiculo.update_xaxes(visible=False)

    # Ajustar a posição dos rótulos dos valores para furtos
    fig_furtos_tipo_veiculo.update_traces(texttemplate='%{text}', textposition='auto')
    #fig_furtos_tipo_veiculo.update_yaxes(range=[0, furtos_por_tipos_veiculos['NUMERO_DE_FURTOS'].max() * 1.1])  # Ajuste do intervalo do eixo y

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig_furtos_tipo_veiculo)

with col2:
    # ------------------------------------------------------------------------- Ocorrências por Marca --------------------------- #

    # Cálculo de ocorrências por marca/modelo
    furtos_por_marca = df_atual['DESCR_MARCA_VEICULO'].value_counts().head(10).reset_index()
    furtos_por_marca.columns = ['DESCR_MARCA_VEICULO', 'NUMERO_DE_FURTOS']

    # # Plotar o gráfico de barras com Plotly
    # fig_furtos_marca = px.bar(
    #     furtos_por_marca,
    #     x='DESCR_MARCA_VEICULO',
    #     y='NUMERO_DE_FURTOS',
    #     title=f'Top 10 Ocorrências por Marca/Modelo em {mes_selecionado} de {ano_selecionado}',
    #     labels={'DESCR_MARCA_VEICULO': 'Marca/Modelo', 'NUMERO_DE_FURTOS': 'Número de Ocorrências'},
    #     color='NUMERO_DE_FURTOS',
    #     color_continuous_scale='cividis',
    #     text='NUMERO_DE_FURTOS'
    # )

    # fig_furtos_marca.update_layout(
    #     width=1700,
    #     height=600,
    #     title_x=0.2,
    #     xaxis_title='Marca/Modelo',
    #     yaxis_title='Número de Ocorrências',
    #     title_font=dict(size=26),
    #     xaxis_tickangle=0,
    #     xaxis_tickmode='array',
    #     xaxis_tickvals=furtos_por_marca['DESCR_MARCA_VEICULO'],
    #     xaxis_ticktext=[text[:10] + '<br>' + text[10:] if len(text) > 10 else text for text in furtos_por_marca['DESCR_MARCA_VEICULO']]  # Quebrar texto
    # )

    # # Ajustar a posição dos rótulos dos valores para furtos
    # fig_furtos_marca.update_traces(texttemplate='%{text}', textposition='outside')
    # fig_furtos_marca.update_yaxes(range=[0, furtos_por_marca['NUMERO_DE_FURTOS'].max() * 1.1])  # Ajuste do intervalo do eixo y

    # # Exibir o gráfico no Streamlit
    # st.plotly_chart(fig_furtos_marca)

    # Plotar o gráfico de barras com Plotly (barras horizontais)
    fig_furtos_marca = px.bar(
        furtos_por_marca,
        y='DESCR_MARCA_VEICULO',  
        x='NUMERO_DE_FURTOS',  
        title=f'Top 10 Marca/Modelo com mais Ocorrências em {mes_selecionado} de {ano_selecionado}',
        labels={'DESCR_MARCA_VEICULO': 'Marca/Modelo', 'NUMERO_DE_FURTOS': 'Número de Ocorrências'},
        color='NUMERO_DE_FURTOS', 
        color_continuous_scale='cividis',  
        text='NUMERO_DE_FURTOS',  
        orientation='h'
    )

    fig_furtos_marca.update_layout(
        width=1400,
        height=600,
        xaxis_title='Número de Ocorrências',
        yaxis_title='Marca/Modelo',
        title_font=dict(size=18),
        yaxis={'categoryorder':'total ascending'}  # Ordenar categorias pelo total de ocorrências
    )

    fig_furtos_marca.update_xaxes(visible=False)

    # Ajustar a posição dos rótulos dos valores para furtos
    fig_furtos_marca.update_traces(texttemplate='%{text}', textposition='auto')

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig_furtos_marca)



# ------------------------------------------------------------------------- Ocorrências por cor --------------------------- #
furtos_por_cor = df_atual['DESC_COR_VEICULO'].value_counts().head(10).reset_index()
furtos_por_cor.columns = ['DESC_COR_VEICULO', 'NUMERO_DE_FURTOS']

if mes_selecionado == 'Todos os Meses':
    title = f'Top 10 Cores de Veículo com mais Ocorrências em {ano_selecionado}'
else:
    title = f'Top 10 Cores de Veículo com mais Ocorrências em {mes_selecionado} de {ano_selecionado}'

# Plotar o gráfico de barras com Plotly
fig_furtos_por_cor= px.bar(
    furtos_por_cor,
    x='DESC_COR_VEICULO',
    y='NUMERO_DE_FURTOS',
    title=title,
    labels={'DESC_COR_VEICULO': 'Ano Fabricação', 'NUMERO_DE_FURTOS': 'Número de Ocorrências'},
    color='NUMERO_DE_FURTOS',
    color_continuous_scale='amp',
    text='NUMERO_DE_FURTOS'
)

fig_furtos_por_cor.update_layout(
    width=2000,
    height=450,
    title_x=0.1,
    xaxis_title='Ano Fabricação',
    yaxis_title='Número de Ocorrências',
    title_font=dict(size=26)
)

# Ajustar a posição dos rótulos dos valores para furtos
fig_furtos_por_cor.update_traces(texttemplate='%{text}', textposition='outside')
fig_furtos_por_cor.update_yaxes(range=[0, furtos_por_cor['NUMERO_DE_FURTOS'].max() * 1.2])  # Ajuste do intervalo do eixo y

# Exibir o gráfico no Streamlit
st.plotly_chart(fig_furtos_por_cor)

# ------------------------------------------------------------------------- Ocorrências por ano de fabricação --------------------------- #

# Cálculo de ocorrências por ano de fabricação
df_atual['ANO_FABRICACAO'] = df_atual['ANO_FABRICACAO'].astype(str)
furtos_por_ano_fabricacao = df_atual['ANO_FABRICACAO'].value_counts().reset_index()
furtos_por_ano_fabricacao.columns = ['ANO_FABRICACAO', 'NUMERO_DE_FURTOS']

# Plotar o gráfico de barras com Plotly
fig_furtos_ano_fabricacao = px.bar(
    furtos_por_ano_fabricacao,
    x='ANO_FABRICACAO',
    y='NUMERO_DE_FURTOS',
    title=f'Ocorrências por Ano de Fabricação do Veículo',
    labels={'ANO_FABRICACAO': 'Ano Fabricação', 'NUMERO_DE_FURTOS': 'Número de Ocorrências'},
    color='NUMERO_DE_FURTOS',
    color_continuous_scale='deep',
    text='NUMERO_DE_FURTOS'
)

fig_furtos_ano_fabricacao.update_layout(
    width=2000,
    height=450,
    title_x=0.2,
    xaxis_title='Ano Fabricação',
    yaxis_title='Número de Ocorrências',
    title_font=dict(size=26)
)

# Ajustar a posição dos rótulos dos valores para furtos
fig_furtos_ano_fabricacao.update_traces(texttemplate='%{text}', textposition='outside')
fig_furtos_ano_fabricacao.update_yaxes(range=[0, furtos_por_ano_fabricacao['NUMERO_DE_FURTOS'].max() * 1.1])  # Ajuste do intervalo do eixo y

# Exibir o gráfico no Streamlit
st.plotly_chart(fig_furtos_ano_fabricacao)
