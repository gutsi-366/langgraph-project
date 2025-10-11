def generate_report(df):
    report = "# E-commerce User Behavior Analysis Report\n\n"
    report += "## Dataset Overview\n"
    report += str(df.describe(include="all")) + "\n\n"

    report += "## Sample Insights\n"
    report += f"- Total users: {df['user_id'].nunique()}\n"
    report += f"- Average age: {df['age'].mean():.1f}\n"
    report += f"- Average total purchases: {df['total_purchases'].mean():.1f}\n"
    report += f"- Average browsing time: {df['browsing_time_minutes'].mean():.1f} minutes\n"

    return report
