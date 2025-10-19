# src/agents/langgraph_agent.py
import os
import pandas as pd
from typing import Dict, Any
from dotenv import load_dotenv

from langgraph.graph import StateGraph, END

# Optional LLM (graceful fallback if key missing)
try:
    from langchain_openai import ChatOpenAI
    from langchain.prompts import ChatPromptTemplate
except Exception:
    ChatOpenAI = None
    ChatPromptTemplate = None

load_dotenv()  # load OPENAI_API_KEY from .env if present


def _get_llm():
    """Return an LLM client if OPENAI_API_KEY is present, else None."""
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key or ChatOpenAI is None:
        return None
    # Use a light/cheap model; change if you have access to larger ones
    return ChatOpenAI(model="gpt-4o-mini", temperature=0.3, api_key=api_key)


# ------------- NODES ------------- #
def load_data_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Load CSV and compute a text summary (head + describe)."""
    path = state.get("dataset_path", "")
    if not path or not os.path.exists(path):
        return {"error": f"Dataset not found: {path}"}

    df = pd.read_csv(path)
    # keep df out of state to avoid serialization issues; only pass text
    head_str = df.head(10).to_string(index=False)
    try:
        desc_str = df.describe(include="all").transpose().to_string()
    except Exception:
        desc_str = "(describe failed)"

    summary = f"Columns: {list(df.columns)}\nRows: {len(df)}\n\nHEAD(10):\n{head_str}\n\nDESCRIBE:\n{desc_str}"
    return {"summary": summary}


def analyze_data_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Use LLM (if available) to infer insights; otherwise simple rules."""
    summary = state.get("summary", "")
    if not summary:
        return {"error": "No data summary found to analyze."}

    llm = _get_llm()
    if llm and ChatPromptTemplate:
        prompt = ChatPromptTemplate.from_template(
            "You are a senior data analyst. Based on the dataset summary below, "
            "write 4-6 concise, practical insights about user behavior, potential segments, "
            "and notable trends. Be specific and business-oriented.\n\n{summary}"
        )
        msgs = prompt.format_messages(summary=summary)
        res = llm.invoke(msgs)
        return {"analysis": res.content.strip()}

    # Fallback (no API key): produce naive insights
    fallback = [
        "Dataset loaded successfully; consider checking missing values and outliers.",
        "Identify high-activity users (e.g., top decile by purchases or browsing time).",
        "Group users by country/region or device to compare KPIs.",
        "Track re-engagement for users with long days-since-login.",
        "Consider VIP cohort (top ~10% value/purchase count) for retention campaigns.",
    ]
    return {"analysis": "- " + "\n- ".join(fallback)}


def report_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Use LLM (if available) to generate a Markdown report; otherwise template it."""
    analysis = state.get("analysis", "").strip()
    summary = state.get("summary", "").strip()

    os.makedirs("outputs", exist_ok=True)
    report_path = os.path.join("outputs", "generated_report.md")

    llm = _get_llm()
    if llm and ChatPromptTemplate:
        prompt = ChatPromptTemplate.from_template(
            "Write a crisp 3–4 section Markdown report for business stakeholders. "
            "Sections: Executive Summary, Key Insights, Recommendations, Data Notes. "
            "Use bullet points where helpful. Keep it under 350 words.\n\n"
            "DATA SUMMARY:\n{summary}\n\nINSIGHTS:\n{analysis}"
        )
        msgs = prompt.format_messages(summary=summary, analysis=analysis)
        res = llm.invoke(msgs)
        md = res.content.strip()
    else:
        # Fallback report
        md = (
            "# AI E-commerce Analysis Report\n\n"
            "## Executive Summary\n"
            "This report presents key observations from the uploaded dataset and offers actionable recommendations.\n\n"
            "## Key Insights\n"
            f"{analysis if analysis else '- (No insights available)'}\n\n"
            "## Recommendations\n"
            "- Focus on retaining high-activity or high-value users.\n"
            "- Improve mobile UX if majority traffic is mobile.\n"
            "- Launch re-engagement for users with long inactivity.\n\n"
            "## Data Notes\n"
            "Basic summary computed from the dataset head/describe. Consider deeper feature engineering for richer insights.\n"
        )

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(md)

    return {"report": md, "report_path": report_path}


# ------------- GRAPH ------------- #
def build_agent_graph():
    """
    Build and compile a simple 3-node LangGraph pipeline:
      load_data -> analyze_data -> report -> END
    Uses dict as the state schema to satisfy newer LangGraph versions.
    """
    graph = StateGraph(dict)  # <-- IMPORTANT: provide state schema
    graph.add_node("load_data", load_data_node)
    graph.add_node("analyze_data", analyze_data_node)
    graph.add_node("report", report_node)

    graph.set_entry_point("load_data")
    graph.add_edge("load_data", "analyze_data")
    graph.add_edge("analyze_data", "report")
    graph.add_edge("report", END)

    return graph.compile()
