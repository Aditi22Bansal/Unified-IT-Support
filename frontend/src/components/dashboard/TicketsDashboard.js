import React, { useState, useEffect } from 'react';
import { Plus, RefreshCw, Filter, Search } from 'lucide-react';
import { ticketsAPI } from '../../services/api';
import TicketList from './TicketList';
import CreateTicketModal from './CreateTicketModal';
import TicketAnalytics from './TicketAnalytics';
import LoadingSpinner from '../common/LoadingSpinner';
import toast from 'react-hot-toast';

const TicketsDashboard = () => {
  const [tickets, setTickets] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [filters, setFilters] = useState({
    status: '',
    priority: '',
    search: ''
  });

  useEffect(() => {
    fetchData();
  }, [filters]);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [ticketsData, analyticsData] = await Promise.all([
        ticketsAPI.getTickets(filters),
        ticketsAPI.getTicketAnalytics()
      ]);

      setTickets(ticketsData);
      setAnalytics(analyticsData);
    } catch (error) {
      console.error('Failed to fetch tickets data:', error);
      toast.error('Failed to load tickets data');
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

  const handleCreateTicket = async (ticketData) => {
    try {
      const newTicket = await ticketsAPI.createTicket(ticketData);
      setTickets(prev => [newTicket, ...prev]);
      setShowCreateModal(false);
      toast.success('Ticket created successfully');
    } catch (error) {
      toast.error('Failed to create ticket');
    }
  };

  const handleUpdateTicket = async (ticketId, updates) => {
    try {
      const updatedTicket = await ticketsAPI.updateTicket(ticketId, updates);
      setTickets(prev =>
        prev.map(ticket =>
          ticket.id === ticketId ? updatedTicket : ticket
        )
      );
      toast.success('Ticket updated successfully');
    } catch (error) {
      toast.error('Failed to update ticket');
    }
  };

  const handleDeleteTicket = async (ticketId) => {
    try {
      await ticketsAPI.deleteTicket(ticketId);
      setTickets(prev => prev.filter(ticket => ticket.id !== ticketId));
      toast.success('Ticket deleted successfully');
    } catch (error) {
      toast.error('Failed to delete ticket');
    }
  };

  if (loading) {
    return <LoadingSpinner text="Loading tickets..." />;
  }

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Ticket Management</h1>
          <p className="mt-1 text-sm text-gray-500">
            Manage and track support tickets
          </p>
        </div>
        <div className="flex space-x-3">
          <button
            onClick={handleRefresh}
            disabled={refreshing}
            className="btn btn-secondary flex items-center"
          >
            <RefreshCw className={`h-4 w-4 mr-2 ${refreshing ? 'animate-spin' : ''}`} />
            Refresh
          </button>
          <button
            onClick={() => setShowCreateModal(true)}
            className="btn btn-primary flex items-center"
          >
            <Plus className="h-4 w-4 mr-2" />
            Create Ticket
          </button>
        </div>
      </div>

      {/* Analytics */}
      {analytics && <TicketAnalytics data={analytics} />}

      {/* Filters */}
      <div className="card p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-medium text-gray-900">Filters</h3>
          <Filter className="h-5 w-5 text-gray-400" />
        </div>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Status
            </label>
            <select
              value={filters.status}
              onChange={(e) => setFilters({ ...filters, status: e.target.value })}
              className="input"
            >
              <option value="">All Statuses</option>
              <option value="open">Open</option>
              <option value="in_progress">In Progress</option>
              <option value="resolved">Resolved</option>
              <option value="closed">Closed</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Priority
            </label>
            <select
              value={filters.priority}
              onChange={(e) => setFilters({ ...filters, priority: e.target.value })}
              className="input"
            >
              <option value="">All Priorities</option>
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="critical">Critical</option>
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
                placeholder="Search tickets..."
                value={filters.search}
                onChange={(e) => setFilters({ ...filters, search: e.target.value })}
                className="input pl-10"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Tickets List */}
      <TicketList
        tickets={tickets}
        onUpdateTicket={handleUpdateTicket}
        onDeleteTicket={handleDeleteTicket}
      />

      {/* Create Ticket Modal */}
      {showCreateModal && (
        <CreateTicketModal
          onClose={() => setShowCreateModal(false)}
          onSubmit={handleCreateTicket}
        />
      )}
    </div>
  );
};

export default TicketsDashboard;

