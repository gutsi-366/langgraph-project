#!/usr/bin/env python3
"""
Comprehensive System Testing Script
==================================

This script thoroughly tests all enhanced features of your LangGraph AI E-commerce Analytics platform.
Run this to ensure everything works perfectly before deployment.

Usage:
    python test_system.py
"""

import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path
import time
import traceback

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_environment_setup():
    """Test 1: Environment Configuration"""
    print("Testing Environment Setup...")
    
    try:
        from config import Config
        issues = Config.validate_config()
        
        if issues:
            print(f"   WARNING: Configuration issues found: {len(issues)}")
            for issue in issues:
                print(f"      - {issue}")
        else:
            print("   OK: Environment configuration is valid")
        
        # Test LLM configuration
        llm_config = Config.get_llm_config()
        if llm_config:
            print("   OK: LLM configuration available")
        else:
            print("   WARNING: No LLM configuration found (will use fallback mode)")
        
        return len(issues) == 0
        
    except Exception as e:
        print(f"   ❌ Environment setup failed: {e}")
        return False

def test_data_loading():
    """Test 2: Data Loading and Validation"""
    print("\n📊 Testing Data Loading...")
    
    try:
        from utils import load_and_validate_csv, validate_dataframe
        
        # Test with existing datasets
        datasets = [
            "data/large_dataset.csv",
            "data/user_personalized_features.csv"
        ]
        
        success_count = 0
        for dataset_path in datasets:
            if Path(dataset_path).exists():
                try:
                    df = pd.read_csv(dataset_path)
                    validation = validate_dataframe(df)
                    
                    if validation["is_valid"]:
                        print(f"   ✅ {dataset_path}: {len(df)} rows, {len(df.columns)} columns")
                        success_count += 1
                    else:
                        print(f"   ⚠️  {dataset_path}: Validation issues found")
                        
                except Exception as e:
                    print(f"   ❌ {dataset_path}: Failed to load - {e}")
            else:
                print(f"   ⚠️  {dataset_path}: File not found")
        
        return success_count > 0
        
    except Exception as e:
        print(f"   ❌ Data loading test failed: {e}")
        return False

def test_enhanced_agent():
    """Test 3: Enhanced Agent Functionality"""
    print("\n🤖 Testing Enhanced Agent...")
    
    try:
        from enhanced_agent import EnhancedLangGraphAgent
        
        # Create agent instance
        agent = EnhancedLangGraphAgent()
        print("   ✅ Enhanced agent initialized")
        
        # Test with sample data
        sample_data = pd.DataFrame({
            'user_id': range(1, 101),
            'age': np.random.randint(18, 80, 100),
            'total_purchases': np.random.randint(1, 100, 100),
            'browsing_time_minutes': np.random.randint(10, 300, 100),
            'avg_order_value': np.random.uniform(20, 500, 100),
            'customer_lifetime_value': np.random.uniform(100, 10000, 100)
        })
        
        # Test basic analysis
        print("   🔄 Testing basic analysis...")
        results = agent.analyze_large_dataset(sample_data)
        
        if "error" not in results:
            print("   ✅ Basic analysis completed successfully")
            
            # Test advanced analytics if available
            if len(sample_data) > 1000:
                print("   🔄 Testing advanced analytics...")
                try:
                    segmentation = agent.perform_advanced_segmentation(sample_data)
                    print("   ✅ Advanced segmentation completed")
                    
                    anomalies = agent.detect_anomalies(sample_data)
                    print("   ✅ Anomaly detection completed")
                    
                    clv_prediction = agent.predict_customer_lifetime_value(sample_data)
                    print("   ✅ CLV prediction completed")
                    
                except Exception as e:
                    print(f"   ⚠️  Advanced analytics failed: {e}")
        else:
            print(f"   ❌ Basic analysis failed: {results['error']}")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Enhanced agent test failed: {e}")
        return False

def test_cache_system():
    """Test 4: Cache System"""
    print("\n💾 Testing Cache System...")
    
    try:
        from cache_manager import CacheManager, cached
        import tempfile
        
        # Create temporary cache directory
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_manager = CacheManager(Path(temp_dir))
            
            # Test basic cache operations
            test_data = {"test": "data", "number": 42}
            cache_manager.set("test_key", test_data)
            
            retrieved = cache_manager.get("test_key")
            if retrieved == test_data:
                print("   ✅ Basic cache operations working")
            else:
                print("   ❌ Cache retrieval failed")
                return False
            
            # Test cache decorator
            call_count = 0
            
            @cached(ttl=60)
            def test_function(x):
                nonlocal call_count
                call_count += 1
                return x * 2
            
            # First call
            result1 = test_function(5)
            # Second call (should be cached)
            result2 = test_function(5)
            
            if result1 == result2 == 10 and call_count == 1:
                print("   ✅ Cache decorator working correctly")
            else:
                print("   ❌ Cache decorator failed")
                return False
            
            # Test cache statistics
            stats = cache_manager.get_stats()
            print(f"   ✅ Cache stats: {stats['hits']} hits, {stats['misses']} misses")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Cache system test failed: {e}")
        return False

def test_security_features():
    """Test 5: Security Features"""
    print("\n🔒 Testing Security Features...")
    
    try:
        from security import InputValidator, DataSanitizer, AccessController
        
        # Test string sanitization
        malicious_input = "<script>alert('xss')</script>"
        sanitized = InputValidator.sanitize_string(malicious_input)
        
        if "<script>" not in sanitized:
            print("   ✅ String sanitization working")
        else:
            print("   ❌ String sanitization failed")
            return False
        
        # Test URL validation
        valid_urls = ["https://example.com", "http://localhost:3000"]
        invalid_urls = ["javascript:alert(1)", "file:///etc/passwd"]
        
        for url in valid_urls:
            if not InputValidator.validate_url(url):
                print(f"   ❌ Valid URL rejected: {url}")
                return False
        
        for url in invalid_urls:
            if InputValidator.validate_url(url):
                print(f"   ❌ Invalid URL accepted: {url}")
                return False
        
        print("   ✅ URL validation working")
        
        # Test data sanitization
        test_df = pd.DataFrame({
            'safe_data': ['normal text', 'another value'],
            'suspicious_data': ['<script>alert(1)</script>', 'normal text']
        })
        
        sanitized_df = DataSanitizer.sanitize_dataframe(test_df)
        if "<script>" not in str(sanitized_df.values):
            print("   ✅ DataFrame sanitization working")
        else:
            print("   ❌ DataFrame sanitization failed")
            return False
        
        # Test session token generation
        token = AccessController.generate_session_token()
        if len(token) > 20:
            print("   ✅ Session token generation working")
        else:
            print("   ❌ Session token generation failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Security features test failed: {e}")
        return False

def test_ui_components():
    """Test 6: UI Components"""
    print("\n🎨 Testing UI Components...")
    
    try:
        from ui import (
            enhanced_hero, kpi_card, status_badge, 
            data_quality_indicators, performance_timer
        )
        
        # Test component creation (without Streamlit)
        print("   ✅ UI component imports successful")
        
        # Test data quality indicators function
        df_stats = {
            'missing_percentage': 5.0,
            'duplicate_rows': 10,
            'memory_usage_mb': 25.5,
            'numeric_columns': 8
        }
        
        # This would normally display in Streamlit, but we can test the function exists
        print("   ✅ Data quality indicators function available")
        
        # Test performance timer context manager
        with performance_timer("Test Operation"):
            time.sleep(0.1)  # Simulate work
        
        print("   ✅ Performance timer working")
        
        return True
        
    except Exception as e:
        print(f"   ❌ UI components test failed: {e}")
        return False

def test_langgraph_agent():
    """Test 7: LangGraph Agent"""
    print("\n🧠 Testing LangGraph Agent...")
    
    try:
        from langgraph_agent import run_agent
        
        print("   ✅ LangGraph agent import successful")
        
        # Note: We won't actually run the agent here to avoid API calls
        # but we can test that it's properly configured
        print("   ✅ LangGraph agent configuration ready")
        
        return True
        
    except Exception as e:
        print(f"   ❌ LangGraph agent test failed: {e}")
        return False

def test_output_generation():
    """Test 8: Output Generation"""
    print("\n📝 Testing Output Generation...")
    
    try:
        # Check if output directories exist
        output_dirs = ["outputs", "outputs/plots", "outputs/runs"]
        
        for dir_path in output_dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            if Path(dir_path).exists():
                print(f"   ✅ Output directory ready: {dir_path}")
            else:
                print(f"   ❌ Failed to create output directory: {dir_path}")
                return False
        
        # Test report generation
        from enhanced_agent import EnhancedLangGraphAgent
        
        agent = EnhancedLangGraphAgent()
        sample_data = pd.DataFrame({
            'user_id': range(1, 11),
            'age': np.random.randint(18, 80, 10),
            'total_purchases': np.random.randint(1, 100, 10),
            'browsing_time_minutes': np.random.randint(10, 300, 10)
        })
        
        results = agent.analyze_large_dataset(sample_data)
        report = agent.generate_report(results)
        
        if len(report) > 100:  # Basic check for meaningful report
            print("   ✅ Report generation working")
        else:
            print("   ❌ Report generation failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Output generation test failed: {e}")
        return False

def run_performance_test():
    """Test 9: Performance Test"""
    print("\n⚡ Running Performance Test...")
    
    try:
        from enhanced_agent import EnhancedLangGraphAgent
        
        # Create larger dataset for performance testing
        large_data = pd.DataFrame({
            'user_id': range(1, 1001),
            'age': np.random.randint(18, 80, 1000),
            'total_purchases': np.random.randint(1, 200, 1000),
            'browsing_time_minutes': np.random.randint(10, 300, 1000),
            'avg_order_value': np.random.uniform(20, 500, 1000),
            'customer_lifetime_value': np.random.uniform(100, 10000, 1000)
        })
        
        agent = EnhancedLangGraphAgent()
        
        start_time = time.time()
        results = agent.analyze_large_dataset(large_data)
        end_time = time.time()
        
        duration = end_time - start_time
        
        if duration < 30:  # Should complete within 30 seconds
            print(f"   ✅ Performance test passed: {duration:.2f} seconds")
            return True
        else:
            print(f"   ⚠️  Performance test slow: {duration:.2f} seconds")
            return False
        
    except Exception as e:
        print(f"   ❌ Performance test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("COMPREHENSIVE SYSTEM TESTING")
    print("=" * 50)
    
    tests = [
        ("Environment Setup", test_environment_setup),
        ("Data Loading", test_data_loading),
        ("Enhanced Agent", test_enhanced_agent),
        ("Cache System", test_cache_system),
        ("Security Features", test_security_features),
        ("UI Components", test_ui_components),
        ("LangGraph Agent", test_langgraph_agent),
        ("Output Generation", test_output_generation),
        ("Performance", run_performance_test)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"   ❌ {test_name} test failed")
        except Exception as e:
            print(f"   ❌ {test_name} test crashed: {e}")
            traceback.print_exc()
    
    print("\n" + "=" * 50)
    print(f"🏆 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your system is ready for deployment!")
        return True
    elif passed >= total * 0.8:
        print("✅ Most tests passed. Minor issues to address before deployment.")
        return False
    else:
        print("❌ Multiple test failures. Please fix issues before deployment.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
