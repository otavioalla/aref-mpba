"""Loader de BASEDADOS (efetivos recomendados Salvador/BA)."""
from __future__ import annotations

import json
from pathlib import Path

_DATA_DIR = Path(__file__).resolve().parent.parent / "data"
_BASEDADOS_PATH = _DATA_DIR / "basedados_ssa.json"

RISCO_PARA_INDICE_BASEDADOS = {
    "MUITO BAIXO": 0,
    "BAIXO": 0,  # mesma coluna que MUITO BAIXO no BASEDADOS (planilha original)
    "MÉDIO": 1,
    "ALTO": 2,
    "MUITO ALTO": 3,
}


def load_basedados() -> dict:
    return json.loads(_BASEDADOS_PATH.read_text(encoding="utf-8"))


def recomendacao_por_risco(basedados: dict, classificacao_risco: str) -> list[dict]:
    """Retorna uma lista plana [{orgao, papel, recomendado}] para um nível de risco."""
    if classificacao_risco not in RISCO_PARA_INDICE_BASEDADOS:
        raise ValueError(f"Classificação inválida: {classificacao_risco}")
    idx = RISCO_PARA_INDICE_BASEDADOS[classificacao_risco]
    rows = []
    for o in basedados["orgaos"]:
        for p in o["papeis"]:
            rows.append({
                "orgao": o["orgao"],
                "orgao_descricao": o["descricao"],
                "papel": p["papel"],
                "recomendado": int(p["valores"][idx]),
            })
    return rows
