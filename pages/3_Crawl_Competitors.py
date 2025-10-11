import os, sys, json, streamlit as st
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from lib.crawler_bridge import crawl_url
from lib.storage import save_crawl  # add this function in storage if you want to save crawls

st.title("🕸️ Crawl Competitor Page")
url = st.text_input("URL", value="https://example.com")
if st.button("Run Crawl"):
    data = crawl_url(url)
    if data.get("status")=="ok" or "title" in data:
        st.success("Done"); st.markdown(f"### {data.get('title','(no title)')}")
        st.write(data.get("snippet") or "_No snippet_")
        st.caption(f"Links found: {data.get('link_count',0)}")
        st.json({"first_10_links": data.get("links", [])[:10]})
    else:
        st.error(f"Error: {data.get('error')}")
