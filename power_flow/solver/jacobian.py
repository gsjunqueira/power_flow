"""
Módulo responsável pela construção da matriz Jacobiana para o método de Newton-Raphson
utilizado na resolução do fluxo de potência em sistemas elétricos.

Este módulo implementa a classe `Jacobian`, que organiza e calcula a Jacobiana completa
através da composição das quatro submatrizes fundamentais:

    - H: Derivadas de ΔP em relação aos ângulos de tensão (θ)
    - N: Derivadas de ΔP em relação aos módulos de tensão (V)
    - M: Derivadas de ΔQ em relação aos ângulos de tensão (θ)
    - L: Derivadas de ΔQ em relação aos módulos de tensão (V)

O tratamento da barra SWING é feito utilizando o artifício do Big Number, o que implica
em forçar os resíduos das variáveis associadas à barra de referência a zero e modificar
a Jacobiana de forma coerente.

Este módulo assume que os vetores e matrizes de entrada (tensões, admitâncias e potências)
já foram previamente calculados e organizados como pandas Series e DataFrames indexados
pelos nomes das barras.

Autor: Giovani Santiago Junqueira
"""
# pylint: disable=invalid-name, too-many-instance-attributes, too-few-public-methods, too-many-arguments, too-many-positional-arguments, line-too-long

from numpy import cos, sin, hstack, vstack, zeros
import pandas as pd
from config import BIG_NUMBER

class Jacobian:
    """
    Classe responsável pela montagem da matriz Jacobiana para o fluxo de potência,
    dividida em submatrizes H, N, M e L.

    A Jacobiana é composta pelas seguintes submatrizes:
        - H: Derivadas de ΔP em relação a θ (ângulos de tensão)
        - N: Derivadas de ΔP em relação a V (módulos de tensão)
        - M: Derivadas de ΔQ em relação a θ
        - L: Derivadas de ΔQ em relação a V

    As variáveis de entrada são pandas Series/DataFrames indexados por nomes das barras.
    O tratamento da barra SWING é feito utilizando o artifício do Big Number.

    Atributos:
        V (pd.Series): Módulos de tensão (pu) por barra.
        theta (pd.Series): Ângulos de tensão (rad) por barra.
        G (pd.DataFrame): Matriz de condutâncias.
        B (pd.DataFrame): Matriz de susceptâncias.
        P (pd.Series): Potências ativas calculadas.
        Q (pd.Series): Potências reativas calculadas.
        pq, pv, swing, index (list[str]): Conjuntos de barras.
        J (np.ndarray): Matriz Jacobiana resultante.
    """
    def __init__(self, V: pd.Series, theta: pd.Series,
                G: pd.DataFrame, B: pd.DataFrame,
                P: pd.Series, Q: pd.Series,
                pq: list[str], pv: list[str], swing: list[str], index: list[str]):
        """
        Inicializa a Jacobiana com os dados do sistema.

        Args:
            V (pd.Series): Módulos de tensão indexados por nome de barra.
            theta (pd.Series): Ângulos de tensão indexados por nome de barra.
            G (pd.DataFrame): Matriz de condutâncias (nome x nome).
            B (pd.DataFrame): Matriz de susceptâncias (nome x nome).
            P (pd.Series): Potências ativas calculadas por barra.
            Q (pd.Series): Potências reativas calculadas por barra.
            pq (list[str]): Lista de barras PQ.
            pv (list[str]): Lista de barras PV.
            swing (list[str]): Lista de barras SWING.
            index (list[str]): Ordem completa das variáveis angulares.
        """
        self.V = V
        self.theta = theta
        self.G = G
        self.B = B
        self.P = P
        self.Q = Q
        self.pq = pq
        self.pv = pv
        self.swing = swing
        self.index = index
        self.J = self._build()

    def _build(self):
        """
        Constrói a matriz Jacobiana completa a partir das submatrizes H, N, M e L.

        Returns:
            np.ndarray: Matriz Jacobiana completa.
        """
        H = self._build_H()
        N = self._build_N()
        M = self._build_M()
        L = self._build_L()
        upper = hstack((H, N))
        lower = hstack((M, L))
        return vstack((upper, lower))

    def _build_H(self):
        """
        Constrói a submatriz H da Jacobiana, correspondente às derivadas parciais
        das potências ativas ΔP em relação aos ângulos de tensão θ.

        Returns:
            np.ndarray: Submatriz H da Jacobiana.
        """
        H = zeros((len(self.index), len(self.index)))
        for i, k in enumerate(self.index):
            for j, m in enumerate(self.index):
                if k in self.swing or m in self.swing:
                    H[i, j] = BIG_NUMBER if k == m else 0.0
                elif k == m:
                    H[i, j] = -self.Q.loc[k] - (self.V.loc[k] ** 2) * self.B.loc[k, k]
                else:
                    theta_km = self.theta.loc[k] - self.theta.loc[m]
                    H[i, j] = self.V.loc[k] * self.V.loc[m] * (
                        self.G.loc[k, m] * sin(theta_km) -
                        self.B.loc[k, m] * cos(theta_km)
                    )
        return H

    def _build_N(self):
        """
        Constrói a submatriz N da Jacobiana, correspondente às derivadas parciais
        das potências ativas ΔP em relação aos módulos de tensão V.

        Returns:
            np.ndarray: Submatriz N da Jacobiana.
        """
        colunas = self.swing + self.pq
        N = zeros((len(self.index), len(colunas)))
        for i, k in enumerate(self.index):
            for j, m in enumerate(colunas):
                if k in self.swing or m in self.swing:
                    N[i, j] = 0.0
                elif k == m:
                    N[i, j] = (self.P.loc[k] + (self.V.loc[k] ** 2) * self.G.loc[k, k]) / self.V.loc[k]
                else:
                    theta_km = self.theta.loc[k] - self.theta.loc[m]
                    N[i, j] = self.V.loc[k] * (
                        self.G.loc[k, m] * cos(theta_km) +
                        self.B.loc[k, m] * sin(theta_km)
                    )
        return N

    def _build_M(self):
        """
        Constrói a submatriz M da Jacobiana, correspondente às derivadas parciais
        das potências reativas ΔQ em relação aos ângulos de tensão θ.

        Returns:
            np.ndarray: Submatriz M da Jacobiana.
        """
        linhas = self.swing + self.pq
        M = zeros((len(linhas), len(self.index)))
        for i, k in enumerate(linhas):
            for j, m in enumerate(self.index):
                if k in self.swing or m in self.swing:
                    M[i, j] = 0.0
                elif k == m:
                    M[i, j] = self.P.loc[k] - (self.V.loc[k] ** 2) * self.G.loc[k, k]
                else:
                    theta_km = self.theta.loc[k] - self.theta.loc[m]
                    M[i, j] = -self.V.loc[k] * self.V.loc[m] * (
                        self.G.loc[k, m] * cos(theta_km) +
                        self.B.loc[k, m] * sin(theta_km)
                    )
        return M

    def _build_L(self):
        """
        Constrói a submatriz L da Jacobiana, correspondente às derivadas parciais
        das potências reativas ΔQ em relação aos módulos de tensão V.

        Returns:
            np.ndarray: Submatriz L da Jacobiana.
        """
        colunas = self.swing + self.pq
        L = zeros((len(colunas), len(colunas)))
        for i, k in enumerate(colunas):
            for j, m in enumerate(colunas):
                if k in self.swing or m in self.swing:
                    L[i, j] = BIG_NUMBER if k == m else 0.0
                elif k == m:
                    L[i, j] = (self.Q.loc[k] - (self.V.loc[k] ** 2) * self.B.loc[k, k]) / self.V.loc[k]
                else:
                    theta_km = self.theta.loc[k] - self.theta.loc[m]
                    L[i, j] = self.V.loc[k] * (
                        self.G.loc[k, m] * sin(theta_km) -
                        self.B.loc[k, m] * cos(theta_km)
                    )
        return L
