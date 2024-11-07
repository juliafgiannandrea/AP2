
import streamlit as st
import pandas as pd
from backend.views import pegar_df_planilhao
from backend.routes import menu_planilhao, menu_estrategia



def render_grafico():
    st.header("GRÁFICOS")
    st.write("Aqui você pode visualizar gráficos com base nos dados.")




