import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  AreaChart,
  Area
} from 'recharts';

const MetricsCharts = ({ data = {} }) => {
  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const formatValue = (value) => {
    return `${(value || 0).toFixed(1)}%`;
  };

  return (
    <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
      {/* CPU Usage Chart */}
      <div className="card p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">CPU Usage</h3>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data.cpu_history || []}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="timestamp"
                tickFormatter={formatTime}
                tick={{ fontSize: 12 }}
              />
              <YAxis
                domain={[0, 100]}
                tick={{ fontSize: 12 }}
              />
              <Tooltip
                labelFormatter={(value) => formatTime(value)}
                formatter={(value) => [formatValue(value), 'CPU Usage']}
              />
              <Area
                type="monotone"
                dataKey="value"
                stroke="#3b82f6"
                fill="#3b82f6"
                fillOpacity={0.1}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Memory Usage Chart */}
      <div className="card p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Memory Usage</h3>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data.memory_history || []}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="timestamp"
                tickFormatter={formatTime}
                tick={{ fontSize: 12 }}
              />
              <YAxis
                domain={[0, 100]}
                tick={{ fontSize: 12 }}
              />
              <Tooltip
                labelFormatter={(value) => formatTime(value)}
                formatter={(value) => [formatValue(value), 'Memory Usage']}
              />
              <Area
                type="monotone"
                dataKey="value"
                stroke="#10b981"
                fill="#10b981"
                fillOpacity={0.1}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Disk Usage Chart */}
      <div className="card p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Disk Usage</h3>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data.disk_history || []}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="timestamp"
                tickFormatter={formatTime}
                tick={{ fontSize: 12 }}
              />
              <YAxis
                domain={[0, 100]}
                tick={{ fontSize: 12 }}
              />
              <Tooltip
                labelFormatter={(value) => formatTime(value)}
                formatter={(value) => [formatValue(value), 'Disk Usage']}
              />
              <Area
                type="monotone"
                dataKey="value"
                stroke="#f59e0b"
                fill="#f59e0b"
                fillOpacity={0.1}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* System Overview */}
      <div className="card p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">System Overview</h3>
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Current CPU</span>
            <span className="text-sm font-medium">
              {((data.system_health || {}).cpu_usage || 0).toFixed(1)}%
            </span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Current Memory</span>
            <span className="text-sm font-medium">
              {((data.system_health || {}).memory_usage || 0).toFixed(1)}%
            </span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Current Disk</span>
            <span className="text-sm font-medium">
              {((data.system_health || {}).disk_usage || 0).toFixed(1)}%
            </span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">System Uptime</span>
            <span className="text-sm font-medium">
              {((data.system_health || {}).uptime_hours || 0).toFixed(1)} hours
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MetricsCharts;

