# src/enhanced_agent.py
import os
import io
import base64
import pandas as pd
from datetime import datetime
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Import new modules
from utils import handle_errors, validate_dataframe, PerformanceTimer, ProjectError
from cache_manager import cached_dataframe, DataFrameCache
from advanced_analytics import AdvancedAnalytics

# Load env (OPENAI_API_KEY, OPENAI_MODEL, etc.)
load_dotenv()

# ---- Optional LLM (graceful fallback if missing) ----
try:
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage
except Exception:
    ChatOpenAI = None
    HumanMessage = None


def create_openai_llm() -> Optional["ChatOpenAI"]:
    """
    Create an OpenAI LLM client using environment variables.
    Returns None if OPENAI_API_KEY or langchain_openai is unavailable.
    """
    if ChatOpenAI is None:
        return None
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return None

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    base_url = os.getenv("OPENAI_BASE_URL", "").strip() or None  # optional proxy
    return ChatOpenAI(
        api_key=api_key,
        model=model,
        temperature=0.3,
        base_url=base_url,
    )


class EnhancedLangGraphAgent:
    """Enhanced analytical agent with adaptive dataset handling + optional LLM."""

    def __init__(self):
        self.llm = create_openai_llm()
        self.advanced_analytics = AdvancedAnalytics()
        self.dataframe_cache = DataFrameCache()

    # ---------- Helpers ----------
    def _find_col(self, df, candidates: list[str]):
        """Return the first matching column by exact (case-insensitive) or substring match."""
        # exact match
        for name in candidates:
            for col in df.columns:
                if col.lower() == name.lower():
                    return col
        # substring match
        for name in candidates:
            for col in df.columns:
                if name.lower() in col.lower():
                    return col
        return None

    def plot_to_base64(self):
        import matplotlib.pyplot as plt
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)
        b64 = base64.b64encode(buf.read()).decode("utf-8")
        return f"data:image/png;base64,{b64}"

    def _make_text_summary(self, df: pd.DataFrame) -> str:
        """Compact textual summary for LLM prompt."""
        head_str = df.head(10).to_string(index=False)
        try:
            desc_str = df.describe(include="all").transpose().to_string()
        except Exception:
            desc_str = "(describe failed)"
        return (
            f"Columns: {list(df.columns)}\n"
            f"Rows: {len(df)}\n\n"
            f"HEAD(10):\n{head_str}\n\n"
            f"DESCRIBE:\n{desc_str}"
        )

    # ---------- Main Analysis ----------
    def analyze_large_dataset(self, df: pd.DataFrame):
        """Perform analysis using flexible column detection (never KeyError)."""
        try:
            results = {
                "key_metrics": self.calculate_key_metrics(df),
                "customer_segments": self.analyze_customer_segments(df),
                "business_insights": self.generate_business_insights(df),
                "visualizations": self.create_visualizations(df),
                "performance_metrics": {
                    "records_processed": len(df),
                    "columns_detected": list(df.columns),
                    "timestamp": datetime.now().isoformat(timespec="seconds"),
                },
            }

            # ---- Optional: LLM-written insights/report snippet ----
            df_summary = self._make_text_summary(df)
            llm_md = self.generate_llm_report(df_summary)
            if llm_md and not llm_md.startswith("❌"):
                results["llm_report"] = llm_md
            else:
                # Add helpful message if LLM fails
                results["llm_info"] = "💡 LLM features disabled. All analytics features work without AI insights!"

            return results
        except Exception as e:
            return {"error": f"Analysis failed: {e}"}

    # ---------- Key Metrics ----------
    def calculate_key_metrics(self, df: pd.DataFrame):
        """Calculate business key metrics with flexible column detection."""

        def find_col(possible_names):
            for name in possible_names:
                for col in df.columns:
                    if col.lower() == name.lower():
                        return col
            return None

        clv_col = find_col(["customer_lifetime_value", "lifetime_value", "clv", "value"])
        aov_col = find_col(["avg_order_value", "average_order_value", "order_value", "aov"])
        browse_col = find_col(["browsing_time_minutes", "browse_time", "session_time", "time_spent"])
        login_col = find_col(["last_login_days", "days_since_login", "login_days"])
        segment_col = find_col(["customer_segment", "segment", "group"])

        total_revenue = df[clv_col].sum() if clv_col else 0
        avg_order_value = df[aov_col].mean() if aov_col else 0
        avg_browse_time = df[browse_col].mean() if browse_col else 0

        if login_col:
            active_users_ratio = (len(df[df[login_col] <= 7]) / len(df)) * 100
        else:
            active_users_ratio = 0

        if segment_col:
            vip_ratio = (len(df[df[segment_col].astype(str).str.lower() == "vip"]) / len(df)) * 100
        else:
            vip_ratio = 0

        return {
            "total_revenue_potential": f"${total_revenue:,.2f}",
            "average_order_value": f"${avg_order_value:,.2f}",
            "average_browsing_time": f"{avg_browse_time:.1f} minutes",
            "active_users_ratio": f"{active_users_ratio:.1f}%",
            "vip_customer_ratio": f"{vip_ratio:.1f}%",
        }

    # ---------- Customer Segments ----------
    def analyze_customer_segments(self, df: pd.DataFrame):
        """Segment analysis robust to missing/variant column names."""
        segment_col = self._find_col(df, ["customer_segment", "segment", "user_segment", "group"])
        clv_col = self._find_col(df, ["customer_lifetime_value", "lifetime_value", "clv", "value"])
        purchases_col = self._find_col(df, ["total_purchases", "purchases", "orders_count", "order_count"])
        browse_col = self._find_col(df, ["browsing_time_minutes", "browse_time", "session_time", "time_spent"])

        if not segment_col:
            return {}

        vc = df[segment_col].astype(str).value_counts(dropna=False)
        segment_analysis = {}

        for segment in vc.index:
            seg_mask = df[segment_col].astype(str) == str(segment)
            seg_df = df[seg_mask]

            segment_analysis[str(segment)] = {
                "count": int(seg_mask.sum()),
                "percentage": f"{(seg_mask.mean()) * 100:.1f}%",
            }
            if clv_col and not seg_df[clv_col].empty:
                segment_analysis[str(segment)]["avg_lifetime_value"] = f"${seg_df[clv_col].mean():.2f}"
            if purchases_col and not seg_df[purchases_col].empty:
                segment_analysis[str(segment)]["avg_purchases"] = float(seg_df[purchases_col].mean())
            if browse_col and not seg_df[browse_col].empty:
                segment_analysis[str(segment)]["avg_browsing_time"] = f"{seg_df[browse_col].mean():.1f} min"

        return segment_analysis

    # ---------- Insights ----------
    def generate_business_insights(self, df: pd.DataFrame):
        """Lightweight static insights; LLM adds richer text separately."""
        insights = []
        if "age" in df.columns:
            avg_age = df["age"].mean()
            insights.append(f"Average customer age: {avg_age:.1f}")
        clv_col = self._find_col(df, ["customer_lifetime_value", "clv", "value"])
        if clv_col:
            top_clv = df[clv_col].nlargest(min(3, len(df))).values
            insights.append(f"Top {min(3, len(df))} lifetime values: {top_clv}")
        insights.append("VIP users contribute disproportionately to revenue potential.")
        return insights

    # ---------- Visualizations ----------
    def create_visualizations(self, df: pd.DataFrame):
        """Create visualizations using matplotlib; skip gracefully if columns are missing."""
        charts = {}
        try:
            import matplotlib.pyplot as plt

            segment_col = self._find_col(df, ["customer_segment", "segment", "user_segment", "group"])
            purchases_col = self._find_col(df, ["total_purchases", "purchases", "orders_count", "order_count"])
            browse_col = self._find_col(df, ["browsing_time_minutes", "browse_time", "session_time", "time_spent"])
            clv_col = self._find_col(df, ["customer_lifetime_value", "lifetime_value", "clv", "value"])

            # 1) Segment distribution
            if segment_col:
                plt.figure(figsize=(10, 6))
                vc = df[segment_col].astype(str).value_counts()
                plt.pie(vc.values, labels=vc.index, autopct="%1.1f%%")
                plt.title("Customer Segmentation Distribution")
                charts["segmentation_pie"] = self.plot_to_base64()

            # 2) Purchases histogram
            if purchases_col and pd.api.types.is_numeric_dtype(df[purchases_col]):
                plt.figure(figsize=(10, 6))
                plt.hist(df[purchases_col].dropna(), bins=20, alpha=0.7)
                plt.xlabel(purchases_col)
                plt.ylabel("Number of Users")
                plt.title(f"Distribution of {purchases_col}")
                charts["purchase_histogram"] = self.plot_to_base64()

            # 3) Scatter: engagement vs value
            if browse_col and clv_col and \
               pd.api.types.is_numeric_dtype(df[browse_col]) and pd.api.types.is_numeric_dtype(df[clv_col]):
                plt.figure(figsize=(10, 6))
                if segment_col:
                    for seg in df[segment_col].astype(str).unique():
                        part = df[df[segment_col].astype(str) == seg]
                        plt.scatter(part[browse_col], part[clv_col], alpha=0.6, label=str(seg))
                    plt.legend(title=segment_col)
                else:
                    plt.scatter(df[browse_col], df[clv_col], alpha=0.6)
                plt.xlabel(browse_col)
                plt.ylabel(clv_col)
                plt.title("Customer Value vs Engagement Time")
                charts["value_engagement"] = self.plot_to_base64()

        except Exception as e:
            charts = {"error": f"Visualization failed: {e}"}

        return charts

    # ---------- LLM: Markdown Insights ----------
    def generate_llm_report(self, df_summary: str) -> Optional[str]:
        """Use OpenAI model to write a concise markdown insights block (fallback to None)."""
        if self.llm is None or HumanMessage is None:
            return None
        prompt = f"""
You are a professional data analyst. Based on the dataset snapshot below, write a concise markdown section with:
- Key patterns or trends
- Likely customer segments or cohorts
- 3–5 practical business actions to improve engagement or revenue

DATASET SNAPSHOT:
{df_summary}
"""
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content.strip()
        except Exception as e:
            return f"❌ LLM generation error: {e}\n\n💡 **Tip:** To enable AI-generated insights, add your OpenAI API key to the environment variables."

    # ---------- Static Professional Report ----------
    def generate_professional_report(self, results, df):
        """Generate Markdown report summary using local (non-LLM) results dictionary."""
        report = "# 🧠 E-commerce Analytics Report\n\n"

        km = results.get("key_metrics", {})
        if km:
            report += "## Key Metrics\n"
            for k, v in km.items():
                report += f"- **{k.replace('_', ' ').title()}**: {v}\n"

        segs = results.get("customer_segments", {})
        if segs:
            report += "\n## Customer Segments\n"
            for seg, data in segs.items():
                report += f"### {seg}\n"
                for k, v in data.items():
                    report += f"- {k.replace('_', ' ').title()}: {v}\n"

        ins = results.get("business_insights", [])
        if ins:
            report += "\n## Insights\n"
            for i in ins:
                report += f"- {i}\n"

        report += "\nGenerated automatically via **LangGraph-powered Agent**."
        return report
    
    # ---------- Advanced Analytics Methods ----------
    @cached_dataframe(ttl=3600)  # Cache for 1 hour
    def perform_advanced_segmentation(self, df: pd.DataFrame, n_clusters: int = 5) -> Dict[str, Any]:
        """Perform advanced customer segmentation using ML."""
        with PerformanceTimer("Advanced Customer Segmentation"):
            return self.advanced_analytics.perform_customer_segmentation(df, n_clusters)
    
    @cached_dataframe(ttl=1800)  # Cache for 30 minutes
    def detect_anomalies(self, df: pd.DataFrame, contamination: float = 0.1) -> Dict[str, Any]:
        """Detect anomalous customers using Isolation Forest."""
        with PerformanceTimer("Anomaly Detection"):
            return self.advanced_analytics.detect_anomalies(df, contamination)
    
    @cached_dataframe(ttl=3600)  # Cache for 1 hour
    def predict_customer_lifetime_value(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Predict customer lifetime value using Random Forest."""
        with PerformanceTimer("CLV Prediction"):
            return self.advanced_analytics.predict_customer_lifetime_value(df)
    
    def generate_comprehensive_report(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate a comprehensive analytics report combining all analyses."""
        with PerformanceTimer("Comprehensive Analysis Report"):
            return self.advanced_analytics.generate_comprehensive_report(df)
