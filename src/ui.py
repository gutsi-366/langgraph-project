import streamlit as st
import pathlib
import time
from typing import Optional, Any, Dict

def load_css():
    """Load enhanced CSS with modern styling and animations."""
    # Enhanced CSS with modern styling
    enhanced_css = """
    /* Modern UI Enhancements */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Enhanced Metric Cards */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 1rem;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    [data-testid="metric-value"] {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: white !important;
    }
    
    [data-testid="metric-label"] {
        font-size: 1rem !important;
        color: rgba(255, 255, 255, 0.9) !important;
    }
    
    /* Loading States */
    .loading-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 2rem;
        min-height: 200px;
    }
    
    .loading-spinner {
        width: 40px;
        height: 40px;
        border: 4px solid #f3f3f3;
        border-top: 4px solid #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .loading-text {
        margin-top: 1rem;
        color: #666;
        font-size: 1.1rem;
    }
    
    /* Enhanced Buttons */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Custom Components */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease;
        border: 1px solid #e9ecef;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
    }
    
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    .status-success {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    
    .status-error {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    
    .status-warning {
        background-color: #fff3cd;
        color: #856404;
        border: 1px solid #ffeaa7;
    }
    
    .status-info {
        background-color: #d1ecf1;
        color: #0c5460;
        border: 1px solid #bee5eb;
    }
    """
    
    # Load existing CSS if file exists
    css_file = pathlib.Path(__file__).resolve().parent / "ui.css"
    existing_css = ""
    if css_file.exists():
        try:
            existing_css = css_file.read_text(encoding="utf-8")
        except Exception:
            pass
    
    # Combine existing and enhanced CSS
    full_css = existing_css + "\n" + enhanced_css
    st.markdown(f"<style>{full_css}</style>", unsafe_allow_html=True)

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

def loading_spinner(text: str = "Loading..."):
    """Display a loading spinner with custom text."""
    st.markdown(f"""
    <div class="loading-container">
        <div class="loading-spinner"></div>
        <div class="loading-text">{text}</div>
    </div>
    """, unsafe_allow_html=True)

def status_badge(text: str, status: str = "info"):
    """Display a status badge with different styles."""
    st.markdown(f'<span class="status-badge status-{status}">{text}</span>', unsafe_allow_html=True)

def enhanced_hero(title: str, subtitle: str = "", features: Optional[list] = None):
    """Enhanced hero section with optional features grid."""
    st.markdown(f"""
    <div class="hero-section">
        <h1 style="margin:0;font-size:3rem;font-weight:700;">{title}</h1>
        <p style="opacity:.9;margin-top:1rem;font-size:1.2rem;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if features:
        st.markdown('<div class="feature-grid">', unsafe_allow_html=True)
        for feature in features:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{feature.get('icon', '✨')}</div>
                <div class="feature-title">{feature.get('title', '')}</div>
                <div class="feature-description">{feature.get('description', '')}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def progress_with_status(current: int, total: int, status_text: str = ""):
    """Display progress with status text."""
    progress = current / total
    st.progress(progress)
    if status_text:
        st.caption(status_text)

def kpi_card(label: str, value: str, change: Optional[str] = None, icon: str = ""):
    """Enhanced KPI card with optional change indicator and icon."""
    change_html = f'<div style="opacity:.7;font-size:12px;margin-top:4px">{change}</div>' if change else ""
    icon_html = f'<div style="font-size:1.5rem;margin-bottom:0.5rem;">{icon}</div>' if icon else ""
    
    st.markdown(f"""
    <div class="card">
        {icon_html}
        <h4>{label}</h4>
        <div style="font-size:22px;font-weight:700;margin-top:2px">{value}</div>
        {change_html}
    </div>
    """, unsafe_allow_html=True)

def info_box(title: str, content: str, type: str = "info"):
    """Display an info box with different types."""
    icons = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌"
    }
    icon = icons.get(type, "ℹ️")
    
    st.markdown(f"""
    <div class="st{type.capitalize()}" style="padding: 1rem; border-radius: 8px;">
        <strong>{icon} {title}</strong><br>
        {content}
    </div>
    """, unsafe_allow_html=True)

def collapsible_section(title: str, content: Any, expanded: bool = False):
    """Create a collapsible section."""
    with st.expander(title, expanded=expanded):
        if callable(content):
            content()
        else:
            st.write(content)

def data_quality_indicators(df_stats: Dict[str, Any]):
    """Display data quality indicators."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        completeness = (1 - df_stats.get('missing_percentage', 0) / 100) * 100
        color = "green" if completeness > 90 else "orange" if completeness > 70 else "red"
        st.metric("Data Completeness", f"{completeness:.1f}%", delta=None, 
                 help="Percentage of non-missing values")
    
    with col2:
        duplicates = df_stats.get('duplicate_rows', 0)
        st.metric("Duplicate Rows", f"{duplicates:,}", delta=None,
                 help="Number of duplicate rows in dataset")
    
    with col3:
        memory_usage = df_stats.get('memory_usage_mb', 0)
        st.metric("Memory Usage", f"{memory_usage:.1f} MB", delta=None,
                 help="Memory footprint of the dataset")
    
    with col4:
        numeric_cols = df_stats.get('numeric_columns', 0)
        st.metric("Numeric Columns", f"{numeric_cols}", delta=None,
                 help="Number of numeric columns")

def performance_timer(operation_name: str):
    """Context manager for timing operations with UI feedback."""
    class Timer:
        def __init__(self, name):
            self.name = name
            self.start_time = None
            self.status_container = None
        
        def __enter__(self):
            self.start_time = time.time()
            self.status_container = st.empty()
            self.status_container.info(f"🔄 Starting {self.name}...")
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            duration = time.time() - self.start_time
            if exc_type is None:
                self.status_container.success(f"✅ {self.name} completed in {duration:.2f} seconds")
            else:
                self.status_container.error(f"❌ {self.name} failed after {duration:.2f} seconds")
    
    return Timer(operation_name)

def create_sidebar_metrics():
    """Create sidebar with key metrics and status."""
    with st.sidebar:
        st.markdown("### 📊 System Status")
        
        # Cache status
        try:
            from cache_manager import cache_manager
            cache_stats = cache_manager.get_stats()
            hit_rate = cache_stats.get('hit_rate', 0) * 100
            st.metric("Cache Hit Rate", f"{hit_rate:.1f}%")
        except:
            st.caption("Cache: Not available")
        
        # Data status
        st.metric("Active Dataset", st.session_state.get('current_dataset_rows', 0))
        
        # System info
        st.markdown("---")
        st.caption("🚀 LangGraph AI Analytics")
        st.caption("Version 2.0 Enhanced")
