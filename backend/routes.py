

import streamlit as st 
from backend.views import (pegar_df_planilhao, carteira)

#from backend.views import selecionar_acoes

def menu_planilhao(data_base):
    df = pegar_df_planilhao(data_base)
    return df 

def menu_estrategia(data, indicador_rent,indicador_desc, num): 
    df = carteira(data, indicador_rent,indicador_desc, num)
    return df



