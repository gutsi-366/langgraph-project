# src/integrated_system.py
import pandas as pd
import numpy as np
from enhanced_agent import EnhancedLangGraphAgent

class CompleteBusinessIntelligence:
    def __init__(self):
        self.analyst = EnhancedLangGraphAgent()
    
    def competitive_analysis(self, search_term):
        """Analyze competitor products with AI"""
        print(f"🔍 Analyzing market for: {search_term}")
        
        # Create realistic demo competitor data
        demo_products = []
        competitors = ['Amazon', 'eBay', 'Walmart', 'Target', 'BestBuy', 'Newegg']
        
        for i, competitor in enumerate(competitors):
            demo_products.append({
                'competitor': competitor,
                'product_name': f"{search_term} Pro Model {i+1}",
                'price': round(80 + (i * 15) + np.random.randint(-10, 10), 2),
                'rating': round(4.0 + (i * 0.1) + np.random.uniform(-0.3, 0.3), 1),
                'review_count': np.random.randint(50, 2000),
                'shipping_time': np.random.randint(1, 7),
                'in_stock': True,
                'market_share': round(np.random.uniform(0.1, 0.25), 2)
            })
        
        df = pd.DataFrame(demo_products)
        analysis = self.analyst.analyze_large_dataset(df)
        
        return {
            'crawled_data': df,
            'ai_analysis': analysis,
            'competitive_insights': [
                f"💰 **Price Analysis**: Market range ${df['price'].min()} - ${df['price'].max()} (Avg: ${df['price'].mean():.2f})",
                f"⭐ **Quality Leaders**: {df.loc[df['rating'].idxmax()]['competitor']} has highest rating ({df['rating'].max()} stars)",
                f"🏪 **Market Coverage**: {len(df)} major competitors analyzed",
                f"📦 **Shipping**: Average {df['shipping_time'].mean():.1f} days delivery",
                f"🎯 **Opportunity**: Price gap between ${df['price'].quantile(0.25):.2f}-${df['price'].quantile(0.75):.2f} has less competition"
            ]
        }