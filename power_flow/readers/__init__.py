"""
Pacote de leitores de dados para sistemas elétricos.

Contém implementações específicas para leitura a partir de diferentes formatos
de arquivos de entrada (.pwf, .json, etc), todas baseadas na interface BaseReader.
"""

from .base_reader import BaseReader
from .reader_pwf import ReaderPwf
from .reader_json import ReaderJson

__all__ = ["BaseReader", "ReaderPwf", "ReaderJson"]
