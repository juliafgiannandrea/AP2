#Caminho das pastas que são utilizadas e  onde os logs serão salvos:

    #Configura caminhos base para separar a parte de backend e frontend E define um sistema de logs com formato e nível de registro ajustados, salvando as mensagens em um arquivo de log (app.log)
import os 
import logging 
from pathlib import Path #manipulação de caminhos

#BASE_DIR: armazena o diretório onde o arquivo de configuração está localizado

# Obter o diretório do arquivo atual e configurar o caminho

#varáveis que armazenam os caminhos dos diretórios backend e frontend
BASE_DIR = Path(__file__).parent.resolve()
BACK_DIR = str(BASE_DIR) + '/backend'
FRONT_DIR = str(BASE_DIR) + '/frontend'


#Configuração dos sistema de logs:
logging.basicConfig(level = logging.INFO,
                    format = '%(asctime)s -  %(name)s - %(levelname)s %(message)s',
                    filename = f'logs/app.log', #NOME DO ARQUIVO LOG
                    filemode = "a")



#salvar os logs num logfile:
#level > set the level to INFO / pode ser qualquer argumento aqui
#file name > onde serão salvas as mensagens de log 
#format para incluir na mensagem:  date, time, level name, module name, line number, and the log message