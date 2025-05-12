"""
Módulo que define a classe Line.

Este módulo representa linhas de transmissão convencionais entre duas barras
em sistemas elétricos de potência. As linhas possuem impedância série e
susceptância total, e podem ser ativadas ou desativadas.

Autor: Giovani Santiago Junqueira
"""

from dataclasses import dataclass

@dataclass
class Line:
    """
    Representa uma linha de transmissão entre duas barras.

    Atributos:
        de (str): Nome da barra de origem.
        para (str): Nome da barra de destino.
        r (float): Resistência série (pu).
        x (float): Reatância série (pu).
        b (float): Susceptância total (pu).
        tap (float): Valor do tap da linha (1.0 por padrão).
        nome (str): Nome da linha (opcional).
        status (bool): Se a linha está ligada (True) ou desligada (False).
    """
    de: str
    para: str
    r: float
    x: float
    b: float
    tap: float = 1.0
    nome: str = ""
    status: bool = True

    @property
    def z(self) -> complex:
        """
        Retorna a impedância da linha de transmissão como um número complexo.

        A impedância é calculada a partir da resistência (r) e da reatância (x) da linha, 
        segundo a fórmula: z = r + jx.

        Returns:
            complex: Impedância da linha (r + jx), em pu.
        """
        return complex(self.r, self.x)
