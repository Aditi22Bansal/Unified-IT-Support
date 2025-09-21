import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8002';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// WebSocket connection for real-time updates
class WebSocketService {
  constructor() {
    this.socket = null;
    this.listeners = new Map();
  }

  connect(token) {
    if (this.socket) {
      this.socket.close();
    }

    const wsUrl = `ws://127.0.0.1:8002/ws${token ? `?token=${token}` : ''}`;
    this.socket = new WebSocket(wsUrl);

    this.socket.onopen = () => {
      console.log('WebSocket connected');
    };

    this.socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        this.notifyListeners(data);
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };

    this.socket.onclose = () => {
      console.log('WebSocket disconnected');
      // Attempt to reconnect after 5 seconds
      setTimeout(() => {
        if (this.socket?.readyState === WebSocket.CLOSED) {
          this.connect(token);
        }
      }, 5000);
    };

    this.socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }

  disconnect() {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }

  addListener(eventType, callback) {
    if (!this.listeners.has(eventType)) {
      this.listeners.set(eventType, []);
    }
    this.listeners.get(eventType).push(callback);
  }

  removeListener(eventType, callback) {
    if (this.listeners.has(eventType)) {
      const callbacks = this.listeners.get(eventType);
      const index = callbacks.indexOf(callback);
      if (index > -1) {
        callbacks.splice(index, 1);
      }
    }
  }

  notifyListeners(data) {
    const eventType = data.type;
    if (this.listeners.has(eventType)) {
      this.listeners.get(eventType).forEach(callback => {
        try {
          callback(data);
        } catch (error) {
          console.error('Error in WebSocket listener:', error);
        }
      });
    }
  }
}

// Create global WebSocket service instance
export const wsService = new WebSocketService();

// MFA API
export const mfaAPI = {
  setup: (userId, userEmail) =>
    api.post('/api/mfa/setup', { user_id: userId, user_email: userEmail }).then(res => res.data),

  getQRCode: (userId) =>
    api.get(`/api/mfa/qr-code/${userId}`).then(res => res.data),

  verifySetup: (userId, token) =>
    api.post('/api/mfa/verify-setup', { user_id: userId, token }).then(res => res.data),

  sendEmailVerification: (userId, userEmail) =>
    api.post('/api/mfa/send-email-verification', { user_id: userId, user_email: userEmail }).then(res => res.data),

  verifyEmailCode: (userId, code) =>
    api.post('/api/mfa/verify-email-code', { user_id: userId, code }).then(res => res.data),

  getStatus: (userId) =>
    api.get(`/api/mfa/status/${userId}`).then(res => res.data),

  refreshToken: (refreshToken) =>
    api.post('/api/mfa/refresh-token', { refresh_token: refreshToken }).then(res => res.data),

  disable: (userId) =>
    api.post(`/api/mfa/disable/${userId}`).then(res => res.data),
};

// Auth API
export const authAPI = {
  login: (username, password) =>
    api.post('/api/auth/login', { username, password }),

  register: (userData) =>
    api.post('/api/auth/register', userData),

  getCurrentUser: () =>
    api.get('/api/auth/me').then(res => res.data),

  getUsers: () =>
    api.get('/api/auth/users').then(res => res.data),
};

// Dashboard API
export const dashboardAPI = {
  getSystemHealth: () =>
    api.get('/api/dashboard/health').then(res => res.data),

  getDashboardMetrics: (hours = 24) =>
    api.get(`/api/dashboard/metrics?hours=${hours}`).then(res => res.data),

  getSystemLogs: (params = {}) =>
    api.get('/api/dashboard/logs', { params }).then(res => res.data),
};

// Tickets API
export const ticketsAPI = {
  getTickets: (params = {}) =>
    api.get('/api/tickets', { params }).then(res => res.data),

  getTicket: (id) =>
    api.get(`/api/tickets/${id}`).then(res => res.data),

  createTicket: (ticketData) =>
    api.post('/api/tickets', ticketData).then(res => res.data),

  updateTicket: (id, ticketData) =>
    api.put(`/api/tickets/${id}`, ticketData).then(res => res.data),

  deleteTicket: (id) =>
    api.delete(`/api/tickets/${id}`).then(res => res.data),

  getTicketAnalytics: () =>
    api.get('/api/analytics/tickets').then(res => res.data),
};

// Chatbot API
export const chatbotAPI = {
  chat: (message, sessionId = null) =>
    api.post('/api/chatbot/chat', { message, sessionId }).then(res => res.data),

  getFAQs: (params = {}) =>
    api.get('/api/chatbot/faqs', { params }).then(res => res.data),

  createFAQ: (faqData) =>
    api.post('/api/chatbot/faqs', faqData).then(res => res.data),

  getAnalytics: () =>
    api.get('/api/chatbot/analytics').then(res => res.data),

  getLogs: (params = {}) =>
    api.get('/api/chatbot/logs', { params }).then(res => res.data),
};

export default api;

