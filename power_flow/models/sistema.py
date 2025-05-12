"""
Módulo que define a classe Sistema para consolidar os componentes elétricos
e organizar os dados necessários à resolução do fluxo de potência.

A classe Sistema encapsula a topologia e os dados elétricos do sistema, incluindo:
- Lista de barras, linhas de transmissão e transformadores
- Construção automática da matriz de admitância nodal (Ybus)
- Cálculo das potências especificadas (geração - carga)
- Estruturação de um DataFrame padronizado das barras (df_bus)

Essa abordagem promove modularidade, clareza e facilidade de extensão,
facilitando o uso integrado em métodos iterativos como Newton-Raphson.

Autor: Giovani Santiago Junqueira
"""

# pylint: disable=too-few-public-methods

from typing import List
import pandas as pd
from power_flow.models import Bus, Line, Transformer
from power_flow.ybus import Ybus

class Sistema:
    """
    Classe que representa o sistema elétrico de potência, consolidando as estruturas
    de barras, linhas, transformadores e admitância nodal (Ybus).

    Ao ser instanciada, esta classe:
        - Armazena os modelos físicos (barras, linhas, transformadores)
        - Constrói automaticamente a matriz Ybus
        - Calcula as potências especificadas (Pg - Pl, Qg - Ql)
        - Constrói um DataFrame padronizado das barras (df_bus)

    Atributos:
        barras (List[Bus])
        linhas (List[Line])
        transformadores (List[Transformer])
        ybus (np.ndarray): Matriz de admitância nodal
        df_bus (pd.DataFrame): Tabela das barras formatada para uso no fluxo
    """

    def __init__(self, barras: List[Bus], linhas: List[Line], transformadores: List[Transformer],
                 nome="sistema"):
        self.barras = barras
        self.linhas = linhas
        self.transformadores = transformadores
        self.nome = nome
        self.base_mva: float = 100.0
        # Extrai todos os shunts associados diretamente às barras
        self.shunts = []
        for b in barras:
            barra_shunts = getattr(b, "shunts", None)
            if barra_shunts:
                if isinstance(barra_shunts, list):
                    self.shunts.extend(barra_shunts)
                else:
                    self.shunts.append(barra_shunts)

        # Montagem da matriz Ybus
        self.ybus = Ybus(linhas, transformadores, barras, self.shunts)

        # Cria DataFrame padronizado para uso no NR
        self.df_bus = pd.DataFrame([
            {
                'barra': b.nome,
                'tipo': [b.tipo], # {'PQ': 0, 'PV': 1, 'SWING': 2}
                'V': b.v,
                'Theta': b.theta,
                'Pg': sum(g.p for g in b.geradores),
                'Qg': sum(g.q for g in b.geradores),
                'Qm': max((g.qmax for g in b.geradores), default=None),
                'Qn': min((g.qmin for g in b.geradores), default=None),
                'Pl': sum(c.p for c in b.cargas),
                'Ql': sum(c.q for c in b.cargas),
                'sh': b.bsh_total
            } for b in barras
        ]).set_index('barra')
        # Calcula potência especificada por barra (P_esp = Pg - Pl, Q_esp = Qg - Ql)
        self.df_bus["P_esp"] = self.df_bus["Pg"] - self.df_bus["Pl"]
        self.df_bus["Q_esp"] = self.df_bus["Qg"] - self.df_bus["Ql"]

    def atualizar_resultados(self, V, theta): # pylint: disable=invalid-name
        """
        Atualiza os vetores de módulo e ângulo de tensão no DataFrame df_bus
        e nos objetos do tipo Bus associados ao sistema.

        Args:
            V (np.ndarray): Vetor de tensões (pu).
            theta (np.ndarray): Vetor de ângulos (rad).
        """
        for barra in self.barras:
            self.df_bus.loc[barra.nome, 'V'] = V[barra.nome]
            self.df_bus.loc[barra.nome, 'Theta'] = theta[barra.nome]
            barra.v = V[barra.nome]
            barra.theta = theta[barra.nome]

    @property
    def pot_esp(self):
        """
        Retorna a potência especificada (geração - carga) por barra.
        """
        return self.df_bus[["P_esp", "Q_esp"]]
