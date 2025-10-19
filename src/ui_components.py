"""
UI Components for Enhanced User Interface
========================================

Reusable UI components with modern styling and animations.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

def load_css():
    """Load custom CSS styles"""
    with open("src/styles.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def theme_toggle():
    """Create a theme toggle button"""
    st.markdown("""
    <div style="position: fixed; top: 20px; right: 20px; z-index: 1000;">
        <button id="theme-toggle" onclick="toggleTheme()" style="
            background: var(--bg-card);
            border: 1px solid var(--border-primary);
            border-radius: 50%;
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: var(--transition);
            box-shadow: var(--shadow-md);
            font-size: 1.5rem;
        " onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'">
            🌙
        </button>
    </div>
    
    <script>
    function toggleTheme() {
        const body = document.body;
        const currentTheme = body.getAttribute('data-theme') || 'dark';
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        body.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        
        // Update button icon
        const button = document.getElementById('theme-toggle');
        button.textContent = newTheme === 'dark' ? '🌙' : '☀️';
    }
    
    // Load saved theme
    document.addEventListener('DOMContentLoaded', function() {
        const savedTheme = localStorage.getItem('theme') || 'dark';
        document.body.setAttribute('data-theme', savedTheme);
        const button = document.getElementById('theme-toggle');
        if (button) {
            button.textContent = savedTheme === 'dark' ? '🌙' : '☀️';
        }
    });
    </script>
    """, unsafe_allow_html=True)

def hero(title, subtitle, icon="🚀", animated=True, variant="default"):
    """Create an enhanced animated hero section with multiple variants"""
    
    variants = {
        "default": {
            "bg": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            "accent": "rgba(102, 126, 234, 0.3)",
            "text_shadow": "0 4px 20px rgba(0,0,0,0.3)"
        },
        "success": {
            "bg": "linear-gradient(135deg, #10b981 0%, #059669 100%)",
            "accent": "rgba(16, 185, 129, 0.3)",
            "text_shadow": "0 4px 20px rgba(0,0,0,0.3)"
        },
        "warning": {
            "bg": "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)",
            "accent": "rgba(245, 158, 11, 0.3)",
            "text_shadow": "0 4px 20px rgba(0,0,0,0.3)"
        },
        "info": {
            "bg": "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)",
            "accent": "rgba(59, 130, 246, 0.3)",
            "text_shadow": "0 4px 20px rgba(0,0,0,0.3)"
        },
        "dark": {
            "bg": "linear-gradient(135deg, #1f2937 0%, #111827 100%)",
            "accent": "rgba(31, 41, 55, 0.3)",
            "text_shadow": "0 4px 20px rgba(0,0,0,0.5)"
        }
    }
    
    style = variants.get(variant, variants["default"])
    animation_class = "floating" if animated else ""
    
    st.markdown(f"""
    <div class="hero-section {animation_class}" style="
        text-align: center;
        padding: 4rem 2rem;
        background: {style['bg']};
        border-radius: 20px;
        margin-bottom: 3rem;
        box-shadow: 0 20px 40px {style['accent']}, 0 0 0 1px rgba(255,255,255,0.1);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
    ">
        <div style="
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 20% 20%, rgba(255,255,255,0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(255,255,255,0.05) 0%, transparent 50%);
            animation: backgroundShift 20s ease-in-out infinite;
        "></div>
        
        <div style="position: relative; z-index: 2;">
            <div style="
                font-size: 5rem; 
                margin-bottom: 1.5rem;
                display: inline-block;
                animation: float 6s ease-in-out infinite;
                filter: drop-shadow(0 0 20px {style['accent']});
                transition: transform 0.3s ease;
            " onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'">{icon}</div>
            
            <h1 style="
                margin: 0; 
                font-size: 3.5rem; 
                font-weight: 800; 
                color: white;
                text-shadow: {style['text_shadow']};
                margin-bottom: 1rem;
                animation: fadeInUp 1s ease-out;
                letter-spacing: -0.02em;
            ">{title}</h1>
            
            <p style="
                font-size: 1.5rem; 
                color: rgba(255,255,255,0.9); 
                margin: 0;
                font-weight: 400;
                animation: fadeInUp 1s ease-out 0.2s both;
                max-width: 600px;
                margin: 0 auto;
                line-height: 1.6;
            ">{subtitle}</p>
            
            <div style="
                margin-top: 2rem;
                display: flex;
                justify-content: center;
                gap: 1rem;
                animation: fadeInUp 1s ease-out 0.4s both;
            ">
                <div style="
                    width: 60px;
                    height: 4px;
                    background: linear-gradient(90deg, rgba(255,255,255,0.8), rgba(255,255,255,0.4));
                    border-radius: 2px;
                    animation: pulse 2s ease-in-out infinite;
                "></div>
                <div style="
                    width: 40px;
                    height: 4px;
                    background: linear-gradient(90deg, rgba(255,255,255,0.6), rgba(255,255,255,0.2));
                    border-radius: 2px;
                    animation: pulse 2s ease-in-out infinite 0.5s;
                "></div>
                <div style="
                    width: 60px;
                    height: 4px;
                    background: linear-gradient(90deg, rgba(255,255,255,0.4), rgba(255,255,255,0.8));
                    border-radius: 2px;
                    animation: pulse 2s ease-in-out infinite 1s;
                "></div>
            </div>
        </div>
    </div>
    
    <style>
    @keyframes fadeInUp {{
        from {{
            opacity: 0;
            transform: translateY(30px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    @keyframes backgroundShift {{
        0%, 100% {{ transform: translateX(0) translateY(0); }}
        25% {{ transform: translateX(-20px) translateY(-10px); }}
        50% {{ transform: translateX(20px) translateY(10px); }}
        75% {{ transform: translateX(-10px) translateY(20px); }}
    }}
    
    @keyframes float {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-10px); }}
    }}
    
    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.5; }}
    }}
    
    .hero-section:hover {{
        transform: translateY(-5px);
        transition: transform 0.3s ease;
    }}
    </style>
    """, unsafe_allow_html=True)

def metric_card(title, value, change=None, icon="📊", color="blue", trend=None, subtitle=None):
    """Create an enhanced modern metric card with animations and trends"""
    colors = {
        "blue": {"primary": "#3b82f6", "light": "#dbeafe", "gradient": "linear-gradient(135deg, #3b82f6, #1d4ed8)"},
        "green": {"primary": "#10b981", "light": "#d1fae5", "gradient": "linear-gradient(135deg, #10b981, #059669)"},
        "purple": {"primary": "#8b5cf6", "light": "#ede9fe", "gradient": "linear-gradient(135deg, #8b5cf6, #7c3aed)"},
        "orange": {"primary": "#f59e0b", "light": "#fef3c7", "gradient": "linear-gradient(135deg, #f59e0b, #d97706)"},
        "red": {"primary": "#ef4444", "light": "#fee2e2", "gradient": "linear-gradient(135deg, #ef4444, #dc2626)"},
        "indigo": {"primary": "#6366f1", "light": "#e0e7ff", "gradient": "linear-gradient(135deg, #6366f1, #4f46e5)"},
        "pink": {"primary": "#ec4899", "light": "#fce7f3", "gradient": "linear-gradient(135deg, #ec4899, #db2777)"},
        "teal": {"primary": "#14b8a6", "light": "#ccfbf1", "gradient": "linear-gradient(135deg, #14b8a6, #0d9488)"}
    }
    
    color_scheme = colors.get(color, colors['blue'])
    
    change_html = ""
    if change is not None:
        change_color = "#10b981" if change >= 0 else "#ef4444"
        change_symbol = "↗" if change >= 0 else "↘"
        change_bg = "#d1fae5" if change >= 0 else "#fee2e2"
        change_html = f"""
        <div style="
            display: inline-flex;
            align-items: center;
            padding: 0.25rem 0.5rem;
            background: {change_bg};
            color: {change_color};
            border-radius: 0.375rem;
            font-size: 0.75rem;
            font-weight: 600;
            margin-top: 0.5rem;
        ">
            <span style="margin-right: 0.25rem;">{change_symbol}</span>
            {abs(change):.1f}%
        </div>
        """
    
    trend_html = ""
    if trend:
        trend_color = "#10b981" if trend == "up" else "#ef4444" if trend == "down" else "#6b7280"
        trend_icon = "📈" if trend == "up" else "📉" if trend == "down" else "➡️"
        trend_html = f"""
        <div style="
            position: absolute;
            top: 1rem;
            right: 1rem;
            font-size: 1.5rem;
            color: {trend_color};
            opacity: 0.7;
        ">{trend_icon}</div>
        """
    
    subtitle_html = f"""
    <div style="
        font-size: 0.75rem;
        color: #6b7280;
        margin-top: 0.25rem;
        font-weight: 400;
    ">{subtitle}</div>
    """ if subtitle else ""
    
    st.markdown(f"""
    <div class="metric-container" style="
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        border: 1px solid #e5e7eb;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        cursor: pointer;
    " onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 20px 25px -5px rgb(0 0 0 / 0.1), 0 10px 10px -5px rgb(0 0 0 / 0.04)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)'">
        {trend_html}
        <div style="
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: {color_scheme['gradient']};
        "></div>
        
        <div style="display: flex; align-items: flex-start; margin-bottom: 1rem;">
            <div style="
                width: 3rem;
                height: 3rem;
                border-radius: 0.75rem;
                background: {color_scheme['gradient']};
                display: flex;
                align-items: center;
                justify-content: center;
                margin-right: 1rem;
                color: white;
                font-size: 1.5rem;
                box-shadow: 0 4px 6px -1px {color_scheme['primary']}40;
                transition: transform 0.2s ease;
            " onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'">{icon}</div>
            <div style="flex: 1;">
                <div style="
                    font-size: 0.875rem; 
                    color: #6b7280; 
                    font-weight: 500;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                    margin-bottom: 0.5rem;
                ">{title}</div>
                <div style="
                    font-size: 2.5rem; 
                    font-weight: 800; 
                    background: {color_scheme['gradient']};
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                    line-height: 1;
                    margin-bottom: 0.5rem;
                ">{value}</div>
                {subtitle_html}
                {change_html}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def stat_card(title, value, icon="📊", color="blue"):
    """Create a statistics card (alias for metric_card)"""
    metric_card(title, value, icon=icon, color=color)

def info_card(title, content, icon="ℹ️", type="info"):
    """Create an info card with different types"""
    colors = {
        "info": {"bg": "#eff6ff", "border": "#3b82f6", "text": "#1e40af"},
        "success": {"bg": "#f0fdf4", "border": "#10b981", "text": "#065f46"},
        "warning": {"bg": "#fffbeb", "border": "#f59e0b", "text": "#92400e"},
        "error": {"bg": "#fef2f2", "border": "#ef4444", "text": "#991b1b"}
    }
    
    color_scheme = colors.get(type, colors["info"])
    
    st.markdown(f"""
    <div style="
        background: {color_scheme['bg']};
        border: 1px solid {color_scheme['border']};
        border-left: 4px solid {color_scheme['border']};
        border-radius: 0.5rem;
        padding: 1rem 1.25rem;
        margin: 1rem 0;
    ">
        <div style="display: flex; align-items: flex-start;">
            <div style="font-size: 1.25rem; margin-right: 0.75rem; margin-top: 0.125rem;">
                {icon}
            </div>
            <div>
                <div style="font-weight: 600; color: {color_scheme['text']}; margin-bottom: 0.5rem;">
                    {title}
                </div>
                <div style="color: {color_scheme['text']}; line-height: 1.5;">
                    {content}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def section(title, description=None):
    """Create a section header"""
    desc_html = f'<p style="color: #6b7280; margin: 0.5rem 0 0 0; font-size: 1rem;">{description}</p>' if description else ""
    
    st.markdown(f"""
    <div style="margin: 2rem 0 1.5rem 0;">
        <h2 style="
            font-size: 1.875rem;
            font-weight: 600;
            color: #1f2937;
            margin: 0;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #e5e7eb;
        ">
            {title}
        </h2>
        {desc_html}
    </div>
    """, unsafe_allow_html=True)

def divider():
    """Create a visual divider"""
    st.markdown("""
    <div style="
        height: 1px;
        background: linear-gradient(90deg, transparent, #e5e7eb, transparent);
        margin: 2rem 0;
    "></div>
    """, unsafe_allow_html=True)

def feature_card(title, description, icon, features=None):
    """Create a feature card"""
    features_html = ""
    if features:
        features_html = "<ul style='margin: 1rem 0 0 0; padding-left: 1.5rem;'>"
        for feature in features:
            features_html += f"<li style='color: #6b7280; margin-bottom: 0.5rem;'>{feature}</li>"
        features_html += "</ul>"
    
    st.markdown(f"""
    <div class="card" style="
        background: white;
        border-radius: 0.75rem;
        padding: 1.5rem;
        box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
        border: 1px solid #e5e7eb;
        transition: all 0.2s ease-in-out;
        margin-bottom: 1rem;
    ">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="
                width: 3rem;
                height: 3rem;
                border-radius: 0.75rem;
                background: linear-gradient(135deg, #3b82f6, #8b5cf6);
                display: flex;
                align-items: center;
                justify-content: center;
                margin-right: 1rem;
                color: white;
                font-size: 1.5rem;
            ">
                {icon}
            </div>
            <div>
                <h3 style="font-size: 1.25rem; font-weight: 600; color: #1f2937; margin: 0;">
                    {title}
                </h3>
                <p style="color: #6b7280; margin: 0.5rem 0 0 0;">
                    {description}
                </p>
            </div>
        </div>
        {features_html}
    </div>
    """, unsafe_allow_html=True)

def progress_bar(value, max_value=100, label="Progress", color="blue"):
    """Create a modern progress bar"""
    colors = {
        "blue": "#3b82f6",
        "green": "#10b981",
        "purple": "#8b5cf6",
        "orange": "#f59e0b"
    }
    
    percentage = (value / max_value) * 100
    color_hex = colors.get(color, colors["blue"])
    
    st.markdown(f"""
    <div style="margin: 1rem 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="font-weight: 500; color: #374151;">{label}</span>
            <span style="font-weight: 600; color: {color_hex};">{value}/{max_value}</span>
        </div>
        <div style="
            width: 100%;
            height: 0.5rem;
            background: #e5e7eb;
            border-radius: 0.25rem;
            overflow: hidden;
        ">
            <div style="
                width: {percentage}%;
                height: 100%;
                background: linear-gradient(90deg, {color_hex}, {color_hex}aa);
                border-radius: 0.25rem;
                transition: width 0.3s ease-in-out;
            "></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def status_badge(status, type="info"):
    """Create a status badge"""
    colors = {
        "info": {"bg": "#dbeafe", "text": "#1e40af"},
        "success": {"bg": "#d1fae5", "text": "#065f46"},
        "warning": {"bg": "#fef3c7", "text": "#92400e"},
        "error": {"bg": "#fee2e2", "text": "#991b1b"}
    }
    
    color_scheme = colors.get(type, colors["info"])
    
    st.markdown(f"""
    <span style="
        display: inline-block;
        padding: 0.25rem 0.75rem;
        background: {color_scheme['bg']};
        color: {color_scheme['text']};
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    ">
        {status}
    </span>
    """, unsafe_allow_html=True)

def data_table(df, title="Data Table", height=400):
    """Create a styled data table"""
    st.markdown(f"<h3 style='margin-bottom: 1rem; color: #1f2937;'>{title}</h3>", unsafe_allow_html=True)
    
    # Style the dataframe
    styled_df = df.style.set_properties(**{
        'background-color': '#f8fafc',
        'border': '1px solid #e5e7eb',
        'border-radius': '0.5rem',
        'padding': '0.75rem'
    }).set_table_styles([
        {'selector': 'thead th', 'props': [
            ('background-color', '#f1f5f9'),
            ('color', '#374151'),
            ('font-weight', '600'),
            ('text-align', 'left'),
            ('padding', '1rem 0.75rem'),
            ('border-bottom', '2px solid #e5e7eb')
        ]},
        {'selector': 'tbody td', 'props': [
            ('padding', '0.75rem'),
            ('border-bottom', '1px solid #f3f4f6')
        ]},
        {'selector': 'tbody tr:hover', 'props': [
            ('background-color', '#f8fafc')
        ]}
    ])
    
    st.dataframe(styled_df, height=height, use_container_width=True)

def loading_spinner(text="Loading..."):
    """Create a custom loading spinner"""
    st.markdown(f"""
    <div style="
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem;
        color: #6b7280;
    ">
        <div style="
            width: 2rem;
            height: 2rem;
            border: 3px solid #e5e7eb;
            border-top: 3px solid #3b82f6;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-right: 1rem;
        "></div>
        {text}
    </div>
    <style>
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
    </style>
    """, unsafe_allow_html=True)

def success_message(message, icon="✅"):
    """Create a success message"""
    st.markdown(f"""
    <div style="
        background: #f0fdf4;
        border: 1px solid #10b981;
        border-left: 4px solid #10b981;
        border-radius: 0.5rem;
        padding: 1rem 1.25rem;
        margin: 1rem 0;
        display: flex;
        align-items: center;
    ">
        <span style="font-size: 1.25rem; margin-right: 0.75rem;">{icon}</span>
        <span style="color: #065f46; font-weight: 500;">{message}</span>
    </div>
    """, unsafe_allow_html=True)

def error_message(message, icon="❌"):
    """Create an error message"""
    st.markdown(f"""
    <div style="
        background: #fef2f2;
        border: 1px solid #ef4444;
        border-left: 4px solid #ef4444;
        border-radius: 0.5rem;
        padding: 1rem 1.25rem;
        margin: 1rem 0;
        display: flex;
        align-items: center;
    ">
        <span style="font-size: 1.25rem; margin-right: 0.75rem;">{icon}</span>
        <span style="color: #991b1b; font-weight: 500;">{message}</span>
    </div>
    """, unsafe_allow_html=True)

def loading_spinner(text="Loading...", size="large"):
    """Create a beautiful loading spinner"""
    size_map = {
        "small": "1rem",
        "medium": "2rem", 
        "large": "3rem"
    }
    
    spinner_size = size_map.get(size, size_map["large"])
    
    st.markdown(f"""
    <div style="
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 3rem;
        text-align: center;
    ">
        <div style="
            width: {spinner_size};
            height: {spinner_size};
            border: 4px solid var(--border-primary);
            border-top: 4px solid var(--primary-color);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-bottom: 1rem;
        "></div>
        <p style="
            color: var(--text-secondary);
            font-size: 1.1rem;
            margin: 0;
            animation: pulse 2s ease-in-out infinite;
        ">{text}</p>
    </div>
    
    <style>
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    </style>
    """, unsafe_allow_html=True)

def skeleton_card(title="Loading...", lines=3):
    """Create a skeleton loading card"""
    skeleton_lines = ""
    for i in range(lines):
        width = 100 - (i * 10) if i < lines - 1 else 60
        skeleton_lines += f"""
        <div style="
            height: 1rem;
            background: linear-gradient(90deg, var(--bg-hover) 25%, var(--border-primary) 50%, var(--bg-hover) 75%);
            background-size: 200% 100%;
            animation: shimmer 1.5s infinite;
            border-radius: 0.25rem;
            margin-bottom: 0.5rem;
            width: {width}%;
        "></div>
        """
    
    st.markdown(f"""
    <div class="card" style="
        background: var(--bg-card);
        border: 1px solid var(--border-primary);
        border-radius: var(--border-radius-lg);
        padding: 2rem;
        margin-bottom: 1.5rem;
        animation: pulse 2s ease-in-out infinite;
    ">
        <div style="
            height: 1.5rem;
            background: linear-gradient(90deg, var(--bg-hover) 25%, var(--border-primary) 50%, var(--bg-hover) 75%);
            background-size: 200% 100%;
            animation: shimmer 1.5s infinite;
            border-radius: 0.25rem;
            margin-bottom: 1rem;
            width: 60%;
        "></div>
        {skeleton_lines}
    </div>
    
    <style>
    @keyframes shimmer {{
        0% {{ background-position: -200% 0; }}
        100% {{ background-position: 200% 0; }}
    }}
    </style>
    """, unsafe_allow_html=True)

def animated_progress_bar(progress, text="Processing...", show_percentage=True):
    """Create an animated progress bar"""
    percentage = int(progress * 100)
    
    st.markdown(f"""
    <div style="
        background: var(--bg-card);
        border: 1px solid var(--border-primary);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        margin: 1rem 0;
    ">
        <div style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
        ">
            <span style="color: var(--text-primary); font-weight: 500;">{text}</span>
            {f'<span style="color: var(--primary-color); font-weight: 600;">{percentage}%</span>' if show_percentage else ''}
        </div>
        <div style="
            width: 100%;
            height: 8px;
            background: var(--bg-hover);
            border-radius: 4px;
            overflow: hidden;
        ">
            <div style="
                width: {percentage}%;
                height: 100%;
                background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
                border-radius: 4px;
                transition: width 0.3s ease;
                position: relative;
            ">
                <div style="
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
                    animation: shimmer 2s infinite;
                "></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def notification(message, type="info", duration=3000):
    """Create a notification toast"""
    colors = {
        "info": {"bg": "var(--primary-color)", "icon": "ℹ️"},
        "success": {"bg": "var(--success-color)", "icon": "✅"},
        "warning": {"bg": "var(--warning-color)", "icon": "⚠️"},
        "error": {"bg": "var(--error-color)", "icon": "❌"}
    }
    
    color_scheme = colors.get(type, colors["info"])
    
    st.markdown(f"""
    <div id="notification" style="
        position: fixed;
        top: 20px;
        right: 20px;
        background: {color_scheme['bg']};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-lg);
        z-index: 1000;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        animation: slideIn 0.3s ease-out;
    ">
        <span style="font-size: 1.2rem;">{color_scheme['icon']}</span>
        <span>{message}</span>
    </div>
    
    <script>
    setTimeout(function() {{
        const notification = document.getElementById('notification');
        if (notification) {{
            notification.style.animation = 'slideOut 0.3s ease-in forwards';
            setTimeout(() => notification.remove(), 300);
        }}
    }}, {duration});
    </script>
    
    <style>
    @keyframes slideIn {{
        from {{ transform: translateX(100%); opacity: 0; }}
        to {{ transform: translateX(0); opacity: 1; }}
    }}
    @keyframes slideOut {{
        from {{ transform: translateX(0); opacity: 1; }}
        to {{ transform: translateX(100%); opacity: 0; }}
    }}
    </style>
    """, unsafe_allow_html=True)
