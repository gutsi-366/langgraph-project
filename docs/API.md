# API Documentation

## Overview

The LangGraph AI E-commerce Analytics platform provides a comprehensive set of APIs for data analysis, machine learning, and business intelligence.

## Core Modules

### 1. Enhanced Agent (`src/enhanced_agent.py`)

The main analytics engine providing advanced e-commerce analysis capabilities.

#### Methods

##### `analyze_large_dataset(df: pd.DataFrame) -> Dict[str, Any]`

Performs comprehensive analysis on large datasets with caching and performance optimization.

**Parameters:**
- `df`: Pandas DataFrame containing e-commerce data

**Returns:**
```python
{
    "key_metrics": {
        "total_customers": int,
        "avg_purchase_value": float,
        "total_revenue": float,
        "customer_segments": dict
    },
    "segment_analysis": dict,
    "visualizations": dict,
    "insights": list,
    "recommendations": list,
    "data_quality": dict,
    "advanced_analytics": dict  # For datasets > 1000 rows
}
```

**Example:**
```python
from src.enhanced_agent import EnhancedLangGraphAgent
import pandas as pd

agent = EnhancedLangGraphAgent()
df = pd.read_csv('data/large_dataset.csv')
results = agent.analyze_large_dataset(df)
```

##### `perform_advanced_segmentation(df: pd.DataFrame, n_clusters: int = 5) -> Dict[str, Any]`

Performs ML-powered customer segmentation using K-means clustering.

**Parameters:**
- `df`: Customer data DataFrame
- `n_clusters`: Number of clusters (default: 5)

**Returns:**
```python
{
    "segmentation_method": str,
    "clusters": int,
    "silhouette_score": float,
    "cluster_analysis": dict,
    "plots": dict,
    "recommendations": list
}
```

##### `detect_anomalies(df: pd.DataFrame, contamination: float = 0.1) -> Dict[str, Any]`

Detects anomalous customers using Isolation Forest algorithm.

**Parameters:**
- `df`: Customer data DataFrame
- `contamination`: Expected proportion of anomalies (default: 0.1)

**Returns:**
```python
{
    "method": str,
    "analysis": {
        "total_anomalies": int,
        "anomaly_percentage": float,
        "anomaly_score_range": dict,
        "anomaly_characteristics": dict
    },
    "plots": dict,
    "recommendations": list
}
```

##### `predict_customer_lifetime_value(df: pd.DataFrame) -> Dict[str, Any]`

Predicts customer lifetime value using Random Forest classifier.

**Parameters:**
- `df`: Customer data DataFrame

**Returns:**
```python
{
    "model": str,
    "feature_importance": dict,
    "accuracy": float,
    "plots": dict,
    "recommendations": list
}
```

### 2. Advanced Analytics (`src/advanced_analytics.py`)

Core machine learning and analytics engine.

#### Methods

##### `generate_comprehensive_report(df: pd.DataFrame) -> Dict[str, Any]`

Generates a complete analytics report combining all advanced analyses.

**Parameters:**
- `df`: Customer data DataFrame

**Returns:**
```python
{
    "timestamp": str,
    "dataset_info": dict,
    "segmentation": dict,
    "anomaly_detection": dict,
    "clv_prediction": dict,
    "executive_summary": list
}
```

### 3. Cache Manager (`src/cache_manager.py`)

Advanced caching system for performance optimization.

#### Methods

##### `CacheManager.get(key_data: Any) -> Optional[Any]`

Retrieve data from cache.

**Parameters:**
- `key_data`: Data to generate cache key from

**Returns:**
- Cached data or None if not found/expired

##### `CacheManager.set(key_data: Any, value: Any, ttl: Optional[int] = None) -> bool`

Store data in cache.

**Parameters:**
- `key_data`: Data to generate cache key from
- `value`: Data to cache
- `ttl`: Time to live in seconds

**Returns:**
- True if successful, False otherwise

#### Decorators

##### `@cached(ttl: Optional[int] = None)`

Decorator for caching function results.

**Example:**
```python
@cached(ttl=3600)  # Cache for 1 hour
def expensive_function(data):
    return process_data(data)
```

##### `@cached_dataframe(ttl: Optional[int] = None)`

Specialized decorator for caching DataFrame operations.

**Example:**
```python
@cached_dataframe(ttl=1800)  # Cache for 30 minutes
def analyze_data(df):
    return complex_analysis(df)
```

### 4. Security (`src/security.py`)

Security utilities for input validation and access control.

#### Classes

##### `InputValidator`

Input validation and sanitization utilities.

**Methods:**

- `validate_file_upload(uploaded_file) -> Dict[str, Any]`: Validate uploaded files
- `sanitize_string(input_string: str, max_length: int = 1000) -> str`: Sanitize string input
- `validate_url(url: str) -> bool`: Validate URLs for security

##### `DataSanitizer`

Data sanitization utilities.

**Methods:**

- `sanitize_dataframe(df: pd.DataFrame) -> pd.DataFrame`: Sanitize DataFrame for security

##### `AccessController`

Access control and authentication utilities.

**Methods:**

- `generate_session_token() -> str`: Generate secure session token
- `hash_password(password: str) -> str`: Hash password securely
- `verify_password(password: str, password_hash: str) -> bool`: Verify password
- `check_rate_limit(identifier: str, max_requests: int = 100, window_seconds: int = 3600) -> bool`: Check rate limits

#### Decorators

##### `@require_authentication`

Decorator to require authentication.

##### `@require_rate_limit(max_requests: int = 10, window_seconds: int = 60)`

Decorator to enforce rate limiting.

##### `@secure_file_upload(allowed_types: List[str] = None)`

Decorator for secure file upload handling.

### 5. Utilities (`src/utils.py`)

Common utility functions and error handling.

#### Methods

##### `validate_dataframe(df: pd.DataFrame, required_columns: List[str] = None) -> Dict[str, Any]`

Validate a DataFrame and return validation results.

**Parameters:**
- `df`: DataFrame to validate
- `required_columns`: List of required column names

**Returns:**
```python
{
    "is_valid": bool,
    "issues": list,
    "suggestions": list,
    "stats": dict
}
```

##### `load_and_validate_csv(file_path: Union[str, Path], required_columns: List[str] = None) -> pd.DataFrame`

Load and validate a CSV file.

**Parameters:**
- `file_path`: Path to CSV file
- `required_columns`: List of required column names

**Returns:**
- Validated DataFrame

**Raises:**
- `FileProcessingError`: If file cannot be loaded
- `DataValidationError`: If data validation fails

##### `safe_execute_code(code: str, timeout: int = 30) -> Dict[str, Any]`

Safely execute Python code with timeout and error handling.

**Parameters:**
- `code`: Python code to execute
- `timeout`: Timeout in seconds

**Returns:**
```python
{
    "success": bool,
    "stdout": str,
    "stderr": str,
    "return_code": int
}
```

#### Context Managers

##### `PerformanceTimer(operation_name: str)`

Context manager for timing operations.

**Example:**
```python
with PerformanceTimer("Data Analysis"):
    result = analyze_data(df)
```

## Configuration

### Environment Variables

The application uses the following environment variables:

```bash
# OpenAI Configuration (Required for LLM features)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
OPENAI_BASE_URL=

# Alternative LLM Configuration (Optional)
PROXY_API_BASE_URL=
PROXY_API_KEY=
PROXY_MODEL=gpt-3.5-turbo

# Application Configuration
DEBUG=False
LOG_LEVEL=INFO
MAX_FILE_SIZE_MB=100
CACHE_TTL_SECONDS=3600

# Streamlit Configuration
STREAMLIT_THEME_BASE=light
STREAMLIT_SERVER_PORT=8501

# Data Storage
DATA_DIR=./data
OUTPUT_DIR=./outputs
CACHE_DIR=./cache

# Security
SECRET_KEY=your_secret_key_here
ALLOWED_FILE_TYPES=csv,xlsx,json
```

## Error Handling

The platform uses custom exception classes for better error handling:

### Exception Classes

- `ProjectError`: Base exception for project-specific errors
- `DataValidationError`: Raised when data validation fails
- `LLMError`: Raised when LLM operations fail
- `FileProcessingError`: Raised when file processing fails
- `SecurityError`: Raised when security validation fails

### Error Handling Decorator

```python
from utils import handle_errors

@handle_errors
def my_function():
    # Function that might raise exceptions
    pass
```

## Performance Optimization

### Caching

The platform includes an advanced caching system:

- **Automatic caching** of analysis results
- **TTL-based expiration** for cache entries
- **Smart cache invalidation** based on data changes
- **Memory-efficient** storage with compression

### Performance Monitoring

```python
from utils import PerformanceTimer

with PerformanceTimer("Operation Name"):
    # Your operation here
    result = perform_analysis(data)
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_utils.py

# Run with coverage
pytest --cov=src

# Run only fast tests
pytest -m "not slow"
```

### Test Structure

- `tests/test_utils.py`: Tests for utility functions
- `tests/test_advanced_analytics.py`: Tests for analytics functionality
- `tests/test_cache_manager.py`: Tests for caching system
- `tests/conftest.py`: Test configuration and fixtures

## Examples

### Basic Analysis

```python
from src.enhanced_agent import EnhancedLangGraphAgent
import pandas as pd

# Initialize agent
agent = EnhancedLangGraphAgent()

# Load data
df = pd.read_csv('data/customers.csv')

# Perform analysis
results = agent.analyze_large_dataset(df)

# Access results
print(f"Total customers: {results['key_metrics']['total_customers']}")
print(f"Average purchase value: ${results['key_metrics']['avg_purchase_value']:.2f}")
```

### Advanced Segmentation

```python
# Perform advanced customer segmentation
segmentation = agent.perform_advanced_segmentation(df, n_clusters=4)

print(f"Segmentation quality: {segmentation['silhouette_score']:.3f}")
print(f"Number of segments: {segmentation['clusters']}")

# View cluster analysis
for cluster_name, cluster_data in segmentation['cluster_analysis'].items():
    print(f"{cluster_name}: {cluster_data['size']} customers ({cluster_data['percentage']:.1f}%)")
```

### Anomaly Detection

```python
# Detect anomalies
anomalies = agent.detect_anomalies(df, contamination=0.05)

print(f"Found {anomalies['analysis']['total_anomalies']} anomalies")
print(f"Anomaly rate: {anomalies['analysis']['anomaly_percentage']:.1f}%")

# View recommendations
for recommendation in anomalies['recommendations']:
    print(f"• {recommendation}")
```

### Caching Example

```python
from src.cache_manager import cached

@cached(ttl=3600)  # Cache for 1 hour
def expensive_analysis(data):
    # Expensive computation here
    return process_data(data)

# First call - executes function
result1 = expensive_analysis(my_data)

# Second call - returns cached result
result2 = expensive_analysis(my_data)  # Much faster!
```
