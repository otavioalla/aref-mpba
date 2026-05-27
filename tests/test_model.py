"""Testes de paridade entre o port Python e a planilha AREF original.

Caso de referência: AREF FLAMENGO X SAO PAULO 1.xlsx (apesar do nome, os times
preenchidos na aba 'Plano de Ação' são Fluminense × Corinthians; o modelo
funciona com quaisquer dois times — os testes usam apenas os inputs numéricos).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from aref.model import (
    aref,
    perfil_ameaca,
    sistema_seguranca,
    efetividade_ameaca,
    historico_torcida,
    probabilidade,
    impacto,
    risco_final,
)
from aref.tables import load_default_tables


TABELAS = load_default_tables()


# ---------- Caso da planilha (oráculo manual derivado das fórmulas) ----------

INPUTS_TIME_A = {
    "publico_esperado": 5, "mando_campo": 5, "recursos": 5,
    "desempenho": 4, "situacao_politica": 1,
    "seg_publica": 5, "incendio": 3, "ordenamento": 3, "acesso": 5,
    "punicao_5anos": "SIM", "violencia_3jogos": "SIM", "ameacas": "NÃO",
    "lesoes": 7, "danos": 5, "imagem": 2,
}

INPUTS_TIME_B = {
    "publico_esperado": 1, "mando_campo": 1, "recursos": 5,
    "desempenho": 1, "situacao_politica": 1,
    "seg_publica": 1, "incendio": 3, "ordenamento": 3, "acesso": 3,
    "punicao_5anos": "SIM", "violencia_3jogos": "NÃO", "ameacas": "NÃO",
    "lesoes": 7, "danos": 2, "imagem": 5,
}


def test_perfil_ameaca_time_a():
    media, nivel = perfil_ameaca(5, 5, 5, 4, 1)
    assert media == 4.0
    assert nivel == "ALTO"


def test_perfil_ameaca_time_b():
    media, nivel = perfil_ameaca(1, 1, 5, 1, 1)
    assert media == 1.8
    assert nivel == "BAIXO"


def test_sistema_seguranca_time_a():
    media, classif = sistema_seguranca(5, 3, 3, 5)
    assert media == 4.0
    assert classif == "SUFICIENTE"


def test_sistema_seguranca_time_b():
    media, classif = sistema_seguranca(1, 3, 3, 3)
    assert media == 2.5
    assert classif == "INSUFICIENTE"


def test_efetividade_alto_suficiente():
    pontos, nivel = efetividade_ameaca("ALTO", "SUFICIENTE", TABELAS["matriz_4"])
    assert pontos == 8
    assert nivel == "MEDIANA"


def test_efetividade_baixo_insuficiente():
    pontos, nivel = efetividade_ameaca("BAIXO", "INSUFICIENTE", TABELAS["matriz_4"])
    assert pontos == 8
    assert nivel == "MEDIANA"


def test_historico_sim_sim_nao():
    nivel, count = historico_torcida("SIM", "SIM", "NÃO")
    assert nivel == "NÍVEL 3"
    assert count == 2


def test_historico_sim_nao_nao():
    nivel, count = historico_torcida("SIM", "NÃO", "NÃO")
    assert nivel == "NÍVEL 2"
    assert count == 1


def test_probabilidade_mediana_nivel3():
    pontos, nivel = probabilidade("MEDIANA", "NÍVEL 3", TABELAS["matriz_7"])
    assert pontos == 9
    assert nivel == "MEDIANA"


def test_probabilidade_mediana_nivel2():
    pontos, nivel = probabilidade("MEDIANA", "NÍVEL 2", TABELAS["matriz_7"])
    assert pontos == 6
    assert nivel == "MEDIANA"


def test_impacto_time_a():
    soma, nivel = impacto(7, 5, 2)
    assert soma == 14
    assert nivel == "MODERADO"


def test_impacto_time_b():
    soma, nivel = impacto(7, 2, 5)
    assert soma == 14
    assert nivel == "MODERADO"


def test_risco_mediana_moderado():
    pontos, classif = risco_final("MEDIANA", "MODERADO", TABELAS["matriz_11"])
    assert pontos == 24
    assert classif == "BAIXO"


def test_aref_orquestrador_caso_planilha():
    result = aref(INPUTS_TIME_A, INPUTS_TIME_B, TABELAS,
                  nome_a="Time A (Fluminense)", nome_b="Time B (Corinthians)")
    assert result.time_a.risco_pontos == 24
    assert result.time_a.risco_classificacao == "BAIXO"
    assert result.time_b.risco_pontos == 24
    assert result.time_b.risco_classificacao == "BAIXO"
    assert result.classificacao_final == "BAIXO"


# ---------- Casos sintéticos para cobertura de fronteiras ----------

def test_minimo_absoluto():
    inputs = {
        "publico_esperado": 1, "mando_campo": 1, "recursos": 1,
        "desempenho": 1, "situacao_politica": 1,
        "seg_publica": 5, "incendio": 5, "ordenamento": 5, "acesso": 5,
        "punicao_5anos": "NÃO", "violencia_3jogos": "NÃO", "ameacas": "NÃO",
        "lesoes": 0, "danos": 0, "imagem": 0,
    }
    result = aref(inputs, inputs, TABELAS)
    assert result.time_a.perfil_nivel == "MUITO BAIXO"
    assert result.time_a.sistema_classificacao == "ADEQUADO"
    assert result.time_a.efetividade_pontos == 1
    assert result.time_a.efetividade_nivel == "MUITO BAIXA"
    assert result.time_a.historico_nivel == "NÍVEL 1"
    assert result.time_a.probabilidade_pontos == 1
    assert result.time_a.probabilidade_nivel == "REMOTA"
    assert result.time_a.impacto_soma == 0
    assert result.time_a.impacto_nivel == "MUITO BAIXO"
    assert result.time_a.risco_pontos == 1
    assert result.time_a.risco_classificacao == "MUITO BAIXO"
    assert result.classificacao_final == "MUITO BAIXO"


def test_maximo_absoluto():
    inputs = {
        "publico_esperado": 5, "mando_campo": 5, "recursos": 5,
        "desempenho": 5, "situacao_politica": 5,
        "seg_publica": 1, "incendio": 1, "ordenamento": 0, "acesso": 1,
        "punicao_5anos": "SIM", "violencia_3jogos": "SIM", "ameacas": "SIM",
        "lesoes": 15, "danos": 10, "imagem": 10,
    }
    result = aref(inputs, inputs, TABELAS)
    assert result.time_a.perfil_nivel == "MUITO ALTO"
    assert result.time_a.sistema_classificacao == "DESPREZÍVEL"
    assert result.time_a.efetividade_pontos == 25
    assert result.time_a.efetividade_nivel == "MUITO ALTA"
    assert result.time_a.historico_nivel == "NÍVEL 4"
    assert result.time_a.probabilidade_pontos == 25
    assert result.time_a.probabilidade_nivel == "ALTAMENTE PROVÁVEL"
    assert result.time_a.impacto_soma == 35
    assert result.time_a.impacto_nivel == "CRÍTICO"
    assert result.time_a.risco_pontos == 100
    assert result.time_a.risco_classificacao == "MUITO ALTO"


def test_classificacao_final_pega_maximo():
    """Quando os dois times têm classificação diferente, a final é a maior."""
    inputs_baixo = {
        "publico_esperado": 1, "mando_campo": 1, "recursos": 1,
        "desempenho": 1, "situacao_politica": 1,
        "seg_publica": 5, "incendio": 5, "ordenamento": 5, "acesso": 5,
        "punicao_5anos": "NÃO", "violencia_3jogos": "NÃO", "ameacas": "NÃO",
        "lesoes": 0, "danos": 0, "imagem": 0,
    }
    inputs_alto = {
        "publico_esperado": 5, "mando_campo": 5, "recursos": 5,
        "desempenho": 5, "situacao_politica": 5,
        "seg_publica": 1, "incendio": 1, "ordenamento": 0, "acesso": 1,
        "punicao_5anos": "SIM", "violencia_3jogos": "SIM", "ameacas": "SIM",
        "lesoes": 15, "danos": 10, "imagem": 10,
    }
    result = aref(inputs_baixo, inputs_alto, TABELAS)
    assert result.time_a.risco_classificacao == "MUITO BAIXO"
    assert result.time_b.risco_classificacao == "MUITO ALTO"
    assert result.classificacao_final == "MUITO ALTO"
