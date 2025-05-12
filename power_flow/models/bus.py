"""
Módulo que define a classe Bus (barra do sistema elétrico).

Cada barra armazena apenas os dados estruturais e elétricos fundamentais.
As potências gerada e consumida são delegadas aos modelos Generator e Load,
que podem ser associados posteriormente a cada barra.

    Autor: Giovani Santiago Junqueira
"""

from dataclasses import dataclass, field
from typing import List
from power_flow.models.generator import Generator
from power_flow.models.load import Load
from power_flow.models.shunt import Shunt

@dataclass
class Bus:
    """
    Classe que representa uma barra no sistema elétrico.

    Atributos:
        numero (int): Identificador da barra.
        tipo (str): Tipo da barra ('PQ', 'PV', 'SWING').
        v (float): Módulo da tensão (pu).
        theta (float): Ângulo da tensão (radianos).
        bsh (float): Susceptância shunt conectada à barra (pu).
        geradores (list[Generator]): Lista de geradores conectados à barra.
        cargas (list[Load]): Lista de cargas conectadas à barra.
    """
    numero: int
    tipo: str
    nome: str
    v: float
    theta: float
    geradores: List[Generator] = field(default_factory=list)
    cargas: List[Load] = field(default_factory=list)
    shunts: List[Shunt] = field(default_factory=list)

    @property
    def p_esp(self) -> float:
        """Potência ativa líquida (soma dos geradores menos soma das cargas)."""
        pg_total = sum(g.p for g in self.geradores)
        pl_total = sum(c.p for c in self.cargas)
        return pg_total - pl_total

    @property
    def q_esp(self) -> float:
        """Potência reativa líquida (soma dos geradores menos soma das cargas)."""
        qg_total = sum(g.q for g in self.geradores)
        ql_total = sum(c.q for c in self.cargas)
        return qg_total - ql_total

    @property
    def bsh_total(self) -> float:
        """
        Soma total da susceptância shunt associada à barra.
        """
        if self.shunts is None:
            return 0.0
        return sum(s.b for s in self.shunts)
