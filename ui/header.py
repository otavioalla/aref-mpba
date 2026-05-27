import streamlit as st
from pathlib import Path


def render_header():
    logo_path = Path(__file__).resolve().parent.parent / "assets" / "mpba_logo.png"

    st.markdown(
        """
        <style>
        .mpba-header {
            background: linear-gradient(90deg, #0B4A2A 0%, #1A6B43 100%);
            padding: 18px 28px;
            border-radius: 8px;
            margin-bottom: 24px;
            color: white;
            display: flex;
            align-items: center;
            gap: 20px;
        }
        .mpba-header h1 {
            color: white !important;
            margin: 0;
            font-size: 1.5rem;
            font-weight: 600;
        }
        .mpba-header .subtitle {
            color: #E8D9A8;
            font-size: 0.85rem;
            margin-top: 2px;
        }
        .mpba-header .gold-bar {
            background: #C9A04A;
            width: 6px;
            height: 56px;
            border-radius: 3px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns([1, 8])
    with cols[0]:
        if logo_path.exists():
            st.image(str(logo_path), width=92)
        else:
            st.markdown(
                """
                <div style="background:#0B4A2A;color:#C9A04A;
                            font-weight:700;text-align:center;
                            padding:24px 8px;border-radius:8px;
                            border:2px solid #C9A04A;font-size:0.85rem;">
                    MPBA
                </div>
                """,
                unsafe_allow_html=True,
            )
    with cols[1]:
        st.markdown(
            """
            <div style="padding-top:8px;">
              <h1 style="color:#0B4A2A;margin:0;font-size:1.6rem;">
                AREF — Análise de Risco em Estádios de Futebol
              </h1>
              <div style="color:#3A5444;font-size:0.95rem;margin-top:4px;">
                Ministério Público do Estado da Bahia &middot;
                Adaptação da metodologia ABIN para Salvador/BA
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("---")
