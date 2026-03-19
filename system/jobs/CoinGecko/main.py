import sys
import os

# adiciona a raiz do projeto ao path pra encontrar main_root
raiz_projeto = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.insert(0, raiz_projeto)

from main_root import main

main()
