import streamlit as st
import pandas as pd
from backend.views import pegar_df_planilhao
from backend.routes import menu_planilhao 

def render_planilhao():
    st.header("PLANILHÃO")
    st.write("Aqui você visualiza os dados da tabela Planilhão, que contém dados de todas as ações num determinado dia.")

    #Input de data:
    data_base = st.date_input("Selecione uma data", value=pd.to_datetime('today')) #today como valor padrão
    
    if st.button("Buscar Dados"):
        df = menu_planilhao(data_base)
        if not df.empty:
            st.dataframe(df, height=500)
        else:
            st.info("Nenhum dado encontrado para a data selecionada.")



#st.dataframe(df)# Exibe o DataFrame em uma tabela no Streamlit
