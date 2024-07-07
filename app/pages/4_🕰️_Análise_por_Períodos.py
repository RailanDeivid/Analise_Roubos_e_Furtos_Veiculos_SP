import streamlit as st


st.set_page_config(
    page_title="Analise por Veículos",
    page_icon="🕰️", 
    initial_sidebar_state="expanded",
    layout="wide"
    )

st.session_state["data"]