"""
Basic Functionality Test
=======================

Quick test to verify that the main components of your LangGraph AI platform are working.
"""

import pandas as pd
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def test_data_loading():
    """Test if we can load the sample dataset."""
    print("🧪 Testing data loading...")
    try:
        df = pd.read_csv("data/large_dataset.csv")
        print(f"✅ Dataset loaded successfully! Shape: {df.shape}")
        print(f"   Columns: {list(df.columns)}")
        print(f"   Sample data:\n{df.head(3)}")
        return df
    except Exception as e:
        print(f"❌ Data loading failed: {e}")
        return None

def test_basic_imports():
    """Test if we can import the main modules."""
    print("\n🧪 Testing module imports...")
    
    try:
        from src.utils import validate_dataframe
        print("✅ Utils module imported successfully")
    except Exception as e:
        print(f"❌ Utils import failed: {e}")
    
    try:
        from src.enhanced_agent import EnhancedLangGraphAgent
        print("✅ Enhanced agent imported successfully")
    except Exception as e:
        print(f"❌ Enhanced agent import failed: {e}")
    
    try:
        from src.advanced_analytics import AdvancedAnalytics
        print("✅ Advanced analytics imported successfully")
    except Exception as e:
        print(f"❌ Advanced analytics import failed: {e}")

def test_basic_analytics(df):
    """Test basic analytics functionality."""
    if df is None:
        return
    
    print("\n🧪 Testing basic analytics...")
    
    try:
        # Test data validation
        from src.utils import validate_dataframe
        validation = validate_dataframe(df)
        if validation['is_valid']:
            print("✅ Data validation passed")
        else:
            print(f"❌ Data validation failed: {validation['issues']}")
        
        # Test basic statistics
        print(f"✅ Basic stats calculated:")
        print(f"   - Total customers: {len(df)}")
        print(f"   - Average age: {df['age'].mean():.1f}")
        print(f"   - Average purchases: {df['total_purchases'].mean():.1f}")
        print(f"   - Average CLV: ${df['customer_lifetime_value'].mean():.2f}")
        
    except Exception as e:
        print(f"❌ Basic analytics failed: {e}")

def main():
    """Run all tests."""
    print("🚀 LangGraph AI Platform - Basic Functionality Test")
    print("=" * 60)
    
    # Test data loading
    df = test_data_loading()
    
    # Test imports
    test_basic_imports()
    
    # Test analytics
    test_basic_analytics(df)
    
    print("\n" + "=" * 60)
    print("🎉 Basic functionality test completed!")
    print("\n📝 Next steps:")
    print("1. Your Streamlit app should be running at: http://localhost:8501")
    print("2. Open your browser and go to that URL")
    print("3. Try loading the sample dataset and running analyses")
    print("4. Explore the different features in the sidebar")

if __name__ == "__main__":
    main()
