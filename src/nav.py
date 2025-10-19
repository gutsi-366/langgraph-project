# src/nav.py
import streamlit as st

def sidebar_nav():
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        st.page_link("app.py", label="Home", icon="🏠")
        st.page_link("pages/2_Analyze.py", label="Analyze", icon="📈")
        st.page_link("pages/3_Crawl_Competitors.py", label="Crawl", icon="🕸️")
        st.page_link("pages/4_Recommendations.py", label="Recommendations", icon="💡")
        st.page_link("pages/5_Runs.py", label="Runs", icon="🗂️")
        st.divider()
        st.caption("LangGraph AI E-commerce • v1.0")
