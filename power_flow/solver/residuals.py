"""
Funções auxiliares para montar e decompor vetores de resíduos e correções
no método de Newton-Raphson, com suporte à presença da barra SWING (via Big Number).

Ordem assumida: SWING → PV → PQ.

Autor: Giovani Santiago Junqueira
"""

import numpy as np
import pandas as pd

def stack_residuals(delta_p: pd.Series, delta_q: pd.Series,
                    idx_theta: list[str]) -> np.ndarray:
    """
    Combina os resíduos [ΔP; ΔQ] na ordem correta.

    Args:
        delta_p (pd.Series): Resíduos de potência ativa, indexados por nome da barra.
        delta_q (pd.Series): Resíduos de potência reativa, indexados por nome da barra.
        idx_theta (list[str]): Nomes das barras com θ variável (SWING + PV + PQ).

    Returns:
        np.ndarray: Vetor [ΔP; ΔQ] montado.
    """
    return np.concatenate((delta_p.loc[idx_theta].values, delta_q.values))

def split_corrections(delta: np.ndarray, n_theta: int, n_v: int) -> tuple[np.ndarray, np.ndarray]:
    """
    Separa o vetor de correções em [Δθ; ΔV].

    Args:
        delta (np.ndarray): Vetor de correções completo.
        n_theta (int): Número de barras com ângulo variável.
        n_v (int): Número de barras com tensão variável.

    Returns:
        tuple:
            - delta_theta: Correções de ângulo.
            - delta_v: Correções de tensão.
    """
    delta_theta = delta[:n_theta]
    delta_v = delta[n_theta:n_theta + n_v]
    return delta_theta, delta_v
