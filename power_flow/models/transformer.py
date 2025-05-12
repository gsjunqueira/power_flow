"""
Módulo que define a classe Transformer.

Este módulo representa transformadores entre duas barras, com possibilidade
de inclusão de tap e ângulo de fase. Permite modelagem de transformadores
defasados ou com controle de tensão.

Autor: Giovani Santiago Junqueira
"""

from dataclasses import dataclass

@dataclass
class Transformer:
    """
    Representa um transformador entre duas barras, incluindo tap e fase.

    Atributos:
        de (str): Barra primária.
        para (str): Barra secundária.
        nome (str): Nome identificador do transformador (gerado automaticamente).
        r (float): Resistência (pu).
        x (float): Reatância (pu).
        tap (float): Relação de tap (default = 1.0).
        fase (float): Ângulo de fase (radianos, default = 0.0).
        status (bool): Se está em operação.
    """
    de: str
    para: str
    nome: str = ""
    r: float =0.0
    x: float = 0.01
    b: float = 0.0
    tap: float = 1.0
    fase: float = 0.0
    status: bool = True

    @property
    def z(self) -> complex:
        """
        Retorna a impedância de transformadores como um número complexo.

        A impedância é calculada a partir da resistência (r) e da reatância (x) da linha, 
        segundo a fórmula: z = r + jx.

        Returns:
            complex: Impedância da linha (r + jx), em pu.
        """
        return complex(self.r, self.x)
