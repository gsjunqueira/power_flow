"""
Módulo responsável pela aplicação das correções calculadas (Δθ e ΔV)
aos vetores de estado do sistema (angulos e tensões), conforme o método
de Newton-Raphson.

Este módulo assume a presença da barra SWING tratada via Big Number, e
a organização dos índices na ordem: SWING → PV → PQ.

A função `apply_delta` aplica as correções extraídas do vetor delta
ao estado atual do sistema elétrico, utilizando a função auxiliar
`split_corrections` para separar Δθ e ΔV.

Autor: Giovani Santiago Junqueira
"""

# pylint: disable=too-many-arguments, too-many-positional-arguments, invalid-name

import pandas as pd
import numpy as np
from power_flow.solver.residuals import split_corrections

def apply_delta(theta: pd.Series, V: pd.Series, delta: np.ndarray,
                index: list[str], swing: list[str], pq: list[str]) -> tuple[pd.Series, pd.Series]:
    """
    Aplica o vetor de correções `delta` aos vetores de estado do sistema: ângulo (theta) e
    módulo (V).

    A estrutura do vetor `delta` é:
        - Δθ para barras SWING + PV + PQ (index)
        - ΔV para barras SWING + PQ (swing + pq)

    Args:
        theta (pd.Series): Vetor de ângulos de tensão (rad), indexado por nome.
        V (pd.Series): Vetor de módulos de tensão (pu), indexado por nome.
        delta (np.ndarray): Vetor completo de correções (Δθ + ΔV).
        index (list[str]): Lista de nomes das barras com ângulo variável.
        swing (list[str]): Lista de nomes das barras SWING.
        pq (list[str]): Lista de nomes das barras PQ.

    Returns:
        tuple[pd.Series, pd.Series]:
            - theta: Série com ângulos atualizados.
            - V: Série com módulos de tensão atualizados.
    """
    delta_theta, delta_v = split_corrections(delta, len(index), len(swing + pq))

    for i, nome in enumerate(index):
        theta.loc[nome] -= delta_theta[i]

    for i, nome in enumerate(swing + pq):
        V.loc[nome] -= delta_v[i]

    return theta, V
