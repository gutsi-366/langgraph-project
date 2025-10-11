import streamlit as st, pathlib

def load_css():
    css = (pathlib.Path(__file__).resolve().parent / "ui.css").read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def hero(title: str, subtitle: str = ""):
    st.markdown(f"""
    <div class="hero">
      <h1 style="margin:0;font-size:28px;">{title}</h1>
      <p style="opacity:.8;margin-top:6px">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def stat_card(label: str, value: str, sub: str = ""):
    st.markdown(f"""
    <div class="card">
      <h4>{label}</h4>
      <div style="font-size:22px;font-weight:700;margin-top:2px">{value}</div>
      <div style="opacity:.7;font-size:12px;margin-top:4px">{sub}</div>
    </div>
    """, unsafe_allow_html=True)

def section(title: str, right: str = ""):
    st.markdown(
        f'<div style="display:flex;justify-content:space-between;align-items:center;margin-top:6px;margin-bottom:8px">'
        f'<h3 style="margin:0">{title}</h3>'
        f'<div>{right}</div></div>', unsafe_allow_html=True
    )

def pill(text: str):
    st.markdown(f'<span class="pill">{text}</span>', unsafe_allow_html=True)

def divider():
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
