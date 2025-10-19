#!/usr/bin/env python3
"""
Demo Script for New UI Design
=============================

Quick demo to showcase the new dark theme and modern design.
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from ui_components import load_css, hero, metric_card, info_card, feature_card, section

def main():
    st.set_page_config(
        page_title="UI Design Demo",
        page_icon="🎨",
        layout="wide"
    )
    
    # Load the new CSS
    load_css()
    
    # Hero Section
    hero(
        "Stunning New Design",
        "Experience the beautiful dark theme with glass effects, gradients, and smooth animations",
        "🎨"
    )
    
    # Metrics Section
    section("Key Metrics", "Beautiful metric cards with gradients and hover effects")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        metric_card("Total Users", "12,345", icon="👥", color="blue")
    
    with col2:
        metric_card("Revenue", "$1.2M", icon="💰", color="green")
    
    with col3:
        metric_card("Growth", "+24%", icon="📈", color="purple")
    
    with col4:
        metric_card("Active", "98.5%", icon="⚡", color="orange")
    
    # Info Cards
    section("Information Cards", "Modern alert boxes with glass effects")
    
    col1, col2 = st.columns(2)
    
    with col1:
        info_card(
            "Success Message",
            "Your data has been processed successfully!",
            "✅",
            "success"
        )
    
    with col2:
        info_card(
            "Info Message", 
            "This is an informational message with modern styling.",
            "ℹ️",
            "info"
        )
    
    # Feature Cards
    section("Feature Showcase", "Beautiful feature cards with hover effects")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        feature_card(
            "AI Analytics",
            "Advanced AI-powered analytics with real-time insights",
            "🤖",
            ["Machine Learning", "Real-time Processing", "Smart Insights"]
        )
    
    with col2:
        feature_card(
            "Data Visualization",
            "Beautiful charts and graphs for data exploration",
            "📊",
            ["Interactive Charts", "Custom Visualizations", "Export Options"]
        )
    
    with col3:
        feature_card(
            "Cloud Integration",
            "Seamless cloud connectivity and data synchronization",
            "☁️",
            ["Real-time Sync", "Secure Storage", "Multi-platform"]
        )
    
    # Sample Data
    section("Data Table", "Styled data tables with dark theme")
    
    # Create sample data
    data = {
        'Product': ['Product A', 'Product B', 'Product C', 'Product D', 'Product E'],
        'Sales': [1200, 1500, 800, 2100, 950],
        'Growth': ['+15%', '+23%', '-5%', '+31%', '+8%'],
        'Status': ['Active', 'Active', 'Inactive', 'Active', 'Pending']
    }
    
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)
    
    # Buttons Demo
    section("Interactive Elements", "Modern buttons with hover effects and animations")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("Primary Action", type="primary"):
            st.success("Primary button clicked!")
    
    with col2:
        if st.button("Secondary Action"):
            st.info("Secondary button clicked!")
    
    with col3:
        if st.button("Success Action", type="primary"):
            st.success("Success action completed!")
    
    with col4:
        if st.button("Warning Action"):
            st.warning("Warning action triggered!")
    
    # Final Message
    st.markdown("""
    <div style="text-align: center; margin: 3rem 0; padding: 2rem; background: var(--bg-card); border-radius: var(--border-radius-lg); border: 1px solid var(--border-primary);">
        <h2 style="color: var(--text-primary); margin-bottom: 1rem;">🎉 Amazing New Design!</h2>
        <p style="color: var(--text-secondary); font-size: 1.1rem; margin: 0;">
            Your LangGraph Analytics Platform now features a stunning dark theme with glass effects, 
            smooth animations, and modern UI components. No more boring white backgrounds!
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
