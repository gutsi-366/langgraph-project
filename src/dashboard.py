# src/dashboard.py — advanced LangGraph analytics dashboard
import os
import sys
import json
import time
from datetime import datetime
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Ensure imports work inside /src
sys.path.append(os.path.dirname(__file__))
try:
    from langgraph_agent import LangGraphAgent
except Exception:
    from enhanced_agent import EnhancedLangGraphAgent as LangGraphAgent

# ------------------- PAGE SETTINGS -------------------
st.set_page_config(
    page_title="LangGraph Intelligence Dashboard",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS for a modern UI
st.markdown("""
<style>
    [data-testid="stMetricValue"] {font-size: 2rem;}
    .main-title {font-size: 2rem; font-weight:600;}
    .subtitle {opacity:0.7; font-size: 1rem;}
    .block-container {padding-top: 1.5rem;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ------------------- SIDEBAR -------------------
st.sidebar.title("⚙️ Control Panel")
mode = st.sidebar.radio("Select Analysis Mode", ["LangGraph Agent", "Enhanced Agent"])
uploaded = st.sidebar.file_uploader("📂 Upload your dataset (CSV)", type=["csv"])
use_demo = st.sidebar.button("Use Demo Dataset")

# ------------------- LOAD DATA -------------------
if use_demo:
    sample = os.path.join(os.path.dirname(__file__), "..", "data", "large_dataset.csv")
    df = pd.read_csv(sample)
    st.toast("✅ Demo dataset loaded")
elif uploaded:
    df = pd.read_csv(uploaded)
else:
    df = None

# ------------------- NO DATA -------------------
if df is None:
    st.markdown("<div class='main-title'>🧠 LangGraph Intelligence Dashboard</div>", unsafe_allow_html=True)
    st.caption("Upload or use demo data to begin analysis.")
    st.info("👈 Choose a CSV or click 'Use Demo Dataset' to preview analytics.")
    st.stop()

# ------------------- DATA FILTERS -------------------
st.markdown("### 🔍 Data Filters")
col1, col2, col3 = st.columns(3)
segments = df["segment"].unique().tolist() if "segment" in df else []
ages = df["age"] if "age" in df else pd.Series(dtype=int)
purchases = df["total_purchases"] if "total_purchases" in df else pd.Series(dtype=float)

with col1:
    chosen_segment = st.multiselect("Segment", segments, default=segments[:2] if segments else [])
with col2:
    if not ages.empty:
        age_range = st.slider("Age Range", int(ages.min()), int(ages.max()), (int(ages.min()), int(ages.max())))
    else:
        age_range = None
with col3:
    if not purchases.empty:
        purch_range = st.slider("Purchase Range", int(purchases.min()), int(purchases.max()), (int(purchases.min()), int(purchases.max())))
    else:
        purch_range = None

filtered = df.copy()
if "segment" in filtered and chosen_segment:
    filtered = filtered[filtered["segment"].isin(chosen_segment)]
if "age" in filtered and age_range:
    filtered = filtered[(filtered["age"] >= age_range[0]) & (filtered["age"] <= age_range[1])]
if "total_purchases" in filtered and purch_range:
    filtered = filtered[(filtered["total_purchases"] >= purch_range[0]) & (filtered["total_purchases"] <= purch_range[1])]

st.caption(f"📊 Showing {len(filtered):,} / {len(df):,} rows after filtering")

# ------------------- KPI CARDS -------------------
st.markdown("### ⚡ Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Users", f"{filtered['user_id'].nunique() if 'user_id' in filtered else len(filtered):,}")
col2.metric("Avg Purchases", f"{filtered['total_purchases'].mean():.2f}" if "total_purchases" in filtered else "—")
col3.metric("Avg LTV", f"${filtered['customer_lifetime_value'].mean():.2f}" if "customer_lifetime_value" in filtered else "—")
col4.metric("Avg Session Time", f"{filtered['browsing_time_minutes'].mean():.1f} min" if "browsing_time_minutes" in filtered else "—")

# ------------------- CLUSTERING -------------------
if set(["age", "total_purchases", "browsing_time_minutes"]).issubset(filtered.columns):
    st.markdown("### 🎯 Smart Segmentation (K-Means Clusters)")
    try:
        features = filtered[["age", "total_purchases", "browsing_time_minutes"]].fillna(0)
        X = StandardScaler().fit_transform(features)
        kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
        filtered["cluster"] = kmeans.fit_predict(X)
        fig = px.scatter_3d(
            filtered,
            x="age", y="total_purchases", z="browsing_time_minutes",
            color="cluster", color_continuous_scale="Bluered",
            title="3D Cluster Segmentation"
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.warning(f"Clustering skipped: {e}")

# ------------------- ANALYTICS -------------------
st.markdown("### 📈 Data Visualizations")
tab1, tab2, tab3 = st.tabs(["Purchasing Patterns", "Time & Engagement", "Correlations"])

with tab1:
    if "segment" in filtered.columns and "total_purchases" in filtered.columns:
        avg_purch = filtered.groupby("segment")["total_purchases"].mean().sort_values(ascending=False)
        fig1 = px.bar(avg_purch, x=avg_purch.index, y=avg_purch.values, color=avg_purch.index,
                      title="Average Purchases by Segment", text_auto=".2f")
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("No 'segment' or 'total_purchases' column found.")

with tab2:
    if "browsing_time_minutes" in filtered.columns and "total_purchases" in filtered.columns:
        fig2 = px.scatter(filtered, x="browsing_time_minutes", y="total_purchases",
                          color="segment" if "segment" in filtered else None,
                          title="Browsing Time vs Total Purchases")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No browsing/purchase data available.")

with tab3:
    numeric_cols = filtered.select_dtypes("number").columns
    if len(numeric_cols) >= 2:
        corr = filtered[numeric_cols].corr()
        fig3 = px.imshow(corr, text_auto=True, color_continuous_scale="Tealrose", title="Correlation Heatmap")
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("Not enough numeric columns to compute correlation.")

# ------------------- SAVE RESULTS -------------------
ts = datetime.now().strftime("%Y%m%d-%H%M%S")
os.makedirs("outputs/runs", exist_ok=True)
results_path = f"outputs/runs/run-{ts}.json"
summary = {
    "timestamp": ts,
    "n_users": int(filtered['user_id'].nunique() if 'user_id' in filtered else len(filtered)),
    "avg_purchases": float(filtered['total_purchases'].mean()) if 'total_purchases' in filtered else None,
    "avg_ltv": float(filtered['customer_lifetime_value'].mean()) if 'customer_lifetime_value' in filtered else None,
}
with open(results_path, "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2)
st.success(f"Results saved → {results_path}")
st.download_button("⬇️ Download Summary JSON", json.dumps(summary, indent=2), file_name=f"results-{ts}.json")
