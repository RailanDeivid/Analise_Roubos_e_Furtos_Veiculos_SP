import pandas as pd
import os
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import folium_static

# Função para carregar os dados
if "data" not in st.session_state:
    # data_path = os.path.abspath(os.path.join(os.getcwd(), '..', 'data', 'processed','VeiculosSubtraidos.parquet'))
    # Caminho dos arquivos
    path = os.path.dirname(__file__)
    my_data = path+'/data/processed/VeiculosSubtraidos.parquet'
    df = pd.read_parquet(my_data)
    st.session_state["data"] = df

# Define o layout da página para wide
st.set_page_config(layout="wide")

# setando titulo
st.markdown("""
    <style>
        .rounded-title {
            text-align: center; 
            font-size: 40px;
        }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='rounded-title'>Análise de Dados Públicos de Furtos e Roubos no municipio de Guarulhos-SP.</h1>", unsafe_allow_html=True)

# setando informações
st.markdown(
"""<p style='font-size: 16px;'>Este projeto faz parte de uma atividade extensiva dedicada à análise e disseminação de dados públicos sobre furtos e roubos em Guarulhos-SP. 
A iniciativa visa não apenas compreender as tendências de crimes na região, mas também proporcionar insights valiosos para a comunidade.
Através da aplicação de técnicas avançadas de ciência de dados, meu objetivo é:</p>""", unsafe_allow_html=True)

st.markdown("""
- **<h3 style='font-size: 20px;'>Objetivos do Projeto:</h3>**
    - **Análise Profunda de Dados:**
        - Utilizando técnicas avançadas de ciência de dados, o projeto visa realizar uma análise abrangente dos registros de furtos e roubos em Guarulhos. Isso inclui a identificação de padrões temporais, locais e tipos de crime mais prevalentes.
    - **Desenvolvimento de Ferramentas Interativas:**
        - Serão desenvolvidas ferramentas interativas e visualizações dinâmicas para facilitar o entendimento e a exploração dos dados por parte dos usuários. Essas ferramentas permitirão a análise espacial dos crimes, comparações ao longo do tempo e insights detalhados sobre áreas de maior incidência.
    - **Engajamento Comunitário:**
        - Além da análise técnica, o projeto busca promover o engajamento comunitário através da divulgação dos resultados. Isso inclui a conscientização sobre questões de segurança, a promoção de práticas preventivas e a participação ativa dos cidadãos na promoção de um ambiente mais seguro.
""", unsafe_allow_html=True)

