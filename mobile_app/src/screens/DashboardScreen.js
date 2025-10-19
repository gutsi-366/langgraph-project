/**
 * Dashboard Screen - Real-time Analytics Dashboard
 * ===============================================
 * 
 * Features:
 * - Real-time metrics display
 * - Interactive charts
 * - Push notifications
 * - Offline data sync
 */

import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  RefreshControl,
  Dimensions,
  Alert,
  TouchableOpacity
} from 'react-native';
import {
  Card,
  Title,
  Paragraph,
  FAB,
  Chip,
  ActivityIndicator,
  Surface
} from 'react-native-paper';
import { LineChart, BarChart, PieChart } from 'react-native-chart-kit';
import { Ionicons } from '@expo/vector-icons';

import { ApiService } from '../services/ApiService';
import { NotificationService } from '../services/NotificationService';
import { DataCache } from '../services/DataCache';

const { width: screenWidth } = Dimensions.get('window');

const DashboardScreen = ({ navigation }) => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [lastUpdate, setLastUpdate] = useState(null);
  const [realTimeMetrics, setRealTimeMetrics] = useState({});
  
  const intervalRef = useRef(null);

  useEffect(() => {
    loadDashboardData();
    startRealTimeUpdates();
    
    // Set up push notifications for insights
    NotificationService.requestPermissions();
    NotificationService.setupInsightNotifications();

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      
      // Try to load from cache first
      const cachedData = await DataCache.get('dashboard_data');
      if (cachedData) {
        setDashboardData(cachedData);
        setLastUpdate(new Date().toLocaleTimeString());
      }

      // Fetch fresh data from API
      const response = await ApiService.getDashboardData();
      
      if (response.success) {
        setDashboardData(response.data);
        setLastUpdate(new Date().toLocaleTimeString());
        
        // Cache the data
        await DataCache.set('dashboard_data', response.data);
        
        // Check for new insights and send notifications
        checkForNewInsights(response.data);
      }
    } catch (error) {
      console.error('Dashboard load error:', error);
      Alert.alert('Error', 'Failed to load dashboard data');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const startRealTimeUpdates = () => {
    // Update real-time metrics every 30 seconds
    intervalRef.current = setInterval(async () => {
      try {
        const metrics = await ApiService.getRealTimeMetrics();
        setRealTimeMetrics(metrics);
      } catch (error) {
        console.error('Real-time update error:', error);
      }
    }, 30000);
  };

  const checkForNewInsights = (data) => {
    // Check for significant changes and send notifications
    const insights = data.insights || [];
    
    insights.forEach(insight => {
      if (insight.priority === 'high') {
        NotificationService.sendNotification(
          'New Insight',
          insight.message,
          { insight_id: insight.id }
        );
      }
    });
  };

  const onRefresh = () => {
    setRefreshing(true);
    loadDashboardData();
  };

  const renderMetricCard = (title, value, change, icon, color = '#2196F3') => (
    <Card style={[styles.metricCard, { borderLeftColor: color }]}>
      <Card.Content>
        <View style={styles.metricHeader}>
          <Ionicons name={icon} size={24} color={color} />
          <Text style={styles.metricTitle}>{title}</Text>
        </View>
        <Text style={[styles.metricValue, { color }]}>{value}</Text>
        {change && (
          <Text style={[
            styles.metricChange,
            { color: change > 0 ? '#4CAF50' : '#F44336' }
          ]}>
            {change > 0 ? '↗' : '↘'} {Math.abs(change)}%
          </Text>
        )}
      </Card.Content>
    </Card>
  );

  const renderChart = (type, data, title) => {
    if (!data || !data.length) return null;

    const chartConfig = {
      backgroundColor: '#ffffff',
      backgroundGradientFrom: '#ffffff',
      backgroundGradientTo: '#ffffff',
      decimalPlaces: 0,
      color: (opacity = 1) => `rgba(33, 150, 243, ${opacity})`,
      labelColor: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
      style: {
        borderRadius: 16
      },
      propsForDots: {
        r: "6",
        strokeWidth: "2",
        stroke: "#2196F3"
      }
    };

    switch (type) {
      case 'line':
        return (
          <Card style={styles.chartCard}>
            <Card.Content>
              <Title>{title}</Title>
              <LineChart
                data={data}
                width={screenWidth - 40}
                height={220}
                chartConfig={chartConfig}
                bezier
                style={styles.chart}
              />
            </Card.Content>
          </Card>
        );
      
      case 'bar':
        return (
          <Card style={styles.chartCard}>
            <Card.Content>
              <Title>{title}</Title>
              <BarChart
                data={data}
                width={screenWidth - 40}
                height={220}
                chartConfig={chartConfig}
                style={styles.chart}
              />
            </Card.Content>
          </Card>
        );
      
      case 'pie':
        return (
          <Card style={styles.chartCard}>
            <Card.Content>
              <Title>{title}</Title>
              <PieChart
                data={data}
                width={screenWidth - 40}
                height={220}
                chartConfig={chartConfig}
                accessor="value"
                backgroundColor="transparent"
                paddingLeft="15"
                style={styles.chart}
              />
            </Card.Content>
          </Card>
        );
      
      default:
        return null;
    }
  };

  const renderRealTimeMetrics = () => (
    <Card style={styles.realtimeCard}>
      <Card.Content>
        <Title>🔴 Real-Time Metrics</Title>
        <View style={styles.realtimeGrid}>
          <View style={styles.realtimeItem}>
            <Text style={styles.realtimeLabel}>Active Users</Text>
            <Text style={styles.realtimeValue}>
              {realTimeMetrics.active_users || 0}
            </Text>
          </View>
          <View style={styles.realtimeItem}>
            <Text style={styles.realtimeLabel}>Processing Rate</Text>
            <Text style={styles.realtimeValue}>
              {realTimeMetrics.processing_rate || 0}/min
            </Text>
          </View>
          <View style={styles.realtimeItem}>
            <Text style={styles.realtimeLabel}>Cache Hit Rate</Text>
            <Text style={styles.realtimeValue}>
              {((realTimeMetrics.cache_hit_rate || 0) * 100).toFixed(1)}%
            </Text>
          </View>
          <View style={styles.realtimeItem}>
            <Text style={styles.realtimeLabel}>System Status</Text>
            <Chip 
              icon={realTimeMetrics.status === 'running' ? 'check' : 'alert'}
              style={[
                styles.statusChip,
                { backgroundColor: realTimeMetrics.status === 'running' ? '#4CAF50' : '#F44336' }
              ]}
            >
              {realTimeMetrics.status === 'running' ? 'Running' : 'Stopped'}
            </Chip>
          </View>
        </View>
      </Card.Content>
    </Card>
  );

  if (loading && !dashboardData) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#2196F3" />
        <Text style={styles.loadingText}>Loading Dashboard...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <ScrollView
        style={styles.scrollView}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={onRefresh}
            colors={['#2196F3']}
          />
        }
      >
        {/* Real-time Metrics */}
        {renderRealTimeMetrics()}

        {/* Key Metrics */}
        <View style={styles.metricsGrid}>
          {renderMetricCard(
            'Total Customers',
            dashboardData?.total_customers || '0',
            dashboardData?.customer_growth || 0,
            'people',
            '#4CAF50'
          )}
          {renderMetricCard(
            'Revenue',
            `$${dashboardData?.total_revenue || '0'}`,
            dashboardData?.revenue_growth || 0,
            'trending-up',
            '#FF9800'
          )}
          {renderMetricCard(
            'Conversion Rate',
            `${dashboardData?.conversion_rate || '0'}%`,
            dashboardData?.conversion_change || 0,
            'analytics',
            '#9C27B0'
          )}
          {renderMetricCard(
            'Avg Order Value',
            `$${dashboardData?.avg_order_value || '0'}`,
            dashboardData?.aov_change || 0,
            'card',
            '#2196F3'
          )}
        </View>

        {/* Charts */}
        {dashboardData?.charts?.sales_trend && 
          renderChart('line', dashboardData.charts.sales_trend, 'Sales Trend')}
        
        {dashboardData?.charts?.customer_segments && 
          renderChart('pie', dashboardData.charts.customer_segments, 'Customer Segments')}
        
        {dashboardData?.charts?.category_performance && 
          renderChart('bar', dashboardData.charts.category_performance, 'Category Performance')}

        {/* Insights */}
        {dashboardData?.insights && dashboardData.insights.length > 0 && (
          <Card style={styles.insightsCard}>
            <Card.Content>
              <Title>💡 Key Insights</Title>
              {dashboardData.insights.map((insight, index) => (
                <View key={index} style={styles.insightItem}>
                  <Ionicons 
                    name={insight.priority === 'high' ? 'alert-circle' : 'information-circle'} 
                    size={20} 
                    color={insight.priority === 'high' ? '#F44336' : '#2196F3'} 
                  />
                  <Text style={styles.insightText}>{insight.message}</Text>
                </View>
              ))}
            </Card.Content>
          </Card>
        )}

        {/* Last Update */}
        {lastUpdate && (
          <Text style={styles.lastUpdate}>
            Last updated: {lastUpdate}
          </Text>
        )}
      </ScrollView>

      {/* Floating Action Button */}
      <FAB
        style={styles.fab}
        icon="refresh"
        onPress={onRefresh}
        label="Refresh"
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  scrollView: {
    flex: 1,
    padding: 16,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
    color: '#666',
  },
  realtimeCard: {
    marginBottom: 16,
    elevation: 4,
  },
  realtimeGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  realtimeItem: {
    width: '48%',
    marginBottom: 16,
  },
  realtimeLabel: {
    fontSize: 12,
    color: '#666',
    marginBottom: 4,
  },
  realtimeValue: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
  },
  statusChip: {
    alignSelf: 'flex-start',
  },
  metricsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    marginBottom: 16,
  },
  metricCard: {
    width: '48%',
    marginBottom: 16,
    elevation: 2,
    borderLeftWidth: 4,
  },
  metricHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  metricTitle: {
    fontSize: 14,
    color: '#666',
    marginLeft: 8,
    flex: 1,
  },
  metricValue: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 4,
  },
  metricChange: {
    fontSize: 12,
    fontWeight: '600',
  },
  chartCard: {
    marginBottom: 16,
    elevation: 4,
  },
  chart: {
    marginVertical: 8,
    borderRadius: 16,
  },
  insightsCard: {
    marginBottom: 16,
    elevation: 4,
  },
  insightItem: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: 12,
  },
  insightText: {
    flex: 1,
    marginLeft: 12,
    fontSize: 14,
    color: '#333',
  },
  lastUpdate: {
    textAlign: 'center',
    fontSize: 12,
    color: '#999',
    marginBottom: 80,
  },
  fab: {
    position: 'absolute',
    margin: 16,
    right: 0,
    bottom: 0,
    backgroundColor: '#2196F3',
  },
});

export default DashboardScreen;
