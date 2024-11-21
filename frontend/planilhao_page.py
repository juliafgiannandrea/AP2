#Frontend da aba PLANILHÃO 

#Importação das bibliotecas:
import streamlit as st
import pandas as pd

#Importação das outras funções criadas em outros arquivos: 
from backend.views import pegar_df_planilhao, validar_data
from backend.routes import menu_planilhao 




#Estrutura - front
def render_planilhao():
    """
    Essa função rendereiza a pagina que exibe a tabela planilhão.
    """
    st.header(" 📡  PLANILHÃO")
    st.write("""Aqui você visualiza os dados da tabela Planilhão, que contém dados de todas as ações num determinado dia.""")

    #Input de data:
    data_base = st.date_input("Selecione uma data", value=pd.to_datetime('today')) #today como valor padrão

    #garantir que a data selecionada não possa ser o dia de hoje nem sábado e domingo
    validar_data(data_base)


    #apertar o botão de busca e executar a função menu_plnaulhão 
    if st.button("Buscar Dados"):
        df = menu_planilhao(data_base)
        if not df.empty:
            st.dataframe(df, height=600, use_container_width=True) #determino o espaço que a tabela vai ocupar 
        else:
            st.info("Nenhum dado encontrado para a data selecionada.")




