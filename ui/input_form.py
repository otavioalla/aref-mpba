"""Formulário de entrada AREF — coleta os 14 parâmetros × 2 torcidas + metadados do jogo."""
from __future__ import annotations

import json
from datetime import date, time
from pathlib import Path

import streamlit as st


_CATALOGOS_PATH = Path(__file__).resolve().parent.parent / "data" / "catalogos_ba.json"


def _load_catalogos():
    return json.loads(_CATALOGOS_PATH.read_text(encoding="utf-8"))


# Opções para selectboxes — texto descritivo + valor numérico
PUBLICO_OPTS = [
    ("Elevado — mais de 60% do público esperado (5)", 5),
    ("Médio — entre 30% e 60% do público esperado (3)", 3),
    ("Baixo — até 30% do público esperado (1)", 1),
]

MANDO_OPTS = [
    ("Elevado — jogo no estádio do clube ou onde a torcida tem grande representação (5)", 5),
    ("Limitado — jogo sem mando, em outro estado/local sem representação (1)", 1),
]

RECURSOS_OPTS = [
    ("Elevados — recursos e apoio logístico para acompanhar em grande número (5)", 5),
    ("Medianos — recursos ou apoio logístico parciais (3)", 3),
    ("Limitados — sem recursos e apoio logístico (1)", 1),
]

DESEMPENHO_OPTS = [
    ("Líder / Potencial Classificação (1ª no 1º Quarto) (1)", 1),
    ("No 2º e 3º Quartos da Tabela / Rebaixamento (1)", 1),
    ("1º Quarto da Tabela — 2º/3º Quarto do Campeonato (2)", 2),
    ("Potencial rebaixamento / eliminação — 1º Quarto (2)", 2),
    ("No 2º e 3º Quartos — Semifinal/Final (3)", 3),
    ("Potencial rebaixamento — 2º/3º Quarto do Campeonato (3)", 3),
    ("1º Quarto da Tabela — Do 4º até Semifinal (3)", 3),
    ("Potencial rebaixamento — Do 4º até Semifinal (4)", 4),
    ("Líder / Potencial Classificação — Do 4º até Semifinal (4)", 4),
    ("Líder / Potencial Classificação — Final (4)", 4),
    ("1º Quarto da Tabela — Final (4)", 4),
    ("Potencial rebaixamento — Final (5)", 5),
]

POLITICA_OPTS = [
    ("Estável — sem eleições próximas, sem insatisfação (1)", 1),
    ("Médio — eleições próximas, sem grande insatisfação (3)", 3),
    ("Instável — eleições próximas + insatisfação + mau desempenho (5)", 5),
]

SEG_PUBLICA_OPTS = [
    ("Elevado — totalidade ou quase das medidas implementadas (5)", 5),
    ("Médio — grande parte das medidas implementadas (3)", 3),
    ("Baixo — pequena parte das medidas implementadas (1)", 1),
]

INCENDIO_OPTS = [
    ("Elevado — CBMBA implementou totalidade ou quase das medidas (5)", 5),
    ("Médio — CBMBA implementou grande parte das medidas (3)", 3),
    ("Baixo — CBMBA implementou pequena parte das medidas (1)", 1),
]

ORDENAMENTO_OPTS = [
    ("Elevado — sem ambulantes/cambistas/bebida no entorno (5)", 5),
    ("Mediano — presença inibida com algum sucesso (3)", 3),
    ("Limitado — sem controle sobre o entorno (0)", 0),
]

ACESSO_OPTS = [
    ("Adequado — transportes, vias e segurança eficientes (5)", 5),
    ("Mediano — transportes/vias/segurança com possíveis falhas (3)", 3),
    ("Inadequado — transportes/vias/segurança ineficientes (1)", 1),
]

LESOES_OPTS = [
    ("Não há lesões (0)", 0),
    ("Lesões leves / perturbações leves à saúde (2)", 2),
    ("Lesões graves / danos graves à saúde / agressão a agente público (7)", 7),
    ("Mortes / lesões graves / danos irreversíveis (15)", 15),
]

DANOS_OPTS = [
    ("Não há danos (0)", 0),
    ("Danos de pequena monta dentro do estádio (2)", 2),
    ("Danos de grande monta dentro e fora do estádio (5)", 5),
    ("Destruição total / atingindo imóveis do entorno (10)", 10),
]

IMAGEM_OPTS = [
    ("Insignificante — apenas dentro do estádio (0)", 0),
    ("Pequena — repercussão na cidade (2)", 2),
    ("Grande — repercussão no estado e no Brasil (5)", 5),
    ("Mundial — repercussão duradoura no Brasil e Exterior (10)", 10),
]


def _select_value(label, options, key, default_value=None):
    idx = 0
    if default_value is not None:
        for i, (_, v) in enumerate(options):
            if v == default_value:
                idx = i
                break
    selected = st.selectbox(
        label,
        options,
        index=idx,
        format_func=lambda x: x[0],
        key=key,
    )
    return selected[1]


def _radio_simnao(label, key, default="NÃO"):
    return st.radio(
        label,
        ["SIM", "NÃO"],
        index=0 if default == "SIM" else 1,
        key=key,
        horizontal=True,
    )


def _render_torcida_form(prefix: str, defaults: dict, label: str):
    st.subheader(label)

    with st.expander("🎯 Caracterização da Fonte de Ameaça", expanded=True):
        publico = _select_value("Público esperado", PUBLICO_OPTS, f"{prefix}_publico", defaults.get("publico_esperado"))
        mando = _select_value("Mando de campo", MANDO_OPTS, f"{prefix}_mando", defaults.get("mando_campo"))
        recursos = _select_value("Recursos da torcida", RECURSOS_OPTS, f"{prefix}_recursos", defaults.get("recursos"))
        desempenho = _select_value("Desempenho desportivo do clube", DESEMPENHO_OPTS, f"{prefix}_desempenho", defaults.get("desempenho"))
        politica = _select_value("Situação política do clube", POLITICA_OPTS, f"{prefix}_politica", defaults.get("situacao_politica"))

    with st.expander("🛡️ Avaliação do Sistema de Segurança", expanded=False):
        seg = _select_value("Atendimento aos padrões de segurança pública", SEG_PUBLICA_OPTS, f"{prefix}_seg", defaults.get("seg_publica"))
        incendio = _select_value("Atendimento aos padrões contra incêndios (CBMBA)", INCENDIO_OPTS, f"{prefix}_incendio", defaults.get("incendio"))
        ordenamento = _select_value("Ordenamento público no entorno do estádio", ORDENAMENTO_OPTS, f"{prefix}_ordenamento", defaults.get("ordenamento"))
        acesso = _select_value("Acesso do público ao estádio", ACESSO_OPTS, f"{prefix}_acesso", defaults.get("acesso"))

    with st.expander("📋 Histórico Ponderado da Torcida", expanded=False):
        punicao = _radio_simnao("O clube foi punido nos últimos 5 anos por ações violentas?", f"{prefix}_punicao", defaults.get("punicao_5anos", "NÃO"))
        violencia = _radio_simnao("Houve violência em algum dos 3 jogos anteriores com o mesmo adversário?", f"{prefix}_violencia", defaults.get("violencia_3jogos", "NÃO"))
        ameacas = _radio_simnao("Foram verificadas ameaças com potencial de concretização para o próximo jogo?", f"{prefix}_ameacas", defaults.get("ameacas", "NÃO"))

    with st.expander("⚡ Fatores de Impacto", expanded=False):
        lesoes = _select_value("Possibilidade de lesões ao ser humano", LESOES_OPTS, f"{prefix}_lesoes", defaults.get("lesoes"))
        danos = _select_value("Possibilidade de danos ao patrimônio", DANOS_OPTS, f"{prefix}_danos", defaults.get("danos"))
        imagem = _select_value("Possibilidade de prejuízos à imagem do clube", IMAGEM_OPTS, f"{prefix}_imagem", defaults.get("imagem"))

    return {
        "publico_esperado": publico,
        "mando_campo": mando,
        "recursos": recursos,
        "desempenho": desempenho,
        "situacao_politica": politica,
        "seg_publica": seg,
        "incendio": incendio,
        "ordenamento": ordenamento,
        "acesso": acesso,
        "punicao_5anos": punicao,
        "violencia_3jogos": violencia,
        "ameacas": ameacas,
        "lesoes": lesoes,
        "danos": danos,
        "imagem": imagem,
    }


def _select_or_other(label, options, key, default=None):
    """Selectbox com opção 'Outro...' que abre input livre."""
    opts = list(options)
    if "Outro..." not in opts:
        opts.append("Outro...")
    initial_idx = 0
    if default is not None and default in opts:
        initial_idx = opts.index(default)
    elif default is not None and default not in opts:
        opts.append(default)
        initial_idx = opts.index(default)
    choice = st.selectbox(label, opts, index=initial_idx, key=f"{key}_sel")
    if choice == "Outro...":
        return st.text_input(f"{label} (informar)", key=f"{key}_txt")
    return choice


def render_metadata_form(defaults: dict) -> dict:
    catalogos = _load_catalogos()

    st.subheader("📌 Identificação da partida")
    c1, c2 = st.columns(2)
    with c1:
        torneio = _select_or_other("Torneio", catalogos["torneios"], "meta_torneio", defaults.get("torneio"))
        local = _select_or_other("Local (estádio)", catalogos["estadios"], "meta_local", defaults.get("local"))
    with c2:
        default_data = defaults.get("data") or date.today().isoformat()
        try:
            dval = date.fromisoformat(default_data)
        except (ValueError, TypeError):
            dval = date.today()
        dt = st.date_input("Data", value=dval, key="meta_data", format="DD/MM/YYYY")
        default_hora = defaults.get("hora") or "16:00"
        try:
            h, m = map(int, default_hora.split(":")[:2])
            tval = time(h, m)
        except (ValueError, AttributeError):
            tval = time(16, 0)
        tm = st.time_input("Hora", value=tval, key="meta_hora")

    c3, c4 = st.columns(2)
    with c3:
        time_a = _select_or_other("Time A (mandante / casa)", catalogos["clubes"], "meta_time_a", defaults.get("time_a", "EC Bahia"))
    with c4:
        time_b = _select_or_other("Time B (visitante)", catalogos["clubes"], "meta_time_b", defaults.get("time_b", "EC Vitória"))

    st.markdown("**Responsabilidade**")
    c5, c6 = st.columns(2)
    with c5:
        promotoria = st.text_input("Promotoria responsável", value=defaults.get("promotoria", ""), key="meta_promotoria")
    with c6:
        promotor = st.text_input("Promotor(a) responsável", value=defaults.get("promotor_responsavel", ""), key="meta_promotor")

    return {
        "torneio": torneio,
        "local": local,
        "data": dt.isoformat() if dt else "",
        "hora": tm.strftime("%H:%M") if tm else "",
        "time_a": time_a,
        "time_b": time_b,
        "promotoria": promotoria,
        "promotor_responsavel": promotor,
    }


def render_input_form(state: dict):
    """Renderiza todo o formulário (metadados + 2 torcidas) e atualiza state in-place."""
    metadata = render_metadata_form(state.get("metadata", {}))
    state["metadata"] = metadata

    st.markdown("### Avaliação por torcida")
    col_a, col_b = st.columns(2)
    with col_a:
        inputs_a = _render_torcida_form(
            "ta",
            state.get("inputs", {}).get("time_a", {}),
            f"🅰️ {metadata['time_a'] or 'Time A'}",
        )
    with col_b:
        inputs_b = _render_torcida_form(
            "tb",
            state.get("inputs", {}).get("time_b", {}),
            f"🅱️ {metadata['time_b'] or 'Time B'}",
        )

    state["inputs"] = {"time_a": inputs_a, "time_b": inputs_b}
    return state
