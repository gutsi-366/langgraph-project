"""
Unit tests for utility functions.
"""
import pytest
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import (
    validate_dataframe, 
    load_and_validate_csv, 
    format_file_size,
    create_cache_key,
    ProjectError,
    DataValidationError
)

class TestDataValidation:
    """Test data validation functions."""
    
    def test_validate_dataframe_empty(self):
        """Test validation of empty DataFrame."""
        df = pd.DataFrame()
        result = validate_dataframe(df)
        
        assert not result["is_valid"]
        assert "DataFrame is empty" in result["issues"]
    
    def test_validate_dataframe_valid(self):
        """Test validation of valid DataFrame."""
        df = pd.DataFrame({
            'id': [1, 2, 3],
            'name': ['A', 'B', 'C'],
            'value': [10, 20, 30]
        })
        result = validate_dataframe(df)
        
        assert result["is_valid"]
        assert result["stats"]["rows"] == 3
        assert result["stats"]["columns"] == 3
    
    def test_validate_dataframe_missing_columns(self):
        """Test validation with missing required columns."""
        df = pd.DataFrame({
            'id': [1, 2, 3],
            'name': ['A', 'B', 'C']
        })
        result = validate_dataframe(df, required_columns=['id', 'name', 'missing_col'])
        
        assert not result["is_valid"]
        assert "Missing required columns" in result["issues"][0]
    
    def test_validate_dataframe_high_missing_data(self):
        """Test validation with high percentage of missing data."""
        df = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'name': ['A', 'B', None, None, None],
            'value': [10, 20, None, None, None]
        })
        result = validate_dataframe(df)
        
        assert result["is_valid"]  # Should still be valid
        assert len(result["issues"]) > 0  # Should have issues
        assert any("High missing data" in issue for issue in result["issues"])

class TestUtilityFunctions:
    """Test utility functions."""
    
    def test_format_file_size(self):
        """Test file size formatting."""
        assert format_file_size(0) == "0 B"
        assert format_file_size(1024) == "1.00 KB"
        assert format_file_size(1024 * 1024) == "1.00 MB"
        assert format_file_size(1024 * 1024 * 1024) == "1.00 GB"
    
    def test_create_cache_key(self):
        """Test cache key creation."""
        key1 = create_cache_key("test", arg1="value1")
        key2 = create_cache_key("test", arg1="value1")
        key3 = create_cache_key("test", arg1="value2")
        
        assert key1 == key2  # Same arguments should produce same key
        assert key1 != key3  # Different arguments should produce different keys
    
    def test_load_and_validate_csv_valid(self, tmp_path):
        """Test loading and validating a valid CSV."""
        # Create test CSV
        test_file = tmp_path / "test.csv"
        df_test = pd.DataFrame({
            'id': [1, 2, 3],
            'name': ['A', 'B', 'C'],
            'value': [10, 20, 30]
        })
        df_test.to_csv(test_file, index=False)
        
        # Load and validate
        result = load_and_validate_csv(test_file)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 3
        assert list(result.columns) == ['id', 'name', 'value']
    
    def test_load_and_validate_csv_invalid_file(self):
        """Test loading non-existent CSV file."""
        with pytest.raises(ProjectError):
            load_and_validate_csv("nonexistent.csv")

class TestExceptions:
    """Test custom exceptions."""
    
    def test_project_error(self):
        """Test ProjectError exception."""
        with pytest.raises(ProjectError, match="Test error"):
            raise ProjectError("Test error")
    
    def test_data_validation_error(self):
        """Test DataValidationError exception."""
        with pytest.raises(DataValidationError, match="Validation failed"):
            raise DataValidationError("Validation failed")
