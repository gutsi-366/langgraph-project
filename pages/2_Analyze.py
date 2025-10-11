# pages/2_Analyze.py
import os, sys, json
import pandas as pd
import plotly.express as px
import streamlit as st

# ----- project paths -----
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

# ----- local imports -----
from enhanced_agent import EnhancedLangGraphAgent
from lib.storage import save_run

# Optional UI helpers (only if you created src/ui.py + src/ui.css)
try:
    from ui import load_css, hero, stat_card, section, divider
    _HAS_UI = True
except Exception:
    _HAS_UI = False

# ----- page setup -----
st.set_page_config(page_title="Analyze Dataset", page_icon="📈", layout="wide")
if _HAS_UI:
    load_css()
    hero("📈 Analyze Dataset",
         "Enhanced agent computes KPIs, segments, insights, visualizations, and a professional report.")
else:
    st.title("📈 Analyze Dataset (Enhanced Agent)")

# ----- file input -----
uploaded = st.file_uploader("Upload CSV", type=["csv"])
use_sample = st.button("Use sample (data/large_dataset.csv)")

df = None
if uploaded:
    try:
        df = pd.read_csv(uploaded)
    except Exception as e:
        st.error(f"Failed to read uploaded CSV: {e}")
elif use_sample:
    sample_path = os.path.join(PROJECT_ROOT, "data", "large_dataset.csv")
    if os.path.exists(sample_path):
        try:
            df = pd.read_csv(sample_path)
            st.toast("Sample loaded", icon="✅")
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
st.dataframe(df.head(20), use_container_width=True)
st.caption(f"Rows: {len(df):,} • Cols: {len(df.columns)}")
if _HAS_UI:
    divider()

# ----- run agent -----
agent = EnhancedLangGraphAgent()
results = agent.analyze_large_dataset(df)

# ----- KPIs -----
km = results.get("key_metrics", {})
if _HAS_UI:
    section("Key Metrics")
    c1, c2, c3, c4 = st.columns(4)
    with c1: stat_card("Total Revenue Potential", km.get("total_revenue_potential", "—"))
    with c2: stat_card("Avg Order Value", km.get("average_order_value", "—"))
    with c3: stat_card("Avg Browsing Time", km.get("average_browsing_time", "—"))
    with c4: stat_card("Active Users (≤7d)", km.get("active_users_ratio", "—"))
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
    st.dataframe(seg_df, use_container_width=True)

    if "count" in seg_df.columns:
        fig = px.bar(seg_df, x="segment", y="count", title="Users per Segment")
        st.plotly_chart(fig, use_container_width=True)
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

# ----- visualizations (base64 images from your agent) -----
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

# ----- professional report -----
if _HAS_UI:
    section("Professional Report")
else:
    st.subheader("Professional Report")
report_md = agent.generate_professional_report(results, df)
st.markdown(report_md)

# ----- save & download -----
colA, colB = st.columns(2)
with colA:
    if st.button("💾 Save analysis"):
        path = save_run(results)
        st.success(f"Saved: {path}")
with colB:
    st.download_button("⬇️ Download results.json", json.dumps(results, indent=2), file_name="results.json")

st.download_button("⬇️ Download report.md", report_md, file_name="report.md")
