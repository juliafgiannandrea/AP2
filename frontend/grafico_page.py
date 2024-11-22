#Frontend da aba GRÁFICOS: 

#Importação das bibliotecas:
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
#Importação das funções encontradas nos outros arquivos
from backend.views import pegar_df_preco_corrigido, pegar_df_preco_diversos, validar_data


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
            df_preco_grouped = pegar_df_preco_corrigido(data_ini, data_fim, acoes_carteira)
             # Criar o gráfico com os valores de retorno de cada dia da carteira  
            plt.figure(figsize=(10, 7))
            plt.plot(df_preco_grouped['data'], df_preco_grouped['fechamento'], linestyle='-', color='green', label='Fechamento da Carteira')
            # Personalização do gráfico
            plt.title('Fechamento da Carteira de Ações por Data')
            plt.xlabel('Data')
            plt.ylabel('Fechamento')
            plt.xticks(rotation=45)  # Rotaciona as datas para melhor visualização
            plt.grid(True)
            plt.legend()
            # Ajustar o layout do gráfico
            plt.tight_layout()  
            print(f"Foram utilizadas para a análise as ações: {acoes_carteira}")
            st.pyplot(plt)
            st.dataframe(df_preco_grouped)
       
        if "IBOV" in graficos_opcoes:
            st.subheader("IBOV")
            st.write("Variação do retorno do Ibovespa")
            df_preco = pegar_df_preco_diversos(data_ini, data_fim)
            plt.figure(figsize=(10, 7))
            plt.plot(df_preco['data'], df_preco['fechamento'], linestyle='-', color='red', label='Fechamento ibov')
            # Personalização do gráfico
            plt.title('Fechamento do Ibovespa por Data')
            plt.xlabel('Data')
            plt.ylabel('Valores de Fechamento do Ibovespa')
            plt.grid(True)
            plt.legend()
            plt.xticks(rotation=45)
            # Ajustar o layout do gráfico
            plt.tight_layout()  
            plt.show()
            st.pyplot(plt)


        if "Comparativo Carteira x IBOV" in graficos_opcoes:
            st.subheader("Carteira de Ações")
            # df_carteira = pegar_df_preco_corrigido(data_ini, data_fim, acoes_carteira)
            df_carteira = pegar_df_preco_corrigido(data_ini, data_fim, acoes_carteira)
            st.subheader("IBOV")
            df_ibov = pegar_df_preco_diversos(data_ini, data_fim)
            st.subheader("Comparativo: Carteira x IBOV")
            st.write("Variação comparada do retorno da Carteira de Ações X Ibovespa")
            fig, ax1 = plt.subplots(figsize=(10, 7))
            # Gráfico para os dados da carteira
            ax1.plot(df_carteira['data'], df_carteira['fechamento'], color='green', label='Carteira')
            ax1.set_xlabel('Data')
            ax1.set_ylabel('Valores de fechamento da Carteira', color='green')
            ax1.tick_params(axis='y', labelcolor='green')
            # Adiciona o segundo eixo y para os dados do Ibovespa
            ax2 = ax1.twinx()
            ax2.plot(df_ibov['data'], df_ibov['fechamento'], color='red', label='Ibovespa')
            ax2.set_ylabel('Valores de fechamento do Ibovespa', color='red')
            ax2.tick_params(axis='y', labelcolor='red')
            # Título e grade
            plt.title('Fechamento da Carteira de Ações X Ibovespa por Data')
            ax1.grid(True)
            # Adiciona legendas de forma combinada
            fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9))
            # Ajustar o layout
            plt.tight_layout()
            st.pyplot(fig)

       



