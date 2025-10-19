"""
Advanced analytics module with sophisticated ML models and insights.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
try:
    import seaborn as sns  # Optional dependency
    SEABORN_AVAILABLE = True
except Exception:
    SEABORN_AVAILABLE = False
try:
    from sklearn.cluster import KMeans, DBSCAN
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    from sklearn.ensemble import RandomForestClassifier, IsolationForest
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report, silhouette_score
    from sklearn.decomposition import PCA
    from sklearn.manifold import TSNE
    SKLEARN_AVAILABLE = True
except Exception:
    # scikit-learn not available on this Python/OS; degrade gracefully
    KMeans = DBSCAN = StandardScaler = LabelEncoder = IsolationForest = RandomForestClassifier = None
    train_test_split = silhouette_score = PCA = TSNE = None
    SKLEARN_AVAILABLE = False
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Tuple, Any, Optional
import warnings
warnings.filterwarnings('ignore')

from utils import handle_errors, PerformanceTimer, ProjectError

class AdvancedAnalytics:
    """Advanced analytics engine with ML-powered insights."""
    
    def __init__(self):
        self.scaler = StandardScaler() if SKLEARN_AVAILABLE else None
        self.label_encoders = {}
        self.models = {}
        self.insights = {}
    
    @handle_errors
    def perform_customer_segmentation(self, df: pd.DataFrame, n_clusters: int = 5) -> Dict[str, Any]:
        """
        Perform advanced customer segmentation using multiple clustering algorithms.
        
        Args:
            df: Customer data DataFrame
            n_clusters: Number of clusters for K-means
            
        Returns:
            Dictionary with segmentation results and insights
        """
        with PerformanceTimer("Customer Segmentation"):
            if not SKLEARN_AVAILABLE:
                raise ProjectError("scikit-learn is not installed; install it to enable segmentation")
            # Prepare features for clustering
            numeric_features = df.select_dtypes(include=[np.number]).columns.tolist()
            
            # Remove ID columns and high-variance columns
            features_to_remove = ['user_id'] if 'user_id' in numeric_features else []
            numeric_features = [f for f in numeric_features if f not in features_to_remove]
            
            if len(numeric_features) < 2:
                raise ProjectError("Not enough numeric features for clustering")
            
            # Prepare data
            X = df[numeric_features].fillna(df[numeric_features].median())
            X_scaled = self.scaler.fit_transform(X)
            
            # K-Means clustering
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            df['kmeans_cluster'] = kmeans.fit_predict(X_scaled)
            
            # DBSCAN clustering for comparison
            dbscan = DBSCAN(eps=0.5, min_samples=5)
            df['dbscan_cluster'] = dbscan.fit_predict(X_scaled)
            
            # Calculate silhouette scores
            kmeans_score = silhouette_score(X_scaled, df['kmeans_cluster'])
            dbscan_score = silhouette_score(X_scaled, df['dbscan_cluster']) if len(set(df['dbscan_cluster'])) > 1 else 0
            
            # Analyze clusters
            cluster_analysis = self._analyze_clusters(df, 'kmeans_cluster', numeric_features)
            
            # Create visualizations
            plots = self._create_clustering_plots(df, numeric_features, X_scaled)
            
            return {
                "segmentation_method": "Advanced ML Clustering",
                "clusters": df['kmeans_cluster'].nunique(),
                "silhouette_score": kmeans_score,
                "cluster_analysis": cluster_analysis,
                "plots": plots,
                "recommendations": self._generate_segmentation_recommendations(cluster_analysis)
            }
    
    def _analyze_clusters(self, df: pd.DataFrame, cluster_col: str, features: List[str]) -> Dict[str, Any]:
        """Analyze cluster characteristics."""
        cluster_stats = {}
        
        for cluster_id in sorted(df[cluster_col].unique()):
            cluster_data = df[df[cluster_col] == cluster_id]
            
            stats = {
                "size": len(cluster_data),
                "percentage": len(cluster_data) / len(df) * 100,
                "characteristics": {}
            }
            
            # Calculate mean values for key features
            for feature in features:
                stats["characteristics"][feature] = {
                    "mean": cluster_data[feature].mean(),
                    "std": cluster_data[feature].std(),
                    "median": cluster_data[feature].median()
                }
            
            cluster_stats[f"Cluster_{cluster_id}"] = stats
        
        return cluster_stats
    
    def _create_clustering_plots(self, df: pd.DataFrame, features: List[str], X_scaled: np.ndarray) -> Dict[str, str]:
        """Create clustering visualization plots."""
        plots = {}
        
        # 2D PCA visualization
        if SKLEARN_AVAILABLE and len(features) > 2:
            pca = PCA(n_components=2)
            X_pca = pca.fit_transform(X_scaled)
            
            fig, ax = plt.subplots(figsize=(10, 8))
            scatter = ax.scatter(X_pca[:, 0], X_pca[:, 1], c=df['kmeans_cluster'], cmap='viridis', alpha=0.6)
            ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%} variance)')
            ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%} variance)')
            ax.set_title('Customer Segmentation (PCA)')
            plt.colorbar(scatter)
            plt.tight_layout()
            
            plots['pca_clustering'] = '../outputs/plots/advanced_pca_clustering.png'
            plt.savefig(plots['pca_clustering'], dpi=300, bbox_inches='tight')
            plt.close()
        
        # Cluster size distribution
        fig, ax = plt.subplots(figsize=(10, 6))
        cluster_counts = df['kmeans_cluster'].value_counts().sort_index()
        bars = ax.bar(range(len(cluster_counts)), cluster_counts.values, color='skyblue', alpha=0.7)
        ax.set_xlabel('Cluster')
        ax.set_ylabel('Number of Customers')
        ax.set_title('Customer Distribution by Cluster')
        ax.set_xticks(range(len(cluster_counts)))
        ax.set_xticklabels([f'Cluster {i}' for i in cluster_counts.index])
        
        # Add value labels on bars
        for bar, count in zip(bars, cluster_counts.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                   str(count), ha='center', va='bottom')
        
        plt.tight_layout()
        plots['cluster_distribution'] = '../outputs/plots/advanced_cluster_distribution.png'
        plt.savefig(plots['cluster_distribution'], dpi=300, bbox_inches='tight')
        plt.close()
        
        return plots
    
    def _generate_segmentation_recommendations(self, cluster_analysis: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations based on cluster analysis."""
        recommendations = []
        
        for cluster_name, stats in cluster_analysis.items():
            size_pct = stats['percentage']
            
            if size_pct > 30:
                recommendations.append(f"🎯 {cluster_name} is your largest segment ({size_pct:.1f}%) - focus marketing efforts here")
            elif size_pct < 5:
                recommendations.append(f"📊 {cluster_name} is a niche segment ({size_pct:.1f}%) - consider specialized campaigns")
            
            # Analyze characteristics for specific recommendations
            characteristics = stats['characteristics']
            
            # Example recommendations based on common e-commerce features
            if 'total_purchases' in characteristics:
                avg_purchases = characteristics['total_purchases']['mean']
                if avg_purchases > 100:
                    recommendations.append(f"💎 {cluster_name} has high-value customers (avg {avg_purchases:.0f} purchases) - VIP treatment recommended")
                elif avg_purchases < 10:
                    recommendations.append(f"🌱 {cluster_name} has low-engagement customers (avg {avg_purchases:.0f} purchases) - re-engagement campaign needed")
        
        return recommendations
    
    @handle_errors
    def detect_anomalies(self, df: pd.DataFrame, contamination: float = 0.1) -> Dict[str, Any]:
        """
        Detect anomalous customers using Isolation Forest.
        
        Args:
            df: Customer data DataFrame
            contamination: Expected proportion of anomalies
            
        Returns:
            Dictionary with anomaly detection results
        """
        with PerformanceTimer("Anomaly Detection"):
            if not SKLEARN_AVAILABLE:
                raise ProjectError("scikit-learn is not installed; install it to enable anomaly detection")
            # Prepare numeric features
            numeric_features = df.select_dtypes(include=[np.number]).columns.tolist()
            features_to_remove = ['user_id'] if 'user_id' in numeric_features else []
            numeric_features = [f for f in numeric_features if f not in features_to_remove]
            
            if len(numeric_features) < 2:
                raise ProjectError("Not enough numeric features for anomaly detection")
            
            # Prepare data
            X = df[numeric_features].fillna(df[numeric_features].median())
            X_scaled = self.scaler.fit_transform(X)
            
            # Fit Isolation Forest
            iso_forest = IsolationForest(contamination=contamination, random_state=42)
            df['anomaly_score'] = iso_forest.decision_function(X_scaled)
            df['is_anomaly'] = iso_forest.predict(X_scaled) == -1
            
            # Analyze anomalies
            anomalies = df[df['is_anomaly']]
            normal_customers = df[~df['is_anomaly']]
            
            anomaly_analysis = {
                "total_anomalies": len(anomalies),
                "anomaly_percentage": len(anomalies) / len(df) * 100,
                "anomaly_score_range": {
                    "min": df['anomaly_score'].min(),
                    "max": df['anomaly_score'].max(),
                    "mean": df['anomaly_score'].mean()
                },
                "anomaly_characteristics": self._analyze_anomaly_characteristics(anomalies, normal_customers, numeric_features)
            }
            
            # Create anomaly visualization
            plots = self._create_anomaly_plots(df, numeric_features)
            
            return {
                "method": "Isolation Forest",
                "analysis": anomaly_analysis,
                "plots": plots,
                "recommendations": self._generate_anomaly_recommendations(anomaly_analysis)
            }
    
    def _analyze_anomaly_characteristics(self, anomalies: pd.DataFrame, normal: pd.DataFrame, features: List[str]) -> Dict[str, Any]:
        """Analyze characteristics of anomalous customers."""
        characteristics = {}
        
        for feature in features:
            characteristics[feature] = {
                "anomaly_mean": anomalies[feature].mean(),
                "normal_mean": normal[feature].mean(),
                "difference_pct": ((anomalies[feature].mean() - normal[feature].mean()) / normal[feature].mean() * 100) if normal[feature].mean() != 0 else 0
            }
        
        return characteristics
    
    def _create_anomaly_plots(self, df: pd.DataFrame, features: List[str]) -> Dict[str, str]:
        """Create anomaly detection visualization plots."""
        plots = {}
        
        # Anomaly score distribution
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Histogram of anomaly scores
        ax1.hist(df[df['is_anomaly'] == False]['anomaly_score'], bins=50, alpha=0.7, label='Normal', color='blue')
        ax1.hist(df[df['is_anomaly'] == True]['anomaly_score'], bins=50, alpha=0.7, label='Anomaly', color='red')
        ax1.set_xlabel('Anomaly Score')
        ax1.set_ylabel('Frequency')
        ax1.set_title('Distribution of Anomaly Scores')
        ax1.legend()
        
        # Scatter plot of top 2 features colored by anomaly status
        if len(features) >= 2:
            ax2.scatter(df[df['is_anomaly'] == False][features[0]], 
                       df[df['is_anomaly'] == False][features[1]], 
                       alpha=0.6, label='Normal', color='blue')
            ax2.scatter(df[df['is_anomaly'] == True][features[0]], 
                       df[df['is_anomaly'] == True][features[1]], 
                       alpha=0.8, label='Anomaly', color='red', s=50)
            ax2.set_xlabel(features[0])
            ax2.set_ylabel(features[1])
            ax2.set_title('Anomalies in Feature Space')
            ax2.legend()
        
        plt.tight_layout()
        plots['anomaly_analysis'] = '../outputs/plots/advanced_anomaly_analysis.png'
        plt.savefig(plots['anomaly_analysis'], dpi=300, bbox_inches='tight')
        plt.close()
        
        return plots
    
    def _generate_anomaly_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on anomaly analysis."""
        recommendations = []
        
        anomaly_pct = analysis['anomaly_percentage']
        
        if anomaly_pct > 15:
            recommendations.append("🚨 High anomaly rate detected - investigate data quality issues")
        elif anomaly_pct < 1:
            recommendations.append("✅ Very low anomaly rate - data appears clean")
        
        recommendations.append(f"🔍 Review {analysis['total_anomalies']} anomalous customers for potential fraud or data errors")
        recommendations.append("📊 Consider manual review of extreme anomaly scores for business insights")
        
        return recommendations
    
    @handle_errors
    def predict_customer_lifetime_value(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Predict customer lifetime value using Random Forest.
        
        Args:
            df: Customer data DataFrame
            
        Returns:
            Dictionary with prediction results and insights
        """
        with PerformanceTimer("CLV Prediction"):
            if not SKLEARN_AVAILABLE:
                raise ProjectError("scikit-learn is not installed; install it to enable CLV prediction")
            # Prepare features and target
            feature_columns = ['age', 'total_purchases', 'browsing_time_minutes', 'avg_order_value']
            feature_columns = [col for col in feature_columns if col in df.columns]
            
            if 'customer_lifetime_value' not in df.columns or len(feature_columns) < 2:
                raise ProjectError("Insufficient data for CLV prediction")
            
            # Prepare data
            X = df[feature_columns].fillna(df[feature_columns].median())
            y = df['customer_lifetime_value']
            
            # Remove rows with missing target values
            valid_indices = ~y.isna()
            X = X[valid_indices]
            y = y[valid_indices]
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Train model
            rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
            rf_model.fit(X_train, y_train)
            
            # Make predictions
            y_pred = rf_model.predict(X_test)
            
            # Feature importance
            feature_importance = dict(zip(feature_columns, rf_model.feature_importances_))
            
            # Create predictions for entire dataset
            df['predicted_clv_category'] = rf_model.predict(X)
            df['predicted_clv_probability'] = rf_model.predict_proba(X).max(axis=1)
            
            # Create visualization
            plots = self._create_clv_plots(df, feature_importance)
            
            return {
                "model": "Random Forest Classifier",
                "feature_importance": feature_importance,
                "accuracy": rf_model.score(X_test, y_test),
                "plots": plots,
                "recommendations": self._generate_clv_recommendations(feature_importance)
            }
    
    def _create_clv_plots(self, df: pd.DataFrame, feature_importance: Dict[str, float]) -> Dict[str, str]:
        """Create CLV prediction visualization plots."""
        plots = {}
        
        # Feature importance plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Feature importance
        features = list(feature_importance.keys())
        importances = list(feature_importance.values())
        
        bars = ax1.barh(features, importances, color='lightcoral')
        ax1.set_xlabel('Feature Importance')
        ax1.set_title('Feature Importance for CLV Prediction')
        ax1.invert_yaxis()
        
        # Add value labels
        for bar, importance in zip(bars, importances):
            ax1.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2, 
                    f'{importance:.3f}', ha='left', va='center')
        
        # Predicted CLV distribution
        clv_counts = df['predicted_clv_category'].value_counts()
        ax2.pie(clv_counts.values, labels=clv_counts.index, autopct='%1.1f%%', startangle=90)
        ax2.set_title('Predicted CLV Category Distribution')
        
        plt.tight_layout()
        plots['clv_prediction'] = '../outputs/plots/advanced_clv_prediction.png'
        plt.savefig(plots['clv_prediction'], dpi=300, bbox_inches='tight')
        plt.close()
        
        return plots
    
    def _generate_clv_recommendations(self, feature_importance: Dict[str, float]) -> List[str]:
        """Generate recommendations based on CLV prediction insights."""
        recommendations = []
        
        # Find most important feature
        most_important = max(feature_importance, key=feature_importance.get)
        recommendations.append(f"🎯 Focus on improving {most_important} as it has the highest impact on CLV")
        
        # General recommendations
        recommendations.append("📈 Implement targeted campaigns for high-CLV predicted customers")
        recommendations.append("🔄 Regular model retraining recommended for better predictions")
        
        return recommendations
    
    @handle_errors
    def generate_comprehensive_report(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate a comprehensive analytics report combining all advanced analyses.
        
        Args:
            df: Customer data DataFrame
            
        Returns:
            Dictionary with complete analysis results
        """
        with PerformanceTimer("Comprehensive Analysis"):
            report = {
                "timestamp": pd.Timestamp.now().isoformat(),
                "dataset_info": {
                    "shape": df.shape,
                    "columns": df.columns.tolist(),
                    "data_types": df.dtypes.to_dict()
                }
            }
            
            # Perform all analyses
            try:
                report["segmentation"] = self.perform_customer_segmentation(df)
            except Exception as e:
                report["segmentation"] = {"error": str(e)}
            
            try:
                report["anomaly_detection"] = self.detect_anomalies(df)
            except Exception as e:
                report["anomaly_detection"] = {"error": str(e)}
            
            try:
                report["clv_prediction"] = self.predict_customer_lifetime_value(df)
            except Exception as e:
                report["clv_prediction"] = {"error": str(e)}
            
            # Generate executive summary
            report["executive_summary"] = self._generate_executive_summary(report)
            
            return report
    
    def _generate_executive_summary(self, report: Dict[str, Any]) -> List[str]:
        """Generate executive summary from all analyses."""
        summary = []
        
        summary.append("📊 ADVANCED E-COMMERCE ANALYTICS REPORT")
        summary.append(f"📅 Generated: {report['timestamp']}")
        summary.append(f"📈 Dataset: {report['dataset_info']['shape'][0]:,} customers, {report['dataset_info']['shape'][1]} attributes")
        
        # Segmentation insights
        if "segmentation" in report and "error" not in report["segmentation"]:
            seg = report["segmentation"]
            summary.append(f"🎯 Customer Segmentation: {seg['clusters']} distinct segments identified")
            summary.append(f"📊 Segmentation Quality: {seg['silhouette_score']:.3f} silhouette score")
        
        # Anomaly insights
        if "anomaly_detection" in report and "error" not in report["anomaly_detection"]:
            anom = report["anomaly_detection"]
            summary.append(f"🚨 Anomaly Detection: {anom['analysis']['total_anomalies']} anomalies found ({anom['analysis']['anomaly_percentage']:.1f}%)")
        
        # CLV insights
        if "clv_prediction" in report and "error" not in report["clv_prediction"]:
            clv = report["clv_prediction"]
            summary.append(f"💰 CLV Prediction: {clv['accuracy']:.3f} accuracy achieved")
        
        summary.append("💡 See detailed recommendations in each analysis section")
        
        return summary
