"""
LLM Setup Script for LangGraph AI Platform
==========================================

This script helps you configure OpenAI API access for AI-generated insights.
"""

import os
import sys
from pathlib import Path

def create_env_file():
    """Create .env file with OpenAI configuration."""
    
    print("🔧 Setting up LLM configuration...")
    
    # Check if .env already exists
    env_file = Path(".env")
    if env_file.exists():
        print("⚠️ .env file already exists")
        overwrite = input("Do you want to overwrite it? (y/n): ").lower().strip()
        if overwrite != 'y':
            print("❌ Setup cancelled")
            return False
    
    # Get API key from user
    print("\n📝 Please enter your OpenAI API key:")
    print("   (Get it from: https://platform.openai.com/api-keys)")
    print("   (It should start with 'sk-')")
    
    api_key = input("API Key: ").strip()
    
    if not api_key:
        print("❌ No API key provided")
        return False
    
    if not api_key.startswith('sk-'):
        print("⚠️ Warning: API key doesn't start with 'sk-'. Are you sure it's correct?")
        confirm = input("Continue anyway? (y/n): ").lower().strip()
        if confirm != 'y':
            return False
    
    # Create .env file content
    env_content = f"""# LangGraph AI Platform Configuration
# OpenAI API Configuration
OPENAI_API_KEY={api_key}
OPENAI_MODEL=gpt-4o-mini
OPENAI_BASE_URL=

# Platform Settings
USE_LLM=true
DEBUG_MODE=false
ENABLE_REALTIME=true
ENABLE_ADVANCED_VIZ=true

# Optional: For custom OpenAI endpoints
# OPENAI_BASE_URL=https://your-custom-endpoint.com/v1
"""
    
    # Write .env file
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print(f"✅ .env file created successfully!")
        print(f"📁 Location: {env_file.absolute()}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def test_llm_connection():
    """Test the LLM connection."""
    
    print("\n🧪 Testing LLM connection...")
    
    try:
        # Load environment
        from dotenv import load_dotenv
        load_dotenv()
        
        # Test imports
        try:
            from langchain_openai import ChatOpenAI
            from langchain_core.messages import HumanMessage
            print("✅ LangChain imports successful")
        except ImportError as e:
            print(f"❌ LangChain import failed: {e}")
            print("💡 Run: pip install langchain-openai langchain-core")
            return False
        
        # Test API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("❌ OPENAI_API_KEY not found in environment")
            return False
        
        # Test connection
        llm = ChatOpenAI(
            api_key=api_key,
            model="gpt-4o-mini",
            temperature=0.3
        )
        
        # Simple test
        response = llm.invoke([HumanMessage(content="Say 'Hello from LangGraph AI!'")])
        print(f"✅ LLM connection successful!")
        print(f"🤖 Response: {response.content}")
        return True
        
    except Exception as e:
        print(f"❌ LLM connection failed: {e}")
        
        if "401" in str(e) or "unauthorized" in str(e).lower():
            print("💡 This usually means your API key is invalid or expired")
        elif "quota" in str(e).lower() or "limit" in str(e).lower():
            print("💡 This usually means you've hit your API usage limit")
        elif "network" in str(e).lower() or "connection" in str(e).lower():
            print("💡 This usually means a network connectivity issue")
        
        return False

def install_dependencies():
    """Install required dependencies for LLM."""
    
    print("\n📦 Installing LLM dependencies...")
    
    try:
        import subprocess
        
        packages = [
            "langchain-openai",
            "langchain-core",
            "python-dotenv"
        ]
        
        for package in packages:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        
        print("✅ All dependencies installed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def main():
    """Main setup function."""
    
    print("🤖 LangGraph AI - LLM Setup")
    print("=" * 40)
    
    # Step 1: Install dependencies
    print("\n📦 Step 1: Installing dependencies...")
    if not install_dependencies():
        print("❌ Setup failed at dependency installation")
        return
    
    # Step 2: Create .env file
    print("\n🔑 Step 2: Setting up API key...")
    if not create_env_file():
        print("❌ Setup failed at API key configuration")
        return
    
    # Step 3: Test connection
    print("\n🧪 Step 3: Testing LLM connection...")
    if test_llm_connection():
        print("\n🎉 LLM setup completed successfully!")
        print("\n📝 Next steps:")
        print("1. Restart your Streamlit app")
        print("2. Go to http://localhost:8501")
        print("3. Run an analysis - you should now see AI-generated insights!")
        print("\n🚀 Run: streamlit run app.py")
    else:
        print("\n❌ LLM setup failed")
        print("💡 Check your API key and try again")

if __name__ == "__main__":
    main()
