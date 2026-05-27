import streamlit as st


def render_footer():
    st.markdown("---")
    st.markdown(
        """
        <div style="font-size:0.82rem;color:#555;line-height:1.6;">
            <strong>Ministério Público do Estado da Bahia</strong> &middot;
            AREF — Análise de Risco em Estádios de Futebol<br/>
            Baseado na metodologia <em>AREF (Avaliação de Risco em Estádios de Futebol)</em>
            desenvolvida pela ABIN — Agência Brasileira de Inteligência.<br/>
            <span style="color:#7A6A2A;">
            🔒 <strong>Privacidade:</strong> esta aplicação não armazena dados no servidor.
            Todas as informações permanecem no seu navegador e podem ser exportadas/importadas
            via arquivo JSON local. Em conformidade com a LGPD.
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )
