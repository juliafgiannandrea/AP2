#Frontend da aba ESTRATÉGIA: 
#Importação das bibliotecas:
import streamlit as st
import pandas as pd
#Importação das outras funções criadas em outros arquivos: 
from backend.views import carteira, validar_data

#Exibição :
def render_estrategia():
    """
        Essa função renderiza a página que exibe a carteira de ações gerada a partir da análise de dois indicadores financeiros.
    """
    st.header("📈 Estratégia de Análise de Ações")
    st.write("**Planeje sua estratégia:** Com base em 2 indicadores financeiros gere uma carteira de ações.")
    st.sidebar.header("Configurações da Estratégia")
    #Input dos indicadores:
    indicador_rent = st.sidebar.selectbox("Selecione o indicador de rentabilidade:", options=["roe", "roic", "roc"])
    indicador_desc = st.sidebar.selectbox("Selecione o indicador de desconto:", options=["earning_yield", "dividend_yield", "p_vp"])
    #Input data e quantidade de ações (número) a serem analisadas: 
    data = st.sidebar.date_input("Selecione uma data", value=pd.to_datetime('today'))
    num = st.sidebar.number_input("Quantas ações você quer analisar?", min_value=1, max_value=30, value=5)
    validar_data(data)
    #Buscar os dados:
    if st.sidebar.button("Buscar"):
        df_sorted = carteira(data, indicador_rent, indicador_desc, num) #gera a carteira de ações
        acoes_carteira = df_sorted['ticker'].tolist()   
        # Armazena no session_state a variável acoes_carteira oriunda da função carteira 
        st.session_state.acoes_carteira = acoes_carteira
        st.session_state.df_sorted = df_sorted #armazena df no cache 
        st.dataframe(df_sorted)    
        #texto explicativo para exibição: 
        st.subheader("Resultados da Análise")
        st.write(f"Top {num} ações pelo indicador de rentabilidade: '{indicador_rent}' e pelo indicador de desconto '{indicador_desc}' em {data.strftime('%Y-%m-%d')}")
        st.table(acoes_carteira)



   
