import pandas as pd
import os
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import folium_static

# Função para carregar os dados
if "data" not in st.session_state:
    data_path = os.path.abspath(os.path.join(os.getcwd(), '..', 'data', 'processed','VeiculosSubtraidos.parquet'))
    df = pd.read_parquet(data_path)
    st.session_state["data"] = df.head()

# Define o layout da página para wide
st.set_page_config(layout="wide")

# setando titulo
st.markdown("""
    <style>
        .rounded-title {
            border-radius: 10px;
            padding: 10px;
            text-align: center; 
            font-size: 35px;
        }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='rounded-title'>Análise de Dados Públicos de Furtos e Roubos no Estado de São Paulo.</h1>", unsafe_allow_html=True)

# setando informações
st.markdown("<h1 style='font-size: 30px;'>Informações do Modelo</h1>", unsafe_allow_html=True)
st.markdown("""
Esta aplicação utiliza um modelo de machine learning para prever o preço de vendas de carros com base nas características inseridas. 
            
O modelo foi treinado com dados de anuncios de vendas de veiculos do site MercadoLivre.
""")