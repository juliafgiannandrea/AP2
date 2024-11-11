#Frontend da aba GRÁFICOS: 

#Importação das bibliotecas:
import streamlit as st
import pandas as pd

#Importação das funções encontradas nos outros arquivos
from backend.views import pegar_df_preco_corrigido, carteira
from backend.routes import menu_estrategia, menu_graficos


#Exibição 
def render_grafico():
    st.header("GRÁFICOS")
    st.write("Aqui você pode visualizar o gráfico correspondente a variação dos valores de fechamento das ações da carteira gerada na aba estratégia em relação ao decorrer do tempo.")


    if 'acoes_carteira' not in st.session_state:
        st.warning("Nenhuma carteira de ações foi gerada. Gere a carteira na página de Estratégia.")
        return

    acoes_carteira = st.session_state.acoes_carteira  # Pega a carteira de ações
    data_ini = st.date_input("Selecione uma data", value=pd.to_datetime('today'),key="data_inicio") #today como valor padrão
    data_fim = st.date_input("Selecione uma data", value=pd.to_datetime('today'), key="data_fim") #today como valor padrão
   
    st.write(f"Variação do valor do fechamento da carteira formada pelas ações: {acoes_carteira}")
    st.write(f"Data de Início: {data_ini}")
    st.write(f"Data de Fim: {data_fim}")


    #Execução da busca: 
    if st.button("Buscar Dados"):
        df = menu_graficos(data_ini, data_fim, acoes_carteira)
        return df
        
        





