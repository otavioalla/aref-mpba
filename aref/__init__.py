"""Pacote ``aref`` — também serve como entrypoint de fallback do Streamlit Cloud.

Quando importado normalmente (``from aref.model import ...``), comporta-se como
um pacote Python comum.

Quando o Streamlit Cloud foi configurado por engano para usar este arquivo como
entrypoint (em vez de ``app.py``), detecta o runtime e delega para o app real.
"""
from __future__ import annotations

import os as _os
import sys as _sys


def _running_under_streamlit() -> bool:
    """True se este arquivo foi disparado como script pelo runtime do Streamlit."""
    if _os.environ.get("STREAMLIT_RUNTIME_PATH") or _os.environ.get("STREAMLIT_SERVER_PORT"):
        return True
    try:
        from streamlit.runtime import get_instance  # type: ignore

        return get_instance() is not None
    except Exception:
        return False


# Garante que o root do projeto esteja em sys.path para imports absolutos
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
if _ROOT not in _sys.path:
    _sys.path.insert(0, _ROOT)


if _running_under_streamlit() and "app" not in _sys.modules:
    # Streamlit executou aref/__init__.py como script — delegar ao app real.
    # Guard com `"app" not in sys.modules` evita recursão: quando app.py
    # importa de aref.model, este __init__.py é re-executado mas dessa vez
    # `app` já está em sys.modules (parcial) e pulamos a delegação.
    from app import main as _main  # noqa: E402

    _main()
