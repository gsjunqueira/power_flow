"""
Arquivo de configuração central do projeto de fluxo de potência.

Este módulo define constantes e parâmetros globais utilizados em diferentes
partes do sistema, permitindo ajustes centralizados e maior flexibilidade.

Autor: Giovani Santiago Junqueira
"""

from pathlib import Path

# --------------------------
# ⚙️  Parâmetros Globais
# --------------------------

# Valor artificial para tratamento da barra SWING na Jacobiana
BIG_NUMBER = 1.0  # ou 1e10 se quiser aplicar Big Number clássico

# Tolerância de convergência para o método de Newton-Raphson
TOLERANCIA_PADRAO = 1e-6

# Número máximo de iterações no Newton-Raphson
MAX_ITER_PADRAO = 20

# Diretório base
PASTA_DATA = Path("data")
PASTA_SAIDA = Path("output")

# Nome do caso (extraído do arquivo)
# NOME_CASO = "ieee14"

# Precisão numérica para exportações (quantidade de casas decimais)
CASAS_DECIMAIS_EXPORTACAO = 6

# Idioma padrão dos relatórios e exportações ('pt' ou 'en')
IDIOMA_PADRAO = "pt"
