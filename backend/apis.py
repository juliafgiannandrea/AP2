#Criação de funções para pegar todas as apis:

#Importação das bibliotecas: 
import requests
import pandas as pd 

#Logging:
import logging
logger = logging.getLogger(__name__) 

#Carregar variáveis de ambiente a partir de um arquivo .env para o ambiente de execução do Python, usando a biblioteca python-dotenv 
from dotenv import load_dotenv
load_dotenv()

#token de acesso lab das finanças: COLOCAR NO .ENV 
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMyNDQ4MDcyLCJqdGkiOiI5YjBlZjFmMzY4MTk0OGUzYjU3ZGM1ZGU3YmI5YTQ4YyIsInVzZXJfaWQiOjM5fQ.xaDuWahZonD9C0v-4zKLk6CEtNg9s8Ohp9hhoLU3qwA"

#Permissão de acesso: 
headers = {'Authorization': 'JWT {}'.format(token)}


#função para pegar a API do planilhão: 
def pegarPlanilhao(data):
    """
    Função que puxa os dados do Planilhão da API do laboratório das finanças e retorna um data frame dos dados. 

    param: data. A função recebe como argumento uma data (que é a data a partir da qual os dados das ações serão obtidos). Essa data será informada pelo usuário no frontend. 

    output: dicionário oriundo da API do planilhão na data informada. 
    """
    params = {'data_base': data} 
    try: 
        #data vai ser fornecido pelo usuário - as seleções do site 
        r = requests.get('https://laboratoriodefinancas.com/api/v1/planilhao',params=params, headers=headers)
        if r.status_code == 200:
            planilhao = r.json()
            logger.info(f"API acessada com sucesso: {data}")
            print(f"API acessada com sucesso: {data}")
            return planilhao
        else:
            logger.warning(f"Não foi possível acessar a API {data}")
            print(f"Erro no acesso ao Planilhão {data}")
    except Exception as e:
        logger.error(f"Erro técnico {e}")
        print(f"Erro técnico {e}")

    

#pegarPlanilhao('2023-04-03') #exemplo de uso da função 

#Para pegar a api do preço corrigido: 
def get_preco_corrigido(ticker, data_ini, data_fim):
    
    """
     Função que puxa os dados da planilha Preço Corrigido da API do laboratório das finanças e retorna um dicionário destes dados. 

    param: parâmetros serão informados pelo usuário no frontend 
        ticker: nome da ação que você quer puxar os dados 
        data_ini: data de início do período que você quer puxar os dados 
        data_fim: data de fim do período que você quer puxar os dados 

    output: dicionário oriundo da api do preço corrigifo da ação e na data informadas. 
    """

    params = {
'ticker': ticker,
'data_ini': data_ini,
'data_fim': data_fim}
    try:
        r = requests.get('https://laboratoriodefinancas.com/api/v1/preco-corrigido',params=params, headers=headers)
        if r.status_code == 200:
            preco_corrigido = r.json()
            logger.info(f"API acessada com sucesso: {ticker}")
            print(f"API acessada com sucesso: {ticker}")
            return(preco_corrigido)
        else:
            logger.warning(f"Não foi possível acessar a API{ticker}")
            print(f"Erro no acesso ao Preço Corrigido {ticker}")
    except Exception as e:
        logger.error(f"Erro técnico{e}")


get_preco_corrigido('PETR4', '2023-01-01', '2023-01-31' ) #exemplo de uso da função para pegar preço corrigido



