"""Pacote ``aref`` — também serve como entrypoint de fallback do Streamlit Cloud.

Quando importado normalmente (``from aref.model import ...``), comporta-se como
um pacote Python comum.

Quando o Streamlit Cloud foi configurado por engano para usar este arquivo como
entrypoint (em vez de ``app.py``), detecta o runtime do script e delega para o
app real.
"""
from __future__ import annotations

import os as _os
import sys as _sys


def _running_as_streamlit_script() -> bool:
    """True se este arquivo está sendo executado como script pelo Streamlit.

    Usa ``get_script_run_ctx()`` que é a API canônica para detectar execução
    dentro do ScriptRunner do Streamlit.
    """
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx  # type: ignore

        return get_script_run_ctx() is not None
    except Exception:
        return False


# Garante que o root do projeto esteja em sys.path para imports absolutos
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
if _ROOT not in _sys.path:
    _sys.path.insert(0, _ROOT)


# Delega para app.main() quando Streamlit roda este arquivo como entrypoint.
# Guard com `"app" not in sys.modules` evita recursão: quando app.py importa
# de aref.model, este __init__.py é re-executado mas dessa vez `app` já está
# em sys.modules (parcial) e pulamos a delegação.
if _running_as_streamlit_script() and "app" not in _sys.modules:
    from app import main as _main  # noqa: E402

    _main()
