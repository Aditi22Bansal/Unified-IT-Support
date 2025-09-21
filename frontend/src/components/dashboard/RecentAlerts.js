import React from 'react';
import { AlertTriangle, Clock } from 'lucide-react';

const RecentAlerts = ({ alerts }) => {
  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical':
        return 'text-danger-600 bg-danger-100';
      case 'high':
        return 'text-danger-600 bg-danger-100';
      case 'medium':
        return 'text-warning-600 bg-warning-100';
      case 'low':
        return 'text-info-600 bg-blue-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="card p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-medium text-gray-900">Recent Alerts</h3>
        <span className="text-sm text-gray-500">{alerts.length} alerts</span>
      </div>

      {alerts.length === 0 ? (
        <div className="text-center py-8">
          <AlertTriangle className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No alerts</h3>
          <p className="mt-1 text-sm text-gray-500">
            All systems are running normally.
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {alerts.map((alert) => (
            <div key={alert.id} className="flex items-start space-x-3">
              <div className="flex-shrink-0">
                <AlertTriangle className="h-5 w-5 text-gray-400" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between">
                  <p className="text-sm font-medium text-gray-900 truncate">
                    {alert.title}
                  </p>
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getSeverityColor(alert.severity)}`}>
                    {alert.severity}
                  </span>
                </div>
                <p className="text-sm text-gray-500 mt-1">
                  {alert.description}
                </p>
                <div className="flex items-center mt-2 text-xs text-gray-400">
                  <Clock className="h-3 w-3 mr-1" />
                  {formatTimestamp(alert.timestamp)}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default RecentAlerts;

