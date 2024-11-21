#Importação das bibliotecas
import pandas as pd
from datetime import date
import os
import logging
import sys 
import matplotlib.pyplot as plt
import streamlit as st 


logger = logging.getLogger(__name__)
logging.basicConfig(
    filename='app.log',  # Arquivo de log
    level=logging.DEBUG,  # Definir o nível de log (DEBUG para tudo, INFO para mensagens gerais, ERROR para erros)
    format='%(asctime)s - %(levelname)s - %(message)s'  # Formato das mensagens de log
)

logger = logging.getLogger()

#Importar as funções criadas no outro arquivo, as que pegam as APIs 
from backend.apis import(pegarPlanilhao,
                          get_preco_corrigido,
                          get_preco_diversos)



#Processamento e consulta dos dados do planilhão: seleção das 4 primeiras letras do ticker 

def pegar_df_planilhao(data_base:date) -> pd.DataFrame:
    """
    Consulta todas as ações com os principais indicadores fundamentalistas

    params:
    data_base (date): Data Base para o cálculo dos indicadores.

    return:
    df (pd.DataFrame): DataFrame com todas as Ações com os indicadores fundamentalistas na data especificada.
    """
    try:
        dados = pegarPlanilhao(data_base)
        if dados: #para verificar se a variável dados não é vazia 
            dados = dados['dados'] 
            planilhao = pd.DataFrame(dados)
            planilhao['empresa'] = [ticker[:4] for ticker in planilhao.ticker.values]  #crio coluna empresa que armazena os 4 primeiros caracteres da coluna ticker 
            df = filtrar_duplicado(planilhao)  ## remoção das ações duplicadas 
        
            logger.info(f"Dados do Planilhao consultados com sucesso: {data_base}")
            print(f"Dados do Planilhao consultados com sucesso: {data_base}")
            return df
        else:
            logger.info(f"Sem Dados no Planilhão: {data_base}")
            print(f"Sem Dados no Planilhão: {data_base}")
    except Exception as e:
        # Loga o erro, se ocorrer uma exceção
        logger.error(f"Erro ao consultar os dados do Planilhao para a data {data_base}: {e}")
        print(f"Erro ao consultar os dados do Planilhao para a data {data_base}: {e}")


#pegar_df_planilhao("2023-04-03")


#Usar algum parâmetro (no geral - o volume) para remover as ações que tem as 3 primeiras letras iguais (são a mesma ação):
#remover linhas duplicadas baseadas em uma coluna escolhida, priorizando o valor mais alto dessa coluna para manter apenas uma ocorrência de cada empresa

def filtrar_duplicado(df:pd.DataFrame, meio:str = None) -> pd.DataFrame:
    """
    Filtra o df das ações duplicadas baseado no meio escolhido. 

    params:
    df (pd.DataFrame): dataframe com os ticker duplicados 
    meio (str): campo escolhido para escolher qual ticker escolher (default: volume) - O valor padrão do argumento meio é volume, a não ser que outro seja indicado, o argumento usado para filtrar o df será o volume das ações. 

    return:
    df (pd.DataFrame): dataframe com os ticker filtrados.
    """
    meio = meio or 'volume'
    df_dup = df[df.empresa.duplicated(keep=False)]  #cria um df que contém apenas as linhas duplicadas na coluna empresa 
    lst_dup = df_dup.empresa.unique() # extrai desse df acima uma lista de empresa duplicadas 
    lst_final = [] #para adicionar as ações que serão mantidas 

    for tic in lst_dup:
        tic_dup = df_dup[df_dup.empresa==tic].sort_values(by=[meio], ascending=False)['ticker'].values[0]  
            #seleciona as duplicatas de uma empresa específica e ordena pelo valor na coluna meio em ordem decrescente. - pego o values[0], que é a ação de maior meio/vol

        lst_final = lst_final + [tic_dup] # add na lista vazia a ação que tem maior valor de meio/vol

    lst_dup = df_dup[~df_dup.ticker.isin(lst_final)]['ticker'].values #lista das ações duplicadas que foram removidas 

    #registrar e printar a lista com os nomes das ações removidas: 
    logger.info(f"Ticker Duplicados Filtrados: {lst_dup}")
    print(f"Ticker Duplicados Filtrados: {lst_dup}")

    return df[~df.ticker.isin(lst_dup)] # data frame sem as ações repetidas (como se isin por causa do ~ virasse in not in
        # ~ é um operador bitwise NOT ---> inverte uma condição booleana === transforma em True os elementos que não estão em lst_dup.


def carteira(data, indicador_rent, indicador_desc, num):

    """
    Gera carteira de ações com determinado número de acordo com 2 indicadores (um de rentabilidade e outro de desconto).

    params:
    data (date): data na qual você quer fazer a análise dos indicadores 
    indicador_rent (str): qual indicador de rentabilidade você quer usar para a análise 
    indicador_desc (str): qual indicador de desconto você quer usar para a análise 
    num (int): o número que representa a quantidade de ações que vc quer que a carteira gerada tenha 

    return:
    df_sorted (pd.DataFrame): um data frame com as ações rankeadas de acordo com os maiores indicadores conjuntos 
    acoes_carteira (list): lista com as ações do df_sorted (ou seja, da carteira gerada)

    """
    try:
        df = pegar_df_planilhao(data)
        colunas = ["ticker","setor","data_base","roc", "roe", "roic","earning_yield","dividend_yield","p_vp"]
        df = df[colunas]

        #criar colunas no df que representem sua classificação de acordo com os indicadores
    
        #rentabilidade:
        df = df.nlargest(len(df),indicador_rent).reset_index(drop = True) 
        df['index_rent'] = df.index #coluna index top indicador de rentabilidade

        #desconto:
        if indicador_desc == 'p_vp': 
            df = df.nsmallest(len(df),indicador_desc).reset_index(drop=True) #qto menor o valor de pvp melhor no ranking ele está 
        else: 
            df = df.nlargest(len(df),indicador_desc).reset_index(drop=True)
        df['index_desc'] = df.index #coluna index top indicador de desconto
        logger.debug("Classificação de rentabilidade realizada.")
        #criação da coluna média que é o ranking novo ranking dos dois indicadores em conjunto 
        df["media"] = df["index_desc"] + df["index_rent"] 
        logger.debug("Coluna média criada.")
        #ordenar a coluna média do menor para o maior 
        df_sorted = df.sort_values(by=['media'], ascending=[True])

        #pegar os maiores rankinhgs conjuntos, ou seja as menores médias, da quantidade 'num' informada e a partir disso gerar uma carteira de ações
        df_sorted = df_sorted.nsmallest(num,'media').reset_index(drop = True) 
        df_sorted.index = df_sorted.index + 1 #para o ranking comçar no 1 e não no 0
        logger.debug(f"Carteira gerada com {num} ações: {df_sorted['ticker'].tolist()}")

        #criar uma lista das ações da carteira gerada: 
        acoes_carteira = df_sorted['ticker'].tolist()  
        logger.info("Função carteira finalizada com sucesso.")

        return df_sorted, acoes_carteira

    except Exception as e:
        logger.error(f"Ocorreu um erro na função carteira: {e}")
        
#carteira('2024-11-05', 'roe', 'earning_yield', 2)


#quero puxar a variável acoes_carteira da função acima para ela entrar como parametro da minha função abaixo  _ usei o cache 
def pegar_df_preco_corrigido(data_ini, data_fim, acoes_carteira) -> pd.DataFrame:
    """
    Consulta os preços Corrigidos de uma lista de ações durante um períodp, calculando o retorno de cada dia para a carteira de ações e gerando um gráfico da variação desse retorno por data.

    params:
    data_ini (date): data inicial da consulta
    data_fim (date): data final da consulta
    acoes_carteira (list): lista de ativos a serem consultados 

    return:
    df_preco_grouped (pd.DataFrame): dataframe com o retorno das ações na carteira de acordo com a data 
    gráfico da variação do retorno da carteira (eixo y) por data (eixo x).
    """ 
   
    df_preco = pd.DataFrame() #crio dataframe

    for ticker in acoes_carteira:
        dados = get_preco_corrigido(ticker, data_ini, data_fim) #para cada ação presente na carteira gerada acima eu execito a função get_preco_corrigido, que é a função que pega a API
       
        if dados and 'dados' in dados: 
            df_temp = pd.DataFrame.from_dict(dados['dados'])  # Converte os dados num df temporário
            df_preco = pd.concat([df_preco, df_temp], axis=0, ignore_index=True) #não entendi do porque criar um data frame temporário e depois concatená-lo. 
            logger.info(f'{ticker} finalizado!')
            print(f'{ticker} finalizado!')
        else:
            logger.error(f"Sem Preço Corrigido: {ticker}")
            print(f"Sem Preço Corrigido: {ticker}")


    col_interesse = ['ticker', 'abertura','fechamento', 'data'] #são as colunas que vou usar para gerar o gráfico 
    df_preco['data'] = pd.to_datetime(df_preco['data']) #garantir que a data esteja no formato de data (type)
    df_preco = df_preco[col_interesse]
    #print(df_preco) #nome da ação, valor de fechamento e data 

    #abertura e fechamento para cada dia para ação:
    abertura_carteira = df_preco["abertura"]
    fechamento_carteira = df_preco["fechamento"]
    
    porc_carteira = (100/(len(acoes_carteira)))/100  
    retorno  = ((fechamento_carteira - abertura_carteira)/abertura_carteira)*porc_carteira
    df_preco["retorno"] = retorno

    #somar todos os valores de retorno de cada ação num mesmo dia --- vou ter valores de fechamento da carteira no dia 
    df_preco_grouped = df_preco.groupby("data")["retorno"].sum().reset_index()

    # Criar o gráfico com os valores de retorno de cada dia da carteira  
    plt.figure(figsize=(10, 7))
    plt.plot(df_preco_grouped['data'], df_preco_grouped['retorno'], linestyle='-', color='green', label='Retorno da Carteira')

    # Personalização do gráfico
    plt.title('Retorno da Carteira de Ações por Data')
    plt.xlabel('Data')
    plt.ylabel('Retorno')
    plt.xticks(rotation=45)  # Rotaciona as datas para melhor visualização
    plt.grid(True)
    plt.legend()

    # Ajustar o layout do gráfico
    plt.tight_layout()  

    print(f"Foram utilizadas para a análise as ações: {acoes_carteira}")
    plt.show()
    st.pyplot(plt)

    return df_preco_grouped #é um data frame com as datas e os valores da soma do fechamento 
    #return df_preco > data frame de cada dia das ações indiviuais com seus valores de abertura,fechamento e retorno 

#pegar_df_preco_corrigido('2024-01-04', '2024-01-10',  ['VBBR3', 'WIZC3'])

#preços diversos é uma tabela utilizada para análise do ibovespa:
def pegar_df_preco_diversos(data_ini:date, data_fim:date) -> pd.DataFrame:
    """
    Consulta os preços históricos de uma carteira de ativos e geração de gráfico do retorno do ibovespa por data

    params:

    data_ini (date): data inicial da consulta
    data_fim (date): data final da consulta

    return:
    df_preco (pd.DataFrame): dataframe com os preços do período dos ativos da lista
    gráfico com a variação dos valores de retorno do ibovespa (eixo y) por data (eixo x)
    """

    df_preco = pd.DataFrame()
    dados = get_preco_diversos(data_ini, data_fim, 'ibov')
    if dados:
        dados = dados['dados']
        df_temp = pd.DataFrame.from_dict(dados)
        df_preco = pd.concat([df_preco, df_temp], axis=0, ignore_index=True)
        logger.info('ibov finalizado!')
        print('ibov finalizado!')   
    else:
        logger.error("Sem Preco Corrigido: ibov")
        print("Sem Preco Corrigido: ibov")

    df_preco['data'] = pd.to_datetime(df_preco['data'])
    ibov_abertura = df_preco["abertura"]
    ibov_fechamento = df_preco["fechamento"]
    retorno_ibov = ((ibov_fechamento - ibov_abertura)/ibov_abertura)
    df_preco["retorno"] = retorno_ibov
       
    #Criação do gráfico: 

    plt.figure(figsize=(10, 7))
    plt.plot(df_preco['data'], df_preco['retorno'], linestyle='-', color='red', label='Retorno ibov')

    # Personalização do gráfico
    plt.title('Retorno do Ibovespa por Data')
    plt.xlabel('Data')
    plt.ylabel('Valores de Retorno do Ibovespa')
    plt.grid(True)
    plt.legend()
    plt.xticks(rotation=45)

    # Ajustar o layout do gráfico
    plt.tight_layout()  

    plt.show()
    st.pyplot(plt)

    return df_preco

#pegar_df_preco_diversos('2024-01-04', '2024-01-10')



#Para fazer o gráfico conjunto 
def comp_ibov_carteira(data_ini:date, data_fim:date, df_carteira, df_ibov):  
    """
    Função que faz o gráfico conjunto do Ibovespa com a carteira de ações para comparação entre ambos.

    param:
    data_ini (data):
    data_fim (data): 
    df_carteira (pd.DataFrame): 
    df_ibov(pd.DataFrame): 

    return:
    gráfico com 2 linhas: uma da carteira outra do ibovespa. 
    Eixo x é a variação das datas no período estabelecido e eixo y os valores de retorno do ibov e da carteira de ações. 
    """
     
    plt.figure(figsize=(10, 7))
    plt.plot(df_carteira['data'], df_carteira['retorno'], color = 'green', label='Carteira')
    plt.plot(df_ibov['data'], df_ibov['retorno'], color='red',label = 'Ibovespa')

    # Personalização do gráfico
    plt.title('Retorno da Carteira de Ações X Ibovespa por Data')
    plt.xlabel('Data')
    plt.ylabel('Retorno')
    plt.grid(True)
    plt.legend()

    # Ajustar o layout do gráfico
    plt.tight_layout()  

    plt.show()
    st.pyplot(plt)



#função para validação de data: não permitir que seja selecionado o dia de hoje nem finais de semana:
def validar_data(data):
        """
        Função para a validação de input de datas estabelecendo restrições para que as datas escolhidas não possam ser sábado e domingo nem dias posteriores a hoje 

        param:
        data(data): data a ser validada 

        return:
        se atender as condições - mensagem de erro 
        """
        if data == pd.to_datetime('today').date():
            st.error("A data não pode ser o dia de hoje.")
        elif data.weekday() in [5, 6]:  # 5 = Sábado, 6 = Domingo
            st.error("Sábados e domingos não são permitidos.")
        elif data == pd.to_datetime('today').date():
            st.error("Datas futuras não são permitidas.")







