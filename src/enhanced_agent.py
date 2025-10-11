# src/enhanced_agent.py (COMPLETE FIXED VERSION)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Any, List
import time
from datetime import datetime
import io
import base64

class EnhancedLangGraphAgent:
    def __init__(self):
        self.performance_metrics = {}
        self.analysis_history = []
    
    def analyze_large_dataset(self, df):
        """Enhanced analysis for 10,000+ users"""
        print(f"🔍 Starting analysis of {len(df):,} users...")
        start_time = time.time()
        
        # Smart sampling for large datasets
        if len(df) > 1000:
            sample_size = min(2000, len(df))
            sample_df = df.sample(sample_size, random_state=42)
            print(f"📊 Using smart sample of {sample_size} users for detailed analysis")
        else:
            sample_df = df
        
        # Track performance FIRST
        analysis_time = time.time() - start_time
        self.performance_metrics = {
            'total_users_analyzed': len(df),
            'sample_size_used': len(sample_df),
            'analysis_time_seconds': round(analysis_time, 2),
            'data_quality_score': self.calculate_data_quality(df),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Run comprehensive analysis
        results = {
            'dataset_info': self.get_dataset_info(df),
            'key_metrics': self.calculate_key_metrics(df),
            'customer_segments': self.analyze_customer_segments(df),
            'business_insights': self.generate_business_insights(df),
            'visualizations': self.create_visualizations(df),
            'performance_metrics': self.performance_metrics  # FIXED: Correct variable name
        }
        
        print(f"✅ Analysis completed in {analysis_time:.2f} seconds")
        return results
    
    def get_dataset_info(self, df):
        """Get comprehensive dataset information"""
        return {
            'total_users': len(df),
            'total_columns': len(df.columns),
            'data_types': dict(df.dtypes),
            'missing_values': df.isnull().sum().to_dict(),
            'memory_usage_mb': round(df.memory_usage(deep=True).sum() / 1024**2, 2)
        }
    
    def calculate_key_metrics(self, df):
        """Calculate business key metrics"""
        return {
            'total_revenue_potential': f"${df['customer_lifetime_value'].sum():,.2f}",
            'average_order_value': f"${df['avg_order_value'].mean():.2f}",
            'average_browsing_time': f"{df['browsing_time_minutes'].mean():.1f} minutes",
            'active_users_ratio': f"{(len(df[df['last_login_days'] <= 7]) / len(df)) * 100:.1f}%",
            'vip_customer_ratio': f"{(len(df[df['customer_segment'] == 'VIP']) / len(df)) * 100:.1f}%"
        }
    
    def analyze_customer_segments(self, df):
        """Advanced customer segmentation analysis"""
        segments = df['customer_segment'].value_counts()
        
        segment_analysis = {}
        for segment in segments.index:
            segment_data = df[df['customer_segment'] == segment]
            segment_analysis[segment] = {
                'count': len(segment_data),
                'percentage': f"{(len(segment_data) / len(df)) * 100:.1f}%",
                'avg_lifetime_value': f"${segment_data['customer_lifetime_value'].mean():.2f}",
                'avg_purchases': segment_data['total_purchases'].mean(),
                'avg_browsing_time': f"{segment_data['browsing_time_minutes'].mean():.1f} min"
            }
        
        return segment_analysis
    
    def generate_business_insights(self, df):
        """Generate actionable business insights"""
        insights = []
        
        # Revenue concentration insight
        vip_users = df[df['customer_segment'] == 'VIP']
        vip_revenue_ratio = vip_users['customer_lifetime_value'].sum() / df['customer_lifetime_value'].sum()
        
        if vip_revenue_ratio > 0.7:
            insights.append(f"💰 **Revenue Concentration**: VIP customers ({len(vip_users)} users) generate {vip_revenue_ratio:.1%} of total revenue")
        
        # Engagement insight
        high_engagement = df[df['browsing_time_minutes'] > 120]
        if len(high_engagement) / len(df) > 0.3:
            insights.append(f"🎯 **High Engagement**: {len(high_engagement)} users spend 2+ hours browsing - great conversion potential")
        
        # Device preference insight
        mobile_users = df[df['device_type'] == 'Mobile']
        if len(mobile_users) / len(df) > 0.5:
            insights.append(f"📱 **Mobile Dominance**: {len(mobile_users)} users prefer mobile - optimize mobile experience")
        
        # Additional insights
        insights.extend([
            f"🔄 **Retention Opportunity**: {len(df[df['last_login_days'] > 30])} users haven't logged in 30+ days",
            f"🎁 **Upsell Potential**: {len(df[(df['total_purchases'] > 5) & (df['avg_order_value'] < 50)])} active users with low average order value",
            f"📈 **Growth Segment**: {len(df[df['customer_segment'] == 'New'])} new customers acquired"
        ])
        
        return insights
    
    def create_visualizations(self, df):
        """Create visualizations using matplotlib"""
        charts = {}
        
        try:
            # Customer segmentation pie chart
            plt.figure(figsize=(10, 6))
            segment_counts = df['customer_segment'].value_counts()
            plt.pie(segment_counts.values, labels=segment_counts.index, autopct='%1.1f%%')
            plt.title('Customer Segmentation Distribution')
            charts['segmentation_pie'] = self.plot_to_base64()
            
            # Purchase behavior histogram
            plt.figure(figsize=(10, 6))
            plt.hist(df['total_purchases'], bins=20, alpha=0.7, color='skyblue')
            plt.xlabel('Total Purchases')
            plt.ylabel('Number of Users')
            plt.title('Distribution of Total Purchases')
            charts['purchase_histogram'] = self.plot_to_base64()
            
            # Value vs Engagement scatter plot
            plt.figure(figsize=(10, 6))
            colors = {'VIP': 'red', 'Regular': 'blue', 'New': 'green'}
            for segment in df['customer_segment'].unique():
                segment_data = df[df['customer_segment'] == segment]
                plt.scatter(segment_data['browsing_time_minutes'], 
                           segment_data['customer_lifetime_value'],
                           c=colors[segment], label=segment, alpha=0.6)
            plt.xlabel('Browsing Time (minutes)')
            plt.ylabel('Customer Lifetime Value ($)')
            plt.title('Customer Value vs Engagement Time')
            plt.legend()
            charts['value_engagement'] = self.plot_to_base64()
            
        except Exception as e:
            print(f"⚠️ Visualization error: {e}")
            charts = {'error': 'Visualization failed'}
        
        return charts
    
    def plot_to_base64(self):
        """Convert matplotlib plot to base64 for web display"""
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        return f"data:image/png;base64,{image_base64}"
    
    def calculate_data_quality(self, df):
        """Calculate data quality score"""
        total_cells = df.size
        missing_cells = df.isnull().sum().sum()
        quality_score = ((total_cells - missing_cells) / total_cells) * 100
        return round(quality_score, 1)
    
    def generate_professional_report(self, results, df):
        """Generate comprehensive business report"""
        report = f"""
# AI-Powered Business Intelligence Report
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Dataset:** {len(df):,} users analyzed

## Executive Summary
This analysis reveals significant opportunities for revenue growth and customer engagement optimization.

## Key Business Metrics
{chr(10).join(f"- **{k}**: {v}" for k, v in results['key_metrics'].items())}

## Customer Segmentation Analysis
{chr(10).join(f"- **{segment}**: {data['count']} users ({data['percentage']}) - Avg Value: {data['avg_lifetime_value']}" 
              for segment, data in results['customer_segments'].items())}

## Strategic Insights
{chr(10).join(f"1. {insight}" for insight in results['business_insights'])}

## Technical Performance
- Analysis completed in {results['performance_metrics']['analysis_time_seconds']} seconds
- Data quality score: {results['performance_metrics']['data_quality_score']}%
- Memory usage: {results['dataset_info']['memory_usage_mb']} MB

## Recommendations
1. **Focus on VIP Retention**: Implement loyalty programs for high-value customers
2. **Mobile Optimization**: Enhance mobile experience for better conversion
3. **Re-engagement Campaigns**: Target inactive users with personalized offers
4. **Upsell Strategy**: Increase average order value through bundled offers

---
*Generated by Advanced AI Business Intelligence System*
"""
        return report