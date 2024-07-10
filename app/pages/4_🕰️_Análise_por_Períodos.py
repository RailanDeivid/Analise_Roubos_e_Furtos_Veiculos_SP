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


st.header('Distribuição de Ocorrências por Períodos', divider='rainbow')
cols = st.columns([2, 3])

with cols[1]:
    # ------------------------------------------------------------ GRÁFICO DE ROUBOS POR MÊS ---------------------------------------- #
    roubos_por_mes = df_atual['DATA_OCORRENCIA_BO'].dt.month.value_counts().sort_index().reset_index()
    roubos_por_mes.columns = ['Mês', 'Número de Ocorrências']

    meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    roubos_por_mes['Mês'] = roubos_por_mes['Mês'].apply(lambda x: meses[x-1])


    # Criar o gráfico de linhas suaves
    fig_mes = px.line(
        roubos_por_mes,
        x='Mês',
        y='Número de Ocorrências',
        title=f'Distribuição de Ocorrências por Mês em {ano_selecionado}',
        labels={'Mês': 'Mês', 'Número de Ocorrências': 'Número de Ocorrências'},
        line_shape='spline',  # Define as linhas como curvas suaves
        render_mode='svg', # Renderização mais suave das curvas,
        text = 'Número de Ocorrências'
    )

    # Ajustar a cor da linha
    fig_mes.update_traces(line=dict(color='red'), fill='tozeroy',fillcolor='rgba(255, 0, 0, 0.1)' )

    fig_mes.update_layout(
        width=1500,
        height=450,
        title_x=0.1,
        xaxis_title='Mês',
        yaxis_title='Número de Ocorrências',
        title_font=dict(size=20)
    )

    fig_mes.update_traces(texttemplate='%{text}', textposition='top center')
    fig_mes.update_yaxes(range=[0, roubos_por_mes['Número de Ocorrências'].max() + 201])


    st.plotly_chart(fig_mes)


    # fig_mes = px.bar(
    #     roubos_por_mes,
    #     x='Mês',
    #     y='Número de Ocorrências',
    #     title=f'Distribuição de Ocorrências por Mês em {ano_selecionado}',
    #     labels={'Mês': 'Mês', 'Número de Ocorrências': 'Número de Ocorrências'},
    #     color='Número de Ocorrências',
    #     color_continuous_scale='bluered',
    #     text='Número de Ocorrências'
    # )

    # fig_mes.update_layout(
    #     width=1500,
    #     height=450,
    #     title_x=0.1,
    #     xaxis_title='Mês',
    #     yaxis_title='Número de Ocorrências',
    #     title_font=dict(size=20)
    # )

    # fig_mes.update_traces(texttemplate='%{text}', textposition='auto')
    # fig_mes.update_yaxes(range=[0, roubos_por_mes['Número de Ocorrências'].max() + 200]) 

    # st.plotly_chart(fig_mes)

# ------------------------------------------------------------ GRÁFICO DE ROUBOS POR ANO ---------------------------------------- #
with cols[0]:
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
        title='Distribuição de Ocorrências por Ano',
        labels={'Ano': 'Ano', 'Número de Ocorrências': 'Número de Ocorrências'},
        color='Número de Ocorrências',
        color_continuous_scale='deep',
        text='Número de Ocorrências'
    )

    fig_ano.update_layout(
        width=1400,
        height=450,
        title_x=0.1,
        xaxis_title='Ano',
        yaxis_title='Número de Ocorrências',
        title_font=dict(size=20),
        xaxis=dict(
            tickmode='array',
            tickvals=[2023, 2024],
            ticktext=['2023', '2024']
        )
    )

    fig_ano.update_traces(texttemplate='%{text}', textposition='auto')
    fig_ano.update_yaxes(range=[0, roubos_por_ano['Número de Ocorrências'].max() * 1.1]) 

    st.plotly_chart(fig_ano)

# ------------------------------------------------------------ ANÁLISE DE ROUBOS POR DIA DA SEMANA ---------------------------------------- #
cols = st.columns([3, 2])
with cols[1]:
    df_atual['DIA_DA_SEMANA'] = df_atual['DATA_OCORRENCIA_BO'].dt.day_name()
    # Dicionário de tradução dos dias da semana
    traducao_dias_semana = {
        'Monday': 'Segunda-feira',
        'Tuesday': 'Terça-feira',
        'Wednesday': 'Quarta-feira',
        'Thursday': 'Quinta-feira',
        'Friday': 'Sexta-feira',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo'
    }
    df_atual['DIA_DA_SEMANA'] = df_atual['DIA_DA_SEMANA'].map(traducao_dias_semana)
    roubos_por_dia = df_atual['DIA_DA_SEMANA'].value_counts().reindex(['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 
                                                                'Quinta-feira', 'Sexta-feira', 'Sábado']).to_frame().reset_index()
    roubos_por_dia.columns = ['Dia da Semana', 'Número de Ocorrências']

    fig_dia_semana = px.bar(
        roubos_por_dia,
        x='Dia da Semana',
        y='Número de Ocorrências',
        labels={'x': 'Dia da Semana', 'y': 'Número de Ocorrências'},
        title='Distribuição de Ocorrências por Dia da Semana',
        color='Número de Ocorrências',
        color_continuous_scale='amp'
    )

    fig_dia_semana.update_layout(
        width=1700,
        height=450,
        xaxis_title='Dia da Semana',
        yaxis_title='Número de Ocorrências',
        title_font=dict(size=18)
    )

    fig_dia_semana.update_traces(texttemplate='%{y}', textposition='outside')  
    fig_dia_semana.update_yaxes(range=[0, roubos_por_dia['Número de Ocorrências'].max() * 1.3]) 
    st.plotly_chart(fig_dia_semana)

# ------------------------------------------------------------ ANÁLISE DE ROUBOS POR HORA DO DIA ---------------------------------------- #

with cols[0]:
    # Extrair apenas a hora como float
    df_atual['HORA_OCORRENCIA'] = pd.to_datetime(df_atual['HORA_OCORRENCIA'], format='%H:%M:%S').dt.hour.astype('float64')
    roubos_por_hora = df_atual['HORA_OCORRENCIA'].value_counts().sort_index().reset_index()
    roubos_por_hora.columns = ['Hora da Ocorrencia', 'Número de Ocorrências']

    # fig_dia_semana = px.bar(
    #     roubos_por_hora,
    #     x='Hora da Ocorrencia',
    #     y='Número de Ocorrências',
    #     labels={'x': 'Hora da Ocorrencia', 'y': 'Número de Ocorrências'},
    #     title='Distribuição de Ocorrências por Hora',
    #     color='Número de Ocorrências',
    #     color_continuous_scale='dense'
    # )

    # fig_dia_semana.update_layout(
    #     width=1700,
    #     height=450,
    #     xaxis_title='Hora da Ocorrencia',
    #     yaxis_title='Número de Ocorrências',
    #     title_font=dict(size=18)
    # )

    # fig_dia_semana.update_traces(texttemplate='%{y}', textposition='outside')  
    # fig_dia_semana.update_yaxes(range=[0, roubos_por_hora['Número de Ocorrências'].max() * 1.1]) 
    # st.plotly_chart(fig_dia_semana)

    # Criar o gráfico de linhas
    fig_dia_semana = px.line(
        roubos_por_hora,
        x='Hora da Ocorrencia',
        y='Número de Ocorrências',
        labels={'x': 'Hora da Ocorrencia', 'y': 'Número de Ocorrências'},
        title='Distribuição de Ocorrências por Hora',
        line_shape='spline',  # Define as linhas como curvas suaves
        render_mode='svg', # Renderização mais suave das curvas,
        text = 'Número de Ocorrências'
    )

    fig_dia_semana.update_layout(
        width=1700,
        height=450,
        xaxis_title='Hora da Ocorrencia',
        yaxis_title='Número de Ocorrências',
        title_font=dict(size=18)
    )

    fig_dia_semana.update_traces(line=dict(color='purple'), fill='tozeroy',fillcolor='rgba(128, 0, 128, 0.1)')  # Define a cor das linhas como vermelho

    fig_dia_semana.update_traces(texttemplate='%{y}', textposition='top center')
    fig_dia_semana.update_yaxes(range=[0, roubos_por_hora['Número de Ocorrências'].max() * 1.2])

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig_dia_semana)
