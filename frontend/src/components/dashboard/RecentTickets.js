import React from 'react';
import { Ticket, Clock } from 'lucide-react';

const RecentTickets = ({ tickets }) => {
  const getPriorityColor = (priority) => {
    switch (priority) {
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

  const getStatusColor = (status) => {
    switch (status) {
      case 'open':
        return 'text-danger-600 bg-danger-100';
      case 'in_progress':
        return 'text-warning-600 bg-warning-100';
      case 'resolved':
        return 'text-success-600 bg-success-100';
      case 'closed':
        return 'text-gray-600 bg-gray-100';
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
        <h3 className="text-lg font-medium text-gray-900">Recent Tickets</h3>
        <span className="text-sm text-gray-500">{tickets.length} tickets</span>
      </div>

      {tickets.length === 0 ? (
        <div className="text-center py-8">
          <Ticket className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No tickets</h3>
          <p className="mt-1 text-sm text-gray-500">
            No recent tickets found.
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {tickets.map((ticket) => (
            <div key={ticket.id} className="flex items-start space-x-3">
              <div className="flex-shrink-0">
                <Ticket className="h-5 w-5 text-gray-400" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between">
                  <p className="text-sm font-medium text-gray-900 truncate">
                    #{ticket.id} {ticket.title}
                  </p>
                  <div className="flex space-x-2">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getPriorityColor(ticket.priority)}`}>
                      {ticket.priority}
                    </span>
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(ticket.status)}`}>
                      {ticket.status.replace('_', ' ')}
                    </span>
                  </div>
                </div>
                <div className="flex items-center mt-2 text-xs text-gray-400">
                  <Clock className="h-3 w-3 mr-1" />
                  {formatTimestamp(ticket.created_at)}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default RecentTickets;

