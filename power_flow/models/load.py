"""
Módulo que define a classe Load.

Cada instância representa uma carga conectada a uma barra do sistema elétrico.
Inclui potência ativa e reativa consumida, e identificação da barra associada
por número e nome.
"""

from dataclasses import dataclass

@dataclass
class Load:
    """
    Representa uma carga conectada a uma barra.

    Atributos:
        nome (str): Nome identificador da barra (string).
        barra (int): Número da barra à qual a carga está conectada.
        p (float): Potência ativa consumida (pu).
        q (float): Potência reativa consumida (pu).
        
    Autor: Giovani Santiago Junqueira
    """
    nome: str
    barra: int
    p: float = 0.0
    q: float = 0.0
