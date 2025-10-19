"""
Real-Time Analytics Module
=========================

This module provides real-time data processing and analytics capabilities
for live e-commerce data streams.

Features:
- Real-time data ingestion
- Live dashboard updates
- Streaming analytics
- Real-time alerts and notifications
"""

import pandas as pd
import numpy as np
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
import json
import queue
from pathlib import Path
import logging

from utils import handle_errors, PerformanceTimer, ProjectError
from cache_manager import cached_dataframe

logger = logging.getLogger(__name__)

class RealTimeDataStream:
    """Real-time data stream handler for e-commerce analytics."""
    
    def __init__(self, stream_config: Dict[str, Any]):
        """
        Initialize real-time data stream.
        
        Args:
            stream_config: Configuration for data stream
        """
        self.config = stream_config
        self.data_queue = queue.Queue(maxsize=stream_config.get('max_queue_size', 1000))
        self.is_running = False
        self.callbacks = []
        self.metrics = {
            'total_records': 0,
            'processed_records': 0,
            'error_count': 0,
            'last_update': None,
            'processing_rate': 0
        }
        
    def add_callback(self, callback: Callable[[Dict[str, Any]], None]):
        """Add callback function for new data events."""
        self.callbacks.append(callback)
    
    def start_stream(self):
        """Start the real-time data stream."""
        self.is_running = True
        logger.info("Real-time data stream started")
    
    def stop_stream(self):
        """Stop the real-time data stream."""
        self.is_running = False
        logger.info("Real-time data stream stopped")
    
    def process_record(self, record: Dict[str, Any]):
        """Process a single data record."""
        try:
            self.metrics['total_records'] += 1
            
            # Validate record
            if self._validate_record(record):
                # Add to queue
                self.data_queue.put(record)
                self.metrics['processed_records'] += 1
                
                # Notify callbacks
                for callback in self.callbacks:
                    try:
                        callback(record)
                    except Exception as e:
                        logger.error(f"Callback error: {e}")
                        
            else:
                self.metrics['error_count'] += 1
                
        except Exception as e:
            logger.error(f"Error processing record: {e}")
            self.metrics['error_count'] += 1
    
    def _validate_record(self, record: Dict[str, Any]) -> bool:
        """Validate incoming data record."""
        required_fields = self.config.get('required_fields', [])
        return all(field in record for field in required_fields)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current stream metrics."""
        self.metrics['last_update'] = datetime.now()
        return self.metrics.copy()

class RealTimeAnalytics:
    """Real-time analytics engine for e-commerce data."""
    
    def __init__(self, stream_config: Dict[str, Any] = None):
        """
        Initialize real-time analytics engine.
        
        Args:
            stream_config: Configuration for data stream
        """
        self.stream_config = stream_config or {
            'max_queue_size': 1000,
            'processing_interval': 5,  # seconds
            'required_fields': ['user_id', 'event_type', 'timestamp']
        }
        
        self.data_stream = RealTimeDataStream(self.stream_config)
        self.analytics_cache = {}
        self.real_time_metrics = {}
        self.is_processing = False
        
        # Initialize analytics modules
        self._initialize_analytics_modules()
        
    def _initialize_analytics_modules(self):
        """Initialize real-time analytics modules."""
        self.modules = {
            'user_activity': UserActivityTracker(),
            'purchase_tracking': PurchaseTracker(),
            'anomaly_detection': RealTimeAnomalyDetector(),
            'performance_monitor': PerformanceMonitor()
        }
        
        # Set up callbacks
        for module in self.modules.values():
            self.data_stream.add_callback(module.process_record)
    
    @handle_errors
    def start_analytics(self):
        """Start real-time analytics processing."""
        self.data_stream.start_stream()
        self.is_processing = True
        
        # Start processing thread
        processing_thread = threading.Thread(target=self._processing_loop)
        processing_thread.daemon = True
        processing_thread.start()
        
        logger.info("Real-time analytics started")
    
    def stop_analytics(self):
        """Stop real-time analytics processing."""
        self.is_processing = False
        self.data_stream.stop_stream()
        logger.info("Real-time analytics stopped")
    
    def _processing_loop(self):
        """Main processing loop for real-time analytics."""
        while self.is_processing:
            try:
                # Process accumulated data
                self._process_batch_data()
                
                # Update real-time metrics
                self._update_real_time_metrics()
                
                # Sleep for processing interval
                time.sleep(self.stream_config['processing_interval'])
                
            except Exception as e:
                logger.error(f"Error in processing loop: {e}")
                time.sleep(1)  # Brief pause on error
    
    def _process_batch_data(self):
        """Process batch of accumulated data."""
        batch_size = self.stream_config.get('batch_size', 100)
        batch_data = []
        
        # Collect batch data
        for _ in range(batch_size):
            try:
                record = self.data_stream.data_queue.get_nowait()
                batch_data.append(record)
            except queue.Empty:
                break
        
        if batch_data:
            # Process batch
            self._analyze_batch(batch_data)
    
    def _analyze_batch(self, batch_data: List[Dict[str, Any]]):
        """Analyze batch of data for insights."""
        try:
            df = pd.DataFrame(batch_data)
            
            # Real-time analysis
            self._update_user_activity(df)
            self._detect_purchase_patterns(df)
            self._check_for_anomalies(df)
            self._update_performance_metrics(df)
            
        except Exception as e:
            logger.error(f"Error analyzing batch: {e}")
    
    def _update_user_activity(self, df: pd.DataFrame):
        """Update user activity metrics."""
        if 'user_id' in df.columns:
            active_users = df['user_id'].nunique()
            self.real_time_metrics['active_users'] = active_users
            self.real_time_metrics['activity_timestamp'] = datetime.now()
    
    def _detect_purchase_patterns(self, df: pd.DataFrame):
        """Detect real-time purchase patterns."""
        if 'event_type' in df.columns:
            purchase_events = df[df['event_type'] == 'purchase']
            if not purchase_events.empty:
                self.real_time_metrics['purchases_last_interval'] = len(purchase_events)
                self.real_time_metrics['purchase_timestamp'] = datetime.now()
    
    def _check_for_anomalies(self, df: pd.DataFrame):
        """Check for real-time anomalies."""
        # Simple anomaly detection for real-time
        if 'value' in df.columns:
            values = df['value'].dropna()
            if len(values) > 10:
                mean_val = values.mean()
                std_val = values.std()
                
                # Flag values beyond 3 standard deviations
                anomalies = values[abs(values - mean_val) > 3 * std_val]
                
                if not anomalies.empty:
                    self.real_time_metrics['anomalies_detected'] = len(anomalies)
                    self.real_time_metrics['anomaly_timestamp'] = datetime.now()
    
    def _update_performance_metrics(self, df: pd.DataFrame):
        """Update performance metrics."""
        self.real_time_metrics['records_processed'] = len(df)
        self.real_time_metrics['processing_timestamp'] = datetime.now()
    
    def _update_real_time_metrics(self):
        """Update overall real-time metrics."""
        stream_metrics = self.data_stream.get_metrics()
        
        self.real_time_metrics.update({
            'stream_metrics': stream_metrics,
            'analytics_status': 'running' if self.is_processing else 'stopped',
            'last_metrics_update': datetime.now()
        })
    
    def get_real_time_metrics(self) -> Dict[str, Any]:
        """Get current real-time metrics."""
        return self.real_time_metrics.copy()
    
    def get_live_dashboard_data(self) -> Dict[str, Any]:
        """Get data for live dashboard."""
        return {
            'metrics': self.real_time_metrics,
            'stream_status': self.data_stream.is_running,
            'processing_status': self.is_processing,
            'timestamp': datetime.now().isoformat()
        }

class UserActivityTracker:
    """Track real-time user activity patterns."""
    
    def __init__(self):
        self.activity_data = {}
        self.session_tracker = {}
    
    def process_record(self, record: Dict[str, Any]):
        """Process user activity record."""
        user_id = record.get('user_id')
        if user_id:
            # Update activity data
            current_time = datetime.now()
            
            if user_id not in self.activity_data:
                self.activity_data[user_id] = {
                    'first_seen': current_time,
                    'last_seen': current_time,
                    'activity_count': 0,
                    'sessions': []
                }
            
            self.activity_data[user_id]['last_seen'] = current_time
            self.activity_data[user_id]['activity_count'] += 1
    
    def get_active_users(self, minutes: int = 5) -> List[str]:
        """Get users active in the last N minutes."""
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        
        active_users = []
        for user_id, data in self.activity_data.items():
            if data['last_seen'] > cutoff_time:
                active_users.append(user_id)
        
        return active_users
    
    def get_user_stats(self) -> Dict[str, Any]:
        """Get user activity statistics."""
        total_users = len(self.activity_data)
        active_users = len(self.get_active_users(5))
        
        return {
            'total_users': total_users,
            'active_users_5min': active_users,
            'activity_rate': active_users / total_users if total_users > 0 else 0
        }

class PurchaseTracker:
    """Track real-time purchase patterns."""
    
    def __init__(self):
        self.purchase_data = []
        self.revenue_tracker = {}
    
    def process_record(self, record: Dict[str, Any]):
        """Process purchase record."""
        if record.get('event_type') == 'purchase':
            self.purchase_data.append({
                'timestamp': datetime.now(),
                'user_id': record.get('user_id'),
                'amount': record.get('amount', 0),
                'product_id': record.get('product_id')
            })
            
            # Track revenue by time
            current_hour = datetime.now().replace(minute=0, second=0, microsecond=0)
            if current_hour not in self.revenue_tracker:
                self.revenue_tracker[current_hour] = 0
            
            self.revenue_tracker[current_hour] += record.get('amount', 0)
    
    def get_recent_purchases(self, minutes: int = 60) -> List[Dict[str, Any]]:
        """Get purchases from the last N minutes."""
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        
        recent_purchases = [
            p for p in self.purchase_data 
            if p['timestamp'] > cutoff_time
        ]
        
        return recent_purchases
    
    def get_revenue_stats(self) -> Dict[str, Any]:
        """Get revenue statistics."""
        recent_purchases = self.get_recent_purchases(60)
        
        if not recent_purchases:
            return {
                'revenue_1hour': 0,
                'purchase_count_1hour': 0,
                'avg_purchase_value': 0
            }
        
        total_revenue = sum(p['amount'] for p in recent_purchases)
        purchase_count = len(recent_purchases)
        
        return {
            'revenue_1hour': total_revenue,
            'purchase_count_1hour': purchase_count,
            'avg_purchase_value': total_revenue / purchase_count if purchase_count > 0 else 0
        }

class RealTimeAnomalyDetector:
    """Detect anomalies in real-time data streams."""
    
    def __init__(self):
        self.value_history = []
        self.anomaly_threshold = 3.0  # Standard deviations
        self.max_history_size = 1000
    
    def process_record(self, record: Dict[str, Any]):
        """Process record for anomaly detection."""
        value = record.get('value')
        if value is not None:
            self.value_history.append(value)
            
            # Keep history size manageable
            if len(self.value_history) > self.max_history_size:
                self.value_history = self.value_history[-self.max_history_size:]
    
    def detect_anomalies(self) -> List[Dict[str, Any]]:
        """Detect anomalies in current data."""
        if len(self.value_history) < 10:
            return []
        
        values = np.array(self.value_history)
        mean_val = np.mean(values)
        std_val = np.std(values)
        
        if std_val == 0:
            return []
        
        # Find anomalies
        z_scores = abs((values - mean_val) / std_val)
        anomaly_indices = np.where(z_scores > self.anomaly_threshold)[0]
        
        anomalies = []
        for idx in anomaly_indices:
            anomalies.append({
                'index': idx,
                'value': values[idx],
                'z_score': z_scores[idx],
                'timestamp': datetime.now()
            })
        
        return anomalies

class PerformanceMonitor:
    """Monitor real-time performance metrics."""
    
    def __init__(self):
        self.performance_data = {
            'processing_times': [],
            'throughput': [],
            'error_rates': []
        }
    
    def process_record(self, record: Dict[str, Any]):
        """Process performance record."""
        # Track processing time
        start_time = time.time()
        # Simulate processing
        time.sleep(0.001)  # 1ms processing time
        end_time = time.time()
        
        processing_time = end_time - start_time
        self.performance_data['processing_times'].append(processing_time)
        
        # Keep data size manageable
        if len(self.performance_data['processing_times']) > 1000:
            self.performance_data['processing_times'] = self.performance_data['processing_times'][-1000:]
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics."""
        if not self.performance_data['processing_times']:
            return {
                'avg_processing_time': 0,
                'max_processing_time': 0,
                'throughput': 0
            }
        
        processing_times = self.performance_data['processing_times']
        
        return {
            'avg_processing_time': np.mean(processing_times),
            'max_processing_time': np.max(processing_times),
            'throughput': len(processing_times) / 60 if processing_times else 0  # records per minute
        }

# Global real-time analytics instance
real_time_analytics = None

def initialize_real_time_analytics(config: Dict[str, Any] = None):
    """Initialize global real-time analytics instance."""
    global real_time_analytics
    real_time_analytics = RealTimeAnalytics(config)
    return real_time_analytics

def get_real_time_analytics() -> Optional[RealTimeAnalytics]:
    """Get global real-time analytics instance."""
    return real_time_analytics
