"""
Módulo utilitário para exportação de resultados do fluxo de potência.

Contém funções para salvar dados calculados em arquivos Excel, incluindo:
- Resultados finais de tensão (módulo e ângulo) por barra
- Matriz de admitância nodal Ybus (partes real e imaginária)
- Sumário por barra com tipo, potências especificadas, tensão e ângulo

Essas funções auxiliam na documentação, análise e verificação dos resultados
obtidos nas simulações de fluxo de potência.

Autor: Giovani Santiago Junqueira
"""
# pylint: disable=invalid-name, too-many-arguments, too-many-positional-arguments, line-too-long

from pathlib import Path
import pandas as pd
from power_flow.utils.labels import COLUNAS, TEXTOS, TIPOS_BARRA
from config import IDIOMA_PADRAO

def salvar_resultado_fluxo(V: pd.Series, theta: pd.Series, caminho: Path, idioma: str = IDIOMA_PADRAO):
    """
    Salva os resultados do fluxo de potência (V e θ) em um arquivo Excel.

    Args:
        V (pd.Series): Vetor dos módulos de tensão (indexado por nome da barra).
        theta (pd.Series): Vetor dos ângulos de tensão (indexado por nome da barra).
        caminho (Path): Caminho completo do arquivo de saída.
        idioma (str): Idioma a ser utilizado nos rótulos ('pt' ou 'en').
    """
    caminho = caminho.with_name(f"{caminho.stem}_resultado_fluxo.xlsx")
    df = pd.DataFrame({
        COLUNAS[idioma]["v_calc"]: V,
        COLUNAS[idioma]["theta_calc"]: theta
    })
    df.index.name = COLUNAS[idioma]["numero"]
    df.to_excel(caminho)

def salvar_ybus_excel(ybus: pd.DataFrame, caminho: Path, idioma: str = IDIOMA_PADRAO):
    """
    Salva a matriz Ybus (complexa) em um arquivo Excel, com parte real e imaginária separadas.

    Args:
        ybus (pd.DataFrame): Matriz Ybus complexa indexada por nome de barra.
        caminho (Path): Caminho do arquivo Excel de saída.
        idioma (str): Idioma a ser utilizado nos rótulos ('pt' ou 'en').
    """
    caminho = caminho.with_name(f"{caminho.stem}_Ybus.xlsx")
    df_real = pd.DataFrame(ybus.map(lambda z: z.real), index=ybus.index, columns=ybus.columns)
    df_imag = pd.DataFrame(ybus.map(lambda z: z.imag), index=ybus.index, columns=ybus.columns)
    df_real.index.name = COLUNAS[idioma]["numero"]
    df_imag.index.name = COLUNAS[idioma]["numero"]
    with pd.ExcelWriter(caminho) as writer:
        df_real.to_excel(writer, sheet_name='Parte Real')
        df_imag.to_excel(writer, sheet_name='Parte Imaginária')

def salvar_sumario_resultado(df_barras: pd.DataFrame, caminho: Path, idioma: str = "pt"):
    """
    Salva um sumário dos resultados do fluxo de potência em um arquivo Excel.

    O sumário inclui:
        - Tipo da barra
        - Potência ativa e reativa especificada
        - Módulo da tensão (pu)
        - Ângulo da tensão (rad)

    Args:
        df_barras (pd.DataFrame): DataFrame com colunas ['tipo', 'P_esp', 'Q_esp', 'V', 'Theta'].
        caminho (Path): Caminho do arquivo Excel de saída.
        idioma (str): Idioma a ser utilizado nos rótulos ('pt' ou 'en').
    """
    caminho = caminho.with_name(f"{caminho.stem}_sumario.xlsx")
    colunas_originais = ['tipo', 'P_esp', 'Q_esp', 'V', 'Theta']
    colunas_traduzidas = {col: COLUNAS[idioma].get(col.lower(), col) for col in colunas_originais}
    df = df_barras[colunas_originais].copy()
    df['tipo'] = df['tipo'].apply(lambda x: x[0] if isinstance(x, list) else x)
    df['tipo'] = df['tipo'].map(TIPOS_BARRA[idioma])
    df.rename(columns=colunas_traduzidas, inplace=True)
    df.to_excel(caminho, index_label=COLUNAS[idioma].get("numero", "Barra"))

def salvar_tabela_completa(sistema, caminho: Path, idioma: str = "pt"):
    """
    Exporta uma tabela completa no estilo ANAREDE contendo:
        - Número da barra
        - Tipo
        - V especificado
        - V final
        - Ângulo Theta
        - Pg, Qg (potência gerada)
        - Pl, Ql (potência da carga)

    Args:
        sistema (Sistema): Objeto com dados das barras, geradores e cargas atualizados.
        caminho (Path): Caminho do arquivo Excel de saída.
        idioma (str): Idioma a ser utilizado nos rótulos ('pt' ou 'en').
    """
    caminho = caminho.with_name(f"{sistema.nome}_tabela_completa.xlsx")
    dados = []
    for barra in sistema.barras:
        dados.append({
            "numero": barra.nome,
            "tipo": barra.tipo,
            "v_esp": sistema.df_bus.loc[barra.nome, 'V'],
            "v_calc": barra.v,
            "theta_calc": barra.theta,
            "p_gerado": sum(g.p for g in barra.geradores) if barra.geradores else 0.0,
            "q_gerado": sum(g.q for g in barra.geradores) if barra.geradores else 0.0,
            "p_carga": sum(c.p for c in barra.cargas) if barra.cargas else 0.0,
            "q_carga": sum(c.q for c in barra.cargas) if barra.cargas else 0.0,
            "shunt": sum(s.b for s in barra.shunts) if barra.shunts else 0.0
        })
    df = pd.DataFrame(dados)
    df['tipo'] = df['tipo'].map(TIPOS_BARRA[idioma])
    colunas_traduzidas = {col: COLUNAS[idioma].get(col, col) for col in df.columns}
    df.rename(columns=colunas_traduzidas, inplace=True)
    df.set_index(COLUNAS[idioma].get("numero", "Barra"), inplace=True)
    df.to_excel(caminho)

def gerar_relatorio(
    nome_caso: str,
    V: pd.Series,
    theta: pd.Series,
    convergiu: bool,
    n_iter: int,
    caminho: Path,
    idioma: str = "pt",
    caminho_fasorial: Path | None = None,
    caminho_perfil: Path | None = None
) -> None:
    """
    Gera um relatório em Markdown com os principais resultados do fluxo de potência.

    Args:
        sistema (Sistema): Objeto com os dados do sistema (barras, resultados).
        nome_caso (str): Nome do caso analisado.
        V (pd.Series): Série dos módulos de tensão (pu), indexada por nome da barra.
        theta (pd.Series): Série dos ângulos de tensão (rad), indexada por nome da barra.
        convergiu (bool): Indicador de convergência do método.
        n_iter (int): Número de iterações realizadas.
        caminho (Path): Caminho do arquivo Markdown de saída.
        idioma (str): Idioma a ser utilizado ('pt' ou 'en').
        caminho_fasorial (Path | None): Caminho do arquivo de imagem do diagrama fasorial (opcional).
        caminho_perfil (Path | None): Caminho do arquivo de imagem do perfil de tensão (opcional).
    """
    caminho = caminho.with_name(f"{nome_caso}_relatorio.md")
    txt = TEXTOS[idioma]

    with open(caminho, "w", encoding="utf-8") as f:
        f.write(f"# {txt['titulo']} – {nome_caso}\n\n")
        f.write(f"**{txt['convergencia']}:** {'Sim' if convergiu else 'Não'} – {txt['iteracoes']}: {n_iter}\n\n")
        f.write(f"## {txt['resultados_barra']}\n\n")
        f.write(f"| {txt['barra']} | {txt['v_calc']} | {txt['theta_calc']} |\n")
        f.write("|--------|----------------|--------------------|\n")
        for nome_barra in V.index:
            f.write(f"| {nome_barra} | {V[nome_barra]:.4f} | {theta[nome_barra]:.4f} |\n")

        if caminho_fasorial is not None:
            f.write("\n## Diagrama Fasorial das Tensões\n\n")
            f.write(f"![Diagrama Fasorial]({caminho_fasorial.name})\n")

        if caminho_perfil is not None:
            f.write("\n## Perfil de Tensão por Barra\n\n")
            f.write(f"![Perfil de Tensão]({caminho_perfil.name})\n")
