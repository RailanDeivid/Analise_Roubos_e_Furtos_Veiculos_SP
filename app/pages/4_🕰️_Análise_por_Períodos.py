import streamlit as st


st.set_page_config(
    page_title="Analise por Veículos",
    page_icon="🕰️", 
    initial_sidebar_state="expanded",
    layout="wide"
    )

# Carregar os dados do estado da sessão
df = st.session_state["data"]
df = df.loc[df['CIDADE'] == "GUARULHOS"]




# # Análise de roubos por ano
# st.subheader('Distribuição de Roubos por Ano')
# roubos_por_ano = df['ANO'].value_counts().sort_index()
# st.line_chart(roubos_por_ano)

# # Análise de roubos por mês
# st.subheader('Distribuição de Roubos por Mês')
# roubos_por_mes = df['MES'].value_counts().sort_index()
# st.bar_chart(roubos_por_mes)

# # Análise de roubos por dia da semana
# st.subheader('Distribuição de Roubos por Dia da Semana')
# df['DATA_OCORRENCIA_BO'] = pd.to_datetime(df['DATA_OCORRENCIA_BO'])
# df['DIA_DA_SEMANA'] = df['DATA_OCORRENCIA_BO'].dt.day_name()
# roubos_por_dia = df['DIA_DA_SEMANA'].value_counts().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
# st.bar_chart(roubos_por_dia)

# # Análise de roubos por hora do dia
# st.subheader('Distribuição de Roubos por Hora do Dia')
# df['HORA_OCORRENCIA'] = pd.to_datetime(df['HORA_OCORRENCIA'], format='%H:%M').dt.hour
# roubos_por_hora = df['HORA_OCORRENCIA'].value_counts().sort_index()
# st.bar_chart(roubos_por_hora)