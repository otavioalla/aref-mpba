"""Carregamento das matrizes ABIN padrão e mecanismo de override por análise."""
from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Optional

_DATA_DIR = Path(__file__).resolve().parent.parent / "data"
_DEFAULTS_PATH = _DATA_DIR / "default_tables.json"


def load_default_tables() -> dict:
    """Carrega o JSON de defaults e retorna apenas as 3 matrizes para uso direto pelo model."""
    raw = json.loads(_DEFAULTS_PATH.read_text(encoding="utf-8"))
    return {
        "matriz_4": raw["matriz_4_efetividade"]["valores"],
        "matriz_7": raw["matriz_7_probabilidade"]["valores"],
        "matriz_11": raw["matriz_11_risco"]["valores"],
        "meta": {
            "matriz_4": {
                "linhas": raw["matriz_4_efetividade"]["linhas"],
                "colunas": raw["matriz_4_efetividade"]["colunas"],
            },
            "matriz_7": {
                "linhas": raw["matriz_7_probabilidade"]["linhas"],
                "colunas": raw["matriz_7_probabilidade"]["colunas"],
            },
            "matriz_11": {
                "linhas": raw["matriz_11_risco"]["linhas"],
                "colunas": raw["matriz_11_risco"]["colunas"],
            },
        },
    }


def apply_overrides(defaults: dict, overrides: Optional[dict]) -> dict:
    """Aplica overrides (parciais ou totais) em cima das matrizes padrão."""
    if not overrides:
        return defaults
    result = deepcopy(defaults)
    for matriz_key in ("matriz_4", "matriz_7", "matriz_11"):
        if matriz_key in overrides and overrides[matriz_key]:
            for linha, cols in overrides[matriz_key].items():
                for col, valor in cols.items():
                    result[matriz_key][linha][col] = int(valor)
    return result


def matrices_differ(defaults: dict, current: dict) -> bool:
    """Retorna True se alguma célula difere entre defaults e current."""
    for k in ("matriz_4", "matriz_7", "matriz_11"):
        if defaults.get(k) != current.get(k):
            return True
    return False
