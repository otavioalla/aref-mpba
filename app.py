"""AREF — Análise de Risco em Estádios de Futebol (MPBA / Salvador)."""
from __future__ import annotations

import streamlit as st

from aref.model import aref
from aref.tables import load_default_tables, matrices_differ
from ui.header import render_header
from ui.footer import render_footer
from ui.input_form import render_input_form
from ui.output_view import render_output
from ui.tables_editor import render_tables_editor
from ui.analysis_io import (
    render_export_button,
    render_import_section,
    render_new_analysis_button,
)


st.set_page_config(
    page_title="AREF — MPBA",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)


def _initial_state() -> dict:
    return {
        "metadata": {
            "torneio": "",
            "local": "",
            "data": "",
            "hora": "",
            "time_a": "",
            "time_b": "",
            "promotoria": "",
            "promotor_responsavel": "",
        },
        "inputs": {"time_a": {}, "time_b": {}},
        "efetivos_declarados": {},
    }


def _get_state() -> dict:
    if "aref_state" not in st.session_state:
        st.session_state["aref_state"] = _initial_state()
    return st.session_state["aref_state"]


def _inputs_completos(state: dict) -> bool:
    required = [
        "publico_esperado", "mando_campo", "recursos", "desempenho",
        "situacao_politica", "seg_publica", "incendio", "ordenamento",
        "acesso", "punicao_5anos", "violencia_3jogos", "ameacas",
        "lesoes", "danos", "imagem",
    ]
    for time_key in ("time_a", "time_b"):
        time_inputs = state.get("inputs", {}).get(time_key, {})
        for r in required:
            if r not in time_inputs:
                return False
    return True


def _render_sidebar(state: dict):
    with st.sidebar:
        st.markdown("### 💾 Análise atual")
        meta = state.get("metadata", {})
        if meta.get("time_a") and meta.get("time_b"):
            st.info(f"**{meta.get('time_a')} × {meta.get('time_b')}**\n\n{meta.get('local', '')}\n\n{meta.get('data', '')} {meta.get('hora', '')}")
        else:
            st.caption("Preencha os dados na aba **Análise** para começar.")

        st.markdown("---")
        if _inputs_completos(state):
            render_export_button(state)
        else:
            st.caption("📥 Botão de exportar aparece quando todos os campos forem preenchidos.")
        render_import_section(state)
        st.markdown("---")
        render_new_analysis_button()

        st.markdown("---")
        st.caption(
            "🔒 Os dados desta análise não são enviados a nenhum servidor — "
            "permanecem apenas no seu navegador."
        )
        st.caption(
            "🛠️ Versão 1.0 &middot; "
            "[Metodologia AREF/ABIN](https://www.gov.br/abin)"
        )


def main():
    render_header()
    state = _get_state()
    _render_sidebar(state)

    tab_analise, tab_resultado, tab_tabelas = st.tabs([
        "📋 Análise",
        "📊 Resultado",
        "⚙️ Editar Tabelas ABIN",
    ])

    with tab_analise:
        render_input_form(state)

    with tab_tabelas:
        render_tables_editor(state)

    with tab_resultado:
        if not _inputs_completos(state):
            st.info(
                "Preencha as entradas na aba **📋 Análise** para visualizar o resultado.\n\n"
                "É necessário informar os 15 parâmetros para cada uma das duas torcidas."
            )
        else:
            tables = state.get("tables") or load_default_tables()
            result = aref(
                state["inputs"]["time_a"],
                state["inputs"]["time_b"],
                tables,
                nome_a=state["metadata"].get("time_a", "Torcida A"),
                nome_b=state["metadata"].get("time_b", "Torcida B"),
            )
            render_output(result, state)

    st.session_state["aref_state"] = state
    render_footer()


if __name__ == "__main__":
    main()
