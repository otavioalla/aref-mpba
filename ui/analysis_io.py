"""Exportar/Importar análises como JSON pelo navegador (sem servidor)."""
from __future__ import annotations

import json
from datetime import datetime
from typing import Optional

import streamlit as st


def _slug(metadata: dict) -> str:
    parts = [
        metadata.get("data", "sem-data"),
        metadata.get("time_a", "TA").replace(" ", ""),
        "vs",
        metadata.get("time_b", "TB").replace(" ", ""),
    ]
    return "_".join(parts) + ".aref.json"


def serialize_state(state: dict) -> str:
    payload = {
        "schema_version": 1,
        "metadata": state.get("metadata", {}),
        "inputs": state.get("inputs", {}),
        "efetivos_declarados": state.get("efetivos_declarados", {}),
        "tables_override": _diff_tables(state.get("tables")),
        "exported_at": datetime.now().isoformat(timespec="seconds"),
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def _diff_tables(tables: Optional[dict]) -> Optional[dict]:
    """Salva apenas as matrizes (sem o meta) — defaults serão recarregados na importação."""
    if not tables:
        return None
    return {k: tables[k] for k in ("matriz_4", "matriz_7", "matriz_11") if k in tables}


def render_export_button(state: dict):
    json_str = serialize_state(state)
    fname = _slug(state.get("metadata", {}))
    st.download_button(
        label="📥 Baixar análise (.json)",
        data=json_str.encode("utf-8"),
        file_name=fname,
        mime="application/json",
        use_container_width=True,
    )


def render_import_section(state: dict):
    uploaded = st.file_uploader(
        "📤 Carregar análise (.json)",
        type=["json"],
        key="aref_uploader",
        help="Importe uma análise previamente exportada por esta aplicação."
    )
    if uploaded is not None and st.session_state.get("_last_uploaded") != uploaded.name:
        try:
            payload = json.loads(uploaded.read().decode("utf-8"))
            state["metadata"] = payload.get("metadata", {})
            state["inputs"] = payload.get("inputs", {})
            state["efetivos_declarados"] = payload.get("efetivos_declarados", {})
            override = payload.get("tables_override")
            if override:
                from aref.tables import load_default_tables, apply_overrides
                defaults = load_default_tables()
                merged = apply_overrides(defaults, override)
                state["tables"] = merged
            else:
                state.pop("tables", None)
            st.session_state["_last_uploaded"] = uploaded.name
            st.session_state["aref_state"] = state
            st.success(f"✓ Análise carregada: **{uploaded.name}**")
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao ler arquivo: {e}")


def render_new_analysis_button():
    if st.button("🆕 Nova análise (limpar tudo)", type="secondary", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()
