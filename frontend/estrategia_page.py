#Frontend da aba ESTRATÉGIA: 

#Importação das bibliotecas:
import streamlit as st
import pandas as pd


#Importação das outras funções criadas em outros arquivos: 
from backend.views import pegar_df_planilhao, carteira
from backend.routes import menu_estrategia


#Exibição :
def render_estrategia():
    st.header("Estratégia")
    st.write("Estratégia para análises conjuntas levando em conta 2 indicadores financeiros: um de desconto e outro de rentabilidade com geração de carteira de ações composta por um número informado por você")

    #Input dos indicadores:
    indicador_rent = st.sidebar.selectbox("Selecione o indicador de rentabilidade que você quer analisar", options=["roe", "roic", "roc"])
    indicador_desc = st.sidebar.radio("Selecione o indicador de desconto que você quer analisar", options=["earning_yield", "dividend_yield", "p_vp"])

    #Input data e quantidade de ações (número) a serem analisadas: 
    data = st.sidebar.date_input("Selecione uma data", value=pd.to_datetime('today'))
    num = st.sidebar.number_input("Quantas ações você quer analisar?", min_value=1, value=10)
    
    #Buscar os dados:
    if st.sidebar.button("Buscar"):
        acoes_carteira = carteira(data, indicador_rent, indicador_desc, num)  # Gerar a carteira de ações
        st.session_state.acoes_carteira = acoes_carteira  # Armazenar as ações da carteira no session_state 
        df = menu_estrategia(data, indicador_rent, indicador_desc, num)
        st.dataframe(df)
    
    #texto explicativo para exibição: 
    st.header("Resultados da Análise")
    st.subheader(f"Top {num} ações pelo indicador de rentabilidade: '{indicador_rent}' e pelo indicador de desconto '{indicador_desc}' em {data.strftime('%Y-%m-%d')}")



   
