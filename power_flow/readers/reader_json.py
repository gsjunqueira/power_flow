"""
Módulo de leitura de dados no formato JSON para estudos de fluxo de potência.

Este módulo implementa a classe ReaderJson, responsável por ler arquivos de entrada no formato JSON
contendo os dados de um sistema elétrico, e converter essas informações em instâncias dos modelos
Bus, Line, Transformer, Generator, Load e Shunt.

A estrutura do JSON deve conter:
- base_mva: valor da base do sistema
- barras: lista de dicionários representando as barras
- linhas: lista de dicionários representando as linhas
- trafos: lista de dicionários representando os transformadores

A classe ReaderJson segue a mesma lógica modular do ReaderPwf, permitindo intercambialidade no main.py.

Autor: Giovani Santiago Junqueira
"""

import json
from pathlib import Path
from typing import Any # pylint: disable=unused-import
from power_flow.models import (
    Bus,
    Line,
    Transformer,
    Generator,
    Load,
    Shunt,
)

class ReaderJson:
    """
    Classe para leitura de arquivos JSON contendo os dados de um sistema elétrico de potência.

    Atributos:
        arquivo (Path): Caminho do arquivo JSON.
        base (float): Base MVA do sistema, extraída do JSON.
    """
    def __init__(self, arquivo: Path):
        """Inicializa o leitor e carrega o conteúdo do arquivo JSON."""
        self.arquivo = arquivo
        with open(self.arquivo, encoding="utf-8") as f:
            self._data = json.load(f)
        self.base = None

    def read_base(self) -> float:
        """Lê e retorna a base MVA do sistema."""
        self.base = float(self._data["base_mva"])
        return self.base

    def read_bus(self):
        """
        Lê os dados das barras e retorna uma lista de objetos Bus.

        Retorna:
            tuple: (barras, geradores, cargas, shunts) como listas.
        """
        barras = []
        geradores = []
        cargas = []
        shunts = []

        for i, b in enumerate(self._data["barras"], 1):
            nome = b.get("nome") or f"BARRA-{i}"
            barras.append(Bus(
                numero=i,
                tipo=b["tipo"],
                nome=nome,
                v=b["v"],
                theta=b["theta"]
            ))
            for g in b.get("geradores", []):
                geradores.append(Generator(
                    id=g["id"],
                    barra=nome,
                    p=g["p"],
                    q=g["q"],
                    qmin=g["qmin"],
                    qmax=g["qmax"]
                ))
            for c in b.get("cargas", []):
                cargas.append(Load(
                    nome=nome,
                    barra=nome,
                    p=c["p"],
                    q=c["q"]
                ))
            for s in b.get("shunts", []):
                shunts.append(Shunt(
                    barra=nome,
                    b=s["b"],
                    status=s.get("status", True)
                ))

        return barras, geradores, cargas, shunts

    def read_line(self):
        """
        Lê os dados das linhas e transformadores e retorna duas listas de objetos Line e Transformer.

        Retorna:
            tuple: (linhas, transformadores)
        """
        barras_nomeadas = [b.get("nome") or f"BARRA-{i+1}" for i, b in enumerate(self._data["barras"])]
        barra_idx = {i + 1: nome for i, nome in enumerate(barras_nomeadas)}

        linhas = []
        for l in self._data.get("linhas", []):
            linhas.append(Line(
                de=barra_idx[l["de"]] if isinstance(l["de"], int) else l["de"],
                para=barra_idx[l["para"]] if isinstance(l["para"], int) else l["para"],
                r=l["r"],
                x=l["x"],
                b=l["b"],
                status=l.get("status", True)
            ))

        transformadores = []
        for t in self._data.get("trafos", []):
            transformadores.append(Transformer(
                de=barra_idx[t["de"]] if isinstance(t["de"], int) else t["de"],
                para=barra_idx[t["para"]] if isinstance(t["para"], int) else t["para"],
                r=t["r"],
                x=t["x"],
                b=t.get("b", 0.0),
                tap=t.get("tap", 1.0),
                fase=t.get("fase", 0.0),
                status=t.get("status", True)
            ))

        return linhas, transformadores
