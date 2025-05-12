"""
Módulo destinado à leitura e extração de dados a partir de arquivos no formato `.pwf`, 
utilizados pelo programa ANAREDE para modelagem de sistemas elétricos de potância.

Este módulo implementa a classe `ReaderPwf`, responsável por interpretar e estruturar
as informações necessárias para a execução de estudos de fluxo de potência, com foco em:

    - Identificação da base MVA do sistema (seção BASE)
    - Leitura dos dados das barras (seção DBAR)
    - Leitura dos dados das linhas de transmissão (seção DLIN)

As seções são lidas diretamente do arquivo `.pwf`, com tratamento de dados ausentes e
normalização de valores conforme a base do sistema. Os dados extraídos são convertidos
em objetos `pandas.DataFrame` organizados e prontos para uso em etapas posteriores, 
como construção da matriz de admitância nodal (Ybus) e cálculo de fluxo de potência.

O arquivo `.pwf` deve estar localizado na pasta `data`, e o caminho completo é montado
automaticamente pela classe.

Este módulo faz parte de um framework modular para estudos de redes elétricas de potência,
e pode ser reutilizado em outras aplicações que utilizem o padrão ANAREDE de entrada.

Autor: Giovani Santiago Junqueira
"""

from numpy import nan
from power_flow.readers.base_reader import BaseReader
from power_flow.models import Bus, Generator, Load, Line, Transformer, Shunt

# pylint: disable=too-many-locals

class ReaderPwf(BaseReader):
    """
    Classe responsável por realizar a leitura de arquivos no formato .pwf (ANAREDE) utilizados em 
    estudos de fluxo de potência.

    A leitura abrange três seções principais do arquivo:
    - BASE: define a base MVA do sistema.
    - DBAR: define os dados das barras do sistema elétrico.
    - DLIN: define os dados das linhas de transmissão e transformadores.

    Atributos:
        arquivo (str): Caminho completo para o arquivo .pwf.
        base (float): Valor da base MVA, extraído da seção BASE.
        _mapa_barra (dict): Mapeia o número da barra para seu nome, usado para identificar conexões.
    """

    def __init__(self, arq: str):
        """
        Inicializa a instância da classe ReaderPwf.

        Args:
            arq (str): Nome do arquivo .pwf (sem caminho), localizado na pasta 'data'.
        """
        self.arquivo = arq
        self.base: float | None = None
        self._mapa_barra: dict[int, str] = {}

    def read_base(self) -> float:
        """
        Lê a seção BASE do arquivo .pwf para determinar a base MVA do sistema.

        Returns:
            float: Valor da base MVA.

        Raises:
            ValueError: Caso a seção BASE não seja encontrada no arquivo.
        """
        with open(self.arquivo, 'r', encoding='latin1') as f:
            for line in f:
                if 'BASE' in line:
                    self.base = float(line[5:11].strip())
                    return self.base
        raise ValueError("Seção BASE não encontrada.")

    def read_bus(self) -> tuple[list[Bus], list[Generator], list[Load], list[Shunt]]:
        """
        Lê e interpreta a seção DBAR do arquivo .pwf e retorna listas de objetos Bus, Generator,
        Load e Shunt.

        Regras aplicadas:
        - Toda barra PV ou SWING recebe um objeto Generator, mesmo que Pg/Qg = 0
        - As potências são convertidas para pu com base no valor de self.base
        - O shunt é normalizado pela base e associado diretamente à barra correspondente

        Returns:
            tuple:
                - list[Bus]: Lista de barras do sistema.
                - list[Generator]: Lista de geradores associados.
                - list[Load]: Lista de cargas associadas.
                - list[Shunt]: Lista de shunts associados.
        """
        barras = []
        geradores = []
        cargas = []
        shunts = []

        with open(self.arquivo, 'r', encoding='latin1') as f:
            capture = False
            for line in f:
                if 'DBAR' in line:
                    capture = True
                    continue
                if capture:
                    if line.strip() == '99999':
                        break
                    if line.strip().startswith('(') or len(line.strip()) < 5:
                        continue
                    try:
                        num = int(line[0:5])
                        tipo_int = int(line[5:8])
                        tipo = {0: 'PQ', 1: 'PV', 2: 'SWING'}.get(tipo_int, 'PQ')
                        nome = line[10:22].strip()
                        v = int(line[24:28].strip()) / 1000
                        theta = float(line[28:32].strip()) if line[28:32].strip() else 0.0

                        pg = float(line[32:37].strip()) / self.base if line[32:37].strip() else 0.0
                        qg = float(line[37:42].strip()) / self.base if line[37:42].strip() else 0.0
                        qn = float(line[42:47].strip()) if line[42:47].strip() else nan
                        qm = float(line[47:52].strip()) if line[47:52].strip() else nan

                        pl = float(line[58:63].strip()) / self.base if line[58:63].strip() else 0.0
                        ql = float(line[63:68].strip()) / self.base if line[63:68].strip() else 0.0

                        sh = float(line[69:74].strip() or 0.0) / self.base

                        barra = Bus(numero=num, tipo=tipo, nome=nome, v=v, theta=theta)
                        barra.geradores = []
                        barra.cargas = []
                        barra.shunts = []
                        barras.append(barra)
                        self._mapa_barra[num] = nome

                        if tipo in ('PV', 'SWING') or pg != 0.0 or qg != 0.0:
                            gerador = Generator(id=num, barra=nome, p=pg, q=qg, qmin=qn, qmax=qm)
                            geradores.append(gerador)
                            barra.geradores.append(gerador)

                        if pl != 0.0 or ql != 0.0:
                            carga = Load(nome=nome, barra=nome, p=pl, q=ql)
                            cargas.append(carga)
                            barra.cargas.append(carga)

                        if sh != 0.0:
                            shunt = Shunt(barra=nome, b=sh)
                            shunts.append(shunt)
                            barra.shunts.append(shunt)
                        else:
                            barra.shunts = None

                    except ValueError:
                        continue

        return barras, geradores, cargas, shunts

    def read_line(self) -> tuple[list[Line], list[Transformer]]:
        """
        Lê e interpreta a seção DLIN do arquivo .pwf, diferenciando entre linhas de transmissão
        e transformadores (com ou sem defasagem angular).

        Critério de classificação:
            - Se 'tap' ≠ 1.0 ou 'fase' ≠ 0.0 → é um Transformer.
            - Caso contrário → é uma Line.

        As grandezas são normalizadas:
            - r e x por 100
            - b por self.base

        Returns:
            tuple:
                - list[Line]: Lista de objetos Line (linhas convencionais).
                - list[Transformer]: Lista de objetos Transformer (com tap e/ou defasagem).
        """
        linhas = []
        transformadores = []
        capture = False

        with open(self.arquivo, 'r', encoding='latin1') as f:
            for line in f:
                if 'DLIN' in line:
                    capture = True
                    continue
                if capture:
                    if line.strip() == '99999':
                        break
                    if line.strip().startswith('(') or len(line.strip()) < 5:
                        continue
                    try:
                        de_num = int(line[0:5])
                        para_num = int(line[10:15])
                        r = float(line[15:26].strip() or 0.0) / 100
                        x = float(line[26:32].strip() or 0.0) / 100
                        b = float(line[32:38].strip() or 0.0) / self.base
                        tap = float(line[38:44].strip() or 1.0)
                        tap = tap if tap != 0.0 else 1.0
                        fase = float(line[54:59].strip() or 0.0)

                        de_nome = self._mapa_barra.get(de_num, str(de_num))
                        para_nome = self._mapa_barra.get(para_num, str(para_num))
                        nome_trafo = f"TRAFO-{de_num}-{para_num}"

                        if tap != 1.0 or fase != 0.0:
                            transformadores.append(Transformer(de_nome, para_nome, nome_trafo,
                                                               r, x, b, tap, fase))
                        else:
                            linhas.append(Line(de_nome, para_nome, r, x, b, tap))

                    except ValueError:
                        continue

        return linhas, transformadores
