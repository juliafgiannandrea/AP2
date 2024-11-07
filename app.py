import matplotlib.pyplot as plt
import sys
import os 
from pathlib import Path
import pandas as pd 
import setup_paths
import streamlit as st

# Obter o diretório do arquivo atual e configurar o caminho
BASE_DIR = Path(__file__).parent.parent.resolve()
sys.path.append(str(BASE_DIR))



# Importando as funções de renderização
from frontend.planilhao_page import render_planilhao
from frontend.estrategia_page import render_estrategia
from frontend.grafico_page import render_grafico
from frontend.doc_page import render_doc

# Título do app
st.title("AP2 - PROJETOS EM CIÊNCIA DE DADOS I")


# Definindo as páginas do app
pages = {
    "PLANILHAO": render_planilhao,
    "ESTRATEGIA": render_estrategia,
    "GRÁFICOS": render_grafico,
    "DOCUMENTAÇÃO": render_doc
}


# Menu de navegação
pagina = st.sidebar.radio("Navegação", options=list(pages.keys()))


# Renderizar a página correspondente
if pagina in pages:
    pages[pagina]()  # Chama a função associada à página selecionada
else:
    st.write("Bem-vindo à página inicial do projeto.")











