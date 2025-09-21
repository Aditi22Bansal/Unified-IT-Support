import React, { useState, useEffect } from 'react';
import { RefreshCw, AlertTriangle, Activity } from 'lucide-react';
import { dashboardAPI } from '../../services/api';
import SystemHealthCards from './SystemHealthCards';
import MetricsCharts from './MetricsCharts';
import SystemLogs from './SystemLogs';
import LoadingSpinner from '../common/LoadingSpinner';
import toast from 'react-hot-toast';

const OperationsDashboard = () => {
  const [systemHealth, setSystemHealth] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [healthData, metricsData, logsData] = await Promise.all([
        dashboardAPI.getSystemHealth(),
        dashboardAPI.getDashboardMetrics(),
        dashboardAPI.getSystemLogs({ limit: 50 })
      ]);

      setSystemHealth(healthData);
      setMetrics(metricsData);
      setLogs(logsData.logs || logsData || []);
    } catch (error) {
      console.error('Failed to fetch operations data:', error);
      toast.error('Failed to load operations data');
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    await fetchData();
    setRefreshing(false);
    toast.success('Data refreshed');
  };

  if (loading) {
    return <LoadingSpinner text="Loading operations data..." />;
  }

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Operations Dashboard</h1>
          <p className="mt-1 text-sm text-gray-500">
            Monitor system health, metrics, and logs
          </p>
        </div>
        <button
          onClick={handleRefresh}
          disabled={refreshing}
          className="btn btn-secondary flex items-center"
        >
          <RefreshCw className={`h-4 w-4 mr-2 ${refreshing ? 'animate-spin' : ''}`} />
          Refresh
        </button>
      </div>

      {/* System Health Cards */}
      {systemHealth && <SystemHealthCards data={systemHealth} />}

      {/* Metrics Charts */}
      {metrics && <MetricsCharts data={metrics} />}

      {/* System Logs */}
      <SystemLogs logs={logs} />
    </div>
  );
};

export default OperationsDashboard;

