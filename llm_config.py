"""
LLM Configuration for LangGraph AI Platform
==========================================

Simple configuration to enable LLM features.
"""

import os

def setup_llm_environment():
    """Setup environment for LLM features."""
    
    # Method 1: Set environment variable directly
    # Replace 'your_api_key_here' with your actual OpenAI API key
    api_key = "your_api_key_here"  # <-- CHANGE THIS TO YOUR ACTUAL API KEY
    
    if api_key != "your_api_key_here":
        os.environ["OPENAI_API_KEY"] = api_key
        os.environ["OPENAI_MODEL"] = "gpt-4o-mini"
        print("✅ LLM environment configured successfully!")
        return True
    else:
        print("❌ Please set your OpenAI API key in this file")
        print("📝 Instructions:")
        print("   1. Get API key from: https://platform.openai.com/api-keys")
        print("   2. Replace 'your_api_key_here' with your actual key")
        print("   3. Save this file and restart the app")
        return False

def test_llm_connection():
    """Test if LLM connection works."""
    
    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import HumanMessage
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your_api_key_here":
            return False, "No valid API key found"
        
        llm = ChatOpenAI(api_key=api_key, model="gpt-4o-mini")
        response = llm.invoke([HumanMessage(content="Say hello!")])
        return True, response.content
        
    except ImportError:
        return False, "LangChain packages not installed. Run: pip install langchain-openai langchain-core"
    except Exception as e:
        return False, f"Connection failed: {e}"

if __name__ == "__main__":
    print("🤖 LangGraph AI - LLM Configuration Test")
    print("=" * 45)
    
    if setup_llm_environment():
        success, message = test_llm_connection()
        if success:
            print(f"✅ LLM connection successful!")
            print(f"🤖 Test response: {message}")
        else:
            print(f"❌ {message}")
    else:
        print("❌ Configuration incomplete")
