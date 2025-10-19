"""
Unit tests for cache manager.
"""
import pytest
import tempfile
import time
import json
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cache_manager import CacheManager, cached, cached_dataframe, DataFrameCache

class TestCacheManager:
    """Test cache manager functionality."""
    
    @pytest.fixture
    def temp_cache_dir(self):
        """Create temporary cache directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)
    
    @pytest.fixture
    def cache_manager(self, temp_cache_dir):
        """Create cache manager instance."""
        return CacheManager(cache_dir=temp_cache_dir, default_ttl=60)
    
    def test_set_and_get(self, cache_manager):
        """Test setting and getting cache values."""
        key_data = {"test": "data"}
        value = {"result": "cached"}
        
        # Set value
        assert cache_manager.set(key_data, value)
        
        # Get value
        retrieved = cache_manager.get(key_data)
        assert retrieved == value
    
    def test_get_nonexistent(self, cache_manager):
        """Test getting non-existent cache value."""
        key_data = {"nonexistent": "key"}
        result = cache_manager.get(key_data)
        assert result is None
    
    def test_cache_expiration(self, cache_manager):
        """Test cache expiration."""
        key_data = {"expiring": "data"}
        value = {"result": "expires"}
        
        # Set with short TTL
        assert cache_manager.set(key_data, value, ttl=1)
        
        # Should be available immediately
        assert cache_manager.get(key_data) == value
        
        # Wait for expiration
        time.sleep(1.1)
        
        # Should be expired
        assert cache_manager.get(key_data) is None
    
    def test_delete(self, cache_manager):
        """Test cache deletion."""
        key_data = {"deletable": "data"}
        value = {"result": "will be deleted"}
        
        # Set value
        assert cache_manager.set(key_data, value)
        assert cache_manager.get(key_data) == value
        
        # Delete value
        assert cache_manager.delete(key_data)
        assert cache_manager.get(key_data) is None
    
    def test_clear(self, cache_manager):
        """Test cache clearing."""
        # Set multiple values
        cache_manager.set({"key1": "data"}, "value1")
        cache_manager.set({"key2": "data"}, "value2")
        
        # Clear cache
        deleted_count = cache_manager.clear()
        assert deleted_count >= 2
        
        # All values should be gone
        assert cache_manager.get({"key1": "data"}) is None
        assert cache_manager.get({"key2": "data"}) is None
    
    def test_stats(self, cache_manager):
        """Test cache statistics."""
        # Initial stats
        stats = cache_manager.get_stats()
        assert stats["hits"] == 0
        assert stats["misses"] == 0
        
        # Set and get value
        cache_manager.set({"test": "data"}, "value")
        cache_manager.get({"test": "data"})
        
        # Check stats
        stats = cache_manager.get_stats()
        assert stats["hits"] == 1
        assert stats["sets"] == 1
    
    def test_cleanup_expired(self, cache_manager):
        """Test cleanup of expired entries."""
        # Set values with different TTLs
        cache_manager.set({"short": "ttl"}, "value1", ttl=1)
        cache_manager.set({"long": "ttl"}, "value2", ttl=60)
        
        # Wait for short TTL to expire
        time.sleep(1.1)
        
        # Cleanup expired
        removed_count = cache_manager.cleanup_expired()
        assert removed_count >= 1
        
        # Short TTL should be gone, long TTL should remain
        assert cache_manager.get({"short": "ttl"}) is None
        assert cache_manager.get({"long": "ttl"}) == "value2"

class TestCachedDecorator:
    """Test caching decorators."""
    
    @pytest.fixture
    def temp_cache_dir(self):
        """Create temporary cache directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)
    
    def test_cached_decorator(self, temp_cache_dir):
        """Test @cached decorator."""
        # Create cache manager
        cache_manager = CacheManager(cache_dir=temp_cache_dir)
        
        # Counter to track function calls
        call_count = 0
        
        @cached(ttl=60)
        def expensive_function(x, y):
            nonlocal call_count
            call_count += 1
            return x + y
        
        # First call
        result1 = expensive_function(1, 2)
        assert result1 == 3
        assert call_count == 1
        
        # Second call (should be cached)
        result2 = expensive_function(1, 2)
        assert result2 == 3
        assert call_count == 1  # Should not have been called again
        
        # Different arguments (should not be cached)
        result3 = expensive_function(2, 3)
        assert result3 == 5
        assert call_count == 2
    
    def test_cached_dataframe_decorator(self, temp_cache_dir):
        """Test @cached_dataframe decorator."""
        import pandas as pd
        
        # Create cache manager
        cache_manager = CacheManager(cache_dir=temp_cache_dir)
        
        # Counter to track function calls
        call_count = 0
        
        @cached_dataframe(ttl=60)
        def analyze_dataframe(df):
            nonlocal call_count
            call_count += 1
            return {"sum": df.sum().sum()}
        
        # Create test DataFrame
        df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
        
        # First call
        result1 = analyze_dataframe(df)
        assert result1["sum"] == 21
        assert call_count == 1
        
        # Second call with same DataFrame (should be cached)
        result2 = analyze_dataframe(df)
        assert result2["sum"] == 21
        assert call_count == 1  # Should not have been called again
        
        # Different DataFrame (should not be cached)
        df2 = pd.DataFrame({'c': [7, 8, 9]})
        result3 = analyze_dataframe(df2)
        assert result3["sum"] == 24
        assert call_count == 2

class TestDataFrameCache:
    """Test DataFrame-specific caching."""
    
    @pytest.fixture
    def temp_cache_dir(self):
        """Create temporary cache directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)
    
    @pytest.fixture
    def dataframe_cache(self, temp_cache_dir):
        """Create DataFrame cache instance."""
        cache_manager = CacheManager(cache_dir=temp_cache_dir)
        return DataFrameCache(cache_manager)
    
    def test_analysis_cache(self, dataframe_cache):
        """Test DataFrame analysis caching."""
        import pandas as pd
        
        # Create test DataFrame
        df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
        
        # Test data
        analysis_result = {"mean": df.mean().to_dict()}
        
        # Set cache
        assert dataframe_cache.set_analysis_cache(df, "mean_analysis", analysis_result)
        
        # Get cache
        cached_result = dataframe_cache.get_analysis_cache(df, "mean_analysis")
        assert cached_result == analysis_result
        
        # Different analysis type should not be cached
        assert dataframe_cache.get_analysis_cache(df, "sum_analysis") is None
