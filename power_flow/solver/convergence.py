"""
Módulo responsável por verificar a convergência do método de Newton-Raphson
no fluxo de potência, com base na norma infinita (máximo valor absoluto)
do vetor combinado de resíduos [ΔP; ΔQ].

A função principal `check_convergence` avalia se o erro atual está abaixo
da tolerância especificada e exibe o valor da norma para rastreamento.

Autor: Giovani Santiago Junqueira
"""

import numpy as np
from power_flow.utils.labels import MENSAGENS
from config import IDIOMA_PADRAO

def check_convergence(mismatch: np.ndarray, tol: float, iteration: int,
                      idioma: str = IDIOMA_PADRAO) -> bool:
    """
    Verifica a convergência com base na norma infinita do vetor de resíduos [ΔP; ΔQ].

    Args:
        mismatch (np.ndarray): Vetor combinado de resíduos [ΔP; ΔQ].
        tol (float): Tolerância para convergência.
        iteration (int): Iteração atual (para exibição do progresso).
        idioma (str): Idioma da mensagem ('pt' ou 'en').

    Returns:
        bool: True se a norma do resíduo for menor que a tolerância.
    """
    max_mismatch = np.max(np.abs(mismatch))
    msg = MENSAGENS[idioma]["mismatch"]
    print(msg.format(iter=iteration + 1, val=max_mismatch))
    return max_mismatch < tol
