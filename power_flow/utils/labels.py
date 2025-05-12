
"""
Módulo de rótulos e traduções utilizados em tabelas e relatórios.

Este dicionário permite alternar dinamicamente entre idiomas nos rótulos
dos campos utilizados em sumários, exportações e relatórios técnicos.

Autor: Giovani Santiago Junqueira
"""

COLUNAS = {
    "pt": {
        "numero": "Barra",
        "tipo": "Tipo",
        "v_esp": "V Esp.",
        "v_calc": "V Calc.",
        "theta_calc": "θ Calc. (rad)",
        "theta_esp": "θ Esp. (rad)",
        "p_esp": "P Esp. (pu)",
        "q_esp": "Q Esp. (pu)",
        "p_gerado": "P Gerado (pu)",
        "q_gerado": "Q Gerado (pu)",
        "p_carga": "P Carga (pu)",
        "q_carga": "Q Carga (pu)",
        "shunt": "Shunt (pu)",
    },
    "en": {
        "numero": "Bus",
        "tipo": "Type",
        "v_esp": "V Setpoint",
        "v_calc": "V Calc.",
        "theta_calc": "θ Calc. (rad)",
        "theta_esp": "θ Setpoint (rad)",
        "p_esp": "P Setpoint (pu)",
        "q_esp": "Q Setpoint (pu)",
        "p_gerado": "P Gen. (pu)",
        "q_gerado": "Q Gen. (pu)",
        "p_carga": "P Load (pu)",
        "q_carga": "Q Load (pu)",
        "shunt": "Shunt (pu)",
    }
}

TEXTOS = {
    "pt": {
        "titulo": "Relatório de Fluxo de Potência",
        "convergencia": "Convergência",
        "iteracoes": "Número de Iterações",
        "resultados_barra": "Resultados por Barra",
        "v_calc": "V Calculado (pu)",
        "theta_calc": "Theta Calculado (rad)",
        "inicio": "Iniciando simulação do caso:",
        "convergiu": "Fluxo convergiu em {n_iter} iterações.",
        "nao_convergiu": "⚠️ O fluxo de potência não convergiu.",
        "barra": "Barra",
        "barra_resultado": "Barra {0}: V = {1:.5f} pu, θ = {2:.5f} rad",
        "arquivo_salvo": "Arquivos salvos na pasta:",
    },
    "en": {
        "titulo": "Power Flow Report",
        "convergencia": "Convergence",
        "iteracoes": "Number of Iterations",
        "resultados_barra": "Results by Bus",
        "v_calc": "V Calculated (pu)",
        "theta_calc": "Theta Calculated (rad)",
        "inicio": "Starting simulation for case:",
        "convergiu": "Power flow converged in {n_iter} iterations.",
        "nao_convergiu": "Power flow did not converge.",
        "barra": "Bus",
        "barra_resultado": "Bus {0}: V = {1:.5f} pu, θ = {2:.5f} rad",
        "arquivo_salvo": "Files saved in folder:",
    }
}

TIPOS_BARRA = {
    "pt": {"PQ": "PQ", "PV": "PV", "SWING": "Swing"},
    "en": {"PQ": "Load", "PV": "Gen", "SWING": "Slack"}
}

MENSAGENS = {
    "pt": {
        "convergiu": "Fluxo de potência convergiu em {n_iter} iterações.",
        "nao_convergiu": "Fluxo de potência não convergiu.",
        "barra_resultado": "Barra {num}: V = {v:.4f} pu, Theta = {theta:.4f} rad",
        "mismatch": "Iteração {iter}: ||Mismatch|| = {val:.3e}"
    },
    "en": {
        "convergiu": "Power flow converged in {n_iter} iterations.",
        "nao_convergiu": "Power flow did not converge.",
        "barra_resultado": "Bus {num}: V = {v:.4f} pu, Theta = {theta:.4f} rad",
        "mismatch": "Iteration {iter}: ||Mismatch|| = {val:.3e}"
    }
}
