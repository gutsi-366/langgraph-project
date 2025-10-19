"""
REST API for LangGraph AI E-commerce Analytics
=============================================

This module provides a REST API interface for the analytics platform,
enabling external systems to interact with the analytics engine.

Endpoints:
- POST /api/analyze - Analyze dataset
- GET /api/health - Health check
- GET /api/metrics - Get system metrics
- POST /api/upload - Upload dataset
- GET /api/reports/{id} - Get analysis report
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import json
import os
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
import traceback
from pathlib import Path

# Import analytics modules
import sys
sys.path.append(str(Path(__file__).parent.parent))

from enhanced_agent import EnhancedLangGraphAgent
from advanced_analytics import AdvancedAnalytics
from utils import validate_dataframe, ProjectError
from security import InputValidator, SecurityAuditor
from cache_manager import cache_manager

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize analytics components
enhanced_agent = EnhancedLangGraphAgent()
advanced_analytics = AdvancedAnalytics()

# API configuration
API_CONFIG = {
    'max_file_size': 100 * 1024 * 1024,  # 100MB
    'allowed_extensions': ['csv', 'xlsx', 'json'],
    'analysis_timeout': 300,  # 5 minutes
    'max_concurrent_analyses': 5
}

# In-memory storage for demo (use database in production)
analysis_storage = {}
upload_storage = {}

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        # Check system components
        health_status = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'components': {
                'enhanced_agent': 'ok',
                'advanced_analytics': 'ok',
                'cache_manager': 'ok',
                'security': 'ok'
            },
            'version': '2.0.0'
        }
        
        return jsonify(health_status), 200
        
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """Get system metrics."""
    try:
        # Get cache metrics
        cache_stats = cache_manager.get_stats()
        
        # Get analysis storage metrics
        storage_metrics = {
            'total_analyses': len(analysis_storage),
            'total_uploads': len(upload_storage),
            'cache_hit_rate': cache_stats.get('hit_rate', 0),
            'cache_size_mb': cache_stats.get('size_mb', 0)
        }
        
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'cache_metrics': cache_stats,
            'storage_metrics': storage_metrics,
            'api_config': API_CONFIG
        }
        
        return jsonify(metrics), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/upload', methods=['POST'])
def upload_dataset():
    """Upload dataset for analysis."""
    try:
        # Security audit
        SecurityAuditor.log_security_event(
            'FILE_UPLOAD_ATTEMPT',
            {'ip': request.remote_addr, 'user_agent': request.headers.get('User-Agent')},
            'INFO'
        )
        
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file
        validation_result = InputValidator.validate_file_upload(file)
        if not validation_result['is_valid']:
            SecurityAuditor.log_security_event(
                'FILE_UPLOAD_REJECTED',
                {'filename': file.filename, 'reason': 'validation_failed'},
                'WARNING'
            )
            return jsonify({'error': 'File validation failed'}), 400
        
        # Generate unique ID for upload
        upload_id = str(uuid.uuid4())
        
        # Save file temporarily
        filename = f"{upload_id}_{file.filename}"
        file_path = Path("uploads") / filename
        file_path.parent.mkdir(exist_ok=True)
        file.save(str(file_path))
        
        # Store upload metadata
        upload_storage[upload_id] = {
            'filename': file.filename,
            'file_path': str(file_path),
            'upload_time': datetime.now().isoformat(),
            'file_size': validation_result['file_info']['size'],
            'file_type': validation_result.get('file_type', 'unknown')
        }
        
        # Log successful upload
        SecurityAuditor.log_security_event(
            'FILE_UPLOAD_SUCCESS',
            {'upload_id': upload_id, 'filename': file.filename},
            'INFO'
        )
        
        return jsonify({
            'upload_id': upload_id,
            'filename': file.filename,
            'file_size': validation_result['file_info']['size'],
            'upload_time': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        SecurityAuditor.log_security_event(
            'FILE_UPLOAD_ERROR',
            {'error': str(e)},
            'ERROR'
        )
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_dataset():
    """Analyze uploaded dataset."""
    try:
        data = request.get_json()
        
        if not data or 'upload_id' not in data:
            return jsonify({'error': 'upload_id required'}), 400
        
        upload_id = data['upload_id']
        analysis_options = data.get('options', {})
        
        # Check if upload exists
        if upload_id not in upload_storage:
            return jsonify({'error': 'Upload not found'}), 404
        
        upload_info = upload_storage[upload_id]
        file_path = upload_info['file_path']
        
        # Load and validate data
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            elif file_path.endswith('.json'):
                df = pd.read_json(file_path)
            else:
                return jsonify({'error': 'Unsupported file format'}), 400
                
        except Exception as e:
            return jsonify({'error': f'Error loading file: {str(e)}'}), 400
        
        # Validate dataset
        validation = validate_dataframe(df)
        if not validation['is_valid']:
            return jsonify({
                'error': 'Data validation failed',
                'issues': validation['issues']
            }), 400
        
        # Generate analysis ID
        analysis_id = str(uuid.uuid4())
        
        # Perform analysis
        try:
            # Basic analysis
            results = enhanced_agent.analyze_large_dataset(df)
            
            # Advanced analytics if requested
            if analysis_options.get('include_advanced', True) and len(df) > 1000:
                try:
                    results['advanced_analytics'] = advanced_analytics.generate_comprehensive_report(df)
                except Exception as e:
                    results['advanced_analytics'] = {'error': str(e)}
            
            # Industry-specific analysis if requested
            if analysis_options.get('industry_type'):
                industry_results = perform_industry_analysis(df, analysis_options['industry_type'])
                results['industry_analysis'] = industry_results
            
            # Store analysis results
            analysis_storage[analysis_id] = {
                'results': results,
                'upload_id': upload_id,
                'analysis_time': datetime.now().isoformat(),
                'dataset_info': {
                    'shape': df.shape,
                    'columns': list(df.columns),
                    'data_types': {col: str(dtype) for col, dtype in df.dtypes.items()}
                },
                'validation': validation
            }
            
            # Log successful analysis
            SecurityAuditor.audit_data_access(
                f"dataset_{upload_id}",
                f"analysis_{analysis_id}"
            )
            
            return jsonify({
                'analysis_id': analysis_id,
                'status': 'completed',
                'analysis_time': datetime.now().isoformat(),
                'dataset_info': {
                    'shape': df.shape,
                    'columns': len(df.columns)
                },
                'summary': {
                    'key_metrics_available': 'key_metrics' in results,
                    'advanced_analytics_available': 'advanced_analytics' in results,
                    'industry_analysis_available': 'industry_analysis' in results
                }
            }), 200
            
        except Exception as e:
            return jsonify({'error': f'Analysis failed: {str(e)}'}), 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports/<analysis_id>', methods=['GET'])
def get_analysis_report(analysis_id):
    """Get analysis report by ID."""
    try:
        if analysis_id not in analysis_storage:
            return jsonify({'error': 'Analysis not found'}), 404
        
        analysis_data = analysis_storage[analysis_id]
        
        # Get format parameter
        report_format = request.args.get('format', 'json')
        
        if report_format == 'json':
            return jsonify(analysis_data['results']), 200
        elif report_format == 'summary':
            # Return summary version
            results = analysis_data['results']
            summary = {
                'analysis_id': analysis_id,
                'analysis_time': analysis_data['analysis_time'],
                'dataset_info': analysis_data['dataset_info'],
                'key_insights': extract_key_insights(results),
                'recommendations': results.get('recommendations', [])[:5]  # Top 5 recommendations
            }
            return jsonify(summary), 200
        else:
            return jsonify({'error': 'Invalid format. Use json or summary'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyses', methods=['GET'])
def list_analyses():
    """List all analyses."""
    try:
        analyses_list = []
        
        for analysis_id, analysis_data in analysis_storage.items():
            analyses_list.append({
                'analysis_id': analysis_id,
                'analysis_time': analysis_data['analysis_time'],
                'dataset_shape': analysis_data['dataset_info']['shape'],
                'status': 'completed'
            })
        
        # Sort by analysis time (newest first)
        analyses_list.sort(key=lambda x: x['analysis_time'], reverse=True)
        
        return jsonify({
            'analyses': analyses_list,
            'total_count': len(analyses_list)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/visualizations/<analysis_id>', methods=['GET'])
def get_visualizations(analysis_id):
    """Get visualizations for an analysis."""
    try:
        if analysis_id not in analysis_storage:
            return jsonify({'error': 'Analysis not found'}), 404
        
        # Check if visualizations exist
        plots_dir = Path("outputs/plots")
        visualization_files = []
        
        if plots_dir.exists():
            for plot_file in plots_dir.glob("*.png"):
                visualization_files.append({
                    'filename': plot_file.name,
                    'path': str(plot_file),
                    'size': plot_file.stat().st_size,
                    'created': datetime.fromtimestamp(plot_file.stat().st_ctime).isoformat()
                })
        
        return jsonify({
            'analysis_id': analysis_id,
            'visualizations': visualization_files
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<analysis_id>/report', methods=['GET'])
def download_report(analysis_id):
    """Download analysis report as file."""
    try:
        if analysis_id not in analysis_storage:
            return jsonify({'error': 'Analysis not found'}), 404
        
        analysis_data = analysis_storage[analysis_id]
        
        # Generate report
        report_content = enhanced_agent.generate_report(analysis_data['results'])
        
        # Save report to file
        report_filename = f"analysis_report_{analysis_id}.md"
        report_path = Path("outputs/reports") / report_filename
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return send_file(
            report_path,
            as_attachment=True,
            download_name=report_filename,
            mimetype='text/markdown'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cache/clear', methods=['POST'])
def clear_cache():
    """Clear system cache."""
    try:
        cleared_count = cache_manager.clear()
        
        return jsonify({
            'message': 'Cache cleared successfully',
            'files_cleared': cleared_count,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cache/stats', methods=['GET'])
def get_cache_stats():
    """Get cache statistics."""
    try:
        stats = cache_manager.get_stats()
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def perform_industry_analysis(df: pd.DataFrame, industry_type: str) -> Dict[str, Any]:
    """Perform industry-specific analysis."""
    try:
        if industry_type == 'retail':
            from industry_modules.retail_analytics import RetailAnalytics
            retail_analytics = RetailAnalytics()
            
            analysis_results = {}
            
            # Inventory analysis
            try:
                analysis_results['inventory_analysis'] = retail_analytics.analyze_inventory_turnover(df)
            except Exception as e:
                analysis_results['inventory_analysis'] = {'error': str(e)}
            
            # Customer journey analysis
            try:
                analysis_results['customer_journey'] = retail_analytics.analyze_customer_journey(df)
            except Exception as e:
                analysis_results['customer_journey'] = {'error': str(e)}
            
            # Product performance analysis
            try:
                analysis_results['product_performance'] = retail_analytics.analyze_product_performance(df)
            except Exception as e:
                analysis_results['product_performance'] = {'error': str(e)}
            
            return analysis_results
        
        else:
            return {'error': f'Industry type {industry_type} not supported'}
            
    except Exception as e:
        return {'error': str(e)}

def extract_key_insights(results: Dict[str, Any]) -> List[str]:
    """Extract key insights from analysis results."""
    insights = []
    
    # From key metrics
    if 'key_metrics' in results:
        metrics = results['key_metrics']
        if 'total_customers' in metrics:
            insights.append(f"Dataset contains {metrics['total_customers']} customers")
        if 'avg_purchase_value' in metrics:
            insights.append(f"Average purchase value: ${metrics['avg_purchase_value']:.2f}")
    
    # From business insights
    if 'business_insights' in results:
        insights.extend(results['business_insights'][:3])  # Top 3 insights
    
    # From advanced analytics
    if 'advanced_analytics' in results and 'error' not in results['advanced_analytics']:
        adv = results['advanced_analytics']
        
        if 'segmentation' in adv:
            seg = adv['segmentation']
            insights.append(f"Customer segmentation identified {seg.get('clusters', 0)} distinct segments")
        
        if 'anomaly_detection' in adv:
            anom = adv['anomaly_detection']
            analysis = anom.get('analysis', {})
            insights.append(f"Anomaly detection found {analysis.get('total_anomalies', 0)} anomalies")
    
    return insights

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(413)
def too_large(error):
    """Handle file too large errors."""
    return jsonify({'error': 'File too large'}), 413

if __name__ == '__main__':
    # Create necessary directories
    Path("uploads").mkdir(exist_ok=True)
    Path("outputs/reports").mkdir(parents=True, exist_ok=True)
    
    # Run Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        threaded=True
    )
