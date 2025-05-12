"""
Módulo que define a classe Shunt.

Este módulo representa elementos shunt conectados diretamente a barras
em sistemas elétricos, geralmente utilizados para controle de tensão
ou compensação reativa (capacitores ou reatores).

Autor: Giovani Santiago Junqueira
"""

from dataclasses import dataclass

@dataclass
class Shunt:
    """
    Representa um elemento shunt conectado a uma barra.

    Atributos:
        barra (str): Nome ou identificador da barra associada.
        b (float): Susceptância shunt (pu). Valor positivo para capacitor,
                   negativo para reator.
        status (bool): Indica se o elemento shunt está ativo no sistema.
    """
    barra: str
    b: float
    status: bool = True
