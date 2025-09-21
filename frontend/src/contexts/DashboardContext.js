import React, { createContext, useContext, useState, useEffect } from 'react';
import { dashboardAPI } from '../services/api';

const DashboardContext = createContext();

export function useDashboard() {
  const context = useContext(DashboardContext);
  if (!context) {
    throw new Error('useDashboard must be used within a DashboardProvider');
  }
  return context;
}

export function DashboardProvider({ children }) {
  const [systemHealth, setSystemHealth] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
    // Set up polling for real-time updates
    const interval = setInterval(fetchDashboardData, 30000); // 30 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const [healthData, metricsData] = await Promise.all([
        dashboardAPI.getSystemHealth(),
        dashboardAPI.getDashboardMetrics()
      ]);

      setSystemHealth(healthData);
      setMetrics(metricsData);
      setAlerts(metricsData.recent_alerts || []);
      setTickets(metricsData.recent_tickets || []);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const refreshData = () => {
    fetchDashboardData();
  };

  const value = {
    systemHealth,
    metrics,
    alerts,
    tickets,
    loading,
    refreshData
  };

  return (
    <DashboardContext.Provider value={value}>
      {children}
    </DashboardContext.Provider>
  );
}

