"""
API pública para execução do fluxo de potência.

Este módulo fornece uma interface de alto nível para uso do motor de fluxo de potência
em outros projetos ou aplicações externas, sem depender da execução via main.py.

Autor: Giovani Santiago Junqueira
"""

import logging
from pathlib import Path  # pylint: disable=unused-import

from config import PASTA_DATA, PASTA_SAIDA, IDIOMA_PADRAO
from power_flow.readers import ReaderPwf, ReaderJson
from power_flow.models import Sistema
from power_flow.newtonraphson import NewtonRaphson
from power_flow.utils.export import (
    salvar_ybus_excel,
    salvar_resultado_fluxo,
    salvar_sumario_resultado,
    salvar_tabela_completa,
    gerar_relatorio
)
from power_flow.utils.labels import TEXTOS
from power_flow.utils.logs import log_resultado_fluxo
from power_flow.utils.graficos import plot_diagrama_fasorial, plot_perfil_tensao

def executar_fluxo(nome_caso: str, idioma: str = IDIOMA_PADRAO) -> Sistema:
    """
    Executa o fluxo de potência para um caso especificado.

    Args:
        nome_caso (str): Nome do caso (sem extensão).
        idioma (str): Idioma a ser utilizado nas mensagens e relatórios. Default = 'pt'.

    Returns:
        Sistema: Objeto com os resultados do fluxo de potência incorporados.
    """
    logging.info(TEXTOS[idioma]["inicio_fluxo"], nome_caso)

    caminho_pwf = PASTA_DATA / f"{nome_caso}.pwf"
    caminho_json = PASTA_DATA / f"{nome_caso}.json"

    if caminho_json.exists():
        reader = ReaderJson(caminho_json)
    elif caminho_pwf.exists():
        reader = ReaderPwf(caminho_pwf)
    else:
        raise FileNotFoundError(TEXTOS[idioma]["arquivo_nao_encontrado"] % nome_caso)

    barras, *_ = reader.read_bus()
    linhas, transformadores = reader.read_line()
    sistema = Sistema(barras, linhas, transformadores)

    fluxo = NewtonRaphson(sistema)
    V, theta, convergiu, n_iter = fluxo.solve() # pylint: disable=invalid-name

    sistema.atualizar_resultados(V, theta)
    fluxo.convergiu = convergiu
    fluxo.n_iter = n_iter

    nome_saida = f"{nome_caso}_Ybus_exportada.xlsx"
    salvar_ybus_excel(sistema.ybus, PASTA_SAIDA / nome_saida)

    salvar_resultado_fluxo( sistema.df_bus["V"], sistema.df_bus["Theta"],
                            PASTA_SAIDA / f"{nome_caso}_resultados.xlsx", idioma)
    salvar_sumario_resultado(sistema.df_bus, PASTA_SAIDA / f"{nome_caso}_sumario.xlsx", idioma)
    salvar_tabela_completa(sistema, PASTA_SAIDA / f"{nome_caso}_tabela_completa.xlsx", idioma)

    caminho_fasorial = PASTA_SAIDA / f"{nome_caso}_fasorial.png"
    caminho_perfil = PASTA_SAIDA / f"{nome_caso}_perfil.png"
    plot_diagrama_fasorial(theta, V, salvar_em=caminho_fasorial)
    plot_perfil_tensao(V, salvar_em=caminho_perfil)

    gerar_relatorio(
        nome_caso=nome_caso,
        V=V,
        theta=theta,
        convergiu=fluxo.convergiu,
        n_iter=fluxo.n_iter,
        caminho=PASTA_SAIDA / f"{nome_caso}_relatorio.md",
        idioma=idioma,
        caminho_fasorial=caminho_fasorial,
        caminho_perfil=caminho_perfil
    )

    log_resultado_fluxo(
        sistema=sistema,
        convergiu=fluxo.convergiu,
        n_iter=fluxo.n_iter,
        caminho_saida=PASTA_SAIDA,
        idioma=idioma
    )

    return sistema
