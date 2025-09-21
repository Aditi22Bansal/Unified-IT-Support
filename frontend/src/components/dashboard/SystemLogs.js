import React, { useState } from 'react';
import { Filter, Search, AlertCircle, Info, AlertTriangle, XCircle } from 'lucide-react';

const SystemLogs = ({ logs = [] }) => {
  const [filters, setFilters] = useState({
    level: '',
    source: '',
    search: ''
  });

  const getLevelIcon = (level) => {
    switch (level.toLowerCase()) {
      case 'error':
      case 'critical':
        return <XCircle className="h-4 w-4 text-danger-600" />;
      case 'warning':
        return <AlertTriangle className="h-4 w-4 text-warning-600" />;
      case 'info':
        return <Info className="h-4 w-4 text-info-600" />;
      default:
        return <AlertCircle className="h-4 w-4 text-gray-400" />;
    }
  };

  const getLevelColor = (level) => {
    switch (level.toLowerCase()) {
      case 'error':
      case 'critical':
        return 'text-danger-600 bg-danger-100';
      case 'warning':
        return 'text-warning-600 bg-warning-100';
      case 'info':
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
      minute: '2-digit',
      second: '2-digit'
    });
  };

  const filteredLogs = (logs || []).filter(log => {
    const matchesLevel = !filters.level || log.level.toLowerCase() === filters.level.toLowerCase();
    const matchesSource = !filters.source || log.source.toLowerCase().includes(filters.source.toLowerCase());
    const matchesSearch = !filters.search ||
      log.message.toLowerCase().includes(filters.search.toLowerCase()) ||
      (log.hostname && log.hostname.toLowerCase().includes(filters.search.toLowerCase()));

    return matchesLevel && matchesSource && matchesSearch;
  });

  const uniqueLevels = [...new Set((logs || []).map(log => log.level))];
  const uniqueSources = [...new Set((logs || []).map(log => log.source))];

  return (
    <div className="card p-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-medium text-gray-900">System Logs</h3>
        <span className="text-sm text-gray-500">
          {filteredLogs.length} of {(logs || []).length} logs
        </span>
      </div>

      {/* Filters */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-4 mb-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Level
          </label>
          <select
            value={filters.level}
            onChange={(e) => setFilters({ ...filters, level: e.target.value })}
            className="input"
          >
            <option value="">All Levels</option>
            {uniqueLevels.map(level => (
              <option key={level} value={level}>{level}</option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Source
          </label>
          <select
            value={filters.source}
            onChange={(e) => setFilters({ ...filters, source: e.target.value })}
            className="input"
          >
            <option value="">All Sources</option>
            {uniqueSources.map(source => (
              <option key={source} value={source}>{source}</option>
            ))}
          </select>
        </div>
        <div className="sm:col-span-2">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Search
          </label>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search logs..."
              value={filters.search}
              onChange={(e) => setFilters({ ...filters, search: e.target.value })}
              className="input pl-10"
            />
          </div>
        </div>
      </div>

      {/* Logs List */}
      <div className="space-y-3 max-h-96 overflow-y-auto">
        {filteredLogs.length === 0 ? (
          <div className="text-center py-8">
            <AlertCircle className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">No logs found</h3>
            <p className="mt-1 text-sm text-gray-500">
              Try adjusting your filters or search terms.
            </p>
          </div>
        ) : (
          filteredLogs.map((log) => (
            <div key={log.id} className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg">
              <div className="flex-shrink-0 mt-0.5">
                {getLevelIcon(log.level)}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getLevelColor(log.level)}`}>
                      {log.level}
                    </span>
                    <span className="text-xs text-gray-500">{log.source}</span>
                    {log.hostname && <span className="text-xs text-gray-400">{log.hostname}</span>}
                  </div>
                  <span className="text-xs text-gray-400">
                    {formatTimestamp(log.timestamp)}
                  </span>
                </div>
                <p className="text-sm text-gray-900 mt-1">{log.message}</p>
                {log.metadata && (
                  <details className="mt-2">
                    <summary className="text-xs text-gray-500 cursor-pointer hover:text-gray-700">
                      View metadata
                    </summary>
                    <pre className="mt-1 text-xs text-gray-600 bg-white p-2 rounded border overflow-x-auto">
                      {JSON.stringify(JSON.parse(log.metadata), null, 2)}
                    </pre>
                  </details>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default SystemLogs;

