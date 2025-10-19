#!/usr/bin/env python3
"""
Test Your Own Data
==================

This script helps you test the system with your own e-commerce datasets.
Place your CSV files in the data/ directory and run this script.

Usage:
    python test_with_your_data.py
"""

import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path
import time

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def analyze_your_dataset(file_path):
    """Analyze a specific dataset file."""
    print(f"\n📊 Analyzing: {file_path}")
    print("-" * 40)
    
    try:
        # Load and validate data
        from utils import load_and_validate_csv, validate_dataframe, display_validation_results
        
        df = pd.read_csv(file_path)
        print(f"✅ Loaded dataset: {len(df)} rows, {len(df.columns)} columns")
        
        # Display basic info
        print(f"\n📋 Dataset Information:")
        print(f"   • Shape: {df.shape}")
        print(f"   • Columns: {list(df.columns)}")
        print(f"   • Memory usage: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
        
        # Validate data quality
        validation = validate_dataframe(df)
        print(f"\n🔍 Data Quality Assessment:")
        if validation["is_valid"]:
            print("   ✅ Data validation passed")
        else:
            print("   ⚠️  Data validation issues found:")
            for issue in validation["issues"]:
                print(f"      - {issue}")
        
        # Run enhanced analysis
        from enhanced_agent import EnhancedLangGraphAgent
        
        agent = EnhancedLangGraphAgent()
        
        print(f"\n🤖 Running Enhanced Analysis...")
        start_time = time.time()
        
        results = agent.analyze_large_dataset(df)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"✅ Analysis completed in {duration:.2f} seconds")
        
        # Display key insights
        if "error" not in results:
            print(f"\n📈 Key Insights:")
            
            # Key metrics
            if "key_metrics" in results:
                metrics = results["key_metrics"]
                print(f"   • Total customers: {metrics.get('total_customers', 'N/A')}")
                print(f"   • Average purchase value: ${metrics.get('avg_purchase_value', 0):.2f}")
                print(f"   • Total revenue: ${metrics.get('total_revenue', 0):.2f}")
            
            # Customer segments
            if "customer_segments" in results:
                segments = results["customer_segments"]
                print(f"   • Customer segments: {len(segments)}")
                for segment, data in segments.items():
                    print(f"      - {segment}: {data.get('count', 0)} customers")
            
            # Business insights
            if "business_insights" in results:
                insights = results["business_insights"]
                print(f"   • Business insights generated: {len(insights)}")
                for i, insight in enumerate(insights[:3], 1):  # Show first 3
                    print(f"      {i}. {insight}")
            
            # Advanced analytics (if available)
            if "advanced_analytics" in results and "error" not in results["advanced_analytics"]:
                print(f"\n🧠 Advanced Analytics Results:")
                adv = results["advanced_analytics"]
                
                if "segmentation" in adv:
                    seg = adv["segmentation"]
                    print(f"   • Customer segments: {seg.get('clusters', 'N/A')}")
                    print(f"   • Segmentation quality: {seg.get('silhouette_score', 0):.3f}")
                
                if "anomaly_detection" in adv:
                    anom = adv["anomaly_detection"]
                    analysis = anom.get("analysis", {})
                    print(f"   • Anomalies detected: {analysis.get('total_anomalies', 0)}")
                    print(f"   • Anomaly rate: {analysis.get('anomaly_percentage', 0):.1f}%")
                
                if "clv_prediction" in adv:
                    clv = adv["clv_prediction"]
                    print(f"   • CLV prediction accuracy: {clv.get('accuracy', 0):.3f}")
            
            # Recommendations
            if "recommendations" in results:
                recommendations = results["recommendations"]
                print(f"\n💡 Recommendations:")
                for i, rec in enumerate(recommendations[:5], 1):  # Show first 5
                    print(f"   {i}. {rec}")
            
            # Check generated outputs
            print(f"\n📁 Generated Outputs:")
            output_files = []
            
            # Check for report
            if Path("outputs/report.md").exists():
                size = Path("outputs/report.md").stat().st_size
                print(f"   ✅ Report: outputs/report.md ({size} bytes)")
                output_files.append("outputs/report.md")
            
            # Check for plots
            plots_dir = Path("outputs/plots")
            if plots_dir.exists():
                plot_files = list(plots_dir.glob("*.png"))
                print(f"   ✅ Visualizations: {len(plot_files)} files")
                for plot in plot_files:
                    output_files.append(str(plot))
            
            # Check for runs
            runs_dir = Path("outputs/runs")
            if runs_dir.exists():
                run_files = list(runs_dir.glob("*.json"))
                print(f"   ✅ Analysis runs: {len(run_files)} files")
            
            return {
                "success": True,
                "duration": duration,
                "output_files": output_files,
                "insights_count": len(results.get("business_insights", [])),
                "recommendations_count": len(results.get("recommendations", []))
            }
            
        else:
            print(f"❌ Analysis failed: {results['error']}")
            return {"success": False, "error": results["error"]}
            
    except Exception as e:
        print(f"❌ Error analyzing {file_path}: {e}")
        return {"success": False, "error": str(e)}

def find_datasets():
    """Find all CSV datasets in the data directory."""
    data_dir = Path("data")
    if not data_dir.exists():
        print("❌ Data directory not found. Creating it...")
        data_dir.mkdir()
        return []
    
    csv_files = list(data_dir.glob("*.csv"))
    return csv_files

def create_sample_dataset():
    """Create a sample dataset for testing if none exists."""
    print("📝 Creating sample dataset for testing...")
    
    np.random.seed(42)
    n_customers = 1000
    
    sample_data = pd.DataFrame({
        'user_id': range(1, n_customers + 1),
        'age': np.random.randint(18, 80, n_customers),
        'country': np.random.choice(['USA', 'Canada', 'UK', 'Germany', 'France'], n_customers),
        'total_purchases': np.random.poisson(50, n_customers),
        'last_login_days': np.random.randint(0, 365, n_customers),
        'browsing_time_minutes': np.random.exponential(60, n_customers),
        'avg_order_value': np.random.lognormal(4, 0.5, n_customers),
        'customer_lifetime_value': np.random.lognormal(6, 1, n_customers),
        'preferred_category': np.random.choice(['Electronics', 'Clothing', 'Books', 'Home'], n_customers),
        'device_type': np.random.choice(['Mobile', 'Desktop', 'Tablet'], n_customers),
        'customer_segment': np.random.choice(['VIP', 'Regular', 'New', 'Churned'], n_customers, p=[0.1, 0.6, 0.2, 0.1]),
        'signup_date': pd.date_range('2020-01-01', '2024-01-01', periods=n_customers)
    })
    
    # Save sample dataset
    sample_path = Path("data/sample_ecommerce_data.csv")
    sample_data.to_csv(sample_path, index=False)
    print(f"✅ Sample dataset created: {sample_path}")
    return [sample_path]

def main():
    """Main function to test with your data."""
    print("🧪 TESTING WITH YOUR OWN DATA")
    print("=" * 50)
    
    # Find datasets
    datasets = find_datasets()
    
    if not datasets:
        print("📝 No datasets found. Creating sample dataset...")
        datasets = create_sample_dataset()
    
    print(f"\n📊 Found {len(datasets)} dataset(s) to analyze:")
    for i, dataset in enumerate(datasets, 1):
        print(f"   {i}. {dataset.name}")
    
    # Analyze each dataset
    results = []
    
    for dataset in datasets:
        result = analyze_your_dataset(dataset)
        results.append({
            "file": dataset.name,
            "result": result
        })
        
        # Add separator between analyses
        if dataset != datasets[-1]:
            print("\n" + "=" * 60)
    
    # Summary
    print("\n" + "=" * 50)
    print("🏆 ANALYSIS SUMMARY")
    print("=" * 50)
    
    successful = 0
    total_insights = 0
    total_recommendations = 0
    total_output_files = 0
    
    for result in results:
        file_name = result["file"]
        analysis_result = result["result"]
        
        if analysis_result["success"]:
            successful += 1
            duration = analysis_result["duration"]
            insights = analysis_result["insights_count"]
            recommendations = analysis_result["recommendations_count"]
            output_files = len(analysis_result["output_files"])
            
            print(f"✅ {file_name}: {duration:.2f}s, {insights} insights, {recommendations} recommendations, {output_files} outputs")
            
            total_insights += insights
            total_recommendations += recommendations
            total_output_files += output_files
        else:
            print(f"❌ {file_name}: Failed - {analysis_result.get('error', 'Unknown error')}")
    
    print(f"\n📈 Overall Results:")
    print(f"   • Successful analyses: {successful}/{len(results)}")
    print(f"   • Total insights generated: {total_insights}")
    print(f"   • Total recommendations: {total_recommendations}")
    print(f"   • Total output files: {total_output_files}")
    
    if successful > 0:
        print(f"\n🎉 Your system is working great with your data!")
        print(f"📁 Check the 'outputs/' directory for generated reports and visualizations.")
        
        # Show next steps
        print(f"\n🚀 Next Steps:")
        print(f"   1. Review the generated reports in outputs/report.md")
        print(f"   2. Check visualizations in outputs/plots/")
        print(f"   3. Run 'streamlit run app.py' to see the web interface")
        print(f"   4. Deploy to Streamlit Cloud for public access")
    else:
        print(f"\n❌ All analyses failed. Please check your data format and try again.")
        print(f"💡 Make sure your CSV files have proper column headers and data types.")

if __name__ == "__main__":
    main()
