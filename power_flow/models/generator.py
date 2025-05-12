"""
Módulo que define a classe Generator.

Cada instância representa um gerador conectado a uma barra do sistema elétrico.
Inclui potência gerada, limites operacionais e identificação da barra associada.
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class Generator:
    """
    Representa um gerador conectado a uma barra do sistema.

    Atributos:
        id (int): Identificador único do gerador.
        barra (str): Nome da barra à qual o gerador está conectado.
        p (float): Potência ativa gerada (pu).
        q (float): Potência reativa gerada (pu).
        qmin (Optional[float]): Limite inferior de Q (pu).
        qmax (Optional[float]): Limite superior de Q (pu).
        
    Autor: Giovani Santiago Junqueira
    """
    id: int
    barra: str
    p: float = 0.0
    q: float = 0.0
    qmin: Optional[float] = None
    qmax: Optional[float] = None
