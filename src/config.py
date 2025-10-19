"""
Configuration management for the LangGraph E-commerce Analytics project.
"""
import os
import logging
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Centralized configuration management."""
    
    # Project paths
    PROJECT_ROOT = Path(__file__).resolve().parents[1]
    SRC_DIR = PROJECT_ROOT / "src"
    DATA_DIR = PROJECT_ROOT / "data"
    OUTPUT_DIR = PROJECT_ROOT / "outputs"
    CACHE_DIR = PROJECT_ROOT / "cache"
    
    # LLM Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
    
    # Alternative LLM Configuration
    PROXY_API_BASE_URL = os.getenv("PROXY_API_BASE_URL")
    PROXY_API_KEY = os.getenv("PROXY_API_KEY")
    PROXY_MODEL = os.getenv("PROXY_MODEL", "gpt-3.5-turbo")
    
    # Application Configuration
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "100"))
    CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "3600"))
    
    # Streamlit Configuration
    STREAMLIT_THEME_BASE = os.getenv("STREAMLIT_THEME_BASE", "light")
    STREAMLIT_SERVER_PORT = int(os.getenv("STREAMLIT_SERVER_PORT", "8501"))
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ALLOWED_FILE_TYPES = os.getenv("ALLOWED_FILE_TYPES", "csv,xlsx,json").split(",")
    
    @classmethod
    def validate_config(cls) -> list[str]:
        """Validate configuration and return list of issues."""
        issues = []
        
        # Check required directories
        for dir_name, dir_path in [
            ("DATA_DIR", cls.DATA_DIR),
            ("OUTPUT_DIR", cls.OUTPUT_DIR),
            ("CACHE_DIR", cls.CACHE_DIR)
        ]:
            if not dir_path.exists():
                try:
                    dir_path.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    issues.append(f"Cannot create {dir_name}: {e}")
        
        # Check LLM configuration
        if not cls.OPENAI_API_KEY and not cls.PROXY_API_KEY:
            issues.append("No LLM API key configured (OPENAI_API_KEY or PROXY_API_KEY)")
        
        # Check file size limits
        if cls.MAX_FILE_SIZE_MB <= 0:
            issues.append("MAX_FILE_SIZE_MB must be positive")
        
        return issues
    
    @classmethod
    def setup_logging(cls):
        """Setup logging configuration."""
        logging.basicConfig(
            level=getattr(logging, cls.LOG_LEVEL.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(cls.OUTPUT_DIR / "app.log"),
                logging.StreamHandler()
            ]
        )
    
    @classmethod
    def get_llm_config(cls) -> dict:
        """Get LLM configuration for LangChain."""
        if cls.OPENAI_API_KEY:
            return {
                "api_key": cls.OPENAI_API_KEY,
                "model": cls.OPENAI_MODEL,
                "base_url": cls.OPENAI_BASE_URL,
                "temperature": 0.1
            }
        elif cls.PROXY_API_KEY:
            return {
                "api_key": cls.PROXY_API_KEY,
                "model": cls.PROXY_MODEL,
                "base_url": cls.PROXY_API_BASE_URL,
                "temperature": 0.1
            }
        else:
            return {}

# Validate configuration on import
config_issues = Config.validate_config()
if config_issues:
    print("⚠️ Configuration Issues:")
    for issue in config_issues:
        print(f"  - {issue}")

# Setup logging
Config.setup_logging()
