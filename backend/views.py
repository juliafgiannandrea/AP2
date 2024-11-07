#Importa as bibliotecas e funções:
import pandas as pd
from datetime import date
import os
import logging
logger = logging.getLogger(__name__)
import sys 



#Importar as funções criadas no outro arquivo, que pegam as APIs 
from backend.apis import(pegarPlanilhao,
                          get_preco_corrigido)

#Processamento e consulta dos dados do planilhão: seleção das 3 primeiras letras do ticker 

def pegar_df_planilhao(data_base:date) -> pd.DataFrame:
    """
    Consulta todas as ações com os principais indicadores fundamentalistas

    params:
    data_base (date): Data Base para o cálculo dos indicadores.

    return:
    df (pd.DataFrame): DataFrame com todas as Ações.
    """
    dados = pegarPlanilhao(data_base)
    if dados: #para verificar se a variável dados não é vazia. 
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




#Colocar essa função dentro da pegarPlanilhao no arquivo apis??? 


#Usar o volume para remover as ações que tem as 3 primeiras letras iguais (são a mesma ação)
#de acordo com algum parâmetro informado - filtrar o data frame fornecido 
#remover linhas duplicadas baseadas em uma coluna escolhida, priorizando o valor mais alto dessa coluna para manter apenas uma ocorrência de cada empresa

def filtrar_duplicado(df:pd.DataFrame, meio:str = None) -> pd.DataFrame:
    """
    Filtra o df das ações duplicados baseado no meio escolhido. 

    params:
    df (pd.DataFrame): dataframe com os ticker duplicados 
    meio (str): campo escolhido para escolher qual ticker escolher (default: volume) 
    O valor padrão do argumento meio é volume, a não ser que outro seja indicado, o argumento usado para filtrar o df será o volume das ações 

    return:
    (pd.DataFrame): dataframe com os ticker filtrados.
    """

    meio = meio or 'volume'
    df_dup = df[df.empresa.duplicated(keep=False)]  #cria um df que contém apenas as linhas duplicadas na coluna empresa 
    lst_dup = df_dup.empresa.unique() # extrai desse df acima uma lista de empresa duplicadas 
    lst_final = [] #para adicionar as ações que serão mantidas 
    for tic in lst_dup:
        tic_dup = df_dup[df_dup.empresa==tic].sort_values(by=[meio], ascending=False)['ticker'].values[0]  
#seleciona as duplicatas de uma empresa específica e ordena pelo valor na coluna meio em ordem decrescente. - pego o values[0], que é a ação de maior meio
        lst_final = lst_final + [tic_dup] # add na lista vazia a ação que tem maior valor de meio  
    lst_dup = df_dup[~df_dup.ticker.isin(lst_final)]['ticker'].values #lista das ações duplicadas que foram removidas 
    #registrar e printar a lista com os nomes das ações removidas 
    logger.info(f"Ticker Duplicados Filtrados: {lst_dup}")
    print(f"Ticker Duplicados Filtrados: {lst_dup}")
    return df[~df.ticker.isin(lst_dup)] # data frame sem as ações repetidas ( como se isin por causa do ~ virasse in not in)
# ~ é um operador bitwise NOT ---> inverte uma condição booleana === transforma em True os elementos que não estão em lst_dup.



#seleção de ações de acordo com um indicador

### dar um valor para a quantidade de ações que vc quer pegar 
### colocar restrição de num (até um valor máximo)

def carteira(data, indicador_rent, indicador_desc, num):
    df = pegar_df_planilhao(data)
    quero = ["ticker","setor","data_base","roc", "roe", "roic","earning_yield","dividend_yield","p_vp"]
    df = df[quero]
    
    #rentabilidade:
    df_rent = df.nlargest(1000,indicador_rent).reset_index(drop = True)
    df_rent['index_rent'] = df_rent.index #coluna index top indicador 
    
       

    #desconto:
    df_desc = df.nlargest(1000,indicador_desc).reset_index(drop = True)
    df_desc['index_desc'] = df_desc.index #coluna index top indicador 



    #juntar os dois data frames somando a coluna index: 
    df_merged  = pd.merge(df_desc[["ticker", "index_desc"]], 
                      df_rent[["ticker", "index_rent"]], 
                      on = "ticker", 
                      how = "inner")
    df_merged["media"] = df_merged["index_desc"] + df_merged["index_rent"]
    df_sorted = df_merged.sort_values(by=['media'], ascending=[True])
    df_sorted = df_sorted.nlargest(num,'media').reset_index(drop = True) ## colocar algo aqui para o ranking começar em 1 ao invés de 0! 
    df_final = df_sorted['ticker']

    return df_final
   


#TESTE: 
carteira('2023-04-03', 'roe', 'earning_yield',10)




def pegar_df_preco_corrigido(data_ini:date, data_fim:date, carteira:list) -> pd.DataFrame:
    """
    Consulta os preços Corrigidos de uma lista de ações

    params:
    data_ini (date): data inicial da consulta
    data_fim (date): data final da consulta
    carteira (list): lista de ativos a serem consultados

    return:
    df_preco (pd.DataFrame): dataframe com os preços do período dos ativos da lista
    """
    df_preco = pd.DataFrame()
    for ticker in carteira:
        dados = get_preco_corrigido(data_ini, data_fim, ticker)
        if dados:
            dados = dados.json()['dados']
            df_temp = pd.DataFrame.from_dict(dados) # converte os dados num df temporário para o ativo atual 
            df_preco = pd.concat([df_preco, df_temp], axis=0, ignore_index=True) #
            logger.info(f'{ticker} finalizado!')
            print(f'{ticker} finalizado!')   
        else:
            logger.error(f"Sem Preco Corrigido: {ticker}")
            print(f"Sem Preco Corrigido: {ticker}")
    return df_preco

## não entendi do porque criar um data frame temporário e depois concatená-lo. 



#testes:
pegar_df_planilhao("2023-04-03")


#qual data frame eu dou como argumento para a função, pq deve ser o df resultante do pegar_df_planilhao
#filtrar_duplicado(df,'volume')



#não ta pegando!!!!
pegar_df_preco_corrigido('2023-01-02-',  '2023-03-31', ['PETR4'])

