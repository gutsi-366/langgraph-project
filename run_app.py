"""
Run LangGraph AI Platform with Better Error Handling
===================================================

This script starts the platform with improved error handling and configuration.
"""

import os
import sys
import subprocess
from pathlib import Path

def setup_environment():
    """Setup environment for running the app."""
    
    # Disable LLM features by default to avoid connection errors
    os.environ["OPENAI_API_KEY"] = ""
    
    # Set other useful environment variables
    os.environ["STREAMLIT_SERVER_PORT"] = "8501"
    os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
    
    print("🔧 Environment configured for local analytics mode")

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import streamlit
        import pandas
        import numpy
        import matplotlib
        import seaborn
        import plotly
        print("✅ All required dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Run: pip install -r requirements.txt")
        return False

def check_data_files():
    """Check if required data files exist."""
    data_file = Path("data/large_dataset.csv")
    if data_file.exists():
        print("✅ Sample dataset found")
        return True
    else:
        print("⚠️ Sample dataset not found")
        print("💡 The app will work, but you'll need to upload your own data")
        return True

def run_streamlit_app():
    """Run the Streamlit application."""
    print("\n🚀 Starting LangGraph AI Analytics Platform...")
    print("=" * 60)
    
    try:
        # Start Streamlit
        result = subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.headless", "true"
        ], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start Streamlit: {e}")
        print("\n💡 Try running manually:")
        print("   streamlit run app.py")
        return False
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
        return True

def main():
    """Main function."""
    print("🤖 LangGraph AI Analytics Platform Launcher")
    print("=" * 50)
    
    # Setup
    setup_environment()
    
    # Checks
    if not check_dependencies():
        return
    
    check_data_files()
    
    print(f"\n🌐 App will be available at: http://localhost:8501")
    print("📱 Network URL will be shown in the terminal")
    print("\n💡 Tips:")
    print("   - LLM features are disabled by default")
    print("   - All local analytics features are fully functional")
    print("   - Press Ctrl+C to stop the app")
    
    # Run app
    run_streamlit_app()

if __name__ == "__main__":
    main()
