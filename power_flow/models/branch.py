"""
Módulo que define a classe Branch.

Este módulo fornece uma representação genérica de ramos em sistemas
elétricos, podendo ser utilizados tanto para linhas de transmissão quanto
para transformadores. Inclui atributos de impedância, tap, defasagem e tipo.

Autor: Giovani Santiago Junqueira
"""

from dataclasses import dataclass
from typing import Literal

@dataclass
class Branch: # pylint: disable=too-many-instance-attributes,
    """
    Representa um ramo entre duas barras (linha ou transformador).

    Atributos:
        de (str): Nome da barra de origem.
        para (str): Nome da barra de destino.
        r (float): Resistência (pu).
        x (float): Reatância (pu).
        b (float): Susceptância total (pu).
        tipo (Literal['linha', 'trafo']): Tipo do ramo.
        tap (float): Tap, usado somente se tipo == 'trafo'.
        defasagem (float): Ângulo de defasagem (radianos), se trafo.
        status (bool): Se está ligado.
    """
    de: str
    para: str
    r: float
    x: float
    b: float
    tipo: Literal['linha', 'trafo']
    tap: float = 1.0
    defasagem: float = 0.0
    status: bool = True
