# app.py
import os, sys
from pathlib import Path
import streamlit as st

# ---------- App setup ----------
st.set_page_config(page_title="AI E-commerce Analytics", page_icon="🧠", layout="wide")

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

# ---------- Optional: UI helpers ----------
_HAS_UI = _HAS_NAV = False
try:
    from ui import load_css, hero, pill, divider  # optional
    _HAS_UI = True
except Exception:
    pass

# ---------- Optional: shared sidebar nav ----------
def _sidebar_fallback():
    # Built-in page links work with multipage Streamlit apps
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        st.page_link("app.py", label="Home", icon="🏠")
        # Only show links that exist in your project
        st.page_link("pages/2_Analyze.py", label="Analyze", icon="📈")
        st.page_link("pages/3_Crawl_Competitors.py", label="Crawl", icon="🕸️")
        st.page_link("pages/4_Recommendations.py", label="Recommendations", icon="💡")
        st.page_link("pages/5_Runs.py", label="Runs", icon="🗂️")
        # If you added this page:
        try:
            st.page_link("pages/4_LLM_Plan_Runner.py", label="LLM Plan Runner", icon="🧪")
        except Exception:
            pass
        st.divider()
        st.caption("LangGraph AI E-commerce • v1.0")

try:
    from nav import sidebar_nav  # if you created src/nav.py
    _HAS_NAV = True
except Exception:
    pass

if _HAS_NAV:
    sidebar_nav()
else:
    _sidebar_fallback()

# ---------- Body ----------
if _HAS_UI:
    load_css()
    hero(
        "🧠 AI E-commerce Analytics",
        "Analyze your dataset, crawl competitors, and generate LLM-planned reports."
    )
    # quick tags row
    col1, col2, col3, col4 = st.columns(4)
    with col1: pill("Analyze")
    with col2: pill("Crawl")
    with col3: pill("Runs")
    with col4: pill("LLM (optional)")
    divider()
else:
    st.title("🧠 AI E-commerce Analytics")
    st.caption("Use the sidebar to navigate between pages.")

st.markdown(
    """
### Quick start
- Open **Analyze** → upload your CSV (or use sample) → see KPIs, segments, insights, and charts → **Save analysis**
- Try **Crawl** → enter a competitor URL → get title/snippet/links and domain/TLD analytics
- Visit **Runs** → browse saved analyses and crawls
- (Optional) **LLM Plan Runner** → execute LangGraph pipeline (report + plots)
"""
)

# Helpful project paths (hidden in expander)
with st.expander("Project paths (debug)"):
    st.code(str(PROJECT_ROOT))
    st.write("src =", str(SRC_DIR))
    outputs = PROJECT_ROOT / "outputs"
    st.write("outputs =", str(outputs))
    st.write("runs dir exists:", (outputs / "runs").exists())
    st.write("crawls dir exists:", (outputs / "crawls").exists())
