"""
Security utilities for input validation, sanitization, and access control.
"""
import re
import hashlib
import secrets
import os
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
import pandas as pd
import streamlit as st
from functools import wraps

from utils import ProjectError

class SecurityError(ProjectError):
    """Raised when security validation fails."""
    pass

class InputValidator:
    """Input validation and sanitization utilities."""
    
    # File type whitelist
    ALLOWED_FILE_TYPES = {
        'csv': ['.csv'],
        'excel': ['.xlsx', '.xls'],
        'json': ['.json'],
        'text': ['.txt']
    }
    
    # Maximum file sizes (in bytes)
    MAX_FILE_SIZES = {
        'csv': 100 * 1024 * 1024,  # 100MB
        'excel': 50 * 1024 * 1024,  # 50MB
        'json': 10 * 1024 * 1024,   # 10MB
        'text': 5 * 1024 * 1024     # 5MB
    }
    
    # Dangerous file extensions
    DANGEROUS_EXTENSIONS = {
        '.exe', '.bat', '.cmd', '.com', '.pif', '.scr', '.vbs', '.js',
        '.jar', '.php', '.asp', '.jsp', '.sh', '.ps1', '.py', '.rb'
    }
    
    @classmethod
    def validate_file_upload(cls, uploaded_file) -> Dict[str, Any]:
        """
        Validate uploaded file for security.
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Dictionary with validation results
            
        Raises:
            SecurityError: If file validation fails
        """
        validation_result = {
            "is_valid": True,
            "warnings": [],
            "file_info": {}
        }
        
        try:
            # Check file size
            file_size = uploaded_file.size
            validation_result["file_info"]["size"] = file_size
            validation_result["file_info"]["size_mb"] = file_size / (1024 * 1024)
            
            # Check file extension
            file_extension = Path(uploaded_file.name).suffix.lower()
            validation_result["file_info"]["extension"] = file_extension
            
            # Validate file extension
            if file_extension in cls.DANGEROUS_EXTENSIONS:
                raise SecurityError(f"Dangerous file extension: {file_extension}")
            
            # Check if extension is allowed
            allowed_extensions = []
            for extensions in cls.ALLOWED_FILE_TYPES.values():
                allowed_extensions.extend(extensions)
            
            if file_extension not in allowed_extensions:
                raise SecurityError(f"File type not allowed: {file_extension}")
            
            # Check file size limits
            file_type = None
            for ftype, extensions in cls.ALLOWED_FILE_TYPES.items():
                if file_extension in extensions:
                    file_type = ftype
                    break
            
            if file_type and file_size > cls.MAX_FILE_SIZES[file_type]:
                raise SecurityError(f"File too large: {file_size / (1024*1024):.1f}MB exceeds limit")
            
            # Validate file name
            if not cls._is_safe_filename(uploaded_file.name):
                raise SecurityError("Unsafe filename detected")
            
            # Additional security checks
            if file_size == 0:
                raise SecurityError("Empty file not allowed")
            
            validation_result["file_type"] = file_type
            validation_result["is_valid"] = True
            
        except SecurityError:
            raise
        except Exception as e:
            raise SecurityError(f"File validation error: {str(e)}")
        
        return validation_result
    
    @classmethod
    def _is_safe_filename(cls, filename: str) -> bool:
        """Check if filename is safe."""
        # Check for path traversal attempts
        dangerous_patterns = ['../', '..\\', '/', '\\', ':', '*', '?', '"', '<', '>', '|']
        
        for pattern in dangerous_patterns:
            if pattern in filename:
                return False
        
        # Check for suspicious characters
        if re.search(r'[^\w\-_\.]', filename):
            return False
        
        return True
    
    @classmethod
    def sanitize_string(cls, input_string: str, max_length: int = 1000) -> str:
        """
        Sanitize string input.
        
        Args:
            input_string: Input string to sanitize
            max_length: Maximum allowed length
            
        Returns:
            Sanitized string
        """
        if not isinstance(input_string, str):
            raise SecurityError("Input must be a string")
        
        # Remove null bytes and control characters
        sanitized = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', input_string)
        
        # Limit length
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>"\']', '', sanitized)
        
        return sanitized.strip()
    
    @classmethod
    def validate_url(cls, url: str) -> bool:
        """
        Validate URL for security.
        
        Args:
            url: URL to validate
            
        Returns:
            True if URL is safe
        """
        # Basic URL pattern
        url_pattern = re.compile(
            r'^https?://'  # http or https
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
            r'(?::\d+)?'  # port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        if not url_pattern.match(url):
            return False
        
        # Check for dangerous schemes
        dangerous_schemes = ['javascript:', 'data:', 'file:', 'ftp:']
        for scheme in dangerous_schemes:
            if url.lower().startswith(scheme):
                return False
        
        return True

class DataSanitizer:
    """Data sanitization utilities."""
    
    @classmethod
    def sanitize_dataframe(cls, df: pd.DataFrame) -> pd.DataFrame:
        """
        Sanitize DataFrame for security.
        
        Args:
            df: DataFrame to sanitize
            
        Returns:
            Sanitized DataFrame
        """
        # Create a copy to avoid modifying original
        sanitized_df = df.copy()
        
        # Limit DataFrame size
        max_rows = 100000  # 100K rows max
        max_cols = 100     # 100 columns max
        
        if len(sanitized_df) > max_rows:
            sanitized_df = sanitized_df.head(max_rows)
            st.warning(f"DataFrame truncated to {max_rows} rows for security")
        
        if len(sanitized_df.columns) > max_cols:
            sanitized_df = sanitized_df.iloc[:, :max_cols]
            st.warning(f"DataFrame truncated to {max_cols} columns for security")
        
        # Sanitize string columns
        for col in sanitized_df.select_dtypes(include=['object']).columns:
            sanitized_df[col] = sanitized_df[col].astype(str).apply(
                lambda x: InputValidator.sanitize_string(str(x), max_length=1000) if pd.notna(x) else x
            )
        
        # Check for suspicious patterns in data
        cls._check_suspicious_patterns(sanitized_df)
        
        return sanitized_df
    
    @classmethod
    def _check_suspicious_patterns(cls, df: pd.DataFrame):
        """Check for suspicious patterns in DataFrame."""
        suspicious_patterns = [
            r'<script.*?>.*?</script>',  # Script tags
            r'javascript:',              # JavaScript URLs
            r'data:text/html',          # Data URLs
            r'<iframe.*?>',             # Iframe tags
            r'<object.*?>',             # Object tags
        ]
        
        for col in df.select_dtypes(include=['object']).columns:
            for pattern in suspicious_patterns:
                if df[col].astype(str).str.contains(pattern, case=False, na=False).any():
                    st.warning(f"Suspicious pattern detected in column '{col}'")
                    break

class AccessController:
    """Access control and authentication utilities."""
    
    @classmethod
    def generate_session_token(cls) -> str:
        """Generate secure session token."""
        return secrets.token_urlsafe(32)
    
    @classmethod
    def hash_password(cls, password: str) -> str:
        """Hash password securely."""
        salt = secrets.token_hex(16)
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return f"{salt}:{password_hash.hex()}"
    
    @classmethod
    def verify_password(cls, password: str, password_hash: str) -> bool:
        """Verify password against hash."""
        try:
            salt, hash_hex = password_hash.split(':')
            password_hash_check = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
            return password_hash_check.hex() == hash_hex
        except:
            return False
    
    @classmethod
    def check_rate_limit(cls, identifier: str, max_requests: int = 100, window_seconds: int = 3600) -> bool:
        """
        Simple rate limiting check.
        
        Args:
            identifier: Unique identifier (IP, user ID, etc.)
            max_requests: Maximum requests allowed
            window_seconds: Time window in seconds
            
        Returns:
            True if request is allowed
        """
        # This is a simplified implementation
        # In production, use Redis or similar for distributed rate limiting
        current_time = int(time.time())
        window_start = current_time - window_seconds
        
        # Store in session state for demo purposes
        if 'rate_limits' not in st.session_state:
            st.session_state.rate_limits = {}
        
        rate_limits = st.session_state.rate_limits
        
        # Clean old entries
        rate_limits[identifier] = [
            timestamp for timestamp in rate_limits.get(identifier, [])
            if timestamp > window_start
        ]
        
        # Check if under limit
        if len(rate_limits[identifier]) >= max_requests:
            return False
        
        # Add current request
        rate_limits[identifier].append(current_time)
        return True

def require_authentication(func):
    """Decorator to require authentication."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Check if user is authenticated
        if 'authenticated' not in st.session_state or not st.session_state.authenticated:
            st.error("🔒 Authentication required")
            st.stop()
        
        return func(*args, **kwargs)
    return wrapper

def require_rate_limit(max_requests: int = 10, window_seconds: int = 60):
    """Decorator to enforce rate limiting."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get client IP (simplified)
            client_ip = "127.0.0.1"  # In production, get real IP
            
            if not AccessController.check_rate_limit(client_ip, max_requests, window_seconds):
                st.error(f"🚫 Rate limit exceeded. Maximum {max_requests} requests per {window_seconds} seconds.")
                st.stop()
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

def secure_file_upload(allowed_types: List[str] = None):
    """Decorator for secure file upload handling."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Validate uploaded files
            for arg in args:
                if hasattr(arg, 'name') and hasattr(arg, 'size'):  # Streamlit uploaded file
                    validation_result = InputValidator.validate_file_upload(arg)
                    if not validation_result["is_valid"]:
                        st.error("🚫 File upload validation failed")
                        st.stop()
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

class SecurityAuditor:
    """Security auditing and logging utilities."""
    
    @classmethod
    def log_security_event(cls, event_type: str, details: Dict[str, Any], severity: str = "INFO"):
        """
        Log security events.
        
        Args:
            event_type: Type of security event
            details: Event details
            severity: Event severity (INFO, WARNING, ERROR)
        """
        import logging
        import json
        
        logger = logging.getLogger('security')
        
        event_data = {
            "timestamp": time.time(),
            "event_type": event_type,
            "severity": severity,
            "details": details,
            "session_id": st.session_state.get('session_id', 'unknown')
        }
        
        if severity == "ERROR":
            logger.error(f"Security Event: {json.dumps(event_data)}")
        elif severity == "WARNING":
            logger.warning(f"Security Event: {json.dumps(event_data)}")
        else:
            logger.info(f"Security Event: {json.dumps(event_data)}")
    
    @classmethod
    def audit_data_access(cls, dataset_name: str, user_action: str):
        """Audit data access events."""
        cls.log_security_event(
            "DATA_ACCESS",
            {
                "dataset": dataset_name,
                "action": user_action,
                "rows_accessed": st.session_state.get('current_dataset_rows', 0)
            },
            "INFO"
        )
    
    @classmethod
    def audit_file_upload(cls, filename: str, file_size: int, validation_result: Dict[str, Any]):
        """Audit file upload events."""
        cls.log_security_event(
            "FILE_UPLOAD",
            {
                "filename": filename,
                "file_size": file_size,
                "validation_result": validation_result
            },
            "WARNING" if not validation_result["is_valid"] else "INFO"
        )

# Initialize security logging
import logging
import time

security_logger = logging.getLogger('security')
security_logger.setLevel(logging.INFO)

# Create security log handler
security_handler = logging.FileHandler('outputs/security.log')
security_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))
security_logger.addHandler(security_handler)
