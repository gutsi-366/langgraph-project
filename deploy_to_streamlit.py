#!/usr/bin/env python3
"""
Streamlit Cloud Deployment Script
================================

This script helps you deploy your LangGraph AI Analytics Platform to Streamlit Cloud.
"""

import os
import subprocess
import sys
from pathlib import Path

def check_requirements():
    """Check if all requirements are met for deployment."""
    print("Checking deployment requirements...")
    
    # Check if we're in a git repository
    if not os.path.exists('.git'):
        print("ERROR: Not a git repository. Please initialize git first:")
        print("   git init")
        print("   git add .")
        print("   git commit -m 'Initial commit'")
        return False
    
    # Check if requirements.txt exists
    if not os.path.exists('requirements.txt'):
        print("ERROR: requirements.txt not found")
        return False
    
    # Check if app.py exists
    if not os.path.exists('app.py'):
        print("ERROR: app.py not found")
        return False
    
    print("SUCCESS: All requirements met!")
    return True

def create_streamlit_config():
    """Create Streamlit configuration for deployment."""
    print("Creating Streamlit configuration...")
    
    config_content = """[server]
port = 8501
headless = true
enableCORS = false
enableXsrfProtection = false

[theme]
primaryColor = "#6366f1"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[browser]
gatherUsageStats = false
"""
    
    os.makedirs('.streamlit', exist_ok=True)
    with open('.streamlit/config.toml', 'w') as f:
        f.write(config_content)
    
    print("SUCCESS: Streamlit config created!")

def create_secrets_template():
    """Create secrets template for environment variables."""
    print("Creating secrets template...")
    
    secrets_content = """# Streamlit Cloud Secrets
# Copy this file to .streamlit/secrets.toml and add your actual values

[secrets]
# Optional: OpenAI API key for advanced features
# OPENAI_API_KEY = "your_openai_api_key_here"

# Optional: Custom configuration
# MAX_FILE_SIZE_MB = 100
# CACHE_TTL_SECONDS = 3600
# DEBUG = false
"""
    
    with open('.streamlit/secrets.toml.template', 'w') as f:
        f.write(secrets_content)
    
    print("SUCCESS: Secrets template created!")

def create_deployment_readme():
    """Create deployment-specific README."""
    print("Creating deployment README...")
    
    readme_content = """# Streamlit Cloud Deployment

## Quick Deploy

1. **Fork this repository** on GitHub
2. **Go to [Streamlit Cloud](https://streamlit.io/cloud)**
3. **Click "New app"**
4. **Select your forked repository**
5. **Set main file path to `app.py`**
6. **Click "Deploy"**

## Environment Variables (Optional)

If you want to use advanced features, add these to your Streamlit Cloud secrets:

```
OPENAI_API_KEY = "your_api_key_here"
```

## Custom Domain (Optional)

1. **Go to your app settings** in Streamlit Cloud
2. **Click "Settings"**
3. **Add your custom domain**
4. **Update DNS records** as instructed

## Troubleshooting

- **App not loading?** Check the logs in Streamlit Cloud
- **Import errors?** Make sure all dependencies are in requirements.txt
- **File not found?** Check file paths are correct

## Support

- **Streamlit Docs:** https://docs.streamlit.io/
- **Streamlit Cloud:** https://streamlit.io/cloud
- **GitHub Issues:** Create an issue in this repository
"""
    
    with open('DEPLOYMENT.md', 'w') as f:
        f.write(readme_content)
    
    print("SUCCESS: Deployment README created!")

def main():
    """Main deployment preparation function."""
    print("Preparing LangGraph AI Analytics Platform for Streamlit Cloud deployment...")
    print("=" * 70)
    
    # Check requirements
    if not check_requirements():
        print("\nERROR: Deployment preparation failed. Please fix the issues above.")
        return False
    
    # Create necessary files
    create_streamlit_config()
    create_secrets_template()
    create_deployment_readme()
    
    print("\n" + "=" * 70)
    print("SUCCESS: Deployment preparation complete!")
    print("\nNext steps:")
    print("1. Push your code to GitHub:")
    print("   git add .")
    print("   git commit -m 'Prepare for Streamlit Cloud deployment'")
    print("   git push origin main")
    print("\n2. Go to https://streamlit.io/cloud")
    print("3. Click 'New app' and select your repository")
    print("4. Set main file path to 'app.py'")
    print("5. Click 'Deploy'")
    print("\nYour app will be live at: https://your-app-name.streamlit.app")
    
    return True

if __name__ == "__main__":
    main()
