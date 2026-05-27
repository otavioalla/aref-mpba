"""Lógica AREF (Avaliação de Risco em Estádios de Futebol) — ABIN.

Reimplementação das fórmulas Excel da planilha original em funções puras.
Sem dependências de Streamlit — pode ser testado e reusado em qualquer contexto.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Literal, Dict, Tuple


SimNao = Literal["SIM", "NÃO"]

NIVEIS_RISCO_ORDEM = ["MUITO BAIXO", "BAIXO", "MÉDIO", "ALTO", "MUITO ALTO"]
RISCO_PARA_NUMERO = {n: i + 1 for i, n in enumerate(NIVEIS_RISCO_ORDEM)}


@dataclass
class TorcidaResult:
    nome: str
    perfil_media: float
    perfil_nivel: str
    sistema_media: float
    sistema_classificacao: str
    efetividade_pontos: int
    efetividade_nivel: str
    historico_nivel: str
    historico_sim_count: int
    probabilidade_pontos: int
    probabilidade_nivel: str
    impacto_soma: int
    impacto_nivel: str
    risco_pontos: int
    risco_classificacao: str


@dataclass
class AREFResult:
    time_a: TorcidaResult
    time_b: TorcidaResult
    classificacao_final: str
    pontos_final: int


def perfil_ameaca(publico: int, mando: int, recursos: int, desempenho: int, politica: int) -> Tuple[float, str]:
    """Tabela 2 ABIN — Perfil/Nível da Ameaça pela média aritmética dos 5 atributos."""
    media = (publico + mando + recursos + desempenho + politica) / 5
    if media > 4.5:
        nivel = "MUITO ALTO"
    elif media > 3.5:
        nivel = "ALTO"
    elif media > 2.5:
        nivel = "MÉDIO"
    elif media > 1.5:
        nivel = "BAIXO"
    else:
        nivel = "MUITO BAIXO"
    return media, nivel


def sistema_seguranca(seg_publica: int, incendio: int, ordenamento: int, acesso: int) -> Tuple[float, str]:
    """Tabela 3 ABIN — Classificação do Sistema de Segurança pela média dos 4 atributos."""
    media = (seg_publica + incendio + ordenamento + acesso) / 4
    if media > 4.5:
        classificacao = "ADEQUADO"
    elif media > 3.5:
        classificacao = "SUFICIENTE"
    elif media > 2.5:
        classificacao = "RAZOÁVEL"
    elif media > 1.5:
        classificacao = "INSUFICIENTE"
    else:
        classificacao = "DESPREZÍVEL"
    return media, classificacao


def _classificar_efetividade(pontos: int) -> str:
    """Tabela 5 ABIN — Nível da Efetividade da Ameaça pela pontuação 1-25."""
    if pontos > 16:
        return "MUITO ALTA"
    if pontos > 10:
        return "ALTA"
    if pontos > 6:
        return "MEDIANA"
    if pontos > 3:
        return "BAIXA"
    return "MUITO BAIXA"


def efetividade_ameaca(perfil_nivel: str, sistema_class: str, matriz_4: Dict[str, Dict[str, int]]) -> Tuple[int, str]:
    """Tabela 4 ABIN — Cruzamento Perfil×Sistema → pontuação, depois Tabela 5 → nível."""
    pontos = matriz_4[perfil_nivel][sistema_class]
    return pontos, _classificar_efetividade(pontos)


def historico_torcida(punicao: SimNao, violencia: SimNao, ameacas: SimNao) -> Tuple[str, int]:
    """Tabela 6 ABIN — Histórico Ponderado da Torcida (3 perguntas SIM/NÃO).

    Reimplementa H24 da planilha: contagem de SIM determina o nível.
    """
    sim_count = sum(1 for x in (punicao, violencia, ameacas) if x == "SIM")
    if sim_count == 0:
        nivel = "NÍVEL 1"
    elif sim_count == 1:
        nivel = "NÍVEL 2"
    elif sim_count == 2:
        nivel = "NÍVEL 3"
    else:
        nivel = "NÍVEL 4"
    return nivel, sim_count


def _classificar_probabilidade(pontos: int) -> str:
    """Tabela 8 ABIN — Nível da Probabilidade pela pontuação 1-25."""
    if pontos > 15:
        return "ALTAMENTE PROVÁVEL"
    if pontos > 9:
        return "PROVÁVEL"
    if pontos > 4:
        return "MEDIANA"
    if pontos > 2:
        return "IMPROVÁVEL"
    return "REMOTA"


def probabilidade(efetividade_nivel: str, historico_nivel: str, matriz_7: Dict[str, Dict[str, int]]) -> Tuple[int, str]:
    """Tabela 7 ABIN — Cruzamento Efetividade×Histórico → pontuação, depois Tabela 8 → nível."""
    pontos = matriz_7[efetividade_nivel][historico_nivel]
    return pontos, _classificar_probabilidade(pontos)


def impacto(lesoes: int, danos: int, imagem: int) -> Tuple[int, str]:
    """Tabela 10 ABIN — Nível do Impacto pela soma dos 3 fatores."""
    soma = lesoes + danos + imagem
    if soma > 24:
        nivel = "CRÍTICO"
    elif soma > 14:
        nivel = "SEVERO"
    elif soma > 9:
        nivel = "MODERADO"
    elif soma > 4:
        nivel = "BAIXO"
    else:
        nivel = "MUITO BAIXO"
    return soma, nivel


def risco_final(probabilidade_nivel: str, impacto_nivel: str, matriz_11: Dict[str, Dict[str, int]]) -> Tuple[int, str]:
    """Tabela 11 ABIN — Cruzamento Probabilidade×Impacto → pontuação final + classificação."""
    pontos = matriz_11[probabilidade_nivel][impacto_nivel]
    if pontos > 79:
        classificacao = "MUITO ALTO"
    elif pontos > 47:
        classificacao = "ALTO"
    elif pontos > 29:
        classificacao = "MÉDIO"
    elif pontos > 9:
        classificacao = "BAIXO"
    else:
        classificacao = "MUITO BAIXO"
    return pontos, classificacao


def compute_torcida(nome: str, inputs: dict, tabelas: dict) -> TorcidaResult:
    """Executa a cascata completa AREF para uma torcida."""
    perfil_media_v, perfil_nivel_v = perfil_ameaca(
        inputs["publico_esperado"],
        inputs["mando_campo"],
        inputs["recursos"],
        inputs["desempenho"],
        inputs["situacao_politica"],
    )
    sistema_media_v, sistema_class_v = sistema_seguranca(
        inputs["seg_publica"],
        inputs["incendio"],
        inputs["ordenamento"],
        inputs["acesso"],
    )
    ef_pontos, ef_nivel = efetividade_ameaca(
        perfil_nivel_v, sistema_class_v, tabelas["matriz_4"]
    )
    hist_nivel, sim_count = historico_torcida(
        inputs["punicao_5anos"],
        inputs["violencia_3jogos"],
        inputs["ameacas"],
    )
    prob_pontos, prob_nivel = probabilidade(ef_nivel, hist_nivel, tabelas["matriz_7"])
    imp_soma, imp_nivel = impacto(inputs["lesoes"], inputs["danos"], inputs["imagem"])
    risco_pts, risco_class = risco_final(prob_nivel, imp_nivel, tabelas["matriz_11"])

    return TorcidaResult(
        nome=nome,
        perfil_media=perfil_media_v,
        perfil_nivel=perfil_nivel_v,
        sistema_media=sistema_media_v,
        sistema_classificacao=sistema_class_v,
        efetividade_pontos=ef_pontos,
        efetividade_nivel=ef_nivel,
        historico_nivel=hist_nivel,
        historico_sim_count=sim_count,
        probabilidade_pontos=prob_pontos,
        probabilidade_nivel=prob_nivel,
        impacto_soma=imp_soma,
        impacto_nivel=imp_nivel,
        risco_pontos=risco_pts,
        risco_classificacao=risco_class,
    )


def aref(inputs_a: dict, inputs_b: dict, tabelas: dict,
         nome_a: str = "Torcida A", nome_b: str = "Torcida B") -> AREFResult:
    """Executa a análise AREF completa e retorna a classificação final (máximo entre torcidas).

    Reproduz exatamente a fórmula `=MAX(R11,R13)` da planilha (AREF INPUT!R15).
    """
    r_a = compute_torcida(nome_a, inputs_a, tabelas)
    r_b = compute_torcida(nome_b, inputs_b, tabelas)
    num_a = RISCO_PARA_NUMERO[r_a.risco_classificacao]
    num_b = RISCO_PARA_NUMERO[r_b.risco_classificacao]
    num_final = max(num_a, num_b)
    classificacao_final = NIVEIS_RISCO_ORDEM[num_final - 1]
    pontos_final = max(r_a.risco_pontos, r_b.risco_pontos)
    return AREFResult(
        time_a=r_a,
        time_b=r_b,
        classificacao_final=classificacao_final,
        pontos_final=pontos_final,
    )


def result_to_dict(result: AREFResult) -> dict:
    return {
        "time_a": asdict(result.time_a),
        "time_b": asdict(result.time_b),
        "classificacao_final": result.classificacao_final,
        "pontos_final": result.pontos_final,
    }
