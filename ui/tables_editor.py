"""Editor das matrizes ABIN (Tabelas 4, 7, 11) usando st.data_editor."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from aref.tables import load_default_tables, matrices_differ


def _matriz_to_df(valores: dict, linhas: list, colunas: list) -> pd.DataFrame:
    data = {col: [valores[linha][col] for linha in linhas] for col in colunas}
    return pd.DataFrame(data, index=linhas)


def _df_to_matriz(df: pd.DataFrame, linhas: list, colunas: list) -> dict:
    return {linha: {col: int(df.loc[linha, col]) for col in colunas} for linha in linhas}


def render_tables_editor(state: dict):
    defaults = load_default_tables()

    current_tables = state.get("tables", defaults)
    if "matriz_4" not in current_tables:
        current_tables = defaults
        state["tables"] = current_tables

    if matrices_differ(defaults, current_tables):
        st.warning(
            "⚠️ As matrizes desta análise foram **alteradas** em relação ao padrão ABIN. "
            "Os resultados refletem as matrizes customizadas."
        )

    st.markdown(
        "### Editor das Matrizes ABIN\n\n"
        "Estas matrizes representam o núcleo da metodologia AREF. "
        "Os valores padrão foram extraídos diretamente das fórmulas da planilha ABIN. "
        "Modificações **alteram a pontuação calculada** em todas as análises desta sessão."
    )

    if st.button("🔄 Resetar todas as matrizes para o padrão ABIN", type="secondary"):
        state["tables"] = defaults
        st.rerun()

    tabs = st.tabs([
        "Matriz 4 — Efetividade (Ameaça × Segurança)",
        "Matriz 7 — Probabilidade (Efetividade × Histórico)",
        "Matriz 11 — Risco Final (Probabilidade × Impacto)",
    ])

    new_tables = {"matriz_4": None, "matriz_7": None, "matriz_11": None,
                  "meta": defaults["meta"]}

    matriz_configs = [
        ("matriz_4", "Pontuação 1–25. Linhas: Perfil da Ameaça. Colunas: Sistema de Segurança."),
        ("matriz_7", "Pontuação 1–25. Linhas: Efetividade da Ameaça. Colunas: Histórico da Torcida."),
        ("matriz_11", "Pontuação 1–100. Linhas: Probabilidade. Colunas: Impacto."),
    ]

    for tab, (key, descricao) in zip(tabs, matriz_configs):
        with tab:
            meta = defaults["meta"][key]
            st.caption(descricao)
            df = _matriz_to_df(current_tables[key], meta["linhas"], meta["colunas"])
            edited = st.data_editor(
                df,
                use_container_width=True,
                key=f"editor_{key}",
                column_config={
                    col: st.column_config.NumberColumn(min_value=0, step=1, format="%d")
                    for col in meta["colunas"]
                },
            )
            new_tables[key] = _df_to_matriz(edited, meta["linhas"], meta["colunas"])

    state["tables"] = new_tables
