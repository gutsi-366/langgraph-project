#!/usr/bin/env python3
"""
Deployment Helper Script
=======================

This script helps you deploy your LangGraph Analytics Platform to Heroku.
"""

import os
import subprocess
import sys

def check_heroku_cli():
    """Check if Heroku CLI is installed"""
    try:
        result = subprocess.run(['heroku', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Heroku CLI found: {result.stdout.strip()}")
            return True
        else:
            print("❌ Heroku CLI not found")
            return False
    except FileNotFoundError:
        print("❌ Heroku CLI not found")
        return False

def check_git():
    """Check if Git is installed"""
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Git found: {result.stdout.strip()}")
            return True
        else:
            print("❌ Git not found")
            return False
    except FileNotFoundError:
        print("❌ Git not found")
        return False

def create_gitignore():
    """Create .gitignore file"""
    gitignore_content = """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# Environment variables
.env
.env.local
.env.production

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Data files (optional - remove if you want to include data)
data/
outputs/
cache/

# Heroku
.heroku/
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    print("✅ Created .gitignore file")

def main():
    print("🚀 LangGraph Analytics Platform - Deployment Helper")
    print("=" * 50)
    
    # Check prerequisites
    print("\n📋 Checking prerequisites...")
    heroku_ok = check_heroku_cli()
    git_ok = check_git()
    
    if not heroku_ok:
        print("\n❌ Please install Heroku CLI first:")
        print("   https://devcenter.heroku.com/articles/heroku-cli")
        return
    
    if not git_ok:
        print("\n❌ Please install Git first:")
        print("   https://git-scm.com/downloads")
        return
    
    print("\n✅ All prerequisites found!")
    
    # Create .gitignore
    create_gitignore()
    
    # Get app name
    app_name = input("\n📝 Enter your Heroku app name (or press Enter for auto-generated): ").strip()
    
    if not app_name:
        app_name = "langgraph-analytics-" + str(hash(os.getcwd()))[-8:]
        print(f"   Using auto-generated name: {app_name}")
    
    # Get API key
    api_key = input("\n🔑 Enter your OpenAI API key: ").strip()
    
    if not api_key:
        print("❌ API key is required for deployment")
        return
    
    print(f"\n🚀 Deploying to Heroku as '{app_name}'...")
    
    try:
        # Initialize git if not already done
        if not os.path.exists('.git'):
            print("📁 Initializing Git repository...")
            subprocess.run(['git', 'init'], check=True)
        
        # Add all files
        print("📦 Adding files to Git...")
        subprocess.run(['git', 'add', '.'], check=True)
        
        # Commit
        print("💾 Committing changes...")
        subprocess.run(['git', 'commit', '-m', 'Initial deployment'], check=True)
        
        # Create Heroku app
        print("🌐 Creating Heroku app...")
        subprocess.run(['heroku', 'create', app_name], check=True)
        
        # Set environment variables
        print("⚙️ Setting environment variables...")
        subprocess.run(['heroku', 'config:set', f'OPENAI_API_KEY={api_key}'], check=True)
        subprocess.run(['heroku', 'config:set', 'PROXY_MODEL=gpt-4o-mini'], check=True)
        subprocess.run(['heroku', 'config:set', 'OPENAI_MODEL=gpt-4o-mini'], check=True)
        
        # Deploy
        print("🚀 Deploying to Heroku...")
        subprocess.run(['git', 'push', 'heroku', 'main'], check=True)
        
        # Open app
        print("🎉 Deployment successful!")
        print(f"🌐 Your app is live at: https://{app_name}.herokuapp.com")
        
        open_app = input("\n🌐 Open your app in browser? (y/n): ").strip().lower()
        if open_app == 'y':
            subprocess.run(['heroku', 'open'], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Deployment failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("   1. Make sure you're logged in: heroku login")
        print("   2. Check your API key is valid")
        print("   3. Try running commands manually")
    except KeyboardInterrupt:
        print("\n⏹️ Deployment cancelled by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
