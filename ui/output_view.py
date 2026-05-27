"""Visualização do resultado AREF: classificação final + cascata de tabelas + efetivos."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from aref.basedados import recomendacao_por_risco, load_basedados
from aref.model import AREFResult, TorcidaResult


COR_RISCO = {
    "MUITO BAIXO":  "#2E8B3E",
    "BAIXO":        "#7FB04F",
    "MÉDIO":        "#F4B400",
    "ALTO":         "#E67E22",
    "MUITO ALTO":   "#C0392B",
}

COR_TEXTO_RISCO = {
    "MUITO BAIXO":  "#FFFFFF",
    "BAIXO":        "#FFFFFF",
    "MÉDIO":        "#1A1A1A",
    "ALTO":         "#FFFFFF",
    "MUITO ALTO":   "#FFFFFF",
}


def _badge(classificacao: str, pontos: int = None, large: bool = False) -> str:
    bg = COR_RISCO.get(classificacao, "#888")
    fg = COR_TEXTO_RISCO.get(classificacao, "#FFF")
    size = "1.6rem" if large else "1.05rem"
    pad = "16px 24px" if large else "6px 14px"
    pts = f" &middot; {pontos} pts" if pontos is not None else ""
    return (
        f'<span style="background:{bg};color:{fg};padding:{pad};'
        f'border-radius:8px;font-weight:700;font-size:{size};'
        f'display:inline-block;letter-spacing:0.5px;">'
        f'{classificacao}{pts}</span>'
    )


def _render_card_torcida(r: TorcidaResult, posicao: str):
    st.markdown(f"#### {posicao}")
    st.markdown(_badge(r.risco_classificacao, r.risco_pontos, large=True), unsafe_allow_html=True)
    st.markdown(" ")
    with st.expander("Detalhamento da cascata ABIN", expanded=False):
        rows = [
            ("Perfil da Ameaça (Tabela 2)",
                f"média {r.perfil_media:.2f}",
                r.perfil_nivel),
            ("Sistema de Segurança (Tabela 3)",
                f"média {r.sistema_media:.2f}",
                r.sistema_classificacao),
            ("Efetividade da Ameaça (Tabelas 4 + 5)",
                f"{r.efetividade_pontos} pts",
                r.efetividade_nivel),
            ("Histórico da Torcida (Tabela 6)",
                f"{r.historico_sim_count} respostas SIM",
                r.historico_nivel),
            ("Probabilidade (Tabelas 7 + 8)",
                f"{r.probabilidade_pontos} pts",
                r.probabilidade_nivel),
            ("Impacto (Tabelas 9 + 10)",
                f"soma {r.impacto_soma}",
                r.impacto_nivel),
            ("Risco Final (Tabela 11)",
                f"{r.risco_pontos} pts",
                r.risco_classificacao),
        ]
        df = pd.DataFrame(rows, columns=["Etapa", "Valor calculado", "Classificação"])
        st.dataframe(df, use_container_width=True, hide_index=True)


def render_output(result: AREFResult, state: dict):
    st.markdown("## Classificação de Risco do Jogo")
    meta = state.get("metadata", {})
    descricao = f"**{meta.get('time_a', 'Time A')} x {meta.get('time_b', 'Time B')}** &middot; "
    descricao += f"{meta.get('local', '')} &middot; {meta.get('data', '')} {meta.get('hora', '')}"
    st.markdown(descricao, unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="background:{COR_RISCO[result.classificacao_final]};
                    padding:32px;border-radius:12px;text-align:center;
                    color:{COR_TEXTO_RISCO[result.classificacao_final]};
                    margin:20px 0;">
            <div style="font-size:0.95rem;letter-spacing:1px;opacity:0.9;">
                CLASSIFICAÇÃO FINAL (máximo entre as torcidas)
            </div>
            <div style="font-size:2.4rem;font-weight:800;letter-spacing:1.5px;margin-top:8px;">
                {result.classificacao_final}
            </div>
            <div style="font-size:1rem;opacity:0.9;margin-top:4px;">
                Pontuação máxima: {result.pontos_final}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Resultado por torcida")
    col_a, col_b = st.columns(2)
    with col_a:
        _render_card_torcida(result.time_a, f"🅰️ {meta.get('time_a', 'Time A')}")
    with col_b:
        _render_card_torcida(result.time_b, f"🅱️ {meta.get('time_b', 'Time B')}")

    st.markdown("---")
    st.markdown("### 👥 Efetivos recomendados (Salvador/BA)")
    st.caption(
        "Valores sugeridos por órgão e papel, com base na classificação final do jogo. "
        "Edite os efetivos declarados na coluna **DECLARADO** para visualizar a diferença."
    )

    basedados = load_basedados()
    recomendados = recomendacao_por_risco(basedados, result.classificacao_final)

    declarados = state.get("efetivos_declarados", {})
    df_rows = []
    for r in recomendados:
        chave = f"{r['orgao']}.{r['papel']}"
        df_rows.append({
            "Órgão": r["orgao"],
            "Papel": r["papel"],
            "Recomendado": r["recomendado"],
            "Declarado": int(declarados.get(chave, 0)),
        })
    df = pd.DataFrame(df_rows)
    df["Diferença"] = df["Declarado"] - df["Recomendado"]

    edited = st.data_editor(
        df,
        column_config={
            "Órgão": st.column_config.TextColumn(disabled=True),
            "Papel": st.column_config.TextColumn(disabled=True),
            "Recomendado": st.column_config.NumberColumn(disabled=True, format="%d"),
            "Declarado": st.column_config.NumberColumn(format="%d", min_value=0, step=1),
            "Diferença": st.column_config.NumberColumn(disabled=True, format="%d"),
        },
        hide_index=True,
        use_container_width=True,
        height=450,
        key="efetivos_editor",
    )

    novos_declarados = {}
    for _, row in edited.iterrows():
        chave = f"{row['Órgão']}.{row['Papel']}"
        novos_declarados[chave] = int(row["Declarado"])
    state["efetivos_declarados"] = novos_declarados

    falta = edited[edited["Diferença"] < 0]
    if not falta.empty:
        st.warning(
            f"⚠️ {len(falta)} item(s) com efetivo declarado **abaixo** do recomendado pela metodologia AREF."
        )
    else:
        if (edited["Declarado"] > 0).any():
            st.success("✓ Todos os efetivos declarados atendem ou superam o recomendado.")
