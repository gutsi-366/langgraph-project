/**
 * LangGraph AI E-commerce Analytics Mobile App
 * ===========================================
 * 
 * Main React Native application with:
 * - Real-time analytics dashboard
 * - Interactive charts and visualizations
 * - Push notifications for insights
 * - Offline data synchronization
 * - API integration with backend
 */

import React, { useState, useEffect } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import { Provider as PaperProvider } from 'react-native-paper';
import { StatusBar } from 'expo-status-bar';
import { Ionicons } from '@expo/vector-icons';

// Import screens
import DashboardScreen from './src/screens/DashboardScreen';
import AnalyticsScreen from './src/screens/AnalyticsScreen';
import ReportsScreen from './src/screens/ReportsScreen';
import SettingsScreen from './src/screens/SettingsScreen';
import LoginScreen from './src/screens/LoginScreen';
import ReportDetailScreen from './src/screens/ReportDetailScreen';

// Import services
import { AuthService } from './src/services/AuthService';
import { ApiService } from './src/services/ApiService';
import { NotificationService } from './src/services/NotificationService';

const Tab = createBottomTabNavigator();
const Stack = createStackNavigator();

// Main Tab Navigator
function MainTabs() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName;

          if (route.name === 'Dashboard') {
            iconName = focused ? 'home' : 'home-outline';
          } else if (route.name === 'Analytics') {
            iconName = focused ? 'analytics' : 'analytics-outline';
          } else if (route.name === 'Reports') {
            iconName = focused ? 'document-text' : 'document-text-outline';
          } else if (route.name === 'Settings') {
            iconName = focused ? 'settings' : 'settings-outline';
          }

          return <Ionicons name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: '#2196F3',
        tabBarInactiveTintColor: 'gray',
        headerStyle: {
          backgroundColor: '#2196F3',
        },
        headerTintColor: '#fff',
        headerTitleStyle: {
          fontWeight: 'bold',
        },
      })}
    >
      <Tab.Screen 
        name="Dashboard" 
        component={DashboardScreen}
        options={{ title: '📊 Dashboard' }}
      />
      <Tab.Screen 
        name="Analytics" 
        component={AnalyticsScreen}
        options={{ title: '📈 Analytics' }}
      />
      <Tab.Screen 
        name="Reports" 
        component={ReportsScreen}
        options={{ title: '📋 Reports' }}
      />
      <Tab.Screen 
        name="Settings" 
        component={SettingsScreen}
        options={{ title: '⚙️ Settings' }}
      />
    </Tab.Navigator>
  );
}

// Main App Component
export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    initializeApp();
  }, []);

  const initializeApp = async () => {
    try {
      // Initialize services
      await AuthService.initialize();
      await ApiService.initialize();
      await NotificationService.initialize();

      // Check authentication status
      const authStatus = await AuthService.checkAuthStatus();
      setIsAuthenticated(authStatus);

    } catch (error) {
      console.error('App initialization error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogin = (token) => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    AuthService.logout();
  };

  if (isLoading) {
    return (
      <PaperProvider>
        <StatusBar style="auto" />
        {/* Loading screen component */}
      </PaperProvider>
    );
  }

  return (
    <PaperProvider>
      <NavigationContainer>
        <StatusBar style="auto" />
        {isAuthenticated ? (
          <Stack.Navigator>
            <Stack.Screen 
              name="MainTabs" 
              component={MainTabs}
              options={{ headerShown: false }}
            />
            <Stack.Screen 
              name="ReportDetail" 
              component={ReportDetailScreen}
              options={{ 
                title: 'Report Details',
                headerStyle: { backgroundColor: '#2196F3' },
                headerTintColor: '#fff'
              }}
            />
          </Stack.Navigator>
        ) : (
          <Stack.Navigator>
            <Stack.Screen 
              name="Login" 
              options={{ headerShown: false }}
            >
              {(props) => (
                <LoginScreen 
                  {...props} 
                  onLogin={handleLogin}
                />
              )}
            </Stack.Screen>
          </Stack.Navigator>
        )}
      </NavigationContainer>
    </PaperProvider>
  );
}
