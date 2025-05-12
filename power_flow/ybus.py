"""
Módulo responsável pela construção da matriz de admitância nodal Ybus a partir dos dados
de barras e linhas de transmissão extraídos de arquivos no formato '.pwf' (utilizado pelo ANAREDE).

A matriz Ybus é um elemento central nos estudos de fluxo de potência e representa, em coordenadas
nodais, as relações de admitância elétrica entre as barras do sistema. Sua construção leva em conta:

    - A impedância série das linhas de transmissão (r + jx)
    - A susceptância de shunt (b/2) associada a cada extremidade das linhas
    - A relação de transformação dos transformadores com tap e defasagem
    - A susceptância shunt de cada barra (se presente)

A implementação é encapsulada na classe `Ybus`, a qual sobrecarrega o método `__new__` para retornar
diretamente a matriz calculada como um `pandas.DataFrame` de tipo complexo, indexada pelos nomes
das barras.

Este módulo é parte integrante da estrutura de solução do fluxo de potência por métodos iterativos,
e assume que os dados de entrada foram previamente lidos e formatados como listas de objetos modelo.

Autor: Giovani Santiago Junqueira
"""
# pylint: disable=too-few-public-methods, line-too-long, invalid-name

from numpy import deg2rad, exp, zeros, conj
import pandas as pd
from power_flow.models.line import Line
from power_flow.models.transformer import Transformer
from power_flow.models.bus import Bus
from power_flow.models.shunt import Shunt


def _admitancia_linha(linha: Line, barra_map: dict) -> list[tuple[int, int, complex]]:
    """
    Gera os termos de contribuição de uma linha de transmissão para a matriz Ybus.
    """
    i = barra_map[linha.de]
    j = barra_map[linha.para]
    z = complex(linha.r, linha.x)
    y = 1 / z
    b = complex(0, linha.b / 2)

    return [
        (i, i, y + b),
        (j, j, y + b),
        (i, j, -y),
        (j, i, -y)
    ]


def _admitancia_transformador(trafo: Transformer, barra_map: dict) -> list[tuple[int, int, complex]]:
    """
    Gera os termos de contribuição de um transformador com tap e defasagem para a matriz Ybus.
    """
    i = barra_map[trafo.de]
    j = barra_map[trafo.para]
    z = complex(trafo.r, trafo.x)
    y = 1 / z
    b = complex(0, trafo.b / 2) if hasattr(trafo, 'b') else 0j
    a = trafo.tap * exp(1j * deg2rad(trafo.fase))

    Yff = y / (a * conj(a)) + b
    Yft = -y / conj(a)
    Ytf = -y / a
    Ytt = y + b

    return [
        (i, i, Yff),
        (i, j, Yft),
        (j, i, Ytf),
        (j, j, Ytt)
    ]


class Ybus:
    """
    Classe destinada à construção da matriz de admitância nodal Ybus a partir dos dados
    das barras, linhas, transformadores e shunts de um sistema elétrico.

    Instanciação:
        Ybus = Ybus(linhas, transformadores, barras, shunts)

    Parâmetros:
        linhas (list[Line]): Linhas de transmissão.
        transformadores (list[Transformer]): Transformadores com ou sem defasagem.
        barras (list[Bus]): Lista de objetos Bus, contendo nomes e parâmetros.
        shunts (list[Shunt]): Lista de elementos shunt conectados às barras.

    Retorna:
        pd.DataFrame: Matriz Ybus (complexa) indexada e nomeada por barra.
    """
    def __new__(cls, linhas: list[Line], transformadores: list[Transformer], barras: list[Bus], shunts: list[Shunt]) -> pd.DataFrame:
        barra_nomes = sorted(set(b.nome for b in barras))
        barra_map = {nome: idx for idx, nome in enumerate(barra_nomes)}
        nb = len(barra_map)
        ybus = zeros((nb, nb), dtype=complex)

        for linha in linhas:
            for i, j, y in _admitancia_linha(linha, barra_map):
                ybus[i, j] += y

        for trafo in transformadores:
            for i, j, y in _admitancia_transformador(trafo, barra_map):
                ybus[i, j] += y

        for shunt in shunts:
            if shunt.status and shunt.barra in barra_map:
                i = barra_map[shunt.barra]
                ybus[i, i] += complex(0, shunt.b)

        return pd.DataFrame(ybus, index=barra_nomes, columns=barra_nomes)
