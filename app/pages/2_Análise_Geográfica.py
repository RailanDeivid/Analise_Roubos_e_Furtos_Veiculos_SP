import streamlit as st
import plotly.express as px
import pandas as pd

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

# ------------------------------------------------------------ ANALISE DE ROUBOS ----------------------------------------#

st.subheader('Distribuição de Roubos e Furtos por Bairro')

# Adicionar um seletor de ano para furtos acima do gráfico
col1, col2 = st.columns(2)
anos_disponiveis_furtos = [2023, 2024]
tipo = ['Selecionar Todos'] + df['DESCR_OCORRENCIA_VEICULO'].unique().tolist()

# Selectbox na primeira coluna para o ano
with col1:
    ano_selecionado = st.selectbox('Ano', anos_disponiveis_furtos)
    bairro_selecionado = st.selectbox('Selecionar Bairro', ['Selecionar Todos'] + df['BAIRRO'].unique().tolist())

# Selectbox na segunda coluna para o tipo de ocorrência
with col2:
    tipo_selecionado = st.selectbox('Tipo Ocorrência', tipo)

# Filtrar os dados pelo ano selecionado e tipo de ocorrência
if tipo_selecionado == 'Selecionar Todos':
    df_furtos = df[df['ANO_BO'] == ano_selecionado]
    titulo_grafico = f'Todas as Ocorrências de Veículos em {ano_selecionado}'
else:
    df_furtos = df[(df['DESCR_OCORRENCIA_VEICULO'] == tipo_selecionado) & (df['ANO_BO'] == ano_selecionado)]
    titulo_grafico = f'Ocorrências de Veículos - {tipo_selecionado} em {ano_selecionado}'

if bairro_selecionado != 'Selecionar Todos':
    df_furtos = df_furtos[df_furtos['BAIRRO'] == bairro_selecionado]


# Calcula contagem de furtos por bairro
furtos_por_bairro = df_furtos['BAIRRO'].value_counts().head(10).reset_index()
furtos_por_bairro.columns = ['BAIRRO', 'NUMERO_DE_FURTOS']
furtos_por_bairro = furtos_por_bairro.loc[furtos_por_bairro['BAIRRO'] != "nan"]

# Plotar o gráfico com Plotly para furtos
fig_furtos = px.bar(
    furtos_por_bairro,
    x='BAIRRO',
    y='NUMERO_DE_FURTOS',
    title=titulo_grafico,
    labels={'BAIRRO': 'Bairro', 'NUMERO_DE_FURTOS': 'Número de Ocorrências'},
    color='NUMERO_DE_FURTOS',
    color_continuous_scale='viridis',
    text='NUMERO_DE_FURTOS'
)

# Ajustar o tamanho do gráfico para furtos
fig_furtos.update_layout(
    width=1500,
    height=500,
    title_x=0.3,
    xaxis_title='Bairro',
    yaxis_title='Número de Ocorrências'
)

# Ajustar a posição dos rótulos dos valores para furtos
fig_furtos.update_traces(texttemplate='%{text}', textposition='outside')

# Exibir o gráfico no Streamlit para furtos
st.plotly_chart(fig_furtos)
