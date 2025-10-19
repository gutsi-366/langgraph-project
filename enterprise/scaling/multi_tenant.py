"""
Multi-Tenant Architecture for Enterprise Scaling
===============================================

This module provides multi-tenant capabilities for the LangGraph AI platform,
enabling multiple organizations to use the platform with data isolation,
custom branding, and scalable resource management.

Features:
- Tenant isolation and data segregation
- Custom branding and configuration per tenant
- Resource quotas and usage tracking
- Billing and subscription management
- Enterprise security and compliance
"""

import uuid
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json
import logging

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

logger = logging.getLogger(__name__)

# Multi-tenant database models
TenantBase = declarative_base()

class TenantStatus(Enum):
    """Tenant status enumeration."""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    TRIAL = "trial"
    CANCELLED = "cancelled"
    PENDING = "pending"

class TenantPlan(Enum):
    """Tenant subscription plan enumeration."""
    FREE = "free"
    BASIC = "basic"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"
    CUSTOM = "custom"

@dataclass
class TenantQuota:
    """Tenant resource quotas."""
    max_users: int = 5
    max_datasets: int = 10
    max_storage_gb: float = 1.0
    max_analyses_per_month: int = 100
    max_api_calls_per_month: int = 1000
    max_concurrent_analyses: int = 2
    data_retention_days: int = 30
    custom_branding: bool = False
    priority_support: bool = False
    sso_enabled: bool = False
    audit_logs: bool = False

class Tenant(TenantBase):
    """Multi-tenant organization model."""
    
    __tablename__ = 'tenants'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(200), nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    domain = Column(String(255), unique=True)
    plan = Column(String(50), default=TenantPlan.FREE.value)
    status = Column(String(50), default=TenantStatus.PENDING.value)
    
    # Configuration
    config = Column(JSON)  # Tenant-specific configuration
    branding = Column(JSON)  # Custom branding settings
    quotas = Column(JSON)  # Resource quotas
    
    # Billing
    billing_email = Column(String(255))
    billing_address = Column(Text)
    subscription_id = Column(String(100))
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    trial_ends_at = Column(DateTime)
    subscription_ends_at = Column(DateTime)
    
    # Relationships
    users = relationship("TenantUser", back_populates="tenant")
    datasets = relationship("TenantDataset", back_populates="tenant")
    analyses = relationship("TenantAnalysis", back_populates="tenant")
    usage_logs = relationship("TenantUsageLog", back_populates="tenant")

class TenantUser(TenantBase):
    """User model for multi-tenant architecture."""
    
    __tablename__ = 'tenant_users'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), ForeignKey('tenants.id'), nullable=False)
    user_id = Column(String(36), nullable=False)  # Reference to global user
    role = Column(String(50), default='user')  # admin, user, viewer
    permissions = Column(JSON)  # Tenant-specific permissions
    
    # Status
    is_active = Column(Boolean, default=True)
    invited_at = Column(DateTime)
    joined_at = Column(DateTime)
    last_active = Column(DateTime)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="users")

class TenantDataset(TenantBase):
    """Dataset model with tenant isolation."""
    
    __tablename__ = 'tenant_datasets'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), ForeignKey('tenants.id'), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer)
    row_count = Column(Integer)
    column_count = Column(Integer)
    
    # Metadata
    uploaded_by = Column(String(36))  # User ID
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="datasets")
    analyses = relationship("TenantAnalysis", back_populates="dataset")

class TenantAnalysis(TenantBase):
    """Analysis model with tenant isolation."""
    
    __tablename__ = 'tenant_analyses'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), ForeignKey('tenants.id'), nullable=False)
    dataset_id = Column(String(36), ForeignKey('tenant_datasets.id'), nullable=False)
    name = Column(String(200), nullable=False)
    analysis_type = Column(String(100), nullable=False)
    status = Column(String(50), default='pending')  # pending, running, completed, failed
    
    # Results
    results = Column(JSON)
    visualizations = Column(JSON)
    report_path = Column(String(500))
    
    # Metadata
    created_by = Column(String(36))  # User ID
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    execution_time = Column(Float)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="analyses")
    dataset = relationship("TenantDataset", back_populates="analyses")

class TenantUsageLog(TenantBase):
    """Usage tracking for tenant billing and monitoring."""
    
    __tablename__ = 'tenant_usage_logs'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), ForeignKey('tenants.id'), nullable=False)
    resource_type = Column(String(50), nullable=False)  # analysis, storage, api_call, user
    resource_id = Column(String(100))
    quantity = Column(Float, default=1.0)
    metadata = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="usage_logs")

class MultiTenantManager:
    """Multi-tenant management system."""
    
    def __init__(self, database_url: str):
        """Initialize multi-tenant manager."""
        self.engine = create_engine(database_url)
        TenantBase.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        
        # Default quotas by plan
        self.plan_quotas = {
            TenantPlan.FREE.value: TenantQuota(
                max_users=5,
                max_datasets=10,
                max_storage_gb=1.0,
                max_analyses_per_month=100,
                max_api_calls_per_month=1000,
                max_concurrent_analyses=2,
                data_retention_days=30
            ),
            TenantPlan.BASIC.value: TenantQuota(
                max_users=25,
                max_datasets=100,
                max_storage_gb=10.0,
                max_analyses_per_month=1000,
                max_api_calls_per_month=10000,
                max_concurrent_analyses=5,
                data_retention_days=90
            ),
            TenantPlan.PROFESSIONAL.value: TenantQuota(
                max_users=100,
                max_datasets=500,
                max_storage_gb=50.0,
                max_analyses_per_month=5000,
                max_api_calls_per_month=50000,
                max_concurrent_analyses=10,
                data_retention_days=365,
                custom_branding=True
            ),
            TenantPlan.ENTERPRISE.value: TenantQuota(
                max_users=1000,
                max_datasets=2000,
                max_storage_gb=500.0,
                max_analyses_per_month=50000,
                max_api_calls_per_month=500000,
                max_concurrent_analyses=50,
                data_retention_days=3650,
                custom_branding=True,
                priority_support=True,
                sso_enabled=True,
                audit_logs=True
            )
        }
    
    def create_tenant(self, name: str, domain: str = None, plan: str = TenantPlan.FREE.value) -> Tenant:
        """Create a new tenant."""
        session = self.Session()
        
        try:
            # Generate unique slug
            slug = self._generate_slug(name)
            
            # Create tenant
            tenant = Tenant(
                name=name,
                slug=slug,
                domain=domain,
                plan=plan,
                status=TenantStatus.PENDING.value,
                quotas=self.plan_quotas[plan].__dict__,
                trial_ends_at=datetime.utcnow() + timedelta(days=14) if plan == TenantPlan.FREE.value else None
            )
            
            session.add(tenant)
            session.commit()
            
            logger.info(f"Created tenant: {name} ({slug})")
            return tenant
            
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to create tenant: {e}")
            raise
        finally:
            session.close()
    
    def get_tenant(self, tenant_id: str) -> Optional[Tenant]:
        """Get tenant by ID."""
        session = self.Session()
        try:
            return session.query(Tenant).filter(Tenant.id == tenant_id).first()
        finally:
            session.close()
    
    def get_tenant_by_slug(self, slug: str) -> Optional[Tenant]:
        """Get tenant by slug."""
        session = self.Session()
        try:
            return session.query(Tenant).filter(Tenant.slug == slug).first()
        finally:
            session.close()
    
    def get_tenant_by_domain(self, domain: str) -> Optional[Tenant]:
        """Get tenant by domain."""
        session = self.Session()
        try:
            return session.query(Tenant).filter(Tenant.domain == domain).first()
        finally:
            session.close()
    
    def update_tenant_plan(self, tenant_id: str, new_plan: str) -> bool:
        """Update tenant subscription plan."""
        session = self.Session()
        try:
            tenant = session.query(Tenant).filter(Tenant.id == tenant_id).first()
            if tenant:
                tenant.plan = new_plan
                tenant.quotas = self.plan_quotas[new_plan].__dict__
                tenant.updated_at = datetime.utcnow()
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to update tenant plan: {e}")
            return False
        finally:
            session.close()
    
    def add_user_to_tenant(self, tenant_id: str, user_id: str, role: str = 'user') -> bool:
        """Add user to tenant."""
        session = self.Session()
        try:
            # Check if user is already in tenant
            existing = session.query(TenantUser).filter(
                TenantUser.tenant_id == tenant_id,
                TenantUser.user_id == user_id
            ).first()
            
            if existing:
                return False
            
            # Check quota
            if not self._check_user_quota(tenant_id):
                return False
            
            # Add user
            tenant_user = TenantUser(
                tenant_id=tenant_id,
                user_id=user_id,
                role=role,
                invited_at=datetime.utcnow()
            )
            
            session.add(tenant_user)
            session.commit()
            
            # Log usage
            self._log_usage(tenant_id, 'user', user_id)
            
            return True
            
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to add user to tenant: {e}")
            return False
        finally:
            session.close()
    
    def create_tenant_dataset(self, tenant_id: str, name: str, file_path: str, 
                             uploaded_by: str, file_size: int, row_count: int, 
                             column_count: int) -> Optional[TenantDataset]:
        """Create dataset for tenant."""
        session = self.Session()
        try:
            # Check quota
            if not self._check_dataset_quota(tenant_id):
                return None
            
            # Create dataset
            dataset = TenantDataset(
                tenant_id=tenant_id,
                name=name,
                file_path=file_path,
                uploaded_by=uploaded_by,
                file_size=file_size,
                row_count=row_count,
                column_count=column_count
            )
            
            session.add(dataset)
            session.commit()
            
            # Log usage
            self._log_usage(tenant_id, 'storage', dataset.id, file_size / (1024**3))  # GB
            
            return dataset
            
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to create tenant dataset: {e}")
            return None
        finally:
            session.close()
    
    def create_tenant_analysis(self, tenant_id: str, dataset_id: str, name: str,
                              analysis_type: str, created_by: str) -> Optional[TenantAnalysis]:
        """Create analysis for tenant."""
        session = self.Session()
        try:
            # Check quota
            if not self._check_analysis_quota(tenant_id):
                return None
            
            # Create analysis
            analysis = TenantAnalysis(
                tenant_id=tenant_id,
                dataset_id=dataset_id,
                name=name,
                analysis_type=analysis_type,
                created_by=created_by
            )
            
            session.add(analysis)
            session.commit()
            
            # Log usage
            self._log_usage(tenant_id, 'analysis', analysis.id)
            
            return analysis
            
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to create tenant analysis: {e}")
            return None
        finally:
            session.close()
    
    def get_tenant_usage(self, tenant_id: str, start_date: datetime = None, 
                        end_date: datetime = None) -> Dict[str, Any]:
        """Get tenant usage statistics."""
        session = self.Session()
        try:
            query = session.query(TenantUsageLog).filter(TenantUsageLog.tenant_id == tenant_id)
            
            if start_date:
                query = query.filter(TenantUsageLog.timestamp >= start_date)
            if end_date:
                query = query.filter(TenantUsageLog.timestamp <= end_date)
            
            logs = query.all()
            
            # Aggregate usage by type
            usage = {}
            for log in logs:
                resource_type = log.resource_type
                if resource_type not in usage:
                    usage[resource_type] = 0
                usage[resource_type] += log.quantity
            
            return usage
            
        finally:
            session.close()
    
    def check_tenant_quota(self, tenant_id: str, resource_type: str) -> Tuple[bool, str]:
        """Check if tenant has quota for resource type."""
        tenant = self.get_tenant(tenant_id)
        if not tenant:
            return False, "Tenant not found"
        
        quotas = tenant.quotas or {}
        usage = self.get_tenant_usage(tenant_id)
        
        if resource_type == 'users':
            current_users = usage.get('user', 0)
            max_users = quotas.get('max_users', 0)
            if current_users >= max_users:
                return False, f"User quota exceeded ({current_users}/{max_users})"
        
        elif resource_type == 'datasets':
            current_datasets = usage.get('dataset', 0)
            max_datasets = quotas.get('max_datasets', 0)
            if current_datasets >= max_datasets:
                return False, f"Dataset quota exceeded ({current_datasets}/{max_datasets})"
        
        elif resource_type == 'storage':
            current_storage = usage.get('storage', 0)
            max_storage = quotas.get('max_storage_gb', 0)
            if current_storage >= max_storage:
                return False, f"Storage quota exceeded ({current_storage:.2f}/{max_storage} GB)"
        
        elif resource_type == 'analyses':
            # Check monthly limit
            start_of_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            monthly_usage = self.get_tenant_usage(tenant_id, start_of_month)
            current_analyses = monthly_usage.get('analysis', 0)
            max_analyses = quotas.get('max_analyses_per_month', 0)
            if current_analyses >= max_analyses:
                return False, f"Monthly analysis quota exceeded ({current_analyses}/{max_analyses})"
        
        return True, "Quota available"
    
    def _generate_slug(self, name: str) -> str:
        """Generate unique slug from name."""
        base_slug = hashlib.md5(name.lower().encode()).hexdigest()[:8]
        session = self.Session()
        try:
            counter = 1
            slug = base_slug
            while session.query(Tenant).filter(Tenant.slug == slug).first():
                slug = f"{base_slug}-{counter}"
                counter += 1
            return slug
        finally:
            session.close()
    
    def _check_user_quota(self, tenant_id: str) -> bool:
        """Check user quota for tenant."""
        has_quota, _ = self.check_tenant_quota(tenant_id, 'users')
        return has_quota
    
    def _check_dataset_quota(self, tenant_id: str) -> bool:
        """Check dataset quota for tenant."""
        has_quota, _ = self.check_tenant_quota(tenant_id, 'datasets')
        return has_quota
    
    def _check_analysis_quota(self, tenant_id: str) -> bool:
        """Check analysis quota for tenant."""
        has_quota, _ = self.check_tenant_quota(tenant_id, 'analyses')
        return has_quota
    
    def _log_usage(self, tenant_id: str, resource_type: str, resource_id: str = None, 
                   quantity: float = 1.0, metadata: Dict = None):
        """Log resource usage for tenant."""
        session = self.Session()
        try:
            usage_log = TenantUsageLog(
                tenant_id=tenant_id,
                resource_type=resource_type,
                resource_id=resource_id,
                quantity=quantity,
                metadata=metadata or {}
            )
            
            session.add(usage_log)
            session.commit()
            
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to log usage: {e}")
        finally:
            session.close()

# Global multi-tenant manager instance
multi_tenant_manager = None

def initialize_multi_tenant(database_url: str) -> MultiTenantManager:
    """Initialize global multi-tenant manager."""
    global multi_tenant_manager
    multi_tenant_manager = MultiTenantManager(database_url)
    return multi_tenant_manager

def get_multi_tenant_manager() -> Optional[MultiTenantManager]:
    """Get global multi-tenant manager."""
    return multi_tenant_manager
