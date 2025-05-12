"""
Módulo de logging personalizado para mensagens durante a execução do fluxo de potência.

Este módulo fornece funções auxiliares para registrar mensagens formatadas
relacionadas ao processo de resolução do fluxo, como convergência e resultados
finais por barra, com suporte à internacionalização.

Autor: Giovani Santiago Junqueira
"""

from pathlib import Path

def log_resultado_fluxo(sistema, convergiu: bool, n_iter: int, caminho_saida: Path,
                        idioma: dict) -> None:
    """
    Exibe e salva o resultado do fluxo de potência no terminal e em arquivo.

    Args:
        sistema (Sistema): Objeto do sistema resolvido.
        convergiu (bool): Indicador de convergência.
        n_iter (int): Número de iterações realizadas.
        caminho_saida (Path): Caminho da pasta onde o resultado será salvo.
        idioma (dict): Dicionário com textos traduzidos (pt/en).
    """
    print("—" * 70)
    if convergiu:
        print(idioma["convergiu"].format(n_iter))
    else:
        print(idioma["nao_convergiu"])

    print("—" * 70)
    resultado_str = sistema.df.to_string(index=False)
    print(resultado_str)
    print("—" * 70)

    caminho_saida.mkdir(parents=True, exist_ok=True)
    nome_arquivo = f"{sistema.nome}_resultado_fluxo.txt"
    with open(caminho_saida / nome_arquivo, "w", encoding="utf-8") as f:
        f.write(resultado_str)
