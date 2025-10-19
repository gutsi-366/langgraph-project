# pages/2_Analyze.py
import os, sys, json
import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np

# ----- project paths -----
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

# ----- local imports -----
from enhanced_agent import EnhancedLangGraphAgent
from lib.storage import save_run
from data_manager import data_manager

# Enhanced UI helpers
try:
    from ui_components import load_css, hero, metric_card, stat_card, info_card, section, divider, success_message, error_message
    _HAS_UI = True
except Exception:
    _HAS_UI = False

# Optional: LangGraph multi-step agent
_HAS_GRAPH_AGENT = False
try:
    from dotenv import load_dotenv
    load_dotenv()
    # expects src/agents/langgraph_agent.py with build_agent_graph()
    from agents.langgraph_agent import build_agent_graph
    _HAS_GRAPH_AGENT = True
except Exception:
    _HAS_GRAPH_AGENT = False

# ----- page setup -----
st.set_page_config(page_title="Analyze Dataset", page_icon="📈", layout="wide")

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
    <div style="font-size: 4rem; margin-bottom: 1rem;">📈</div>
    <h1 style="
        margin: 0; 
        font-size: 3rem; 
        font-weight: 800;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    ">Analyze Dataset</h1>
    <p style="
        margin: 1rem 0 0 0; 
        font-size: 1.3rem; 
        opacity: 0.9;
        font-weight: 400;
    ">Enhanced agent computes KPIs, segments, insights, visualizations, and a professional report.</p>
</div>
""", unsafe_allow_html=True)

# ----- file input -----
uploaded = st.file_uploader("Upload CSV", type=["csv"])
use_sample = st.button("Use sample (data/large_dataset.csv)")

df = None
dataset_path = None

if uploaded:
    try:
        df = pd.read_csv(uploaded)  # in-memory for the enhanced agent
        # also save to /data so optional LangGraph agent can read by path
        os.makedirs(os.path.join(PROJECT_ROOT, "data"), exist_ok=True)
        dataset_path = os.path.join(PROJECT_ROOT, "data", uploaded.name)
        with open(dataset_path, "wb") as f:
            f.write(uploaded.getbuffer())
        
        # Save to session state for other pages
        st.session_state.dataset = df
        st.session_state.dataset_name = uploaded.name
        
        # Save to persistent storage
        dataset_id = data_manager.save_dataset(
            df, 
            uploaded.name, 
            f"Uploaded CSV file with {len(df)} rows and {len(df.columns)} columns",
            "uploaded"
        )
        st.session_state.current_dataset_id = dataset_id
        
        st.success(f"✅ Data uploaded and saved: {len(df)} rows, {len(df.columns)} columns")
        st.info(f"💾 Data saved permanently with ID: {dataset_id}")
        
    except Exception as e:
        st.error(f"Failed to read uploaded CSV: {e}")

elif use_sample:
    sample_path = os.path.join(PROJECT_ROOT, "data", "large_dataset.csv")
    if os.path.exists(sample_path):
        try:
            df = pd.read_csv(sample_path)
            dataset_path = sample_path
            
            # Save to session state for other pages
            st.session_state.dataset = df
            st.session_state.dataset_name = "Sample Dataset"
            
            # Save to persistent storage
            dataset_id = data_manager.save_dataset(
                df, 
                "Sample Dataset", 
                f"Sample dataset with {len(df)} rows and {len(df.columns)} columns",
                "sample"
            )
            st.session_state.current_dataset_id = dataset_id
            
            st.toast("Sample loaded", icon="✅")
            st.info(f"💾 Sample data saved permanently with ID: {dataset_id}")
        except Exception as e:
            st.error(f"Failed to read sample CSV: {e}")
    else:
        st.warning("data/large_dataset.csv not found")

if df is None:
    st.info("Upload a CSV or click **Use sample** to run the analysis.")
    st.stop()

# ----- preview -----
if _HAS_UI:
    section("Preview")
else:
    st.subheader("Preview")

st.dataframe(df.head(20), width="stretch")
st.caption(f"Rows: {len(df):,} • Cols: {len(df.columns)}")
if _HAS_UI:
    divider()

# =========================
# Enhanced (local) Agent
# =========================
agent = EnhancedLangGraphAgent()
results = agent.analyze_large_dataset(df)

# ----- KPIs -----
km = results.get("key_metrics", {})
if _HAS_UI:
    section("Key Metrics")
    c1, c2, c3, c4 = st.columns(4)
    with c1: metric_card("Total Revenue Potential", km.get("total_revenue_potential", "—"), icon="💰", color="blue")
    with c2: metric_card("Avg Order Value", km.get("average_order_value", "—"), icon="🛒", color="green")
    with c3: metric_card("Avg Browsing Time", km.get("average_browsing_time", "—"), icon="⏱️", color="purple")
    with c4: metric_card("Active Users (≤7d)", km.get("active_users_ratio", "—"), icon="👥", color="orange")
    divider()
else:
    st.subheader("Key Metrics")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Revenue Potential", km.get("total_revenue_potential", "—"))
    c2.metric("Avg Order Value", km.get("average_order_value", "—"))
    c3.metric("Avg Browsing Time", km.get("average_browsing_time", "—"))
    c4.metric("Active Users (≤7d)", km.get("active_users_ratio", "—"))

# ----- segments -----
segments = results.get("customer_segments", {})
if _HAS_UI:
    section("Customer Segments")
else:
    st.subheader("Customer Segments")

if segments:
    seg_rows = []
    for seg, data in segments.items():
        row = {"segment": seg}
        for k in ["count", "percentage", "avg_lifetime_value", "avg_purchases", "avg_browsing_time"]:
            if k in data:
                row[k] = data[k]
        seg_rows.append(row)

    seg_df = pd.DataFrame(seg_rows)
    st.dataframe(seg_df, width="stretch")

    if "count" in seg_df.columns:
        fig = px.bar(seg_df, x="segment", y="count", title="Users per Segment")
        # Streamlit 1.39+: replace use_container_width with width param
        st.plotly_chart(fig, width="stretch")
else:
    st.caption("No segments available.")
if _HAS_UI:
    divider()

# ----- insights -----
ins = results.get("business_insights", [])
if _HAS_UI:
    section("Insights")
else:
    st.subheader("Insights")
if ins:
    for i in ins:
        st.write("• " + str(i))
else:
    st.caption("No insights returned.")
if _HAS_UI:
    divider()

# ----- visualizations -----
viz = results.get("visualizations", {})
if _HAS_UI:
    section("Visualizations")
else:
    st.subheader("Visualizations")

img_keys = [k for k, v in viz.items() if isinstance(v, str) and v.startswith("data:image")]
if img_keys:
    cols = st.columns(3)
    for idx, k in enumerate(img_keys):
        with cols[idx % 3]:
            st.markdown(f"**{k.replace('_',' ').title()}**")
            st.image(viz[k])
elif "error" in viz:
    st.warning("Visualization error: " + str(viz["error"]))
else:
    st.caption("No charts were generated.")
if _HAS_UI:
    divider()

# ----- performance -----
if _HAS_UI:
    section("Performance")
else:
    st.subheader("Performance")
st.json(results.get("performance_metrics", {}))
if _HAS_UI:
    divider()

# ----- professional report (local) -----
if _HAS_UI:
    section("Professional Report")
else:
    st.subheader("Professional Report")
report_md = agent.generate_professional_report(results, df)
st.markdown(report_md)

# ----- optional: LLM-written block if your agent added it -----
if "llm_report" in results and results["llm_report"]:
    if _HAS_UI:
        divider()
    st.subheader("🤖 LLM-Generated Insights")
    st.markdown(results["llm_report"])

# =========================
# LangGraph LLM Agent (optional, button-triggered)
# =========================
if _HAS_GRAPH_AGENT:
    if _HAS_UI:
        divider()
        section("🤖 AI Agent (LangGraph)", "Runs a multi-step LLM workflow to produce insights + a Markdown report.")
    else:
        st.subheader("🤖 AI Agent (LangGraph)")

    if dataset_path is None and uploaded is not None:
        dataset_path = os.path.join(PROJECT_ROOT, "data", uploaded.name)
        os.makedirs(os.path.dirname(dataset_path), exist_ok=True)
        with open(dataset_path, "wb") as f:
            f.write(uploaded.getbuffer())

    run_graph = st.button("🚀 Run LangGraph Agent")
    if run_graph:
        try:
            if not dataset_path or not os.path.exists(dataset_path):
                st.error("Dataset path not found. Please upload a file or use the sample first.")
            else:
                st.info("Running LangGraph agent, please wait...")
                graph = build_agent_graph()
                result = graph.invoke({"dataset_path": dataset_path})
                st.success("✅ LangGraph Agent completed successfully!")

                if "summary" in result:
                    with st.expander("📋 Dataset Summary (LLM view)"):
                        st.text(result["summary"])

                if "analysis" in result:
                    st.markdown("### 🔍 LLM-Generated Insights")
                    st.write(result["analysis"])

                if "report" in result:
                    st.markdown("### 🧾 LLM Markdown Report")
                    st.markdown(result["report"])
                    st.caption(f"Saved to: `{result.get('report_path', 'outputs/generated_report.md')}`")
        except Exception as e:
            st.error(f"❌ LangGraph agent error: {e}")

# ----- save & download -----
if _HAS_UI:
    divider()

colA, colB = st.columns(2)

def make_json_safe(obj):
    """Recursively convert non-serializable objects into JSON-safe types."""
    if isinstance(obj, (np.integer, int)):
        return int(obj)
    if isinstance(obj, (np.floating, float)):
        return float(obj)
    if isinstance(obj, (np.ndarray, list, tuple)):
        return [make_json_safe(x) for x in obj]
    if isinstance(obj, dict):
        return {str(k): make_json_safe(v) for k, v in obj.items()}
    if hasattr(obj, "isoformat"):
        return obj.isoformat()
    return str(obj)

with colA:
    if st.button("💾 Save analysis"):
        try:
            path = save_run(results)
            st.success(f"Saved: {path}")
        except Exception as e:
            st.error(f"Failed to save: {e}")

safe_results = make_json_safe(results)
with colB:
    st.download_button(
        "⬇️ Download results.json",
        json.dumps(safe_results, indent=2),
        file_name="results.json"
    )

st.download_button(
    "⬇️ Download report.md",
    report_md,
    file_name="report.md"
)
