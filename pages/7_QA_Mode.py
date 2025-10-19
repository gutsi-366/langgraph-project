import os, sys
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Import data manager and UI components
from data_manager import data_manager
try:
    from ui_components import load_css, hero, metric_card, info_card, section, success_message, error_message
    _HAS_UI = True
except Exception:
    _HAS_UI = False

def process_question(question, df, features_df):
    """Process the question and return an answer"""
    question_lower = question.lower()
    
    # Record count questions
    if any(word in question_lower for word in ["how many", "total records", "number of", "how many customers", "total customers", "number of customers"]):
        if 'user_id' in df.columns or 'customer_id' in df.columns:
            return f"**Answer:** You have **{len(df)} customers** in your dataset."
        else:
            return f"**Answer:** You have **{len(df)} records** in your dataset."
    
    # Age questions
    elif any(word in question_lower for word in ["average age", "mean age", "customer age"]):
        if 'age' in df.columns:
            avg_age = df['age'].mean()
            return f"**Answer:** The average customer age is **{avg_age:.1f} years**."
        else:
            return "**Answer:** Age data is not available in the current dataset."
    
    # Category questions
    elif any(word in question_lower for word in ["category", "categories", "most popular"]):
        if 'preferred_category' in df.columns:
            top_category = df['preferred_category'].value_counts().index[0]
            count = df['preferred_category'].value_counts().iloc[0]
            return f"**Answer:** The most popular category is **{top_category}** with **{count} customers**."
        else:
            return "**Answer:** Category data is not available in the current dataset."
    
    # Revenue questions
    elif any(word in question_lower for word in ["revenue", "total revenue", "sales"]):
        if 'customer_lifetime_value' in df.columns:
            total_revenue = df['customer_lifetime_value'].sum()
            return f"**Answer:** The total customer lifetime value is **${total_revenue:,.2f}**."
        else:
            return "**Answer:** Revenue data is not available in the current dataset."
    
    # Purchase questions
    elif any(word in question_lower for word in ["purchase", "purchases", "orders"]):
        if 'total_purchases' in df.columns:
            total_purchases = df['total_purchases'].sum()
            avg_purchases = df['total_purchases'].mean()
            return f"**Answer:** Total purchases: **{total_purchases:,}** | Average per customer: **{avg_purchases:.1f}**"
        else:
            return "**Answer:** Purchase data is not available in the current dataset."
    
    # Age group questions
    elif any(word in question_lower for word in ["age group", "age groups", "age distribution"]):
        if 'age' in df.columns:
            age_groups = pd.cut(df['age'], bins=[0, 25, 35, 45, 55, 100], labels=['18-25', '26-35', '36-45', '46-55', '55+'])
            age_dist = age_groups.value_counts()
            result = "**Answer:** Age group distribution:\n"
            for group, count in age_dist.items():
                result += f"- {group}: {count} customers\n"
            return result
        else:
            return "**Answer:** Age data is not available in the current dataset."
    
    # General data info
    elif any(word in question_lower for word in ["data", "dataset", "information", "overview"]):
        # Get column types
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        text_cols = df.select_dtypes(include=['object']).columns.tolist()
        date_cols = df.select_dtypes(include=['datetime']).columns.tolist()
        
        overview = f"""**Answer:** Here's an overview of your data:
        
- **Total Records:** {len(df):,}
- **Data Columns:** {len(df.columns)}
- **Column Types:** {len(numeric_cols)} numeric, {len(text_cols)} text, {len(date_cols)} date
- **Data Quality:** {df.isnull().sum().sum()} missing values
- **Memory Usage:** {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB

**Available Columns:** {', '.join(df.columns[:8])}{'...' if len(df.columns) > 8 else ''}"""
        
        if numeric_cols:
            overview += f"\n\n**Numeric Columns:** {', '.join(numeric_cols[:5])}{'...' if len(numeric_cols) > 5 else ''}"
        
        return overview
    
    # Data statistics questions
    elif any(word in question_lower for word in ["statistics", "stats", "describe", "summary"]):
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            stats = df[numeric_cols].describe()
            result = "**Answer:** Here are the statistical summary for numeric columns:\n\n"
            result += stats.to_string()
            return result
        else:
            return "**Answer:** No numeric columns found for statistical analysis."
    
    # Missing data questions
    elif any(word in question_lower for word in ["missing", "null", "empty", "na"]):
        missing_data = df.isnull().sum()
        missing_cols = missing_data[missing_data > 0]
        if len(missing_cols) > 0:
            result = "**Answer:** Missing data information:\n\n"
            for col, count in missing_cols.items():
                percentage = (count / len(df)) * 100
                result += f"- **{col}**: {count} missing values ({percentage:.1f}%)\n"
            return result
        else:
            return "**Answer:** No missing data found in the dataset!"
    
    # Data types questions
    elif any(word in question_lower for word in ["data types", "dtypes", "column types"]):
        dtypes = df.dtypes.value_counts()
        result = "**Answer:** Data types in the dataset:\n\n"
        for dtype, count in dtypes.items():
            result += f"- **{dtype}**: {count} columns\n"
        return result
    
    # Top values questions
    elif any(word in question_lower for word in ["top values", "highest", "maximum", "max"]):
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            result = "**Answer:** Top values in numeric columns:\n\n"
            for col in numeric_cols[:5]:  # Show top 5 columns
                max_val = df[col].max()
                result += f"- **{col}**: {max_val}\n"
            return result
        else:
            return "**Answer:** No numeric columns found for top values analysis."
    
    # Default response
    else:
        return f"""**Answer:** I understand you're asking about "{question}". 

Here's what I can help you with:
- Customer statistics and demographics
- Purchase patterns and revenue
- Data quality and overview
- Age groups and categories
- Product preferences
- Data statistics and summaries
- Missing data analysis
- Data types information

Try asking something like:
- "How many customers do we have?"
- "What's the average age?"
- "Show me the data overview"
- "What are the data statistics?"
- "Show me missing data information"

Or use one of the sample questions above!"""

def show_visualization(question, df):
    """Show relevant visualizations based on the question"""
    st.subheader("📊 Visualization")
    
    question_lower = question.lower()
    
    # Age distribution chart
    if any(word in question_lower for word in ["age", "age group", "age distribution"]):
        if 'age' in df.columns:
            import plotly.express as px
            fig = px.histogram(df, x='age', title='Customer Age Distribution', nbins=20)
            st.plotly_chart(fig, use_container_width=True)
    
    # Category distribution
    elif any(word in question_lower for word in ["category", "categories", "popular"]):
        if 'preferred_category' in df.columns:
            import plotly.express as px
            category_counts = df['preferred_category'].value_counts()
            fig = px.pie(values=category_counts.values, names=category_counts.index, title='Category Distribution')
            st.plotly_chart(fig, use_container_width=True)
    
    # Purchase distribution
    elif any(word in question_lower for word in ["purchase", "purchases", "orders"]):
        if 'total_purchases' in df.columns:
            import plotly.express as px
            fig = px.histogram(df, x='total_purchases', title='Purchase Distribution', nbins=20)
            st.plotly_chart(fig, use_container_width=True)

# Load sample data
@st.cache_data
def load_sample_data():
    """Load sample datasets"""
    try:
        large_df = pd.read_csv("data/large_dataset.csv")
        features_df = pd.read_csv("data/user_personalized_features.csv")
        return large_df, features_df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

def main():
    """Main Q&A Mode function."""
    # Create hero section with inline styles (no CSS variables)
    st.markdown("""
    <div style="
        text-align: center; 
        padding: 3rem 2rem; 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        border-radius: 15px; 
        margin-bottom: 2rem; 
        color: white;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    ">
        <div style="font-size: 4rem; margin-bottom: 1rem;">❓</div>
        <h1 style="
            margin: 0; 
            font-size: 3rem; 
            font-weight: 800;
            text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        ">Question & Answer Mode</h1>
        <p style="
            margin: 1rem 0 0 0; 
            font-size: 1.3rem; 
            opacity: 0.9;
            font-weight: 400;
        ">Ask questions about your data and get instant answers! No API calls required - works completely offline.</p>
    </div>
    """, unsafe_allow_html=True)

    # Try to load the last used dataset if no current data
    if 'dataset' not in st.session_state or st.session_state.dataset is None:
        if 'current_dataset_id' in st.session_state:
            # Load the last used dataset
            df, error = data_manager.load_dataset(st.session_state.current_dataset_id)
            if df is not None:
                st.session_state.dataset = df
                st.session_state.dataset_name = data_manager.get_dataset_info(st.session_state.current_dataset_id)['name']
                st.info("🔄 Loaded your last used dataset!")
            else:
                st.info("💡 **To ask questions about your own data:** Upload a CSV file in the **📊 Data Analysis** page first, then come back here!")
        else:
            st.info("💡 **To ask questions about your own data:** Upload a CSV file in the **📊 Data Analysis** page first, then come back here!")

    # Data selection section
    st.subheader("📊 Select Dataset")

    # Check for available datasets
    available_datasets = []

    # Check session state for current data (if any)
    if 'dataset' in st.session_state and st.session_state.dataset is not None:
        dataset_name = st.session_state.get('dataset_name', 'Current Dataset')
        available_datasets.append({
            'name': f"🔄 {dataset_name} (Current)",
            'data': st.session_state.dataset,
            'type': 'current',
            'id': 'current'
        })

    # Load all saved datasets from persistent storage
    saved_datasets = data_manager.list_datasets()
    for dataset_id, info in saved_datasets.items():
        try:
            df, error = data_manager.load_dataset(dataset_id)
            if df is not None:
                source_icon = "📁" if info['source'] == 'uploaded' else "📊" if info['source'] == 'sample' else "💾"
                available_datasets.append({
                    'name': f"{source_icon} {info['name']} ({info['rows']} rows)",
                    'data': df,
                    'type': info['source'],
                    'id': dataset_id,
                    'info': info
                })
        except Exception as e:
            st.warning(f"Could not load dataset {info['name']}: {e}")

    # Check for sample data file (fallback)
    try:
        sample_df = pd.read_csv("data/large_dataset.csv")
        # Only add if not already in saved datasets
        if not any(ds['type'] == 'sample' for ds in available_datasets):
            available_datasets.append({
                'name': '📊 Sample Dataset (File)',
                'data': sample_df,
                'type': 'sample_file',
                'id': 'sample_file'
            })
    except:
        pass

    if not available_datasets:
        st.error("❌ No datasets available. Please upload data in the Analyze page first.")
        st.stop()

    # Dataset selection
    if len(available_datasets) == 1:
        selected_dataset = available_datasets[0]
        st.info(f"📁 Using: **{selected_dataset['name']}**")
    else:
        dataset_options = [ds['name'] for ds in available_datasets]
        selected_idx = st.selectbox(
            "Choose a dataset:",
            range(len(available_datasets)),
            format_func=lambda x: dataset_options[x]
        )
        selected_dataset = available_datasets[selected_idx]

    # Load selected dataset
    large_df = selected_dataset['data']
    features_df = None  # No separate features for uploaded data

    # Show dataset info
    st.success(f"✅ **{selected_dataset['name']}**: {len(large_df)} rows, {len(large_df.columns)} columns")

    # Show additional info for saved datasets
    if 'info' in selected_dataset:
        info = selected_dataset['info']
        st.caption(f"📅 Created: {info['created_at'][:19]} | 💾 Source: {info['source']}")

    # Quick stats section
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 Total Records", f"{len(large_df):,}")
    with col2:
        st.metric("📋 Columns", len(large_df.columns))
    with col3:
        numeric_cols = len(large_df.select_dtypes(include=[np.number]).columns)
        st.metric("🔢 Numeric Columns", numeric_cols)
    with col4:
        missing_count = large_df.isnull().sum().sum()
        st.metric("⚠️ Missing Values", f"{missing_count:,}")

    # Show dataset type info
    if selected_dataset['type'] == 'current':
        st.info("💡 This is your current session data")
    elif selected_dataset['type'] == 'uploaded':
        st.info("💡 This data was uploaded and saved permanently")
    elif selected_dataset['type'] == 'sample':
        st.info("💡 This is the sample dataset (saved)")
    else:
        st.info("💡 This is the sample dataset (from file)")

    # Add dataset management section
    with st.expander("🗂️ Dataset Management", expanded=False):
        st.subheader("Saved Datasets")
        
        if saved_datasets:
            for dataset_id, info in saved_datasets.items():
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**{info['name']}** ({info['rows']} rows, {info['columns']} cols)")
                    st.caption(f"Created: {info['created_at'][:19]}")
                with col2:
                    if st.button("Load", key=f"load_{dataset_id}"):
                        df, error = data_manager.load_dataset(dataset_id)
                        if df is not None:
                            st.session_state.dataset = df
                            st.session_state.dataset_name = info['name']
                            st.session_state.current_dataset_id = dataset_id
                            st.rerun()
                with col3:
                    if st.button("Delete", key=f"delete_{dataset_id}"):
                        success, error = data_manager.delete_dataset(dataset_id)
                        if success:
                            st.success("Dataset deleted!")
                            st.rerun()
                        else:
                            st.error(f"Error: {error}")
        else:
            st.info("No saved datasets yet. Upload data in the Analyze page to save it permanently.")

    # Generate dynamic sample questions based on available data
    def generate_sample_questions(df):
        """Generate sample questions based on the actual data columns"""
        questions = []
        
        # Always include basic questions
        questions.append("How many records do we have?")
        questions.append("Show me the data overview")
        
        # Add questions based on available columns
        if 'age' in df.columns:
            questions.append("What's the average age?")
            questions.append("How many people are in each age group?")
        
        if 'customer_lifetime_value' in df.columns or 'revenue' in df.columns or 'total_revenue' in df.columns:
            questions.append("What's the total revenue?")
        
        if 'total_purchases' in df.columns or 'purchases' in df.columns:
            questions.append("What's the average purchase value?")
        
        if 'preferred_category' in df.columns or 'category' in df.columns:
            questions.append("Which category is most popular?")
        
        if 'user_id' in df.columns or 'customer_id' in df.columns:
            questions.append("How many customers do we have?")
        
        # Add more generic questions
        questions.extend([
            "What are the top values in the data?",
            "Show me data distribution",
            "What patterns do you see?",
            "What are the data statistics?",
            "Show me missing data information",
            "What are the data types?"
        ])
        
        return questions[:8]  # Limit to 8 questions

    sample_questions = generate_sample_questions(large_df)

    # Display sample questions
    st.subheader("💡 Sample Questions")
    col1, col2 = st.columns(2)
    for i, question in enumerate(sample_questions):
        with col1 if i % 2 == 0 else col2:
            if st.button(f"❓ {question}", key=f"sample_{i}", width='stretch'):
                st.session_state.current_question = question

    # Question input
    st.subheader("🤔 Ask Your Question")
    question = st.text_input("Type your question here:", placeholder="e.g., How many customers do we have?")

    # Use sample question if selected
    if hasattr(st.session_state, 'current_question'):
        question = st.session_state.current_question
        st.session_state.current_question = None

    if question:
        st.write(f"**Your Question:** {question}")
        
        # Process the question and provide answer
        with st.spinner("Analyzing your question..."):
            answer = process_question(question, large_df, features_df)
            
            # Display answer
            st.subheader("📝 Answer")
            st.markdown(answer)
            
            # Show related data if applicable
            if "chart" in answer.lower() or "graph" in answer.lower():
                show_visualization(question, large_df)

    # Add some helpful tips
    st.sidebar.markdown("""
    ## 💡 Tips for Better Questions

    **Ask about:**
    - Customer demographics
    - Purchase patterns  
    - Data quality
    - Revenue metrics
    - Category preferences

    **Examples:**
    - "How many customers are in each age group?"
    - "What's the most popular category?"
    - "Show me the data overview"
    - "What's the average purchase value?"

    **Note:** This Q&A mode works with your local data and doesn't require API calls!
    """)

    # Show data preview
    with st.expander("📋 Data Preview", expanded=False):
        st.subheader(f"Dataset: {selected_dataset['name']}")
        st.dataframe(large_df.head(10))
        st.caption(f"Showing first 10 rows of {len(large_df)} total rows")
        
        # Show column info
        st.subheader("Column Information")
        col_info = []
        for col in large_df.columns:
            col_type = str(large_df[col].dtype)
            null_count = large_df[col].isnull().sum()
            col_info.append({
                'Column': col,
                'Type': col_type,
                'Null Values': null_count,
                'Sample Values': str(large_df[col].iloc[0])[:50] + "..." if len(str(large_df[col].iloc[0])) > 50 else str(large_df[col].iloc[0])
            })
        
        st.dataframe(pd.DataFrame(col_info), width='stretch')

if __name__ == "__main__":
    st.set_page_config(page_title="Q&A Mode", page_icon="❓", layout="wide")
    main()