"""
Unit tests for advanced analytics module.
"""
import pytest
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from advanced_analytics import AdvancedAnalytics
from utils import ProjectError

class TestAdvancedAnalytics:
    """Test advanced analytics functionality."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing."""
        np.random.seed(42)
        return pd.DataFrame({
            'user_id': range(100),
            'age': np.random.randint(18, 80, 100),
            'total_purchases': np.random.randint(1, 200, 100),
            'browsing_time_minutes': np.random.randint(10, 300, 100),
            'avg_order_value': np.random.uniform(20, 500, 100),
            'customer_lifetime_value': np.random.uniform(100, 10000, 100),
            'segment': np.random.choice(['VIP', 'Regular', 'New'], 100)
        })
    
    @pytest.fixture
    def analytics(self):
        """Create analytics instance."""
        return AdvancedAnalytics()
    
    def test_customer_segmentation(self, analytics, sample_data):
        """Test customer segmentation."""
        result = analytics.perform_customer_segmentation(sample_data, n_clusters=3)
        
        assert "segmentation_method" in result
        assert "clusters" in result
        assert "silhouette_score" in result
        assert "cluster_analysis" in result
        assert result["clusters"] == 3
        assert 0 <= result["silhouette_score"] <= 1
    
    def test_customer_segmentation_insufficient_data(self, analytics):
        """Test segmentation with insufficient data."""
        df = pd.DataFrame({'col1': [1, 2]})  # Too few rows and columns
        
        with pytest.raises(ProjectError):
            analytics.perform_customer_segmentation(df)
    
    def test_anomaly_detection(self, analytics, sample_data):
        """Test anomaly detection."""
        result = analytics.detect_anomalies(sample_data, contamination=0.1)
        
        assert "method" in result
        assert "analysis" in result
        assert "plots" in result
        assert "recommendations" in result
        assert "total_anomalies" in result["analysis"]
        assert result["analysis"]["total_anomalies"] >= 0
    
    def test_anomaly_detection_insufficient_data(self, analytics):
        """Test anomaly detection with insufficient data."""
        df = pd.DataFrame({'col1': [1, 2]})  # Too few rows and columns
        
        with pytest.raises(ProjectError):
            analytics.detect_anomalies(df)
    
    def test_clv_prediction(self, analytics, sample_data):
        """Test CLV prediction."""
        result = analytics.predict_customer_lifetime_value(sample_data)
        
        assert "model" in result
        assert "feature_importance" in result
        assert "accuracy" in result
        assert "plots" in result
        assert "recommendations" in result
        assert 0 <= result["accuracy"] <= 1
    
    def test_clv_prediction_missing_target(self, analytics):
        """Test CLV prediction with missing target column."""
        df = pd.DataFrame({
            'age': [25, 30, 35],
            'total_purchases': [10, 20, 30]
        })
        
        with pytest.raises(ProjectError):
            analytics.predict_customer_lifetime_value(df)
    
    def test_comprehensive_report(self, analytics, sample_data):
        """Test comprehensive report generation."""
        result = analytics.generate_comprehensive_report(sample_data)
        
        assert "timestamp" in result
        assert "dataset_info" in result
        assert "executive_summary" in result
        assert "segmentation" in result
        assert "anomaly_detection" in result
        assert "clv_prediction" in result
        
        # Check that at least one analysis succeeded
        analyses = ["segmentation", "anomaly_detection", "clv_prediction"]
        successful_analyses = sum(1 for analysis in analyses if "error" not in result[analysis])
        assert successful_analyses > 0
    
    def test_cluster_analysis(self, analytics, sample_data):
        """Test cluster analysis functionality."""
        # First perform segmentation
        segmentation_result = analytics.perform_customer_segmentation(sample_data, n_clusters=3)
        
        # Check cluster analysis structure
        cluster_analysis = segmentation_result["cluster_analysis"]
        assert isinstance(cluster_analysis, dict)
        
        # Should have clusters
        assert len(cluster_analysis) > 0
        
        # Each cluster should have expected structure
        for cluster_name, cluster_data in cluster_analysis.items():
            assert "size" in cluster_data
            assert "percentage" in cluster_data
            assert "characteristics" in cluster_data
            assert cluster_data["size"] > 0
            assert 0 <= cluster_data["percentage"] <= 100
    
    def test_anomaly_characteristics(self, analytics, sample_data):
        """Test anomaly characteristics analysis."""
        # First detect anomalies
        anomaly_result = analytics.detect_anomalies(sample_data)
        
        # Check anomaly characteristics
        characteristics = anomaly_result["analysis"]["anomaly_characteristics"]
        assert isinstance(characteristics, dict)
        
        # Should have characteristics for numeric features
        expected_features = ['age', 'total_purchases', 'browsing_time_minutes', 'avg_order_value']
        for feature in expected_features:
            if feature in characteristics:
                feature_data = characteristics[feature]
                assert "anomaly_mean" in feature_data
                assert "normal_mean" in feature_data
                assert "difference_pct" in feature_data
