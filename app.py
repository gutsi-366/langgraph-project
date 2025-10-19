"""
LangGraph AI E-commerce Analytics Platform
==========================================

Main Streamlit application that provides a comprehensive analytics platform
with AI-powered insights, real-time processing, and advanced visualizations.

Features:
- Data analysis and visualization
- AI-powered insights with LangGraph agents
- Real-time analytics dashboard
- Industry-specific analytics
- Advanced machine learning models
- Interactive charts and reports
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
try:
    import seaborn as sns  # Optional; app should run without it
    SEABORN_AVAILABLE = True
except Exception:
    SEABORN_AVAILABLE = False
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import sys
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

# Import our modules
try:
    from src.enhanced_agent import EnhancedLangGraphAgent
    from src.advanced_analytics import AdvancedAnalytics
    from src.utils import validate_dataframe, PerformanceTimer, ProjectError
    from src.ui_components import (
        load_css, hero, metric_card, stat_card, info_card, section, divider, 
        feature_card, success_message, error_message, data_table, theme_toggle,
        loading_spinner, skeleton_card, animated_progress_bar, notification
    )
    from src.config import Config
    from src.security import InputValidator, SecurityAuditor
    from src.cache_manager import cache_manager
    
    # Phase 2 imports
    from src.realtime_analytics import get_real_time_analytics, initialize_real_time_analytics
    from src.industry_modules.retail_analytics import RetailAnalytics
    from src.visualizations.advanced_charts import AdvancedVisualizations
    
    MODULES_LOADED = True
    _HAS_UI = True
except ImportError as e:
    st.error(f"Error loading modules: {e}")
    MODULES_LOADED = False
    _HAS_UI = False

# Page configuration
st.set_page_config(
    page_title="LangGraph AI Analytics Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .error-box {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'dataset' not in st.session_state:
    st.session_state.dataset = None
if 'real_time_analytics' not in st.session_state:
    st.session_state.real_time_analytics = None

def main():
    """Main application function."""
    
    # Create hero section with inline styles (no CSS variables)
    st.markdown("""
    <div style="
        text-align: center; 
        padding: 4rem 2rem; 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        border-radius: 20px; 
        margin-bottom: 3rem; 
        color: white;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
    ">
        <div style="font-size: 5rem; margin-bottom: 1.5rem;">🤖</div>
        <h1 style="
            margin: 0; 
            font-size: 3.5rem; 
            font-weight: 800;
            text-shadow: 0 4px 20px rgba(0,0,0,0.3);
            margin-bottom: 1rem;
        ">LangGraph AI E-commerce Analytics Platform</h1>
        <p style="
            margin: 0; 
            font-size: 1.5rem; 
            opacity: 0.9;
            font-weight: 400;
        ">Advanced AI-powered analytics with real-time processing and intelligent insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/200x100/667eea/ffffff?text=LangGraph+AI", width=200)
        
        st.markdown("## 🎯 Navigation")
        page = st.selectbox(
            "Choose a page:",
            ["🏠 Dashboard", "📊 Data Analysis", "❓ Q&A Mode", "🎨 UI Demo", "🔴 Real-time Analytics", "🏭 Industry Analytics", 
             "📈 Advanced Analytics", "📋 Reports", "⚙️ Settings"]
        )
        
        # System status
        if MODULES_LOADED:
            st.markdown("## ✅ System Status")
            st.success("All modules loaded successfully")
            
            # Initialize real-time analytics
            if st.button("🚀 Start Real-time Analytics"):
                try:
                    rt_analytics = initialize_real_time_analytics()
                    st.session_state.real_time_analytics = rt_analytics
                    st.success("Real-time analytics started!")
                except Exception as e:
                    st.error(f"Failed to start real-time analytics: {e}")
        else:
            st.markdown("## ❌ System Status")
            st.error("Some modules failed to load")
    
    # Main content based on page selection
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "📊 Data Analysis":
        show_data_analysis()
    elif page == "❓ Q&A Mode":
        show_qa_mode()
    elif page == "🎨 UI Demo":
        show_ui_demo()
    elif page == "🔴 Real-time Analytics":
        show_realtime_analytics()
    elif page == "🏭 Industry Analytics":
        show_industry_analytics()
    elif page == "📈 Advanced Analytics":
        show_advanced_analytics()
    elif page == "📋 Reports":
        show_reports()
    elif page == "⚙️ Settings":
        show_settings()

def show_dashboard():
    """Show main dashboard."""
    st.header("📊 Analytics Dashboard")
    
    # Load sample data if no dataset is loaded
    if st.session_state.dataset is None:
        if st.button("📁 Load Sample Dataset"):
            try:
                # Try to load the sample dataset
                df = pd.read_csv("data/large_dataset.csv")
                st.session_state.dataset = df
                st.success("✅ Sample dataset loaded successfully!")
                st.rerun()
            except FileNotFoundError:
                st.error("❌ Sample dataset not found. Please upload a dataset.")
                return
            except Exception as e:
                st.error(f"❌ Error loading dataset: {e}")
                return
    
    if st.session_state.dataset is not None:
        df = st.session_state.dataset
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if _HAS_UI:
                metric_card("Total Customers", f"{len(df):,}", icon="👥", color="blue")
            else:
                st.metric("Total Customers", f"{len(df):,}")
        
        with col2:
            if 'total_purchases' in df.columns:
                avg_purchases = df['total_purchases'].mean()
                if _HAS_UI:
                    metric_card("Avg Purchases", f"{avg_purchases:.1f}", icon="🛒", color="green")
                else:
                    st.metric("Avg Purchases", f"{avg_purchases:.1f}")
            else:
                if _HAS_UI:
                    metric_card("Data Columns", f"{len(df.columns)}", icon="📊", color="purple")
                else:
                    st.metric("Data Columns", f"{len(df.columns)}")
        
        with col3:
            if 'customer_lifetime_value' in df.columns:
                avg_clv = df['customer_lifetime_value'].mean()
                if _HAS_UI:
                    metric_card("Avg CLV", f"${avg_clv:,.2f}", icon="💰", color="orange")
                else:
                    st.metric("Avg CLV", f"${avg_clv:,.2f}")
            else:
                if _HAS_UI:
                    metric_card("Data Rows", f"{len(df):,}", icon="📈", color="blue")
                else:
                    st.metric("Data Rows", f"{len(df):,}")
        
        with col4:
            if 'preferred_category' in df.columns:
                top_category = df['preferred_category'].value_counts().index[0]
                if _HAS_UI:
                    metric_card("Top Category", top_category, icon="🏆", color="red")
                else:
                    st.metric("Top Category", top_category)
            else:
                if _HAS_UI:
                    metric_card("Data Size", f"{df.memory_usage(deep=True).sum() / 1024**2:.1f} MB", icon="💾", color="purple")
                else:
                    st.metric("Data Size", f"{df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
        
        # Quick analysis button
        if st.button("🚀 Run Quick Analysis", type="primary"):
            if MODULES_LOADED:
                with st.spinner("Running AI analysis..."):
                    try:
                        agent = EnhancedLangGraphAgent()
                        results = agent.analyze_large_dataset(df)
                        st.session_state.analysis_results = results
                        st.success("✅ Analysis completed successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Analysis failed: {e}")
            else:
                st.error("❌ Modules not loaded. Please check system status.")
        
        # Show data preview
        def show_data_preview():
            st.dataframe(df.head(10))
            
            # Data quality indicators
            from src.utils import validate_dataframe
            df_stats = validate_dataframe(df)['stats']
            data_quality_indicators(df_stats)
        
        collapsible_section("📋 Dataset Preview", show_data_preview, expanded=False)

def show_data_analysis():
    """Show data analysis page."""
    # Simple header with inline styles (no CSS variables)
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
        <div style="font-size: 4rem; margin-bottom: 1rem;">📊</div>
        <h1 style="
            margin: 0; 
            font-size: 3rem; 
            font-weight: 800;
            text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        ">Analyze Dataset</h1>
        <p style="
            margin: 1rem 0 0 0; 
            font-size: 1.3rem; 
            opacity: 0.9;
            font-weight: 400;
        ">Enhanced agent computes KPIs, segments, insights, visualizations, and a professional report.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.dataset is None:
        st.warning("⚠️ Please load a dataset first from the Dashboard page.")
        return
    
    df = st.session_state.dataset
    
    # Analysis options
    st.subheader("🎯 Analysis Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        analysis_type = st.selectbox(
            "Analysis Type:",
            ["Basic Statistics", "Customer Segmentation", "Purchase Analysis", "Trend Analysis"]
        )
    
    with col2:
        if st.button("▶️ Run Analysis"):
            run_analysis(df, analysis_type)
    
    # Show analysis results
    if st.session_state.analysis_results:
        show_analysis_results()

def run_analysis(df, analysis_type):
    """Run the selected analysis."""
    if not MODULES_LOADED:
        st.error("❌ Modules not loaded.")
        return
    
    with st.spinner(f"Running {analysis_type}..."):
        try:
            if analysis_type == "Basic Statistics":
                results = {
                    'type': 'basic_stats',
                    'data': df.describe(),
                    'summary': f"Analyzed {len(df)} records with {len(df.columns)} columns"
                }
            elif analysis_type == "Customer Segmentation":
                if MODULES_LOADED:
                    analytics = AdvancedAnalytics()
                    results = analytics.customer_segmentation(df)
                else:
                    results = {'error': 'Advanced analytics not available'}
            elif analysis_type == "Purchase Analysis":
                if 'total_purchases' in df.columns:
                    results = {
                        'type': 'purchase_analysis',
                        'total_purchases': df['total_purchases'].sum(),
                        'avg_purchases': df['total_purchases'].mean(),
                        'max_purchases': df['total_purchases'].max(),
                        'purchase_distribution': df['total_purchases'].value_counts().head(10)
                    }
                else:
                    results = {'error': 'Purchase data not available'}
            else:
                results = {'type': 'trend_analysis', 'message': 'Trend analysis completed'}
            
            st.session_state.analysis_results = results
            st.success("✅ Analysis completed!")
            
        except Exception as e:
            st.error(f"❌ Analysis failed: {e}")

def show_analysis_results():
    """Show analysis results."""
    results = st.session_state.analysis_results
    
    st.subheader("📈 Analysis Results")
    
    if results.get('type') == 'basic_stats':
        st.dataframe(results['data'])
        st.info(results['summary'])
    
    elif results.get('type') == 'customer_segmentation':
        if 'clusters' in results:
            st.success(f"✅ Found {results['clusters']} customer segments")
            if 'segment_summary' in results:
                st.dataframe(results['segment_summary'])
    
    elif results.get('type') == 'purchase_analysis':
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Purchases", f"{results['total_purchases']:,}")
        with col2:
            st.metric("Average Purchases", f"{results['avg_purchases']:.2f}")
        with col3:
            st.metric("Max Purchases", f"{results['max_purchases']:,}")
    
    elif 'error' in results:
        st.error(f"❌ {results['error']}")
    
    else:
        st.info("Analysis completed successfully!")
        st.json(results)

def show_realtime_analytics():
    """Show real-time analytics page."""
    st.header("🔴 Real-time Analytics")
    
    if st.session_state.real_time_analytics is None:
        st.warning("⚠️ Real-time analytics not started. Please start it from the sidebar.")
        return
    
    rt_analytics = st.session_state.real_time_analytics
    
    # Real-time metrics
    st.subheader("📊 Live Metrics")
    
    metrics = rt_analytics.get_real_time_metrics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Users", metrics.get('active_users', 0))
    
    with col2:
        st.metric("Processing Rate", f"{metrics.get('processing_rate', 0)}/min")
    
    with col3:
        cache_stats = cache_manager.get_stats()
        st.metric("Cache Hit Rate", f"{cache_stats.get('hit_rate', 0):.1%}")
    
    with col4:
        status = "🟢 Running" if metrics.get('status') == 'running' else "🔴 Stopped"
        st.metric("Status", status)
    
    # Simulate real-time data
    if st.button("📡 Simulate Data Stream"):
        sample_data = {
            'user_id': f'user_{np.random.randint(1000, 9999)}',
            'event_type': 'purchase',
            'timestamp': datetime.now(),
            'amount': np.random.uniform(10, 500)
        }
        
        rt_analytics.data_stream.process_record(sample_data)
        st.success("✅ Data streamed successfully!")

def show_industry_analytics():
    """Show industry-specific analytics."""
    st.header("🏭 Industry Analytics")
    
    if st.session_state.dataset is None:
        st.warning("⚠️ Please load a dataset first.")
        return
    
    df = st.session_state.dataset
    
    industry_type = st.selectbox(
        "Select Industry:",
        ["Retail", "B2B", "SaaS", "Marketplace"]
    )
    
    if industry_type == "Retail" and MODULES_LOADED:
        if st.button("🏪 Run Retail Analytics"):
            with st.spinner("Running retail analytics..."):
                try:
                    retail_analytics = RetailAnalytics()
                    
                    # Inventory analysis
                    inventory_analysis = retail_analytics.analyze_inventory_turnover(df)
                    st.success("✅ Inventory analysis completed!")
                    
                    # Customer journey analysis
                    customer_journey = retail_analytics.analyze_customer_journey(df)
                    st.success("✅ Customer journey analysis completed!")
                    
                    # Show results
                    def show_inventory_results():
                        if 'turnover_metrics' in inventory_analysis:
                            metrics = inventory_analysis['turnover_metrics']['overall_metrics']
                            st.metric("Average Turnover Rate", f"{metrics.get('avg_turnover_rate', 0):.2f}")
                            st.metric("High Turnover Products", metrics.get('high_turnover_products', 0))
                            st.metric("Low Turnover Products", metrics.get('low_turnover_products', 0))
                    
                    def show_customer_journey_results():
                        if 'lifecycle_stages' in customer_journey:
                            stages = customer_journey['lifecycle_stages']['stage_distribution']
                            st.write("Customer Lifecycle Distribution:")
                            st.bar_chart(stages)
                    
                    collapsible_section("📊 Inventory Analysis Results", show_inventory_results)
                    collapsible_section("🛤️ Customer Journey Results", show_customer_journey_results)
                    
                except Exception as e:
                    st.error(f"❌ Retail analytics failed: {e}")

def show_advanced_analytics():
    """Show advanced analytics page."""
    st.header("📈 Advanced Analytics")
    
    if st.session_state.dataset is None:
        st.warning("⚠️ Please load a dataset first.")
        return
    
    df = st.session_state.dataset
    
    if not MODULES_LOADED:
        st.error("❌ Advanced analytics modules not loaded.")
        return
    
    st.subheader("🔬 Advanced Analytics Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🧠 Customer Segmentation"):
            with st.spinner("Running customer segmentation..."):
                try:
                    analytics = AdvancedAnalytics()
                    results = analytics.customer_segmentation(df)
                    
                    if 'clusters' in results:
                        st.success(f"✅ Found {results['clusters']} customer segments!")
                        if 'segment_summary' in results:
                            st.dataframe(results['segment_summary'])
                    
                except Exception as e:
                    st.error(f"❌ Segmentation failed: {e}")
    
    with col2:
        if st.button("🔍 Anomaly Detection"):
            with st.spinner("Running anomaly detection..."):
                try:
                    analytics = AdvancedAnalytics()
                    results = analytics.anomaly_detection(df)
                    
                    if 'total_anomalies' in results:
                        st.success(f"✅ Found {results['total_anomalies']} anomalies!")
                        if 'anomaly_summary' in results:
                            st.dataframe(results['anomaly_summary'])
                    
                except Exception as e:
                    st.error(f"❌ Anomaly detection failed: {e}")

def show_reports():
    """Show reports page."""
    st.header("📋 Reports")
    
    if st.session_state.analysis_results:
        st.subheader("📊 Analysis Reports")
        
        # Generate report
        if st.button("📄 Generate Report"):
            try:
                if MODULES_LOADED:
                    agent = EnhancedLangGraphAgent()
                    report = agent.generate_report(st.session_state.analysis_results)
                    
                    st.markdown("## 📋 Generated Report")
                    st.markdown(report)
                    
                    # Download option
                    st.download_button(
                        label="📥 Download Report",
                        data=report,
                        file_name=f"analytics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown"
                    )
                else:
                    st.error("❌ Report generation not available.")
                    
            except Exception as e:
                st.error(f"❌ Report generation failed: {e}")
    else:
        st.info("ℹ️ No analysis results available. Please run an analysis first.")

def show_qa_mode():
    """Show Q&A Mode page."""
    # Import the Q&A mode functionality
    import sys
    from pathlib import Path
    
    # Add pages directory to path
    pages_dir = Path(__file__).parent / "pages"
    sys.path.insert(0, str(pages_dir))
    
    # Import and run the Q&A mode
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("qa_mode", pages_dir / "7_QA_Mode.py")
        qa_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(qa_module)
        
        # Run the Q&A mode main function
        qa_module.main()
    except Exception as e:
        st.error(f"Error loading Q&A Mode: {e}")
        st.info("Please check that pages/7_QA_Mode.py exists and is properly configured.")

def show_ui_demo():
    """Show UI Demo page."""
    # Import the UI demo functionality
    import sys
    from pathlib import Path
    
    # Add pages directory to path
    pages_dir = Path(__file__).parent / "pages"
    sys.path.insert(0, str(pages_dir))
    
    # Import and run the UI demo
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("ui_demo", pages_dir / "8_UI_Demo.py")
        ui_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ui_module)
        
        # Run the UI demo main function
        ui_module.main()
    except Exception as e:
        st.error(f"Error loading UI Demo: {e}")
        st.info("Please check that pages/8_UI_Demo.py exists and is properly configured.")

def show_settings():
    """Show settings page."""
    st.header("⚙️ Settings")
    
    st.subheader("🔧 System Configuration")
    
    # Cache management
    if MODULES_LOADED:
        cache_stats = cache_manager.get_stats()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Cache Size", f"{cache_stats.get('size_mb', 0):.2f} MB")
            st.metric("Cache Files", cache_stats.get('file_count', 0))
        
        with col2:
            st.metric("Hit Rate", f"{cache_stats.get('hit_rate', 0):.1%}")
            st.metric("Miss Rate", f"{cache_stats.get('miss_rate', 0):.1%}")
        
        if st.button("🗑️ Clear Cache"):
            cleared_count = cache_manager.clear()
            st.success(f"✅ Cleared {cleared_count} cache files!")
            st.rerun()
    
    # System information
    st.subheader("ℹ️ System Information")
    
    info_data = {
        "Python Version": sys.version,
        "Streamlit Version": st.__version__,
        "Modules Loaded": "✅ Yes" if MODULES_LOADED else "❌ No",
        "Working Directory": os.getcwd(),
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    for key, value in info_data.items():
        st.text(f"{key}: {value}")

if __name__ == "__main__":
    main()