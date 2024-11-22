#Criação de funções para pegar todas as apis:

#Importação das bibliotecas: 
import requests
import pandas as pd 
import os
import streamlit as st 
#Logging:
import logging
logger = logging.getLogger(__name__) 

#Carregar variáveis de ambiente a partir de um arquivo .env para o ambiente de execução do Python, usando a biblioteca python-dotenv 
from dotenv import load_dotenv
load_dotenv()

#token: desse jeito para rodar no streamlit (st.secrets)

token = os.getenv("token")
if not token:
    logger.error("Token de acesso não encontrado no ambiente.")
    raise ValueError("Token de acesso não encontrado.")

#Permissão de acesso: 
headers = {'Authorization': 'JWT {}'.format(token)}

#função para pegar a API do planilhão: 
def pegarPlanilhao(data):
    """
    Função que puxa os dados do Planilhão da API do laboratório das finanças. 

    param:
    data(date): Data a partir da qual os dados das ações serão obtidos. Essa data será informada pelo usuário no frontend. 

    return: 
    planilhao (dict): dicionário oriundo da API do planilhão na data informada. 
    """
    params = {'data_base': data} 
    try: 
        #data vai ser fornecido pelo usuário - as seleções do site 
        r = requests.get('https://laboratoriodefinancas.com/api/v1/planilhao',params=params, headers=headers)
        if r.status_code == 200:
            planilhao = r.json()
            logger.info(f"API do Planilhão acessada com sucesso: {data}")
            print(f"API do Planilhão acessada com sucesso: {data}")
            return planilhao
        else:
            logger.warning(f"Não foi possível acessar a API do Planilhão {data}")
            print(f"Erro no acesso ao Planilhão {data}")
    except Exception as e:
        logger.error(f"Erro técnico {e}")
        print(f"Erro técnico {e}")
  
#pegarPlanilhao('2023-04-03') #exemplo de uso da função 

#Para pegar a api do preço corrigido: 
def get_preco_corrigido(ticker, data_ini, data_fim):
    
    """
    Função que puxa os dados da planilha Preço Corrigido da API do laboratório das finanças. 

    param: parâmetros serão informados pelo usuário no frontend 
        ticker(str): nome da ação que você quer puxar os dados 
        data_ini(date): data de início do período que você quer puxar os dados 
        data_fim (date): data de fim do período que você quer puxar os dados 

    return: 
        preco_corrigido (dict): dicionário oriundo da api do preço corrigido da ação nas datas informadas. 
    """

    params = {
'ticker': ticker,
'data_ini': data_ini,
'data_fim': data_fim}
    try:
        r = requests.get('https://laboratoriodefinancas.com/api/v1/preco-corrigido',params=params, headers=headers)
        if r.status_code == 200:
            preco_corrigido = r.json()
            logger.info(f"API do Preço Corrigido acessada com sucesso: {ticker}")
            print(f"API do Preço Corrigido acessada com sucesso: {ticker}")
            return preco_corrigido
        else:
            logger.warning(f"Não foi possível acessar a API do Preço Corrigido: {ticker}")
            print(f"Erro no acesso ao Preço Corrigido: {ticker}")
    except Exception as e:
        logger.error(f"Erro técnico{e}")
        print(f"Erro técnico {e}")

#get_preco_corrigido('PETR4', '2023-01-01', '2023-01-31' ) #teste de uso da função para pegar preço corrigido


#Calcular o IBOVESPA do período: ticker = ibov 

def get_preco_diversos(data_ini, data_fim, ticker):
    """
    Função que puxa os dados da planilha Preços Diversos da API do laboratório das finanças. 

    param: parâmetros serão informados pelo usuário no frontend 
        data_ini(date): data de início do período que você quer puxar os dados 
        data_fim (date): data de fim do período que você quer puxar os dados 
        ticker (str): nome da ação para puxar os dados. Para essa API o nome da ação deve ser sempre 'ibov'

    return:
        response_ibov (dict): dicionário oriundo da api dos preços diversos nas datas informadas.
    """
    params_ibov = {'ticker': {ticker}, 
'data_ini': {data_ini},
'data_fim': {data_fim} }
    try:
        ibovespa = requests.get('https://laboratoriodefinancas.com/api/v1/preco-diversos', params=params_ibov, headers=headers)
        if ibovespa.status_code == 200:
            response_ibov = ibovespa.json() 
            logger.info(f"API dos Preços Diversos acessada com sucesso: {ticker}")
            print(f"API dos Preços Diversos acessada com sucesso: {ticker}")
            return response_ibov
        else:
            logger.warning(f"Não foi possível acessar a API dos Preços Diversos: {ticker}")
            print(f"Erro no acesso ao Preços Diversos: {ticker}")
    except Exception as e:
        logger.error(f"Erro técnico{e}")
        print(f"Erro técnico {e}")

#get_preco_diversos('2023-01-01', '2023-01-31', 'ibov') #teste de uso da função para pegar preços diversos