"""
Retail-Specific Analytics Module
===============================

Specialized analytics for retail e-commerce businesses including:
- Inventory turnover analysis
- Seasonal trend analysis
- Customer journey mapping
- Product performance analytics
- Store performance metrics
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import matplotlib.pyplot as plt
try:
    import seaborn as sns  # Optional dependency
    SEABORN_AVAILABLE = True
except Exception:
    SEABORN_AVAILABLE = False
try:
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except Exception:
    KMeans = StandardScaler = None
    SKLEARN_AVAILABLE = False

from utils import handle_errors, PerformanceTimer, ProjectError

class RetailAnalytics:
    """Retail-specific analytics engine."""
    
    def __init__(self):
        self.retail_metrics = {}
        self.seasonal_patterns = {}
        self.inventory_insights = {}
    
    @handle_errors
    def analyze_inventory_turnover(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze inventory turnover patterns.
        
        Args:
            df: DataFrame with product and sales data
            
        Returns:
            Dictionary with inventory turnover analysis
        """
        with PerformanceTimer("Inventory Turnover Analysis"):
            # Calculate inventory turnover metrics
            if 'product_id' in df.columns and 'quantity' in df.columns:
                turnover_analysis = self._calculate_turnover_metrics(df)
                
                # Identify slow-moving products
                slow_moving = self._identify_slow_moving_products(df)
                
                # Seasonal inventory patterns
                seasonal_patterns = self._analyze_seasonal_patterns(df)
                
                # Inventory optimization recommendations
                recommendations = self._generate_inventory_recommendations(turnover_analysis, slow_moving)
                
                return {
                    'turnover_metrics': turnover_analysis,
                    'slow_moving_products': slow_moving,
                    'seasonal_patterns': seasonal_patterns,
                    'recommendations': recommendations,
                    'analysis_timestamp': datetime.now().isoformat()
                }
            else:
                raise ProjectError("Required columns 'product_id' and 'quantity' not found")
    
    def _calculate_turnover_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate inventory turnover metrics."""
        # Group by product and calculate turnover
        product_metrics = df.groupby('product_id').agg({
            'quantity': ['sum', 'count', 'mean'],
            'total_purchases': 'sum' if 'total_purchases' in df.columns else lambda x: x.count()
        }).round(2)
        
        # Calculate turnover rate
        product_metrics['turnover_rate'] = product_metrics[('quantity', 'sum')] / product_metrics[('quantity', 'count')]
        
        # Overall metrics
        overall_turnover = {
            'avg_turnover_rate': product_metrics['turnover_rate'].mean(),
            'total_products': len(product_metrics),
            'high_turnover_products': len(product_metrics[product_metrics['turnover_rate'] > 2.0]),
            'low_turnover_products': len(product_metrics[product_metrics['turnover_rate'] < 0.5])
        }
        
        return {
            'product_level': product_metrics.to_dict('index'),
            'overall_metrics': overall_turnover
        }
    
    def _identify_slow_moving_products(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Identify slow-moving products."""
        product_sales = df.groupby('product_id')['quantity'].sum().sort_values()
        
        # Bottom 20% of products by sales
        slow_moving_threshold = product_sales.quantile(0.2)
        slow_moving_products = product_sales[product_sales <= slow_moving_threshold]
        
        return [
            {
                'product_id': product_id,
                'total_sales': sales,
                'recommendation': 'Consider discounting or bundling'
            }
            for product_id, sales in slow_moving_products.items()
        ]
    
    def _analyze_seasonal_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze seasonal sales patterns."""
        if 'signup_date' in df.columns or 'timestamp' in df.columns:
            # Convert to datetime
            date_col = 'signup_date' if 'signup_date' in df.columns else 'timestamp'
            df[date_col] = pd.to_datetime(df[date_col])
            
            # Extract month and season
            df['month'] = df[date_col].dt.month
            df['season'] = df['month'].map({
                12: 'Winter', 1: 'Winter', 2: 'Winter',
                3: 'Spring', 4: 'Spring', 5: 'Spring',
                6: 'Summer', 7: 'Summer', 8: 'Summer',
                9: 'Fall', 10: 'Fall', 11: 'Fall'
            })
            
            # Seasonal sales analysis
            seasonal_sales = df.groupby('season')['quantity'].sum() if 'quantity' in df.columns else df.groupby('season').size()
            
            return {
                'seasonal_distribution': seasonal_sales.to_dict(),
                'peak_season': seasonal_sales.idxmax(),
                'low_season': seasonal_sales.idxmin()
            }
        
        return {'error': 'No date column found for seasonal analysis'}
    
    def _generate_inventory_recommendations(self, turnover_analysis: Dict, slow_moving: List) -> List[str]:
        """Generate inventory optimization recommendations."""
        recommendations = []
        
        overall_metrics = turnover_analysis['overall_metrics']
        
        if overall_metrics['low_turnover_products'] > overall_metrics['total_products'] * 0.3:
            recommendations.append("High percentage of low-turnover products - consider inventory reduction")
        
        if overall_metrics['avg_turnover_rate'] < 1.0:
            recommendations.append("Low average turnover rate - review purchasing strategy")
        
        if len(slow_moving) > 0:
            recommendations.append(f"{len(slow_moving)} slow-moving products identified - implement clearance strategy")
        
        recommendations.append("Consider implementing just-in-time inventory for high-turnover products")
        recommendations.append("Monitor seasonal patterns to optimize inventory levels")
        
        return recommendations
    
    @handle_errors
    def analyze_customer_journey(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze customer journey patterns for retail.
        
        Args:
            df: DataFrame with customer behavior data
            
        Returns:
            Dictionary with customer journey analysis
        """
        with PerformanceTimer("Customer Journey Analysis"):
            journey_analysis = {}
            
            # Customer lifecycle stages
            lifecycle_stages = self._identify_lifecycle_stages(df)
            journey_analysis['lifecycle_stages'] = lifecycle_stages
            
            # Purchase funnel analysis
            funnel_analysis = self._analyze_purchase_funnel(df)
            journey_analysis['funnel_analysis'] = funnel_analysis
            
            # Customer touchpoints
            touchpoints = self._analyze_touchpoints(df)
            journey_analysis['touchpoints'] = touchpoints
            
            # Journey optimization recommendations
            recommendations = self._generate_journey_recommendations(lifecycle_stages, funnel_analysis)
            journey_analysis['recommendations'] = recommendations
            
            return journey_analysis
    
    def _identify_lifecycle_stages(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Identify customer lifecycle stages."""
        if 'total_purchases' in df.columns and 'signup_date' in df.columns:
            # Calculate days since signup
            df['signup_date'] = pd.to_datetime(df['signup_date'])
            df['days_since_signup'] = (datetime.now() - df['signup_date']).dt.days
            
            # Define lifecycle stages
            def categorize_stage(row):
                if row['total_purchases'] == 0:
                    return 'Prospect'
                elif row['total_purchases'] == 1:
                    return 'New Customer'
                elif row['total_purchases'] <= 5:
                    return 'Developing'
                elif row['total_purchases'] <= 20:
                    return 'Established'
                else:
                    return 'VIP'
            
            df['lifecycle_stage'] = df.apply(categorize_stage, axis=1)
            
            stage_distribution = df['lifecycle_stage'].value_counts().to_dict()
            
            return {
                'stage_distribution': stage_distribution,
                'stage_characteristics': {
                    'Prospect': {'avg_days': 0, 'conversion_potential': 'High'},
                    'New Customer': {'avg_days': df[df['lifecycle_stage'] == 'New Customer']['days_since_signup'].mean(), 'conversion_potential': 'Very High'},
                    'Developing': {'avg_days': df[df['lifecycle_stage'] == 'Developing']['days_since_signup'].mean(), 'conversion_potential': 'High'},
                    'Established': {'avg_days': df[df['lifecycle_stage'] == 'Established']['days_since_signup'].mean(), 'conversion_potential': 'Medium'},
                    'VIP': {'avg_days': df[df['lifecycle_stage'] == 'VIP']['days_since_signup'].mean(), 'conversion_potential': 'Maintain'}
                }
            }
        
        return {'error': 'Required columns not found for lifecycle analysis'}
    
    def _analyze_purchase_funnel(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze purchase funnel metrics."""
        total_customers = len(df)
        
        # Calculate funnel metrics
        funnel_metrics = {
            'total_visitors': total_customers,
            'registered_users': len(df[df['user_id'].notna()]) if 'user_id' in df.columns else total_customers,
            'first_time_buyers': len(df[df['total_purchases'] == 1]) if 'total_purchases' in df.columns else 0,
            'repeat_buyers': len(df[df['total_purchases'] > 1]) if 'total_purchases' in df.columns else 0,
            'vip_customers': len(df[df['total_purchases'] > 20]) if 'total_purchases' in df.columns else 0
        }
        
        # Calculate conversion rates
        conversion_rates = {
            'registration_rate': funnel_metrics['registered_users'] / funnel_metrics['total_visitors'],
            'first_purchase_rate': funnel_metrics['first_time_buyers'] / funnel_metrics['registered_users'],
            'repeat_purchase_rate': funnel_metrics['repeat_buyers'] / funnel_metrics['first_time_buyers'] if funnel_metrics['first_time_buyers'] > 0 else 0,
            'vip_conversion_rate': funnel_metrics['vip_customers'] / funnel_metrics['repeat_buyers'] if funnel_metrics['repeat_buyers'] > 0 else 0
        }
        
        return {
            'funnel_metrics': funnel_metrics,
            'conversion_rates': conversion_rates
        }
    
    def _analyze_touchpoints(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze customer touchpoints."""
        touchpoint_analysis = {}
        
        if 'device_type' in df.columns:
            device_distribution = df['device_type'].value_counts().to_dict()
            touchpoint_analysis['device_preferences'] = device_distribution
        
        if 'browsing_time_minutes' in df.columns:
            touchpoint_analysis['engagement_metrics'] = {
                'avg_browsing_time': df['browsing_time_minutes'].mean(),
                'high_engagement_threshold': df['browsing_time_minutes'].quantile(0.8),
                'low_engagement_threshold': df['browsing_time_minutes'].quantile(0.2)
            }
        
        return touchpoint_analysis
    
    def _generate_journey_recommendations(self, lifecycle_stages: Dict, funnel_analysis: Dict) -> List[str]:
        """Generate customer journey optimization recommendations."""
        recommendations = []
        
        # Based on lifecycle stages
        if 'Prospect' in lifecycle_stages.get('stage_distribution', {}):
            prospect_count = lifecycle_stages['stage_distribution']['Prospect']
            recommendations.append(f"Focus on converting {prospect_count} prospects to customers")
        
        # Based on funnel analysis
        conversion_rates = funnel_analysis.get('conversion_rates', {})
        
        if conversion_rates.get('first_purchase_rate', 0) < 0.3:
            recommendations.append("Low first purchase rate - improve onboarding and product discovery")
        
        if conversion_rates.get('repeat_purchase_rate', 0) < 0.4:
            recommendations.append("Low repeat purchase rate - implement retention strategies")
        
        recommendations.append("Implement personalized email campaigns based on lifecycle stage")
        recommendations.append("Create targeted promotions for each customer segment")
        
        return recommendations
    
    @handle_errors
    def analyze_product_performance(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze product performance for retail.
        
        Args:
            df: DataFrame with product and sales data
            
        Returns:
            Dictionary with product performance analysis
        """
        with PerformanceTimer("Product Performance Analysis"):
            if 'preferred_category' in df.columns:
                # Category performance
                category_analysis = self._analyze_category_performance(df)
                
                # Product recommendations
                product_recommendations = self._generate_product_recommendations(df)
                
                # Market basket analysis
                basket_analysis = self._analyze_market_basket(df)
                
                return {
                    'category_performance': category_analysis,
                    'product_recommendations': product_recommendations,
                    'basket_analysis': basket_analysis,
                    'analysis_timestamp': datetime.now().isoformat()
                }
            else:
                raise ProjectError("Required column 'preferred_category' not found")
    
    def _analyze_category_performance(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze category performance."""
        category_metrics = df.groupby('preferred_category').agg({
            'total_purchases': 'mean' if 'total_purchases' in df.columns else 'count',
            'customer_lifetime_value': 'mean' if 'customer_lifetime_value' in df.columns else lambda x: 0,
            'user_id': 'count'
        }).round(2)
        
        category_metrics.columns = ['avg_purchases', 'avg_clv', 'customer_count']
        
        # Calculate category scores
        category_metrics['performance_score'] = (
            category_metrics['avg_purchases'] * 0.4 +
            category_metrics['avg_clv'] * 0.4 +
            category_metrics['customer_count'] * 0.2
        )
        
        return {
            'category_metrics': category_metrics.to_dict('index'),
            'top_performing_category': category_metrics['performance_score'].idxmax(),
            'bottom_performing_category': category_metrics['performance_score'].idxmin()
        }
    
    def _generate_product_recommendations(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Generate product recommendations."""
        if 'preferred_category' in df.columns and 'total_purchases' in df.columns:
            # Find high-value customers by category
            category_customers = df.groupby('preferred_category').agg({
                'total_purchases': 'mean',
                'customer_lifetime_value': 'mean'
            })
            
            recommendations = []
            for category, metrics in category_customers.iterrows():
                if metrics['total_purchases'] > df['total_purchases'].quantile(0.7):
                    recommendations.append({
                        'category': category,
                        'recommendation': 'Expand product range',
                        'reason': f'High-performing category with {metrics["total_purchases"]:.1f} avg purchases'
                    })
                elif metrics['total_purchases'] < df['total_purchases'].quantile(0.3):
                    recommendations.append({
                        'category': category,
                        'recommendation': 'Review and optimize',
                        'reason': f'Low-performing category with {metrics["total_purchases"]:.1f} avg purchases'
                    })
            
            return recommendations
        
        return []
    
    def _analyze_market_basket(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze market basket patterns."""
        # Simple market basket analysis based on customer segments
        if 'preferred_category' in df.columns and 'customer_segment' in df.columns:
            basket_patterns = df.groupby(['customer_segment', 'preferred_category']).size().unstack(fill_value=0)
            
            return {
                'segment_category_preferences': basket_patterns.to_dict('index'),
                'cross_category_opportunities': self._identify_cross_category_opportunities(basket_patterns)
            }
        
        return {'error': 'Required columns not found for market basket analysis'}
    
    def _identify_cross_category_opportunities(self, basket_patterns: pd.DataFrame) -> List[Dict[str, Any]]:
        """Identify cross-category selling opportunities."""
        opportunities = []
        
        # Find categories that are popular together
        for segment in basket_patterns.index:
            segment_data = basket_patterns.loc[segment]
            top_categories = segment_data.nlargest(2).index.tolist()
            
            if len(top_categories) >= 2:
                opportunities.append({
                    'segment': segment,
                    'primary_category': top_categories[0],
                    'secondary_category': top_categories[1],
                    'opportunity': 'Bundle these categories for this segment'
                })
        
        return opportunities
    
    def generate_retail_report(self, df: pd.DataFrame) -> str:
        """Generate comprehensive retail analytics report."""
        report = "# Retail Analytics Report\n\n"
        
        # Inventory analysis
        try:
            inventory_analysis = self.analyze_inventory_turnover(df)
            report += "## Inventory Turnover Analysis\n"
            report += f"- Average turnover rate: {inventory_analysis['turnover_metrics']['overall_metrics']['avg_turnover_rate']:.2f}\n"
            report += f"- High turnover products: {inventory_analysis['turnover_metrics']['overall_metrics']['high_turnover_products']}\n"
            report += f"- Slow moving products: {len(inventory_analysis['slow_moving_products'])}\n\n"
        except Exception as e:
            report += f"## Inventory Analysis\n- Error: {str(e)}\n\n"
        
        # Customer journey analysis
        try:
            journey_analysis = self.analyze_customer_journey(df)
            report += "## Customer Journey Analysis\n"
            report += f"- Lifecycle stages identified: {len(journey_analysis.get('lifecycle_stages', {}).get('stage_distribution', {}))}\n"
            report += f"- Funnel conversion rates calculated\n"
            report += f"- Touchpoint analysis completed\n\n"
        except Exception as e:
            report += f"## Customer Journey Analysis\n- Error: {str(e)}\n\n"
        
        # Product performance analysis
        try:
            product_analysis = self.analyze_product_performance(df)
            report += "## Product Performance Analysis\n"
            report += f"- Categories analyzed: {len(product_analysis.get('category_performance', {}).get('category_metrics', {}))}\n"
            report += f"- Product recommendations generated\n"
            report += f"- Market basket analysis completed\n\n"
        except Exception as e:
            report += f"## Product Performance Analysis\n- Error: {str(e)}\n\n"
        
        report += f"**Report generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += "**Analysis powered by:** LangGraph AI Retail Analytics\n"
        
        return report
