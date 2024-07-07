import streamlit as st

# Define o layout da página
st.set_page_config(
    page_title="Analise por Veículos",
    page_icon="🚗", 
    initial_sidebar_state="expanded",
    layout="wide"
    )

st.session_state["data"]


