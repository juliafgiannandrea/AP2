#Comunicação do frontend com o backend 

import streamlit as st 
from backend.views import (pegar_df_planilhao, carteira, pegar_df_preco_corrigido, pegar_df_preco_diversos)

#Planilhão
def menu_planilhao(data_base):
    df = pegar_df_planilhao(data_base)
    return df 

#Estratégia
def menu_estrategia(data, indicador_rent,indicador_desc, num): 
    df = carteira(data, indicador_rent,indicador_desc, num)
    return df

#Gráficos
def menu_graficos(data_ini, data_fim, acoes_carteira):
    df = pegar_df_preco_corrigido(data_ini, data_fim, acoes_carteira)
    return df 


def grafico_ibov(data_ini, data_fim, acoes_carteira):
    df = pegar_df_preco_diversos(data_ini, data_fim, acoes_carteira) 
    return df 