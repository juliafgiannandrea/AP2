#Para facilitar a importação de módulos dentro da estrutura do projeto 

import sys
from pathlib import Path #manipulação de caminhos de arquivos 

# Define o diretório base e o diretório backend
BASE_DIR = Path(__file__).resolve().parent.parent 
FRONT_DIR = BASE_DIR / 'frontend'
BACK_DIR = BASE_DIR / 'backend'

# Adiciona os diretórios ao sys.path
sys.path.append(str(BASE_DIR))
sys.path.append(str(FRONT_DIR))
sys.path.append(str(BACK_DIR))

print(sys.path)


#cada diretório é convertido para uma string e adicionado ao sys path
#permite que qualquer módulo ou pacote nesses diretórios seja importado de qualquer lugar no código do projeto. Isso facilita o uso de módulos internos do projeto sem precisar especificar caminhos relativos complexos.
#facilita a organização do código em módulos separados. 