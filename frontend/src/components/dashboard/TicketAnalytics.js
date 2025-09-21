import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const TicketAnalytics = ({ data }) => {
  // Create status data from the backend response
  const statusData = [
    { status: 'Open', count: data.status_distribution?.open || 0 },
    { status: 'In Progress', count: data.status_distribution?.['in_progress'] || 0 },
    { status: 'Resolved', count: data.status_distribution?.resolved || 0 }
  ];

  // Create priority data from priority_distribution
  const priorityData = Object.entries(data.priority_distribution || {}).map(([priority, count]) => ({
    priority: priority.charAt(0).toUpperCase() + priority.slice(1),
    count
  }));

  // Create category data from category_distribution
  const categoryData = Object.entries(data.category_distribution || {}).map(([category, count]) => ({
    category: category.replace('_', ' '),
    count
  }));

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

  return (
    <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
      {/* Status Distribution */}
      <div className="card p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Tickets by Status</h3>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={statusData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="status" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Priority Distribution */}
      <div className="card p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Tickets by Priority</h3>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={priorityData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ priority, count }) => `${priority}: ${count}`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="count"
              >
                {priorityData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Category Distribution */}
      <div className="card p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Tickets by Category</h3>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={categoryData} layout="horizontal">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis dataKey="category" type="category" width={100} />
              <Tooltip />
              <Bar dataKey="count" fill="#10b981" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Summary Stats */}
      <div className="card p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Summary Statistics</h3>
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Total Tickets</span>
            <span className="text-2xl font-bold text-gray-900">{data.total_tickets || 0}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Average Resolution Time</span>
            <span className="text-lg font-semibold text-gray-900">
              {data.avg_resolution_time || 0}h
            </span>
          </div>
          <div className="grid grid-cols-2 gap-4 pt-4 border-t">
            <div>
              <p className="text-xs text-gray-500 uppercase tracking-wide">Open Tickets</p>
              <p className="text-lg font-semibold text-danger-600">
                {data.open_tickets || 0}
              </p>
            </div>
            <div>
              <p className="text-xs text-gray-500 uppercase tracking-wide">Resolved Tickets</p>
              <p className="text-lg font-semibold text-success-600">
                {data.resolved_tickets || 0}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TicketAnalytics;

