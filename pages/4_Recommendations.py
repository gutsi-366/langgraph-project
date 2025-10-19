# pages/4_Recommendations.py
import os, sys, json
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

from enhanced_agent import EnhancedLangGraphAgent
from lib.storage import list_runs, load_run

try:
    from ui import load_css, hero, section, divider, stat_card
    _HAS_UI = True
except Exception:
    _HAS_UI = False

st.set_page_config(page_title="AI Recommendations", page_icon="💡", layout="wide")

# Create hero section with inline styles (no CSS variables)
st.markdown("""
<div style="
    text-align: center; 
    padding: 3rem 2rem; 
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    border-radius: 15px; 
    margin-bottom: 2rem; 
    color: white;
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
">
    <div style="font-size: 4rem; margin-bottom: 1rem;">💡</div>
    <h1 style="
        margin: 0; 
        font-size: 3rem; 
        font-weight: 800;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    ">AI Recommendations</h1>
    <p style="
        margin: 1rem 0 0 0; 
        font-size: 1.3rem; 
        opacity: 0.9;
        font-weight: 400;
    ">Personalized strategies based on the analyzed dataset.</p>
</div>
""", unsafe_allow_html=True)

# --- Select last analysis run ---
runs = list_runs()
if not runs:
    st.warning("No previous analysis found. Run Analyze Dataset first.")
    st.stop()

run_choice = st.selectbox("Select analysis to load", runs, format_func=lambda r: r.get("id", str(r)))
run_id = run_choice.get("id") if isinstance(run_choice, dict) else str(run_choice)
data = load_run(run_id)
if not data and isinstance(run_choice, dict) and run_choice.get("path"):
    try:
        data = json.loads(Path(run_choice["path"]).read_text(encoding="utf-8"))
    except Exception:
        data = None
if not data:
    st.error("Failed to load analysis file.")
    st.stop()

agent = EnhancedLangGraphAgent()
df = pd.DataFrame.from_dict(data.get("customer_segments", {}), orient="index").reset_index()
st.dataframe(df, use_container_width=True)

# --- Generate recommendations ---
st.subheader("Strategic Recommendations")
insights = data.get("business_insights", [])
recs = []

if "vip" in " ".join(insights).lower():
    recs.append("🎯 Launch a VIP loyalty program to retain high-value users.")
if "mobile" in " ".join(insights).lower():
    recs.append("📱 Optimize mobile UI for better conversions.")
if "retention" in " ".join(insights).lower():
    recs.append("🔄 Start re-engagement campaigns for inactive users.")
if "upsell" in " ".join(insights).lower():
    recs.append("💸 Use bundle offers to increase average order value.")
if not recs:
    recs = ["✅ The dataset shows balanced performance — maintain current engagement strategies."]

for r in recs:
    st.write("- " + r)

# --- Visual summary ---
if "df_domains" in data:
    fig = px.bar(df, x="index", y="avg_lifetime_value", title="Avg Lifetime Value by Segment")
    st.plotly_chart(fig, use_container_width=True)

# --- Export ---
report = agent.generate_professional_report(data, pd.DataFrame())
st.download_button("⬇️ Download AI Recommendations", report, file_name="recommendations.md")
