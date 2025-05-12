"""
Módulo base que define a interface para leitores de dados do sistema elétrico.

Este módulo estabelece a classe abstrata BaseReader, que deve ser herdada por qualquer
implementação de leitor de arquivos de entrada (.pwf, .json, .xlsx etc).

Autor: Giovani Santiago Junqueira
"""


from abc import ABC, abstractmethod
from typing import Tuple
from power_flow.models import Bus, Line, Transformer

class BaseReader(ABC):
    """
    Classe base abstrata para leitores de dados do sistema elétrico.

    Define a interface padrão para qualquer leitor de entrada, como .pwf, .json, .xlsx.

    Métodos:
        read_base(): Retorna o valor da base MVA do sistema.
        read_bus(): Retorna a lista de objetos Bus.
        read_line(): Retorna as listas de objetos Line e Transformer.
    """

    @abstractmethod
    def read_base(self) -> float:
        """
        Retorna a base MVA do sistema elétrico.

        Returns:
            float: Valor da base em MVA.
        """

    @abstractmethod
    def read_bus(self) -> list[Bus]:
        """
        Retorna a lista de objetos Bus do sistema.

        Returns:
            list[Bus]: Lista contendo as barras do sistema.
        """

    @abstractmethod
    def read_line(self) -> Tuple[list[Line], list[Transformer]]:
        """
        Retorna as conexões do sistema, incluindo linhas e transformadores.

        Returns:
            tuple:
                - list[Line]: Lista de linhas de transmissão.
                - list[Transformer]: Lista de transformadores.
        """
