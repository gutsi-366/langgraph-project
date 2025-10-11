import pandas as pd
import numpy as np
from faker import Faker
import random
import os

def generate_10k_users():
    print("🚀 Generating 10,000 user dataset...")
    
    fake = Faker()
    users = []
    
    for user_id in range(1, 10001):
        # Create realistic user segments
        if user_id <= 2000:  # VIP customers (20%)
            total_purchases = random.randint(50, 200)
            browsing_time = random.randint(180, 480)
            lifetime_value = random.uniform(1000, 5000)
            segment = "VIP"
        elif user_id <= 7000:  # Regular customers (50%)
            total_purchases = random.randint(10, 49)
            browsing_time = random.randint(60, 179)
            lifetime_value = random.uniform(200, 999)
            segment = "Regular"
        else:  # New customers (30%)
            total_purchases = random.randint(1, 9)
            browsing_time = random.randint(5, 59)
            lifetime_value = random.uniform(50, 199)
            segment = "New"
        
        user_data = {
            'user_id': user_id,
            'age': random.randint(18, 70),
            'country': fake.country(),
            'total_purchases': total_purchases,
            'last_login_days': random.randint(0, 90),
            'browsing_time_minutes': browsing_time,
            'avg_order_value': round(random.uniform(25, 250), 2),
            'customer_lifetime_value': round(lifetime_value, 2),
            'preferred_category': random.choice(['Electronics', 'Fashion', 'Home', 'Books', 'Sports']),
            'device_type': random.choice(['Mobile', 'Desktop', 'Tablet']),
            'customer_segment': segment,
            'signup_date': fake.date_between(start_date='-2y', end_date='today')
        }
        users.append(user_data)
    
    df = pd.DataFrame(users)
    
    # Save to your existing data folder
    df.to_csv('data/large_dataset.csv', index=False)
    
    print("✅ SUCCESS: Generated 10,000 user dataset!")
    print(f"📊 Dataset saved to: data/large_dataset.csv")
    print(f"📈 User segments:")
    print(f"   - VIP Customers: {len(df[df['customer_segment'] == 'VIP'])}")
    print(f"   - Regular Customers: {len(df[df['customer_segment'] == 'Regular'])}")
    print(f"   - New Customers: {len(df[df['customer_segment'] == 'New'])}")
    print(f"💰 Total lifetime value: ${df['customer_lifetime_value'].sum():,.2f}")

if __name__ == "__main__":
    generate_10k_users()