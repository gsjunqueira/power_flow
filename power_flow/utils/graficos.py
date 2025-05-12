"""
Módulo para geração de gráficos do fluxo de potência, como:
- Diagrama fasorial de tensões em coordenadas polares
- Perfil de tensão por barra

Autor: Giovani Santiago Junqueira
"""
# pylint: disable=invalid-name

import matplotlib.pyplot as plt
import pandas as pd

def plot_diagrama_fasorial(theta: pd.Series, V: pd.Series, salvar_em: str = None) -> None:
    """
    Gera o diagrama fasorial (polar) das tensões de barra.

    Args:
        theta (pd.Series): Série de ângulos de tensão (rad), indexada por nome da barra.
        V (pd.Series): Série de módulos de tensão (pu), indexada por nome da barra.
        salvar_em (str, opcional): Caminho para salvar o gráfico como imagem.
    """
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, polar=True)
    ax.set_title("Diagrama Fasorial de Tensões (Coordenadas Polares)", va='bottom')

    ax.scatter(theta.values, V.values, c='blue', s=30)

    # Adiciona rótulos para as 10 maiores tensões
    maiores = V.nlargest(10)
    for barra in maiores.index:
        ax.text(theta[barra], V[barra] + 0.03, f"{barra}", ha='center', fontsize=8)

    if salvar_em:
        plt.savefig(salvar_em, bbox_inches='tight')
    else:
        plt.show()

def plot_perfil_tensao(V: pd.Series, salvar_em: str = None) -> None:
    """
    Gera o gráfico de perfil de tensão por barra.

    Args:
        V (pd.Series): Série de tensões (pu), indexada por nome da barra.
        salvar_em (str, opcional): Caminho para salvar o gráfico como imagem.
    """
    plt.figure(figsize=(10, 4))
    plt.plot(V.index, V.values, marker='o')
    plt.grid(True)
    plt.title("Perfil de Tensão por Barra")
    plt.xlabel("Barra")
    plt.ylabel("Tensão (pu)")
    plt.xticks(rotation=90 if len(V) > 30 else 0)
    plt.tight_layout()

    if salvar_em:
        plt.savefig(salvar_em, bbox_inches='tight')
    else:
        plt.show()
