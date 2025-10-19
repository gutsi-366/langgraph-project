#!/usr/bin/env python3
"""
Simple System Test
==================

Basic test to check if the system is working properly.
"""

import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test if all modules can be imported"""
    print("Testing module imports...")
    
    try:
        from src.enhanced_agent import EnhancedLangGraphAgent
        print("  OK: Enhanced agent imported")
    except Exception as e:
        print(f"  ERROR: Enhanced agent import failed: {e}")
        return False
    
    try:
        from src.advanced_analytics import AdvancedAnalytics
        print("  OK: Advanced analytics imported")
    except Exception as e:
        print(f"  ERROR: Advanced analytics import failed: {e}")
        return False
    
    try:
        from src.utils import validate_dataframe
        print("  OK: Utils imported")
    except Exception as e:
        print(f"  ERROR: Utils import failed: {e}")
        return False
    
    return True

def test_data_loading():
    """Test data loading"""
    print("\nTesting data loading...")
    
    try:
        # Check if data files exist
        data_files = [
            "data/large_dataset.csv",
            "data/user_personalized_features.csv"
        ]
        
        for file_path in data_files:
            if Path(file_path).exists():
                df = pd.read_csv(file_path)
                print(f"  OK: {file_path} loaded - {len(df)} rows, {len(df.columns)} columns")
            else:
                print(f"  WARNING: {file_path} not found")
        
        return True
    except Exception as e:
        print(f"  ERROR: Data loading failed: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality"""
    print("\nTesting basic functionality...")
    
    try:
        # Create sample data
        sample_data = pd.DataFrame({
            'user_id': range(1, 101),
            'age': np.random.randint(18, 80, 100),
            'total_purchases': np.random.randint(1, 100, 100),
            'browsing_time_minutes': np.random.randint(10, 300, 100),
            'avg_order_value': np.random.uniform(20, 500, 100),
            'customer_lifetime_value': np.random.uniform(100, 10000, 100)
        })
        
        print(f"  OK: Sample data created - {len(sample_data)} rows")
        
        # Test data validation
        from src.utils import validate_dataframe
        validation = validate_dataframe(sample_data)
        print(f"  OK: Data validation completed - Valid: {validation['is_valid']}")
        
        return True
    except Exception as e:
        print(f"  ERROR: Basic functionality test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("SIMPLE SYSTEM TEST")
    print("=" * 30)
    
    tests = [
        ("Module Imports", test_imports),
        ("Data Loading", test_data_loading),
        ("Basic Functionality", test_basic_functionality)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"  FAILED: {test_name}")
        except Exception as e:
            print(f"  CRASHED: {test_name} - {e}")
    
    print("\n" + "=" * 30)
    print(f"RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("SUCCESS: All tests passed!")
        return True
    else:
        print("ISSUES: Some tests failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
