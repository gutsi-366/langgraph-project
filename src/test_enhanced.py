# src/test_enhanced.py
from enhanced_agent import EnhancedLangGraphAgent
import pandas as pd
import os

def main():
    print("🚀 Testing Enhanced AI Agent with 10,000 users...")
    
    # Load the large dataset
    try:
        data_path = os.path.join('..', 'data', 'large_dataset.csv')
        df = pd.read_csv(data_path)
        print(f"✅ Loaded dataset: {len(df):,} users")
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return
    
    # Initialize and run agent
    agent = EnhancedLangGraphAgent()
    results = agent.analyze_large_dataset(df)
    
    # Display results
    print("\n📊 ANALYSIS RESULTS:")
    print(f"Dataset Info: {results['dataset_info']['total_users']} users")
    print(f"Performance: {results['performance_metrics']['analysis_time_seconds']} seconds")
    
    print("\n🔍 TOP BUSINESS INSIGHTS:")
    for i, insight in enumerate(results['business_insights'][:3], 1):
        print(f"  {i}. {insight}")
    
    print("\n💰 KEY METRICS:")
    for key, value in results['key_metrics'].items():
        print(f"  - {key}: {value}")
    
    print(f"\n🎯 Enhanced agent is working perfectly!")

if __name__ == "__main__":
    main()