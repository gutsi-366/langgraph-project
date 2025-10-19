"""
Pytest configuration and fixtures.
"""
import pytest
import pandas as pd
import numpy as np
from pathlib import Path

@pytest.fixture(scope="session")
def sample_ecommerce_data():
    """Create comprehensive sample e-commerce data for testing."""
    np.random.seed(42)
    
    n_customers = 1000
    
    data = {
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
    }
    
    return pd.DataFrame(data)

@pytest.fixture
def temp_output_dir(tmp_path):
    """Create temporary output directory for tests."""
    output_dir = tmp_path / "outputs"
    output_dir.mkdir()
    plots_dir = output_dir / "plots"
    plots_dir.mkdir()
    return output_dir

@pytest.fixture
def mock_llm():
    """Mock LLM for testing without API calls."""
    class MockLLM:
        def __call__(self, messages):
            return type('Response', (), {'content': 'Mock LLM response'})()
        
        def invoke(self, messages):
            return type('Response', (), {'content': 'Mock LLM response'})()
    
    return MockLLM()

@pytest.fixture(autouse=True)
def setup_test_environment(monkeypatch, temp_output_dir):
    """Setup test environment for each test."""
    # Mock environment variables
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("DEBUG", "True")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    
    # Mock output directories
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    
    # Create mock directories
    temp_output_dir.mkdir(exist_ok=True)
    (temp_output_dir / "plots").mkdir(exist_ok=True)
    (temp_output_dir / "runs").mkdir(exist_ok=True)
    
    yield
    
    # Cleanup
    sys.path.pop(0)
