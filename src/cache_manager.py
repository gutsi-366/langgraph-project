"""
Advanced caching system for performance optimization.
"""
import pickle
import hashlib
import json
import time
import os
from pathlib import Path
from typing import Any, Dict, Optional, Union, Callable
import pandas as pd
import logging
from functools import wraps

from config import Config

logger = logging.getLogger(__name__)

class CacheManager:
    """Advanced caching system with TTL, compression, and smart invalidation."""
    
    def __init__(self, cache_dir: Optional[Path] = None, default_ttl: int = None):
        self.cache_dir = cache_dir or Config.CACHE_DIR
        self.default_ttl = default_ttl or Config.CACHE_TTL_SECONDS
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Cache statistics
        self.stats = {
            "hits": 0,
            "misses": 0,
            "sets": 0,
            "deletes": 0,
            "size_bytes": 0
        }
    
    def _generate_key(self, key_data: Any) -> str:
        """Generate a unique cache key from data."""
        if isinstance(key_data, str):
            key_str = key_data
        else:
            key_str = json.dumps(key_data, sort_keys=True, default=str)
        
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def _get_cache_path(self, key: str) -> Path:
        """Get the file path for a cache key."""
        return self.cache_dir / f"{key}.cache"
    
    def _get_meta_path(self, key: str) -> Path:
        """Get the metadata file path for a cache key."""
        return self.cache_dir / f"{key}.meta"
    
    def get(self, key_data: Any) -> Optional[Any]:
        """
        Retrieve data from cache.
        
        Args:
            key_data: Data to generate cache key from
            
        Returns:
            Cached data or None if not found/expired
        """
        key = self._generate_key(key_data)
        cache_path = self._get_cache_path(key)
        meta_path = self._get_meta_path(key)
        
        # Check if cache file exists
        if not cache_path.exists() or not meta_path.exists():
            self.stats["misses"] += 1
            return None
        
        try:
            # Load metadata
            with open(meta_path, 'r') as f:
                metadata = json.load(f)
            
            # Check if cache has expired
            if time.time() > metadata['expires_at']:
                self.delete(key_data)
                self.stats["misses"] += 1
                return None
            
            # Load cached data
            with open(cache_path, 'rb') as f:
                data = pickle.load(f)
            
            # Update access time
            metadata['last_accessed'] = time.time()
            with open(meta_path, 'w') as f:
                json.dump(metadata, f)
            
            self.stats["hits"] += 1
            logger.debug(f"Cache hit for key: {key}")
            return data
            
        except Exception as e:
            logger.error(f"Error reading cache for key {key}: {e}")
            self.delete(key_data)  # Remove corrupted cache
            self.stats["misses"] += 1
            return None
    
    def set(self, key_data: Any, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Store data in cache.
        
        Args:
            key_data: Data to generate cache key from
            value: Data to cache
            ttl: Time to live in seconds (uses default if None)
            
        Returns:
            True if successful, False otherwise
        """
        key = self._generate_key(key_data)
        cache_path = self._get_cache_path(key)
        meta_path = self._get_meta_path(key)
        
        try:
            # Calculate expiration time
            ttl = ttl or self.default_ttl
            expires_at = time.time() + ttl
            
            # Create metadata
            metadata = {
                'created_at': time.time(),
                'expires_at': expires_at,
                'last_accessed': time.time(),
                'ttl': ttl,
                'size_bytes': 0  # Will be updated after saving
            }
            
            # Save data
            with open(cache_path, 'wb') as f:
                pickle.dump(value, f)
            
            # Update metadata with actual file size
            metadata['size_bytes'] = cache_path.stat().st_size
            
            # Save metadata
            with open(meta_path, 'w') as f:
                json.dump(metadata, f)
            
            self.stats["sets"] += 1
            self.stats["size_bytes"] += metadata['size_bytes']
            logger.debug(f"Cached data for key: {key}")
            return True
            
        except Exception as e:
            logger.error(f"Error caching data for key {key}: {e}")
            return False
    
    def delete(self, key_data: Any) -> bool:
        """
        Delete data from cache.
        
        Args:
            key_data: Data to generate cache key from
            
        Returns:
            True if successful, False otherwise
        """
        key = self._generate_key(key_data)
        cache_path = self._get_cache_path(key)
        meta_path = self._get_meta_path(key)
        
        try:
            # Get file size before deletion
            if cache_path.exists():
                file_size = cache_path.stat().st_size
                cache_path.unlink()
                self.stats["size_bytes"] -= file_size
            
            if meta_path.exists():
                meta_path.unlink()
            
            self.stats["deletes"] += 1
            logger.debug(f"Deleted cache for key: {key}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting cache for key {key}: {e}")
            return False
    
    def clear(self) -> int:
        """
        Clear all cached data.
        
        Returns:
            Number of files deleted
        """
        deleted_count = 0
        
        try:
            for cache_file in self.cache_dir.glob("*.cache"):
                cache_file.unlink()
                deleted_count += 1
            
            for meta_file in self.cache_dir.glob("*.meta"):
                meta_file.unlink()
            
            self.stats = {
                "hits": 0,
                "misses": 0,
                "sets": 0,
                "deletes": 0,
                "size_bytes": 0
            }
            
            logger.info(f"Cleared {deleted_count} cache files")
            
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
        
        return deleted_count
    
    def cleanup_expired(self) -> int:
        """
        Remove expired cache entries.
        
        Returns:
            Number of expired entries removed
        """
        removed_count = 0
        
        try:
            current_time = time.time()
            
            for meta_file in self.cache_dir.glob("*.meta"):
                try:
                    with open(meta_file, 'r') as f:
                        metadata = json.load(f)
                    
                    if current_time > metadata['expires_at']:
                        # Remove both meta and cache files
                        cache_file = self._get_cache_path(meta_file.stem)
                        
                        if cache_file.exists():
                            file_size = cache_file.stat().st_size
                            cache_file.unlink()
                            self.stats["size_bytes"] -= file_size
                        
                        meta_file.unlink()
                        removed_count += 1
                        
                except Exception as e:
                    logger.error(f"Error processing cache file {meta_file}: {e}")
            
            logger.info(f"Cleaned up {removed_count} expired cache entries")
            
        except Exception as e:
            logger.error(f"Error during cache cleanup: {e}")
        
        return removed_count
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        hit_rate = 0
        if self.stats["hits"] + self.stats["misses"] > 0:
            hit_rate = self.stats["hits"] / (self.stats["hits"] + self.stats["misses"])
        
        return {
            **self.stats,
            "hit_rate": hit_rate,
            "cache_dir": str(self.cache_dir),
            "cache_files": len(list(self.cache_dir.glob("*.cache"))),
            "size_mb": self.stats["size_bytes"] / (1024 * 1024)
        }
    
    def get_cache_info(self) -> Dict[str, Any]:
        """Get detailed cache information."""
        cache_files = list(self.cache_dir.glob("*.cache"))
        total_size = sum(f.stat().st_size for f in cache_files)
        
        # Analyze cache entries
        entries = []
        for cache_file in cache_files:
            meta_file = self._get_meta_path(cache_file.stem)
            if meta_file.exists():
                try:
                    with open(meta_file, 'r') as f:
                        metadata = json.load(f)
                    entries.append({
                        "key": cache_file.stem,
                        "created_at": metadata.get('created_at', 0),
                        "expires_at": metadata.get('expires_at', 0),
                        "size_bytes": metadata.get('size_bytes', 0),
                        "is_expired": time.time() > metadata.get('expires_at', 0)
                    })
                except:
                    pass
        
        return {
            "total_files": len(cache_files),
            "total_size_mb": total_size / (1024 * 1024),
            "entries": entries,
            "stats": self.get_stats()
        }

# Global cache manager instance
cache_manager = CacheManager()

def cached(ttl: Optional[int] = None, key_func: Optional[Callable] = None):
    """
    Decorator for caching function results.
    
    Args:
        ttl: Time to live in seconds
        key_func: Custom function to generate cache key from arguments
    
    Example:
        @cached(ttl=3600)  # Cache for 1 hour
        def expensive_function(data):
            return process_data(data)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                cache_key = {
                    "function": func.__name__,
                    "args": args,
                    "kwargs": kwargs
                }
            
            # Try to get from cache
            cached_result = cache_manager.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache_manager.set(cache_key, result, ttl)
            
            return result
        
        return wrapper
    return decorator

def cached_dataframe(ttl: Optional[int] = None, include_shape: bool = True):
    """
    Specialized decorator for caching DataFrame operations.
    
    Args:
        ttl: Time to live in seconds
        include_shape: Whether to include DataFrame shape in cache key
    
    Example:
        @cached_dataframe(ttl=1800)  # Cache for 30 minutes
        def analyze_data(df):
            return complex_analysis(df)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key including DataFrame info
            cache_key = {
                "function": func.__name__,
                "args": []
            }
            
            # Process arguments
            for arg in args:
                if isinstance(arg, pd.DataFrame):
                    cache_key["args"].append({
                        "type": "dataframe",
                        "shape": arg.shape if include_shape else None,
                        "columns": list(arg.columns),
                        "hash": pd.util.hash_pandas_object(arg).sum() if not include_shape else None
                    })
                else:
                    cache_key["args"].append(arg)
            
            cache_key["kwargs"] = kwargs
            
            # Try to get from cache
            cached_result = cache_manager.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache_manager.set(cache_key, result, ttl)
            
            return result
        
        return wrapper
    return decorator

class DataFrameCache:
    """Specialized cache for DataFrame operations with smart invalidation."""
    
    def __init__(self, cache_manager: CacheManager = None):
        self.cache_manager = cache_manager or cache_manager
    
    def get_analysis_cache(self, df: pd.DataFrame, analysis_type: str, **params) -> Optional[Any]:
        """Get cached analysis result for a DataFrame."""
        cache_key = self._generate_analysis_key(df, analysis_type, params)
        return self.cache_manager.get(cache_key)
    
    def set_analysis_cache(self, df: pd.DataFrame, analysis_type: str, result: Any, 
                          ttl: int = None, **params) -> bool:
        """Cache analysis result for a DataFrame."""
        cache_key = self._generate_analysis_key(df, analysis_type, params)
        return self.cache_manager.set(cache_key, result, ttl)
    
    def _generate_analysis_key(self, df: pd.DataFrame, analysis_type: str, params: Dict) -> Dict:
        """Generate cache key for DataFrame analysis."""
        return {
            "type": "dataframe_analysis",
            "analysis": analysis_type,
            "shape": df.shape,
            "columns": list(df.columns),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "params": params,
            "data_hash": pd.util.hash_pandas_object(df).sum()
        }
