# Exemplo inicial de código para carregar e visualizar dados no Streamlit
import pandas as pd
import os
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import folium_static

# Função para carregar os dados

if "data" not in st.session_state:
    df = pd.read_excel('../data/raw/VeiculosSubtraidos_2024.xlsx')
    st.session_state["data"] = df.head()


st.title("testes")

