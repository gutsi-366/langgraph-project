# pages/8_UI_Demo.py
"""
UI Demo Page - Showcase All New Features
========================================

This page demonstrates all the new UI components and features.
"""

import streamlit as st
import pandas as pd
import numpy as np
import time
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ui_components import (
    load_css, hero, metric_card, stat_card, info_card, section, divider, 
    feature_card, success_message, error_message, data_table, theme_toggle,
    loading_spinner, skeleton_card, animated_progress_bar, notification
)

def main():
    """Main UI Demo function."""
    
    # Hero Section with inline styles (no CSS variables)
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
        <div style="font-size: 4rem; margin-bottom: 1rem;">🎨</div>
        <h1 style="
            margin: 0; 
            font-size: 3rem; 
            font-weight: 800;
            text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        ">UI Components Showcase</h1>
        <p style="
            margin: 1rem 0 0 0; 
            font-size: 1.3rem; 
            opacity: 0.9;
            font-weight: 400;
        ">Experience all the beautiful new components and animations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Loading States Demo
    section("Loading States", "Beautiful loading animations and skeleton screens")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Show Loading Spinner"):
            with st.spinner("Loading..."):
                time.sleep(2)
            notification("Loading completed!", "success")
    
    with col2:
        if st.button("Show Skeleton Cards"):
            for i in range(3):
                skeleton_card(f"Loading Card {i+1}", lines=4)
            time.sleep(2)
            st.success("Skeleton cards loaded!")
    
    with col3:
        if st.button("Show Progress Bar"):
            progress_bar = st.progress(0)
            for i in range(100):
                progress_bar.progress(i + 1)
                time.sleep(0.01)
            notification("Progress completed!", "success")
    
    divider()
    
    # Metrics Demo
    section("Enhanced Metrics", "Beautiful metric cards with animations")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        metric_card("Total Users", "12,345", change=12.5, icon="👥", color="blue")
    
    with col2:
        metric_card("Revenue", "$1.2M", change=8.3, icon="💰", color="green")
    
    with col3:
        metric_card("Growth", "+24%", change=-2.1, icon="📈", color="purple")
    
    with col4:
        metric_card("Active", "98.5%", change=0.5, icon="⚡", color="orange")
    
    divider()
    
    # Feature Cards Demo
    section("Feature Cards", "Interactive cards with hover effects")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        feature_card(
            "AI Analytics",
            "Advanced AI-powered analytics with real-time insights and machine learning",
            "🤖",
            ["Machine Learning", "Real-time Processing", "Smart Insights", "Predictive Analytics"]
        )
    
    with col2:
        feature_card(
            "Data Visualization",
            "Beautiful charts and graphs for comprehensive data exploration",
            "📊",
            ["Interactive Charts", "Custom Visualizations", "Export Options", "Real-time Updates"]
        )
    
    with col3:
        feature_card(
            "Cloud Integration",
            "Seamless cloud connectivity and enterprise-grade security",
            "☁️",
            ["Real-time Sync", "Secure Storage", "Multi-platform", "Scalable Infrastructure"]
        )
    
    divider()
    
    # Info Cards Demo
    section("Info Cards", "Modern alert and info boxes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        info_card(
            "Success Message",
            "Your data has been processed successfully! All analytics are now available.",
            "✅",
            "success"
        )
        
        info_card(
            "Info Message", 
            "This is an informational message with modern styling and glass effects.",
            "ℹ️",
            "info"
        )
    
    with col2:
        info_card(
            "Warning Message",
            "Please review your data before proceeding with the analysis.",
            "⚠️",
            "warning"
        )
        
        info_card(
            "Error Message",
            "There was an issue processing your request. Please try again.",
            "❌",
            "error"
        )
    
    divider()
    
    # Interactive Demo
    section("Interactive Elements", "Buttons and interactive components")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("Primary Action", type="primary"):
            notification("Primary action executed!", "success")
    
    with col2:
        if st.button("Secondary Action"):
            notification("Secondary action executed!", "info")
    
    with col3:
        if st.button("Success Action", type="primary"):
            notification("Success action completed!", "success")
    
    with col4:
        if st.button("Warning Action"):
            notification("Warning action triggered!", "warning")
    
    divider()
    
    # Data Table Demo
    section("Enhanced Data Tables", "Beautiful data tables with hover effects")
    
    # Create sample data
    data = {
        'Product': ['Product A', 'Product B', 'Product C', 'Product D', 'Product E', 'Product F'],
        'Sales': [1200, 1500, 800, 2100, 950, 1800],
        'Growth': ['+15%', '+23%', '-5%', '+31%', '+8%', '+19%'],
        'Status': ['Active', 'Active', 'Inactive', 'Active', 'Pending', 'Active'],
        'Revenue': ['$12K', '$15K', '$8K', '$21K', '$9.5K', '$18K']
    }
    
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)
    
    divider()
    
    # Progress Demo
    section("Progress Indicators", "Animated progress bars and indicators")
    
    if st.button("Start Progress Demo"):
        progress_container = st.container()
        
        with progress_container:
            for i in range(5):
                animated_progress_bar(
                    (i + 1) / 5,
                    f"Processing step {i + 1} of 5...",
                    show_percentage=True
                )
                time.sleep(0.5)
        
        notification("All steps completed successfully!", "success")
    
    divider()
    
    # Theme Demo
    section("Theme Features", "Dark and light theme support")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="
            background: var(--bg-card);
            border: 1px solid var(--border-primary);
            border-radius: var(--border-radius-lg);
            padding: 2rem;
            text-align: center;
        ">
            <h3 style="color: var(--text-primary); margin-bottom: 1rem;">🌙 Dark Theme</h3>
            <p style="color: var(--text-secondary);">
                Beautiful dark theme with glass effects, gradients, and smooth animations.
                Perfect for extended use and modern aesthetics.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="
            background: var(--bg-card);
            border: 1px solid var(--border-primary);
            border-radius: var(--border-radius-lg);
            padding: 2rem;
            text-align: center;
        ">
            <h3 style="color: var(--text-primary); margin-bottom: 1rem;">☀️ Light Theme</h3>
            <p style="color: var(--text-secondary);">
                Clean light theme with subtle shadows and professional styling.
                Great for presentations and bright environments.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Final Message
    st.markdown("""
    <div style="
        text-align: center; 
        margin: 3rem 0; 
        padding: 3rem; 
        background: var(--bg-card); 
        border-radius: var(--border-radius-xl); 
        border: 1px solid var(--border-primary);
        box-shadow: var(--shadow-xl);
    ">
        <h2 style="color: var(--text-primary); margin-bottom: 1.5rem;">🎉 Amazing UI Components!</h2>
        <p style="color: var(--text-secondary); font-size: 1.2rem; margin: 0;">
            Your LangGraph Analytics Platform now features stunning UI components with 
            smooth animations, glass effects, theme switching, and modern design patterns.
            Every interaction feels premium and professional!
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    st.set_page_config(
        page_title="UI Demo - LangGraph Analytics",
        page_icon="🎨",
        layout="wide"
    )
    main()
