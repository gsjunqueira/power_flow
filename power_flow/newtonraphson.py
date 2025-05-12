"""
Módulo responsável pela resolução do Subsistema 1 do fluxo de potência utilizando
o método de Newton-Raphson, com suporte completo à barra SWING por meio da técnica
do Big Number.

Implementa a classe `NewtonRaphson`, que executa iterativamente a correção dos vetores
de estado (ângulos e módulos de tensão) até que os resíduos das equações de potência
ativa (ΔP) e reativa (ΔQ) estejam abaixo de uma tolerância especificada.

Etapas principais por iteração:

    1. Cálculo das potências injetadas (P e Q)
    2. Avaliação dos resíduos (ΔP, ΔQ)
    3. Verificação do critério de convergência
    4. Construção da matriz Jacobiana (com submatrizes H, N, M e L)
    5. Resolução do sistema linear J·Δx = -resíduos
    6. Atualização dos vetores de estado (θ e V)

A barra SWING permanece no sistema e é tratada com grandes valores artificiais (Big Number),
garantindo estabilidade numérica e imposição de suas condições.

Este módulo integra uma arquitetura modular, devendo ser utilizado junto com os módulos
de leitura (`ReaderPwf`), construção da Ybus e cálculo da Jacobiana.

Autor: Giovani Santiago Junqueira
"""

# pylint: disable=invalid-name, too-many-instance-attributes, too-few-public-methods, too-many-arguments, too-many-positional-arguments, line-too-long


from pathlib import Path
import logging
from numpy import linalg, concatenate

from config import TOLERANCIA_PADRAO, MAX_ITER_PADRAO, PASTA_SAIDA
from power_flow.models import Sistema
from power_flow.solver.convergence import check_convergence
from power_flow.solver.jacobian import Jacobian
from power_flow.solver.power_balance import (
    calc_injected_power,
    calc_delta_p,
    calc_delta_q,
)
from power_flow.solver.update import apply_delta
from power_flow.utils.export import salvar_resultado_fluxo
from power_flow.utils.labels import TEXTOS

logging.basicConfig(level=logging.INFO, format="%(message)s")

class NewtonRaphson:
    """
    Classe responsável por resolver o fluxo de potência utilizando
    o método iterativo de Newton-Raphson com suporte à barra SWING
    via técnica do Big Number.

    Esta implementação recebe um objeto do tipo `Sistema`, do qual
    extrai os dados necessários para montar a Jacobiana, calcular
    potências injetadas e aplicar as correções nas tensões.

    Atributos:
        V (np.ndarray): Vetor dos módulos de tensão (inicial e atualizado).
        theta (np.ndarray): Vetor dos ângulos de tensão (inicial e atualizado).
        Ybus (np.ndarray): Matriz de admitância nodal do sistema.
        dbus (pandas.DataFrame): Tabela com os dados das barras.
        tol (float): Tolerância para critério de convergência.
        max_iter (int): Número máximo de iterações permitidas.
        pq (list[int]): Índices das barras tipo PQ.
        pv (list[int]): Índices das barras tipo PV.
        swing (list[int]): Índices das barras tipo SWING.
        index (list[int]): Lista ordenada de todas as barras do sistema.
    """

    def __init__(self, sistema: Sistema, tol=TOLERANCIA_PADRAO, max_iter=MAX_ITER_PADRAO):
        """
        Inicializa o resolvedor de fluxo de potência a partir de um objeto `Sistema`.

        Args:
            sistema (Sistema): Objeto contendo as barras, Ybus e demais dados do sistema.
            tol (float, opcional): Tolerância para convergência do método. Default = 1e-6.
            max_iter (int, opcional): Número máximo de iterações. Default = 20.
        """
        self.V = sistema.df_bus['V'].copy()
        self.theta = sistema.df_bus['Theta'].copy()
        self.Ybus = sistema.ybus
        self.dbus = sistema.df_bus
        self.pot_esp = sistema.pot_esp
        self.tol = tol
        self.max_iter = max_iter
        self.pq = self.dbus.index[self.dbus['tipo'].str[0] == 'PQ'].to_list()
        self.pv = self.dbus.index[self.dbus['tipo'].str[0] == 'PV'].to_list()
        self.swing = self.dbus.index[self.dbus['tipo'].str[0] == 'SWING'].to_list()
        self.index = self.dbus.index.to_list()


    def solve(self, idioma: str = "pt", quiet: bool = False):
        """
        Executa o método iterativo de Newton-Raphson para resolver o fluxo de potência.

        Retorna:
            tuple: (V_final, theta_final, convergência, número de iterações)
        """
        for iteration in range(self.max_iter):
            # 1. Calcular as potências injetadas (P e Q)
            # P, Q = calc_injected_power(self.Ybus, self.V, self.theta)
            P, Q = calc_injected_power(self.Ybus, self.V, self.theta)

            # 2. Calcular os resíduos
            deltaP = calc_delta_p(P, self.pot_esp, self.index, self.swing)
            deltaQ = calc_delta_q(Q, self.pot_esp, self.pq, self.swing)

            # Para debug:
            print("ΔP:")
            print(deltaP)
            print("ΔQ:")
            print(deltaQ)

            print(f"Norma ΔP: {linalg.norm(deltaP):.4e}")
            print(f"Norma ΔQ: {linalg.norm(deltaQ):.4e}")

            # 3. Calcular mismatch
            mismatch = concatenate((deltaP, deltaQ))

            # 4. Verificar convergência
            if check_convergence(mismatch=mismatch, tol=self.tol, iteration=iteration, idioma=idioma):
                if not quiet:
                    logging.info(TEXTOS[idioma]["convergiu"].format(n_iter=iteration + 1))
                prefixo_idioma = f"{idioma.upper()}_"
                caminho_saida = Path(PASTA_SAIDA) / f"{prefixo_idioma}{len(self.V)}_resultado_fluxo.xlsx"
                salvar_resultado_fluxo(self.V, self.theta, caminho_saida)
                return self.V, self.theta, True, iteration + 1

            # 5. Montar a matriz Jacobiana
            J = Jacobian(
                self.V, self.theta,
                self.Ybus.map(lambda z: z.real), self.Ybus.map(lambda z: z.imag),
                P, Q,
                self.pq, self.pv, self.swing, self.index
            ).J

            # 6. Resolver o sistema linear
            delta = linalg.solve(J, -mismatch)

            # 7. Atualizar as variáveis
            self.theta, self.V = apply_delta(self.theta, self.V, delta, self.index, self.swing, self.pq)

        if not quiet:
            logging.warning(TEXTOS[idioma]["nao_convergiu"])
        prefixo_idioma = f"{idioma.upper()}_"
        caminho_saida = Path(PASTA_SAIDA) / f"{prefixo_idioma}{len(self.V)}_resultado_fluxo.xlsx"
        salvar_resultado_fluxo(self.V, self.theta, caminho_saida)
        return self.V, self.theta, False, self.max_iter
