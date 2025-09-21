import React, { useState } from 'react';
import { Ticket, Clock, User, Edit, CheckCircle, Trash2 } from 'lucide-react';
import EditTicketModal from './EditTicketModal';

const TicketList = ({ tickets, onUpdateTicket, onDeleteTicket }) => {
  const [editingTicket, setEditingTicket] = useState(null);
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

  const handleStatusChange = async (ticketId, newStatus) => {
    await onUpdateTicket(ticketId, { status: newStatus });
  };

  const handleEditTicket = (ticket) => {
    setEditingTicket(ticket);
  };

  const handleCloseEditModal = () => {
    setEditingTicket(null);
  };

  const handleSaveTicket = async (ticketId, updatedData) => {
    await onUpdateTicket(ticketId, updatedData);
    setEditingTicket(null);
  };

  const handleDeleteTicket = async (ticketId) => {
    if (window.confirm('Are you sure you want to delete this ticket? This action cannot be undone.')) {
      await onDeleteTicket(ticketId);
    }
  };

  return (
    <div className="card p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-medium text-gray-900">Tickets</h3>
        <span className="text-sm text-gray-500">{tickets.length} tickets</span>
      </div>

      {tickets.length === 0 ? (
        <div className="text-center py-8">
          <Ticket className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No tickets found</h3>
          <p className="mt-1 text-sm text-gray-500">
            No tickets match your current filters.
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {tickets.map((ticket) => (
            <div key={ticket.id} className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50">
              <div className="flex items-start justify-between">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center space-x-2 mb-2">
                    <Ticket className="h-4 w-4 text-gray-400" />
                    <span className="text-sm font-medium text-gray-900">
                      #{ticket.id} {ticket.title}
                    </span>
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getPriorityColor(ticket.priority)}`}>
                      {ticket.priority}
                    </span>
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(ticket.status)}`}>
                      {ticket.status.replace('_', ' ')}
                    </span>
                  </div>

                  <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                    {ticket.description}
                  </p>

                  <div className="flex items-center space-x-4 text-xs text-gray-500">
                    <div className="flex items-center">
                      <Clock className="h-3 w-3 mr-1" />
                      {formatTimestamp(ticket.created_at)}
                    </div>
                    <div className="flex items-center">
                      <User className="h-3 w-3 mr-1" />
                      Created by user {ticket.created_by}
                    </div>
                    {ticket.auto_categorized && (
                      <span className="text-xs text-blue-600">Auto-categorized</span>
                    )}
                  </div>
                </div>

                <div className="flex items-center space-x-2 ml-4">
                  {ticket.status === 'open' && (
                    <button
                      onClick={() => handleStatusChange(ticket.id, 'in_progress')}
                      className="btn btn-warning text-xs px-3 py-1"
                    >
                      Start
                    </button>
                  )}
                  {ticket.status === 'in_progress' && (
                    <button
                      onClick={() => handleStatusChange(ticket.id, 'resolved')}
                      className="btn btn-success text-xs px-3 py-1 flex items-center"
                    >
                      <CheckCircle className="h-3 w-3 mr-1" />
                      Resolve
                    </button>
                  )}
                  <button
                    onClick={() => handleEditTicket(ticket)}
                    className="btn btn-secondary text-xs px-3 py-1 flex items-center"
                  >
                    <Edit className="h-3 w-3 mr-1" />
                    Edit
                  </button>
                  <button
                    onClick={() => handleDeleteTicket(ticket.id)}
                    className="btn btn-danger text-xs px-3 py-1 flex items-center"
                  >
                    <Trash2 className="h-3 w-3 mr-1" />
                    Delete
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Edit Ticket Modal */}
      {editingTicket && (
        <EditTicketModal
          ticket={editingTicket}
          onClose={handleCloseEditModal}
          onSave={handleSaveTicket}
        />
      )}
    </div>
  );
};

export default TicketList;

