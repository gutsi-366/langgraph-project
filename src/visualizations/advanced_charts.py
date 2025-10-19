"""
Advanced Visualization Module
============================

This module provides advanced visualization capabilities including:
- Interactive 3D visualizations
- Real-time dashboards
- Custom chart types
- Advanced statistical plots
- Interactive data exploration
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
try:
    import seaborn as sns  # Optional dependency
    SEABORN_AVAILABLE = True
except Exception:
    SEABORN_AVAILABLE = False
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from typing import Dict, List, Any, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

from utils import handle_errors, PerformanceTimer, ProjectError

class AdvancedVisualizations:
    """Advanced visualization engine for e-commerce analytics."""
    
    def __init__(self):
        self.chart_config = {
            'color_palette': 'viridis',
            'default_width': 1200,
            'default_height': 800,
            'dpi': 300,
            'style': 'whitegrid'
        }
        
        # Set up matplotlib style
        plt.style.use('seaborn-v0_8-whitegrid')
        if SEABORN_AVAILABLE:
            sns.set_palette(self.chart_config['color_palette'])
    
    @handle_errors
    def create_3d_customer_segmentation(self, df: pd.DataFrame, features: List[str] = None) -> go.Figure:
        """
        Create 3D customer segmentation visualization.
        
        Args:
            df: DataFrame with customer data
            features: List of features to use for 3D visualization
            
        Returns:
            Plotly 3D scatter plot figure
        """
        with PerformanceTimer("3D Customer Segmentation"):
            if features is None:
                features = ['age', 'total_purchases', 'browsing_time_minutes']
            
            # Ensure features exist in dataframe
            available_features = [f for f in features if f in df.columns]
            if len(available_features) < 3:
                raise ProjectError(f"Need at least 3 features. Available: {available_features}")
            
            # Use first 3 available features
            x_feat, y_feat, z_feat = available_features[:3]
            
            # Create 3D scatter plot
            fig = go.Figure(data=go.Scatter3d(
                x=df[x_feat],
                y=df[y_feat],
                z=df[z_feat],
                mode='markers',
                marker=dict(
                    size=8,
                    color=df.get('customer_lifetime_value', df.get('total_purchases', 0)),
                    colorscale='Viridis',
                    opacity=0.8,
                    colorbar=dict(title="CLV" if 'customer_lifetime_value' in df.columns else "Purchases")
                ),
                text=[f"Customer {i}" for i in df.index],
                hovertemplate=f'<b>%{{text}}</b><br>' +
                             f'{x_feat}: %{{x}}<br>' +
                             f'{y_feat}: %{{y}}<br>' +
                             f'{z_feat}: %{{z}}<extra></extra>'
            ))
            
            fig.update_layout(
                title='3D Customer Segmentation Analysis',
                scene=dict(
                    xaxis_title=x_feat.replace('_', ' ').title(),
                    yaxis_title=y_feat.replace('_', ' ').title(),
                    zaxis_title=z_feat.replace('_', ' ').title()
                ),
                width=self.chart_config['default_width'],
                height=self.chart_config['default_height']
            )
            
            return fig
    
    @handle_errors
    def create_interactive_dashboard(self, df: pd.DataFrame) -> go.Figure:
        """
        Create interactive dashboard with multiple charts.
        
        Args:
            df: DataFrame with customer data
            
        Returns:
            Plotly figure with subplots
        """
        with PerformanceTimer("Interactive Dashboard"):
            # Create subplots
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Customer Distribution by Segment', 
                               'Purchase Value Distribution',
                               'Age vs Lifetime Value', 
                               'Browsing Time Analysis'),
                specs=[[{"type": "pie"}, {"type": "histogram"}],
                       [{"type": "scatter"}, {"type": "box"}]]
            )
            
            # 1. Customer distribution by segment
            if 'customer_segment' in df.columns:
                segment_counts = df['customer_segment'].value_counts()
                fig.add_trace(
                    go.Pie(labels=segment_counts.index, values=segment_counts.values, name="Segments"),
                    row=1, col=1
                )
            
            # 2. Purchase value distribution
            if 'avg_order_value' in df.columns:
                fig.add_trace(
                    go.Histogram(x=df['avg_order_value'], name="Order Values", nbinsx=30),
                    row=1, col=2
                )
            
            # 3. Age vs Lifetime Value scatter
            if 'age' in df.columns and 'customer_lifetime_value' in df.columns:
                fig.add_trace(
                    go.Scatter(
                        x=df['age'], 
                        y=df['customer_lifetime_value'],
                        mode='markers',
                        name="Age vs CLV",
                        marker=dict(size=6, opacity=0.6)
                    ),
                    row=2, col=1
                )
            
            # 4. Browsing time by segment
            if 'browsing_time_minutes' in df.columns and 'customer_segment' in df.columns:
                for segment in df['customer_segment'].unique():
                    segment_data = df[df['customer_segment'] == segment]['browsing_time_minutes']
                    fig.add_trace(
                        go.Box(y=segment_data, name=segment, showlegend=False),
                        row=2, col=2
                    )
            
            fig.update_layout(
                title_text="E-commerce Analytics Dashboard",
                showlegend=True,
                width=self.chart_config['default_width'],
                height=self.chart_config['default_height']
            )
            
            return fig
    
    @handle_errors
    def create_heatmap_correlation(self, df: pd.DataFrame, method: str = 'pearson') -> go.Figure:
        """
        Create advanced correlation heatmap.
        
        Args:
            df: DataFrame with numeric data
            method: Correlation method ('pearson', 'spearman', 'kendall')
            
        Returns:
            Plotly heatmap figure
        """
        with PerformanceTimer("Correlation Heatmap"):
            # Select numeric columns
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            
            if len(numeric_cols) < 2:
                raise ProjectError("Need at least 2 numeric columns for correlation")
            
            # Calculate correlation matrix
            corr_matrix = df[numeric_cols].corr(method=method)
            
            # Create heatmap
            fig = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='RdBu',
                zmid=0,
                text=np.round(corr_matrix.values, 2),
                texttemplate="%{text}",
                textfont={"size": 10},
                hoverongaps=False
            ))
            
            fig.update_layout(
                title=f'{method.title()} Correlation Heatmap',
                width=self.chart_config['default_width'],
                height=self.chart_config['default_height'],
                xaxis_title="Features",
                yaxis_title="Features"
            )
            
            return fig
    
    @handle_errors
    def create_advanced_time_series(self, df: pd.DataFrame, date_col: str = None) -> go.Figure:
        """
        Create advanced time series visualization.
        
        Args:
            df: DataFrame with time series data
            date_col: Name of date column
            
        Returns:
            Plotly time series figure
        """
        with PerformanceTimer("Advanced Time Series"):
            # Find date column if not specified
            if date_col is None:
                date_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
                if date_cols:
                    date_col = date_cols[0]
                else:
                    raise ProjectError("No date column found")
            
            if date_col not in df.columns:
                raise ProjectError(f"Date column '{date_col}' not found")
            
            # Convert to datetime
            df[date_col] = pd.to_datetime(df[date_col])
            
            # Create time series plot
            fig = go.Figure()
            
            # Add multiple metrics if available
            metrics_to_plot = []
            if 'total_purchases' in df.columns:
                metrics_to_plot.append('total_purchases')
            if 'customer_lifetime_value' in df.columns:
                metrics_to_plot.append('customer_lifetime_value')
            if 'avg_order_value' in df.columns:
                metrics_to_plot.append('avg_order_value')
            
            # Group by date and aggregate
            for metric in metrics_to_plot:
                time_series = df.groupby(df[date_col].dt.date)[metric].mean()
                
                fig.add_trace(go.Scatter(
                    x=time_series.index,
                    y=time_series.values,
                    mode='lines+markers',
                    name=metric.replace('_', ' ').title(),
                    line=dict(width=3)
                ))
            
            # Add trend lines
            for metric in metrics_to_plot:
                time_series = df.groupby(df[date_col].dt.date)[metric].mean()
                if len(time_series) > 1:
                    z = np.polyfit(range(len(time_series)), time_series.values, 1)
                    p = np.poly1d(z)
                    
                    fig.add_trace(go.Scatter(
                        x=time_series.index,
                        y=p(range(len(time_series))),
                        mode='lines',
                        name=f'{metric.replace("_", " ").title()} Trend',
                        line=dict(dash='dash', width=2),
                        opacity=0.7
                    ))
            
            fig.update_layout(
                title='Advanced Time Series Analysis',
                xaxis_title='Date',
                yaxis_title='Value',
                hovermode='x unified',
                width=self.chart_config['default_width'],
                height=self.chart_config['default_height']
            )
            
            return fig
    
    @handle_errors
    def create_advanced_distribution_plots(self, df: pd.DataFrame, column: str) -> go.Figure:
        """
        Create advanced distribution plots.
        
        Args:
            df: DataFrame with data
            column: Column to analyze distribution
            
        Returns:
            Plotly figure with distribution analysis
        """
        with PerformanceTimer("Advanced Distribution Plots"):
            if column not in df.columns:
                raise ProjectError(f"Column '{column}' not found")
            
            # Create subplots
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Histogram', 'Box Plot', 'Violin Plot', 'Q-Q Plot'),
                specs=[[{"type": "histogram"}, {"type": "box"}],
                       [{"type": "violin"}, {"type": "scatter"}]]
            )
            
            data = df[column].dropna()
            
            # 1. Histogram
            fig.add_trace(
                go.Histogram(x=data, name="Distribution", nbinsx=30),
                row=1, col=1
            )
            
            # 2. Box plot
            fig.add_trace(
                go.Box(y=data, name="Box Plot", showlegend=False),
                row=1, col=2
            )
            
            # 3. Violin plot
            fig.add_trace(
                go.Violin(y=data, name="Violin Plot", showlegend=False),
                row=2, col=1
            )
            
            # 4. Q-Q plot (simplified version)
            sorted_data = np.sort(data)
            n = len(sorted_data)
            theoretical_quantiles = np.linspace(0, 1, n)
            
            fig.add_trace(
                go.Scatter(
                    x=theoretical_quantiles,
                    y=sorted_data,
                    mode='markers',
                    name="Q-Q Plot",
                    showlegend=False
                ),
                row=2, col=2
            )
            
            fig.update_layout(
                title=f'Advanced Distribution Analysis: {column.replace("_", " ").title()}',
                showlegend=False,
                width=self.chart_config['default_width'],
                height=self.chart_config['default_height']
            )
            
            return fig
    
    @handle_errors
    def create_network_analysis(self, df: pd.DataFrame, 
                               source_col: str = 'user_id', 
                               target_col: str = 'preferred_category') -> go.Figure:
        """
        Create network analysis visualization.
        
        Args:
            df: DataFrame with network data
            source_col: Source node column
            target_col: Target node column
            
        Returns:
            Plotly network figure
        """
        with PerformanceTimer("Network Analysis"):
            if source_col not in df.columns or target_col not in df.columns:
                raise ProjectError(f"Required columns not found: {source_col}, {target_col}")
            
            # Create edge list
            edges = df[[source_col, target_col]].dropna()
            edge_counts = edges.groupby([source_col, target_col]).size().reset_index(name='weight')
            
            # Get unique nodes
            all_nodes = list(set(edge_counts[source_col].unique()) | set(edge_counts[target_col].unique()))
            
            # Create node positions (simplified layout)
            n_nodes = len(all_nodes)
            angles = np.linspace(0, 2*np.pi, n_nodes, endpoint=False)
            x_pos = np.cos(angles)
            y_pos = np.sin(angles)
            
            node_positions = {node: (x, y) for node, x, y in zip(all_nodes, x_pos, y_pos)}
            
            # Create edges
            edge_x = []
            edge_y = []
            edge_info = []
            
            for _, row in edge_counts.iterrows():
                x0, y0 = node_positions[row[source_col]]
                x1, y1 = node_positions[row[target_col]]
                
                edge_x.extend([x0, x1, None])
                edge_y.extend([y0, y1, None])
                edge_info.append(f"{row[source_col]} → {row[target_col]}<br>Weight: {row['weight']}")
            
            # Create edge trace
            edge_trace = go.Scatter(
                x=edge_x, y=edge_y,
                line=dict(width=2, color='#888'),
                hoverinfo='none',
                mode='lines'
            )
            
            # Create node trace
            node_x = [node_positions[node][0] for node in all_nodes]
            node_y = [node_positions[node][1] for node in all_nodes]
            
            node_trace = go.Scatter(
                x=node_x, y=node_y,
                mode='markers+text',
                hoverinfo='text',
                text=all_nodes,
                textposition="middle center",
                marker=dict(
                    size=20,
                    color='lightblue',
                    line=dict(width=2, color='darkblue')
                )
            )
            
            # Create figure
            fig = go.Figure(data=[edge_trace, node_trace],
                           layout=go.Layout(
                               title='Network Analysis',
                               titlefont_size=16,
                               showlegend=False,
                               hovermode='closest',
                               margin=dict(b=20,l=5,r=5,t=40),
                               annotations=[ dict(
                                   text="Network visualization of customer-category relationships",
                                   showarrow=False,
                                   xref="paper", yref="paper",
                                   x=0.005, y=-0.002,
                                   xanchor="left", yanchor="bottom",
                                   font=dict(color="gray", size=12)
                               )],
                               xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                               yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                               width=self.chart_config['default_width'],
                               height=self.chart_config['default_height']
                           ))
            
            return fig
    
    @handle_errors
    def create_advanced_statistical_plots(self, df: pd.DataFrame) -> Dict[str, go.Figure]:
        """
        Create advanced statistical visualizations.
        
        Args:
            df: DataFrame with data
            
        Returns:
            Dictionary of statistical plot figures
        """
        with PerformanceTimer("Advanced Statistical Plots"):
            plots = {}
            
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            
            if len(numeric_cols) < 2:
                raise ProjectError("Need at least 2 numeric columns for statistical analysis")
            
            # 1. Pair plot (simplified)
            if len(numeric_cols) >= 2:
                x_col, y_col = numeric_cols[0], numeric_cols[1]
                
                fig = px.scatter_matrix(
                    df[numeric_cols[:4]],  # Use first 4 numeric columns
                    dimensions=numeric_cols[:4],
                    color=df.get('customer_segment', None),
                    title="Pair Plot Analysis"
                )
                
                plots['pair_plot'] = fig
            
            # 2. Statistical summary plot
            summary_stats = df[numeric_cols].describe()
            
            fig = go.Figure(data=go.Heatmap(
                z=summary_stats.values,
                x=summary_stats.columns,
                y=summary_stats.index,
                colorscale='Blues',
                text=np.round(summary_stats.values, 2),
                texttemplate="%{text}",
                textfont={"size": 10}
            ))
            
            fig.update_layout(
                title='Statistical Summary Heatmap',
                width=self.chart_config['default_width'],
                height=400
            )
            
            plots['statistical_summary'] = fig
            
            # 3. Distribution comparison
            if 'customer_segment' in df.columns and len(numeric_cols) > 0:
                metric_col = numeric_cols[0]
                
                fig = go.Figure()
                
                for segment in df['customer_segment'].unique():
                    segment_data = df[df['customer_segment'] == segment][metric_col].dropna()
                    
                    fig.add_trace(go.Violin(
                        y=segment_data,
                        name=segment,
                        box_visible=True,
                        meanline_visible=True
                    ))
                
                fig.update_layout(
                    title=f'{metric_col.replace("_", " ").title()} Distribution by Segment',
                    yaxis_title=metric_col.replace('_', ' ').title(),
                    width=self.chart_config['default_width'],
                    height=self.chart_config['default_height']
                )
                
                plots['distribution_comparison'] = fig
            
            return plots
    
    def save_plot(self, fig: go.Figure, filename: str, format: str = 'png') -> str:
        """
        Save plot to file.
        
        Args:
            fig: Plotly figure
            filename: Output filename
            format: Output format ('png', 'html', 'pdf')
            
        Returns:
            Path to saved file
        """
        output_dir = Path("outputs/plots")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = output_dir / f"{filename}.{format}"
        
        if format == 'html':
            fig.write_html(str(file_path))
        elif format == 'png':
            fig.write_image(str(file_path), 
                          width=self.chart_config['default_width'],
                          height=self.chart_config['default_height'])
        elif format == 'pdf':
            fig.write_image(str(file_path), 
                          width=self.chart_config['default_width'],
                          height=self.chart_config['default_height'])
        else:
            raise ProjectError(f"Unsupported format: {format}")
        
        return str(file_path)
    
    def create_visualization_report(self, df: pd.DataFrame) -> Dict[str, str]:
        """
        Create comprehensive visualization report.
        
        Args:
            df: DataFrame to visualize
            
        Returns:
            Dictionary mapping plot names to file paths
        """
        report_plots = {}
        
        try:
            # 3D segmentation
            fig_3d = self.create_3d_customer_segmentation(df)
            report_plots['3d_segmentation'] = self.save_plot(fig_3d, '3d_customer_segmentation')
            
        except Exception as e:
            print(f"3D segmentation failed: {e}")
        
        try:
            # Interactive dashboard
            fig_dashboard = self.create_interactive_dashboard(df)
            report_plots['interactive_dashboard'] = self.save_plot(fig_dashboard, 'interactive_dashboard')
            
        except Exception as e:
            print(f"Dashboard creation failed: {e}")
        
        try:
            # Correlation heatmap
            fig_heatmap = self.create_heatmap_correlation(df)
            report_plots['correlation_heatmap'] = self.save_plot(fig_heatmap, 'correlation_heatmap')
            
        except Exception as e:
            print(f"Heatmap creation failed: {e}")
        
        try:
            # Statistical plots
            stat_plots = self.create_advanced_statistical_plots(df)
            for name, fig in stat_plots.items():
                report_plots[f'statistical_{name}'] = self.save_plot(fig, f'statistical_{name}')
                
        except Exception as e:
            print(f"Statistical plots failed: {e}")
        
        return report_plots

# Global visualization instance
advanced_viz = AdvancedVisualizations()

def create_advanced_visualizations(df: pd.DataFrame) -> Dict[str, str]:
    """Create all advanced visualizations for a dataset."""
    return advanced_viz.create_visualization_report(df)
