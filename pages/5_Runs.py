# pages/5_Runs.py
import os, sys, json
import streamlit as st
import pandas as pd
from pathlib import Path

# Add src/ to path and import storage helpers
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.append(str(SRC_DIR))

from lib.storage import list_runs, load_run, list_crawls  # save_crawl not needed here

st.title("🗂 Saved Items")

tab1, tab2 = st.tabs(["📊 Analyses", "🕸️ Crawls"])

# ---------------------- Analyses ----------------------
with tab1:
    runs = list_runs()
    if not runs:
        st.info("No saved analyses yet. Go to **Analyze** and click **Save analysis**.")
    else:
        st.caption(f"{len(runs)} saved analyses")

        rows = []
        for r in runs:
            summary = r.get("summary") or {}
            rows.append({
                "id": r["id"],
                "total_users": summary.get("total_users") or summary.get("rows"),
                "avg_purchases": summary.get("avg_purchases"),
                "avg_lifetime_value": summary.get("avg_lifetime_value"),
            })
        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        for r in runs:
            with st.expander(f"Open {r['id']}"):
                data = load_run(r["id"])
                if not data:
                    st.warning("Could not load this run.")
                    continue

                if "key_metrics" in data:
                    st.subheader("Key Metrics")
                    st.json(data["key_metrics"])

                if "dataset_info" in data:
                    st.subheader("Dataset Info")
                    st.json(data["dataset_info"])

                if "customer_segments" in data:
                    st.subheader("Customer Segments")
                    seg_df = pd.DataFrame([{"segment": k, **v} for k, v in data["customer_segments"].items()])
                    st.dataframe(seg_df, use_container_width=True)

                if "business_insights" in data:
                    st.subheader("Insights")
                    for i in data["business_insights"]:
                        st.write("• " + str(i))

                if "performance_metrics" in data:
                    st.subheader("Performance")
                    st.json(data["performance_metrics"])

                st.subheader("Raw JSON")
                st.json(data)
                st.download_button(
                    "⬇️ Download JSON",
                    json.dumps(data, indent=2),
                    file_name=f"{r['id']}.json",
                    use_container_width=True
                )

# ---------------------- Crawls ----------------------
with tab2:
    crawls = list_crawls()
    if not crawls:
        st.info("No saved crawls yet. Go to **Crawl Competitors** and run a crawl.")
    else:
        st.caption(f"{len(crawls)} saved crawls")

        df = pd.DataFrame([{
            "id": c["id"],
            "title": c.get("title"),
            "url": c.get("url"),
            "links": c.get("link_count", 0),
        } for c in crawls])
        st.dataframe(df, use_container_width=True, hide_index=True)

        crawls_dir = PROJECT_ROOT / "outputs" / "crawls"
        for c in crawls:
            with st.expander(f"{c['id']}  •  {c.get('title') or '(no title)'}"):
                p = crawls_dir / f"{c['id']}.json"
                if p.exists():
                    data = json.loads(p.read_text(encoding="utf-8"))
                    st.json({
                        "url": data.get("url"),
                        "title": data.get("title"),
                        "snippet": data.get("snippet"),
                        "link_count": data.get("link_count"),
                        "first_10_links": data.get("links", [])[:10],
                    })
                    st.download_button(
                        "⬇️ Download crawl.json",
                        json.dumps(data, indent=2),
                        file_name=f"{c['id']}.json",
                        use_container_width=True
                    )
                else:
                    st.warning("Saved JSON not found on disk.")
