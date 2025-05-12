"""
Subpacote solver

Contém os módulos e funções auxiliares para a resolução do fluxo de potência
utilizando o método de Newton-Raphson. Inclui cálculo de potências injetadas,
resíduos, atualização de estado e verificação de convergência.

Autor: Giovani Santiago Junqueira
"""

from .jacobian import Jacobian
from .power_balance import (
    calc_injected_power,
    calc_delta_p,
    calc_delta_q,
)
from .update import apply_delta
from .residuals import stack_residuals, split_corrections
from .convergence import check_convergence

__all__ = [
    "Jacobian",
    "calc_injected_power",
    "calc_delta_p",
    "calc_delta_q",
    "apply_delta",
    "stack_residuals",
    "split_corrections",
    "check_convergence"
]
