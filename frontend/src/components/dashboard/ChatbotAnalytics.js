import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const ChatbotAnalytics = ({ data }) => {
  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444'];

  const commonQueriesData = (data.common_queries || []).slice(0, 5).map((query, index) => ({
    query: query.query.length > 30 ? query.query.substring(0, 30) + '...' : query.query,
    count: query.count
  }));

  return (
    <div className="card p-6 mb-6">
      <h3 className="text-lg font-medium text-gray-900 mb-4">Chatbot Analytics</h3>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Summary Stats */}
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-blue-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">{data.total_queries || 0}</div>
              <div className="text-sm text-blue-600">Total Queries</div>
            </div>
            <div className="bg-green-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-green-600">{data.escalated_queries || 0}</div>
              <div className="text-sm text-green-600">Escalated Queries</div>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="bg-yellow-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-yellow-600">{data.escalation_rate || 0}%</div>
              <div className="text-sm text-yellow-600">Escalation Rate</div>
            </div>
            <div className="bg-purple-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-purple-600">{(data.avg_confidence_score * 100 || 0).toFixed(0)}%</div>
              <div className="text-sm text-purple-600">Avg Confidence</div>
            </div>
          </div>
        </div>

        {/* Common Queries Chart */}
        <div>
          <h4 className="text-md font-medium text-gray-900 mb-4">Most Common Queries</h4>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={commonQueriesData} layout="horizontal">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis dataKey="query" type="category" width={120} />
                <Tooltip />
                <Bar dataKey="count" fill="#3b82f6" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Performance Metrics */}
      <div className="mt-6 pt-6 border-t border-gray-200">
        <h4 className="text-md font-medium text-gray-900 mb-4">Performance Metrics</h4>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <div className="text-center">
            <div className="text-lg font-semibold text-gray-900">
              {data.total_queries || 0}
            </div>
            <div className="text-sm text-gray-500">Total Interactions</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-semibold text-gray-900">
              {((data.total_queries - data.escalated_queries) / data.total_queries * 100 || 0).toFixed(1)}%
            </div>
            <div className="text-sm text-gray-500">Self-Service Rate</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-semibold text-gray-900">
              {(data.avg_confidence_score * 100 || 0).toFixed(1)}%
            </div>
            <div className="text-sm text-gray-500">Average Confidence</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatbotAnalytics;

