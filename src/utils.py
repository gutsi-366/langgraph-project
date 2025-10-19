"""
Utility functions for error handling, validation, and common operations.
"""
import logging
import traceback
import pandas as pd
import streamlit as st
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
import json
import time
from functools import wraps

logger = logging.getLogger(__name__)

class ProjectError(Exception):
    """Base exception for project-specific errors."""
    pass

class DataValidationError(ProjectError):
    """Raised when data validation fails."""
    pass

class LLMError(ProjectError):
    """Raised when LLM operations fail."""
    pass

class FileProcessingError(ProjectError):
    """Raised when file processing fails."""
    pass

def handle_errors(func):
    """Decorator for consistent error handling."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ProjectError as e:
            logger.error(f"Project error in {func.__name__}: {e}")
            if st.session_state.get('show_errors', True):
                st.error(f"❌ {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {e}")
            logger.error(traceback.format_exc())
            if st.session_state.get('show_errors', True):
                st.error(f"❌ Unexpected error: {str(e)}")
            raise
    return wrapper

def validate_dataframe(df: pd.DataFrame, required_columns: List[str] = None) -> Dict[str, Any]:
    """
    Validate a DataFrame and return validation results.
    
    Args:
        df: DataFrame to validate
        required_columns: List of required column names
        
    Returns:
        Dictionary with validation results and suggestions
    """
    validation_results = {
        "is_valid": True,
        "issues": [],
        "suggestions": [],
        "stats": {}
    }
    
    # Check if DataFrame is empty
    if df.empty:
        validation_results["is_valid"] = False
        validation_results["issues"].append("DataFrame is empty")
        return validation_results
    
    # Check required columns
    if required_columns:
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            validation_results["is_valid"] = False
            validation_results["issues"].append(f"Missing required columns: {missing_columns}")
    
    # Check for completely empty columns
    empty_columns = df.columns[df.isnull().all()].tolist()
    if empty_columns:
        validation_results["issues"].append(f"Completely empty columns: {empty_columns}")
        validation_results["suggestions"].append("Consider removing empty columns")
    
    # Check for high percentage of missing values
    missing_percentages = (df.isnull().sum() / len(df) * 100)
    high_missing_cols = missing_percentages[missing_percentages > 50].index.tolist()
    if high_missing_cols:
        validation_results["issues"].append(f"High missing data (>50%): {high_missing_cols}")
        validation_results["suggestions"].append("Consider data imputation or column removal")
    
    # Basic statistics
    validation_results["stats"] = {
        "rows": len(df),
        "columns": len(df.columns),
        "memory_usage": df.memory_usage(deep=True).sum() / 1024 / 1024,  # MB
        "duplicate_rows": df.duplicated().sum(),
        "numeric_columns": len(df.select_dtypes(include=['number']).columns),
        "categorical_columns": len(df.select_dtypes(include=['object', 'category']).columns)
    }
    
    return validation_results

@handle_errors
def load_and_validate_csv(file_path: Union[str, Path], required_columns: List[str] = None) -> pd.DataFrame:
    """
    Load and validate a CSV file.
    
    Args:
        file_path: Path to CSV file
        required_columns: List of required column names
        
    Returns:
        Validated DataFrame
        
    Raises:
        FileProcessingError: If file cannot be loaded
        DataValidationError: If data validation fails
    """
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Loaded CSV with shape: {df.shape}")
    except Exception as e:
        raise FileProcessingError(f"Failed to load CSV file: {e}")
    
    # Validate the DataFrame
    validation = validate_dataframe(df, required_columns)
    
    if not validation["is_valid"]:
        raise DataValidationError(f"Data validation failed: {'; '.join(validation['issues'])}")
    
    # Log validation results
    if validation["issues"]:
        logger.warning(f"Data issues found: {validation['issues']}")
    
    return df

def create_progress_bar(total_steps: int, description: str = "Processing"):
    """Create a progress bar for Streamlit."""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    def update_progress(current_step: int, step_description: str = None):
        progress = current_step / total_steps
        progress_bar.progress(progress)
        status_text.text(f"{description}: {step_description or f'Step {current_step}/{total_steps}'}")
    
    return update_progress

def display_validation_results(validation_results: Dict[str, Any]):
    """Display validation results in Streamlit."""
    if validation_results["is_valid"]:
        st.success("✅ Data validation passed!")
    else:
        st.error("❌ Data validation failed!")
        for issue in validation_results["issues"]:
            st.error(f"  • {issue}")
    
    if validation_results["suggestions"]:
        st.info("💡 Suggestions:")
        for suggestion in validation_results["suggestions"]:
            st.info(f"  • {suggestion}")
    
    # Display statistics
    stats = validation_results["stats"]
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Rows", f"{stats['rows']:,}")
    with col2:
        st.metric("Columns", stats['columns'])
    with col3:
        st.metric("Memory Usage", f"{stats['memory_usage']:.2f} MB")
    with col4:
        st.metric("Duplicates", stats['duplicate_rows'])

@handle_errors
def safe_execute_code(code: str, timeout: int = 30) -> Dict[str, Any]:
    """
    Safely execute Python code with timeout and error handling.
    
    Args:
        code: Python code to execute
        timeout: Timeout in seconds
        
    Returns:
        Dictionary with execution results
    """
    import subprocess
    import tempfile
    import sys
    from pathlib import Path
    
    # Create temporary file for code execution
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        temp_file = f.name
    
    try:
        # Execute code with timeout
        result = subprocess.run(
            [sys.executable, temp_file],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=Path(__file__).parent.parent
        )
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode
        }
    
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Code execution timed out after {timeout} seconds",
            "return_code": -1
        }
    except Exception as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Execution error: {str(e)}",
            "return_code": -1
        }
    finally:
        # Clean up temporary file
        try:
            Path(temp_file).unlink()
        except:
            pass

def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.2f} {size_names[i]}"

def create_cache_key(*args, **kwargs) -> str:
    """Create a cache key from arguments."""
    key_data = {
        "args": args,
        "kwargs": sorted(kwargs.items()) if kwargs else {}
    }
    return f"cache_{hash(json.dumps(key_data, sort_keys=True, default=str))}"

class PerformanceTimer:
    """Context manager for timing operations."""
    
    def __init__(self, operation_name: str = "Operation"):
        self.operation_name = operation_name
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        logger.info(f"Starting {self.operation_name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        logger.info(f"{self.operation_name} completed in {duration:.2f} seconds")
        
        # Display in Streamlit if available
        if hasattr(st, 'info'):
            st.info(f"⏱️ {self.operation_name} took {duration:.2f} seconds")
