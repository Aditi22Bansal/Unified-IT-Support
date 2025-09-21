import React from 'react';
import { useDashboard } from '../../contexts/DashboardContext';
import SystemHealthCards from './SystemHealthCards';
import MetricsCharts from './MetricsCharts';
import RecentAlerts from './RecentAlerts';
import RecentTickets from './RecentTickets';
import LoadingSpinner from '../common/LoadingSpinner';

const Dashboard = () => {
  const { systemHealth, metrics, alerts, tickets, loading } = useDashboard();

  if (loading) {
    return <LoadingSpinner />;
  }

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-1 text-sm text-gray-500">
          Overview of your IT support system
        </p>
      </div>

      {/* System Health Cards */}
      {systemHealth && <SystemHealthCards data={systemHealth} />}

      {/* Metrics Charts */}
      {metrics && <MetricsCharts data={metrics} />}

      {/* Recent Alerts and Tickets */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <RecentAlerts alerts={alerts} />
        <RecentTickets tickets={tickets} />
      </div>
    </div>
  );
};

export default Dashboard;

