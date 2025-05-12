"""
Módulo principal para execução do estudo de fluxo de potência em sistemas elétricos 
utilizando o método de Newton-Raphson.

Este script realiza, de forma automatizada, modular e configurável, as seguintes etapas:

    1. Leitura dos dados do sistema a partir de um arquivo '.pwf' compatível com o ANAREDE.
    2. Construção da matriz de admitância nodal Ybus.
    3. Solução do fluxo de potência via método de Newton-Raphson.
    4. Exportação dos resultados para Excel, imagens e Markdown.
    5. Geração automática de gráficos (diagrama fasorial e perfil de tensão).
    6. Suporte multilíngue (português e inglês) e modo silencioso (--quiet).

Este módulo integra as funcionalidades desenvolvidas no projeto de análise
de redes elétricas e foi estruturado para fins acadêmicos e computacionais.

Autor: Giovani Santiago Junqueira
"""

from pathlib import Path # pylint: disable=unused-import
import argparse
import logging
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
from power_flow.utils.graficos import plot_diagrama_fasorial, plot_perfil_tensao

logging.basicConfig(level=logging.DEBUG, format="%(message)s")

def main():
    """
    Função principal que executa o processo de:
    - Leitura dos dados do sistema (.pwf)
    - Construção da matriz de admitância nodal (Ybus)
    - Solução do fluxo de potência
    - Exportação dos resultados para Excel, imagens e Markdown.
    - Geração automática de gráficos (diagrama fasorial e perfil de tensão).
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("caso", help="Nome do arquivo .pwf (sem extensão)")
    parser.add_argument("--idioma", default=IDIOMA_PADRAO, choices=["pt", "en"],
                        help="Idioma das mensagens (pt ou en)")
    parser.add_argument("--formato", choices=["pwf", "json"], help="Formato preferido de entrada")
    args = parser.parse_args()

    logging.getLogger().setLevel(logging.DEBUG)

    if not PASTA_DATA.exists():
        raise FileNotFoundError(f"Pasta de entrada não encontrada: {PASTA_DATA}")
    if not PASTA_SAIDA.exists():
        raise FileNotFoundError(f"Pasta de saída não encontrada: {PASTA_SAIDA}")

    idioma = TEXTOS[args.idioma]
    nome_caso = args.caso

    caminho_pwf = PASTA_DATA / f"{nome_caso}.pwf"
    caminho_json = PASTA_DATA / f"{nome_caso}.json"

    if args.formato == "pwf" or (args.formato is None and caminho_pwf.exists()):
        reader = ReaderPwf(caminho_pwf)
        logging.debug("🧾 Leitura via .pwf")
    elif args.formato == "json" or (args.formato is None and caminho_json.exists()):
        reader = ReaderJson(caminho_json)
        logging.debug("🧾 Leitura via .json")
    else:
        raise FileNotFoundError(
            f"Arquivo {nome_caso}.pwf ou {nome_caso}.json não encontrado em {PASTA_DATA}"
        )

    arquivo_ybus = PASTA_SAIDA / f"{nome_caso}_Ybus_exportada.xlsx"
    arquivo_resultado = PASTA_SAIDA / f"{nome_caso}_resultado_fluxo.xlsx"
    arquivo_sumario = PASTA_SAIDA / f"{nome_caso}_sumario.xlsx"

    logging.info("%s %s", idioma['inicio'], nome_caso)

    reader.read_base()
    barras, *_ = reader.read_bus()
    linhas, transformadores = reader.read_line()

    sistema = Sistema(barras, linhas, transformadores, nome=nome_caso)

    fluxo = NewtonRaphson(sistema)
    V, theta, convergiu, n_iter = fluxo.solve(idioma=args.idioma) # pylint: disable=invalid-name
    sistema.atualizar_resultados(V, theta)

    # Geração dos gráficos
    caminho_grafico_fasorial = PASTA_SAIDA / f"{nome_caso}_diagrama_fasorial.png"
    caminho_grafico_perfil = PASTA_SAIDA / f"{nome_caso}_perfil_tensao.png"
    plot_diagrama_fasorial(theta, V, salvar_em=caminho_grafico_fasorial)
    plot_perfil_tensao(V, salvar_em=caminho_grafico_perfil)

    salvar_ybus_excel(sistema.ybus, arquivo_ybus)
    salvar_resultado_fluxo(V, theta, arquivo_resultado)
    salvar_sumario_resultado(sistema.df_bus, arquivo_sumario)

    arquivo_completo = PASTA_SAIDA / f"{nome_caso}_tabela_completa.xlsx"
    salvar_tabela_completa(sistema, arquivo_completo)

    caminho_md = PASTA_SAIDA / f"{nome_caso}_relatorio.md"
    gerar_relatorio(
        nome_caso=nome_caso,
        V=V,
        theta=theta,
        convergiu=convergiu,
        n_iter=n_iter,
        caminho=caminho_md,
        caminho_fasorial=caminho_grafico_fasorial,
        caminho_perfil=caminho_grafico_perfil
    )

    if convergiu:
        logging.info(idioma["convergiu"].format(n_iter=n_iter))
    else:
        logging.warning(idioma["nao_convergiu"])
    for barra in V.index:
        logging.info(idioma["barra_resultado"].format(barra, V[barra], theta[barra]))
    logging.info("%s %s", idioma['arquivo_salvo'], PASTA_SAIDA)

if __name__ == "__main__":
    main()
