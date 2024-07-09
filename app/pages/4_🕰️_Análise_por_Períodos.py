import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="Análise por Veículos",
    page_icon="🕰️", 
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

st.markdown("<h1 class='rounded-title'>Análise de Ocorrência por Períodos</h1><br>", unsafe_allow_html=True)

# ------------------------------------------------------------ CONFIGURAÇÕES DE FILTROS ---------------------------------------- # 
anos_disponiveis_furtos = [2023, 2024]
tipos_veiculos = ['Todos os Tipos'] + df['DESCR_TIPO_VEICULO'].unique().tolist()
marcas = ['Todas as Marcas'] + df['DESCR_MARCA_VEICULO'].unique().tolist()
tipo_ocorrencia = ['Todas as Ocorrências'] + df['DESCR_OCORRENCIA_VEICULO'].unique().tolist()

# Setar título
st.write('Os filtros se aplicam a todos os gráficos da página.')

# Layout dos filtros
col1, col2, col3 = st.columns(3)

# Selectbox para o ano e bairro
with col1:
    ano_selecionado = st.selectbox('Ano', anos_disponiveis_furtos)
    bairro_selecionado = st.selectbox('Selecionar Bairro', ['Todos os Bairros'] + df['BAIRRO'].unique().tolist())

# Selectbox para tipo de veículo e marca
with col2:
    tipo_veiculo_selecionado = st.selectbox('Tipo Veículo', tipos_veiculos)
    marca_selecionada = st.selectbox('Marca/Modelo', marcas)

# Selectbox para tipo de ocorrência
with col3:
    tipo_selecionado = st.selectbox('Tipo Ocorrência', tipo_ocorrencia)

# Filtrar os dados com base nos filtros selecionados
df['DATA_OCORRENCIA_BO'] = pd.to_datetime(df['DATA_OCORRENCIA_BO'])
df_atual = df[df['DATA_OCORRENCIA_BO'].dt.year == ano_selecionado]

if tipo_selecionado != 'Todas as Ocorrências':
    df_atual = df_atual[df_atual['DESCR_OCORRENCIA_VEICULO'] == tipo_selecionado]

if bairro_selecionado != 'Todos os Bairros':
    df_atual = df_atual[df_atual['BAIRRO'] == bairro_selecionado]

if tipo_veiculo_selecionado != 'Todos os Tipos':
    df_atual = df_atual[df_atual['DESCR_TIPO_VEICULO'] == tipo_veiculo_selecionado]

if marca_selecionada != 'Todas as Marcas':
    df_atual = df_atual[df_atual['DESCR_MARCA_VEICULO'] == marca_selecionada]

# ------------------------------------------------------------ GRÁFICO DE ROUBOS POR MÊS ---------------------------------------- #
st.header('Distribuição de Ocorrências por Períodos', divider='rainbow')
roubos_por_mes = df_atual['DATA_OCORRENCIA_BO'].dt.month.value_counts().sort_index().reset_index()
roubos_por_mes.columns = ['Mês', 'Número de Ocorrências']

meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
roubos_por_mes['Mês'] = roubos_por_mes['Mês'].apply(lambda x: meses[x-1])

fig_mes = px.bar(
    roubos_por_mes,
    x='Mês',
    y='Número de Ocorrências',
    title=f'Distribuição de Ocorrências por Mês em {ano_selecionado}',
    labels={'Mês': 'Mês', 'Número de Ocorrências': 'Número de Ocorrências'},
    color='Número de Ocorrências',
    color_continuous_scale='viridis',
    text='Número de Ocorrências'
)

fig_mes.update_layout(
    width=1700,
    height=600,
    title_x=0.2,
    xaxis_title='Mês',
    yaxis_title='Número de Ocorrências',
    title_font=dict(size=26)
)

fig_mes.update_traces(texttemplate='%{text}', textposition='outside')

st.plotly_chart(fig_mes)

# ------------------------------------------------------------ GRÁFICO DE ROUBOS POR ANO ---------------------------------------- #

df_filtrado = df.copy()
if tipo_selecionado != 'Todas as Ocorrências':
    df_filtrado = df_filtrado[df_filtrado['DESCR_OCORRENCIA_VEICULO'] == tipo_selecionado]

if bairro_selecionado != 'Todos os Bairros':
    df_filtrado = df_filtrado[df_filtrado['BAIRRO'] == bairro_selecionado]

if tipo_veiculo_selecionado != 'Todos os Tipos':
    df_filtrado = df_filtrado[df_filtrado['DESCR_TIPO_VEICULO'] == tipo_veiculo_selecionado]

if marca_selecionada != 'Todas as Marcas':
    df_filtrado = df_filtrado[df_filtrado['DESCR_MARCA_VEICULO'] == marca_selecionada]

roubos_por_ano = df_filtrado[df_filtrado['DATA_OCORRENCIA_BO'].dt.year.isin([2023, 2024])]
roubos_por_ano = roubos_por_ano['DATA_OCORRENCIA_BO'].dt.year.value_counts().sort_index().reset_index()
roubos_por_ano.columns = ['Ano', 'Número de Ocorrências']

fig_ano = px.bar(
    roubos_por_ano,
    x='Ano',
    y='Número de Ocorrências',
    title='Distribuição de Roubos por Ano',
    labels={'Ano': 'Ano', 'Número de Ocorrências': 'Número de Ocorrências'},
    color='Número de Ocorrências',
    color_continuous_scale='viridis',
    text='Número de Ocorrências'
)

fig_ano.update_layout(
    width=1400,
    height=600,
    title_x=0.2,
    xaxis_title='Ano',
    yaxis_title='Número de Ocorrências',
    title_font=dict(size=26),
    xaxis=dict(
        tickmode='array',
        tickvals=[2023, 2024],
        ticktext=['2023', '2024']
    )
)

fig_ano.update_traces(texttemplate='%{text}', textposition='outside')

st.plotly_chart(fig_ano)

# ------------------------------------------------------------ ANÁLISE DE ROUBOS POR DIA DA SEMANA ---------------------------------------- #

df['DIA_DA_SEMANA'] = df['DATA_OCORRENCIA_BO'].dt.day_name()
roubos_por_dia = df['DIA_DA_SEMANA'].value_counts().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

fig_dia_semana = px.bar(
    x=roubos_por_dia.index,
    y=roubos_por_dia.values,
    labels={'x': 'Dia da Semana', 'y': 'Número de Ocorrências'},
    title='Distribuição de Roubos por Dia da Semana',
    color=roubos_por_dia.values,
    color_continuous_scale='viridis'
)

fig_dia_semana.update_layout(
    width=1400,
    height=600,
    title_x=0.2,
    xaxis_title='Dia da Semana',
    yaxis_title='Número de Ocorrências',
    title_font=dict(size=24)
)

fig_dia_semana.update_traces(texttemplate='%{y}', textposition='outside')  
fig_dia_semana.update_yaxes(range=[0, roubos_por_dia.max() * 1.1]) 
st.plotly_chart(fig_dia_semana)

# ------------------------------------------------------------ ANÁLISE DE ROUBOS POR HORA DO DIA ---------------------------------------- #

