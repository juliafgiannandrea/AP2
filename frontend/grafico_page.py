#Frontend da aba GRÁFICOS: 

#Importação das bibliotecas:
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
#Importação das funções encontradas nos outros arquivos
from backend.views import pegar_df_preco_corrigido, carteira, pegar_df_preco_diversos, validar_data
from backend.routes import menu_estrategia, menu_graficos, grafico_ibov, comp


#Exibição 
def render_grafico():
        
    """
        Essa função faz a exibição dos gráficos que podem ser gerados pelas funções que estão no script views.py    
    """
    
    st.header(" 📊  ANÁLISE DE GRÁFICOS")
    st.write("Aqui você pode visualizar o gráfico que mostra a variação dos valores de retorno das ações da carteira gerada na aba Estratégia ao longo do tempo, bem como a variação do retorno do Ibovespa num determinado período. Em seguida, é possível comparar essas duas variações num gráfico só.")

    #verificar se a lista das ações da carteira foi gerada e está no cache: 
    if 'acoes_carteira' not in st.session_state:
        st.warning("Nenhuma carteira de ações foi gerada. Gere a carteira na página de Estratégia.")
        return

    acoes_carteira = st.session_state.acoes_carteira  # Pega a carteira de ações
    
    #Inputs das datas 
    data_ini = st.date_input("Selecione uma data de início", value=pd.to_datetime('today'),key="data_inicio") #today como valor padrão
    validar_data(data_ini)

    data_fim = st.date_input("Selecione uma data de fim", value=pd.to_datetime('today'), key="data_fim") #today como valor padrão
    validar_data(data_fim)

    if data_ini > data_fim:
        st.error("A data de fim deve ser posterior a data de início")

    st.warning("Antes de clicar em Gerar Gráficos selecione a opção de visualização.")

   
#FILTROS INTERATIVOS PARA A VISUALIZAÇÃO DOS GRÁFICOS: 
    st.sidebar.header("Opções de Visualização")
    graficos_opcoes = st.sidebar.multiselect(
        "Escolha os gráficos:",
        ["Carteira de Ações", "IBOV", "Comparativo Carteira x IBOV"]
    )

    #Execução da busca: 
    if st.button("Gerar Gráficos"):
        if "Carteira de Ações" in graficos_opcoes:
            st.subheader("Carteira de Ações")
            st.write(f"Variação do retorno da carteira formada pelas ações: {acoes_carteira}")
            df = menu_graficos(data_ini, data_fim, acoes_carteira)
       
        if "IBOV" in graficos_opcoes:
            st.subheader("IBOV")
            st.write("Variação do retorno do Ibovespa")
            ibov = grafico_ibov(data_ini, data_fim)


        if "Comparativo Carteira x IBOV" in graficos_opcoes:
            st.subheader("Carteira de Ações")
            df_carteira = pegar_df_preco_corrigido(data_ini, data_fim, acoes_carteira)
            st.subheader("IBOV")
            df_ibov = pegar_df_preco_diversos(data_ini, data_fim)
            st.subheader("Comparativo: Carteira x IBOV")
            st.write("Variação comparada do retorno da Carteira de Ações X Ibovespa")
            comparativo = comp(data_ini, data_fim, df_carteira, df_ibov)
            

       



