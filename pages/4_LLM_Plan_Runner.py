# pages/4_LLM_Plan_Runner.py
import os, sys, time, glob, json
from pathlib import Path
import streamlit as st

# Make src importable
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.append(str(SRC_DIR))

# Import your LLM-driven agent
try:
    from langgraph_agent import run_agent
    _agent_import_error = None
except Exception as e:
    run_agent = None
    _agent_import_error = e

st.title("🧪 LLM Plan Runner (LangGraph)")

# Environment check
st.caption("Runs your LLM-driven planning/code-generation/execution pipeline and collects outputs.")

with st.expander("Environment check", expanded=False):
    st.write("PROJECT_ROOT:", str(PROJECT_ROOT))
    if _agent_import_error:
        st.error(f"Could not import langgraph_agent: {_agent_import_error}")
    else:
        st.success("langgraph_agent import OK")

# Optional: show current .env keys present (without values)
env_path = PROJECT_ROOT / ".env"
if env_path.exists():
    with st.expander(".env found", expanded=False):
        for line in env_path.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.strip().startswith("#"):
                key = line.split("=",1)[0].strip()
                st.write(f"• {key}=***")
else:
    st.info("No .env file found. The agent will fall back to the non-LLM templates.")

run_btn = st.button("🚀 Run LLM Pipeline")

report_path = PROJECT_ROOT / "outputs" / "report.md"
plots_dir   = PROJECT_ROOT / "outputs" / "plots"
runs_dir    = PROJECT_ROOT / "outputs" / "runs"
plots_dir.mkdir(parents=True, exist_ok=True)

if run_btn:
    if run_agent is None:
        st.error("langgraph_agent.run_agent() not available.")
        st.stop()

    with st.spinner("Running LangGraph agent… this will plan, generate code, execute, and compile a report."):
        try:
            final_state = run_agent()
            st.success("Run complete!")
        except Exception as e:
            st.error(f"Agent crashed: {e}")
            st.stop()

    # Show summary from final_state if available
    with st.expander("Final State (debug)", expanded=False):
        try:
            st.json(final_state)
        except Exception:
            st.write("(final_state not JSON-serializable)")

# Render the latest report if present
st.subheader("📄 Generated Report")
if report_path.exists():
    st.markdown(report_path.read_text(encoding="utf-8"))
    st.download_button("⬇️ Download report.md",
                       report_path.read_bytes(),
                       file_name="report.md",
                       use_container_width=True)
else:
    st.caption("No report.md found yet. Click the Run button above.")

# Show any generated plots
st.subheader("🖼️ Generated Plots")
pngs = sorted(glob.glob(str(plots_dir / "*.png")))
if pngs:
    cols = st.columns(3)
    for i, p in enumerate(pngs):
        with cols[i % 3]:
            st.image(p, caption=Path(p).name, use_container_width=True)
else:
    st.caption("No plots found yet.")

# Convenience: list any saved analysis runs too
if runs_dir.exists():
    with st.expander("Saved Analysis Runs (JSON files)", expanded=False):
        files = sorted(runs_dir.glob("run-*.json"))
        if not files:
            st.write("No saved runs yet.")
        for f in files:
            st.write("•", f.name)
            st.download_button(f"Download {f.name}", f.read_bytes(), file_name=f.name)
