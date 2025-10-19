"""
Configuration Example for LangGraph AI Platform
==============================================

This file shows you how to configure the platform for different scenarios.
"""

import os

# Configuration options
CONFIG = {
    # Set to True to enable LLM features (requires OpenAI API key)
    "USE_LLM": False,
    
    # Set to True to show detailed error messages
    "DEBUG_MODE": True,
    
    # Set to True to enable real-time analytics
    "ENABLE_REALTIME": True,
    
    # Set to True to enable advanced visualizations
    "ENABLE_ADVANCED_VIZ": True
}

def setup_environment():
    """Setup environment variables based on configuration."""
    
    # Disable LLM if not configured
    if not CONFIG["USE_LLM"]:
        os.environ["OPENAI_API_KEY"] = ""
        print("🔧 LLM features disabled - using local analytics only")
    
    # Set debug mode
    if CONFIG["DEBUG_MODE"]:
        print("🐛 Debug mode enabled")
    
    print("✅ Configuration loaded successfully!")

def get_llm_status():
    """Check if LLM is available."""
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if api_key and api_key != "your_api_key_here_if_you_have_one":
        return "✅ LLM Available"
    else:
        return "❌ LLM Not Available (Local analytics only)"

if __name__ == "__main__":
    setup_environment()
    print(f"LLM Status: {get_llm_status()}")
    print("\n📝 To enable LLM features:")
    print("1. Get an OpenAI API key from: https://platform.openai.com/api-keys")
    print("2. Set the environment variable: OPENAI_API_KEY=your_key_here")
    print("3. Set USE_LLM=True in this config file")
