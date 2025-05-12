# pylint: disable=invalid-name, line-too-long

"""
Módulo responsável pelo cálculo do balanço de potência em barras de sistemas elétricos.

Fornece funções auxiliares para:
- Cálculo das potências injetadas (P, Q) a partir da matriz Ybus, tensões e ângulos.
- Cálculo dos resíduos de potência ativa (ΔP) e reativa (ΔQ) com base nas potências especificadas.

Essas funções são utilizadas no método de Newton-Raphson para fluxo de potência.

Autor: Giovani Santiago Junqueira
"""

from numpy import cos, sin
import pandas as pd

def calc_injected_power(Ybus: pd.DataFrame, V: pd.Series, theta: pd.Series) -> tuple[pd.Series, pd.Series]:
    """
    Calcula as potências ativa (P) e reativa (Q) injetadas em cada barra do sistema.

    Args:
        Ybus (pd.DataFrame): Matriz de admitância nodal.
        V (pd.Series): Módulo das tensões (pu), indexado por nome da barra.
        theta (pd.Series): Ângulo das tensões (rad), indexado por nome da barra.

    Returns:
        tuple:
            - P (pd.Series): Potência ativa injetada (pu).
            - Q (pd.Series): Potência reativa injetada (pu).
    """
    G = Ybus.map(lambda z: z.real)
    B = Ybus.map(lambda z: z.imag)
    P = pd.Series(0.0, index=V.index)
    Q = pd.Series(0.0, index=V.index)
    ordem = V.index
    G = G.loc[ordem, ordem]
    B = B.loc[ordem, ordem]
    assert list(G.index) == list(V.index), "Erro: índices de G e V não coincidem"
    assert list(B.index) == list(V.index), "Erro: índices de B e V não coincidem"
    assert list(theta.index) == list(V.index), "Erro: índices de theta e V não coincidem"
    for k in V.index:
        for m in V.index:
            theta_km = theta[k] - theta[m]
            P[k] += V[k] * V[m] * (G.loc[k, m] * cos(theta_km) + B.loc[k, m] * sin(theta_km))
            Q[k] += V[k] * V[m] * (G.loc[k, m] * sin(theta_km) - B.loc[k, m] * cos(theta_km))

    return P, Q

def calc_delta_p(P: pd.Series, pot_esp: pd.DataFrame, index: list[str], swing: list[str]) -> pd.Series:
    """
    Calcula o vetor de resíduos de potência ativa (ΔP).

    Args:
        P (pd.Series): Potências ativas injetadas calculadas.
        pot_esp (pd.DataFrame): DataFrame com colunas ['P_esp', 'Q_esp'], indexado por nome da barra.
        index (list[str]): Barras com ângulo variável.
        swing (list[str]): Barras tipo SWING.

    Returns:
        pd.Series: Vetor de ΔP.
    """
    delta_P = pd.Series(index=index, dtype=float)

    for barra in index:
        try:
            delta_P[barra] = pot_esp.loc[barra, "P_esp"] - P[barra]
        except KeyError as exc:
            raise KeyError(f"Barra '{barra}' não encontrada em pot_esp") from exc


    print(index)
    print(swing)
    for barra in swing:
        if barra in delta_P:
            delta_P[barra] = 0.0

    return delta_P

def calc_delta_q(Q: pd.Series, pot_esp: pd.DataFrame, pq: list[str], swing: list[str]) -> pd.Series:
    """
    Calcula o vetor de resíduos de potência reativa (ΔQ).

    Args:
        Q (pd.Series): Potências reativas injetadas calculadas.
        pot_esp (pd.DataFrame): DataFrame com colunas ['P_esp', 'Q_esp'], indexado por nome da barra.
        pq (list[str]): Barras PQ.
        swing (list[str]): Barras SWING.

    Returns:
        pd.Series: Vetor de ΔQ.
    """
    barras_q = swing + pq
    delta_Q = pd.Series(index=barras_q, dtype=float)

    for barra in barras_q:
        try:
            delta_Q[barra] = pot_esp.loc[barra, "Q_esp"] - Q[barra]
        except KeyError as exc:
            raise KeyError(f"Barra '{barra}' não encontrada em pot_esp") from exc

    for barra in swing:
        if barra in delta_Q:
            delta_Q[barra] = 0.0

    return delta_Q
