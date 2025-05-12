"""
Pacote principal do sistema de fluxo de potência.

Este módulo expõe as classes e funções essenciais para a leitura, modelagem e resolução do fluxo de
potência, incluindo:

- Leitura de arquivos (.pwf)
- Construção da matriz Ybus
- Geração da Jacobiana
- Resolução com o método de Newton-Raphson

Autor: Giovani Santiago Junqueira
"""

__version__ = "0.1.0"

# Exposição das principais classes do pacote
from .readers.reader_pwf import ReaderPwf
from .ybus import Ybus
from .solver import Jacobian
from .newtonraphson import NewtonRaphson

__all__ = [
    "ReaderPwf",
    "Ybus",
    "Jacobian",
    "NewtonRaphson",
]
