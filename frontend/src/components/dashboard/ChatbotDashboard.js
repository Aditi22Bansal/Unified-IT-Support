import React, { useState, useEffect, useRef } from 'react';
import { Send, Bot, User, RefreshCw, BarChart3, MessageSquare } from 'lucide-react';
import { chatbotAPI } from '../../services/api';
import ChatbotAnalytics from './ChatbotAnalytics';
import LoadingSpinner from '../common/LoadingSpinner';
import FormattedMessage from '../chatbot/FormattedMessage';
import toast from 'react-hot-toast';

const ChatbotDashboard = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [sessionId, setSessionId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [analytics, setAnalytics] = useState(null);
  const [showAnalytics, setShowAnalytics] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const fetchAnalytics = async () => {
    try {
      const data = await chatbotAPI.getAnalytics();
      setAnalytics(data);
    } catch (error) {
      console.error('Failed to fetch analytics:', error);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim() || loading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setLoading(true);

    try {
      const response = await chatbotAPI.chat(inputMessage, sessionId);

      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: response.response,
        timestamp: new Date(),
        confidence: response.confidence_score,
        escalated: response.was_escalated,
        ticketId: response.ticket_id
      };

      setMessages(prev => [...prev, botMessage]);

      if (!sessionId) {
        setSessionId(response.session_id);
      }

      if (response.was_escalated) {
        toast.success(`Your query has been escalated to ticket #${response.ticket_id}`);
      }
    } catch (error) {
      console.error('Failed to send message:', error);
      toast.error('Failed to send message. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([]);
    setSessionId(null);
  };

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">AI Chatbot</h1>
          <p className="mt-1 text-sm text-gray-500">
            Get instant help with your IT questions
          </p>
        </div>
        <div className="flex space-x-3">
          <button
            onClick={() => setShowAnalytics(!showAnalytics)}
            className="btn btn-secondary flex items-center"
          >
            <BarChart3 className="h-4 w-4 mr-2" />
            Analytics
          </button>
          <button
            onClick={clearChat}
            className="btn btn-secondary flex items-center"
          >
            <RefreshCw className="h-4 w-4 mr-2" />
            Clear Chat
          </button>
        </div>
      </div>

      {/* Analytics Panel */}
      {showAnalytics && analytics && (
        <ChatbotAnalytics data={analytics} />
      )}

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Chat Interface */}
        <div className="lg:col-span-2">
          <div className="card p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-medium text-gray-900">Chat with AI Assistant</h3>
              <div className="flex items-center text-sm text-gray-500">
                <MessageSquare className="h-4 w-4 mr-1" />
                {messages.length} messages
              </div>
            </div>

            {/* Messages */}
            <div className="h-96 overflow-y-auto space-y-4 mb-4">
              {messages.length === 0 ? (
                <div className="text-center py-8">
                  <Bot className="mx-auto h-12 w-12 text-gray-400" />
                  <h3 className="mt-2 text-sm font-medium text-gray-900">Start a conversation</h3>
                  <p className="mt-1 text-sm text-gray-500">
                    Ask me anything about IT support or common issues.
                  </p>
                </div>
              ) : (
                messages.map((message) => (
                  <FormattedMessage
                    key={message.id}
                    message={message.content}
                    isUser={message.type === 'user'}
                    timestamp={formatTimestamp(message.timestamp)}
                    confidence={message.confidence}
                  />
                ))
              )}
              {loading && (
                <div className="flex justify-start">
                  <div className="bg-gray-100 text-gray-900 px-4 py-2 rounded-lg">
                    <div className="flex items-center space-x-2">
                      <Bot className="h-4 w-4" />
                      <div className="flex space-x-1">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Input Form */}
            <form onSubmit={handleSendMessage} className="flex space-x-2">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder="Type your message..."
                className="input flex-1"
                disabled={loading}
              />
              <button
                type="submit"
                disabled={loading || !inputMessage.trim()}
                className="btn btn-primary px-4 py-2"
              >
                <Send className="h-4 w-4" />
              </button>
            </form>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="space-y-6">
          <div className="card p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Quick Actions</h3>
            <div className="space-y-2">
              <button
                onClick={() => setInputMessage('How do I reset my password?')}
                className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-md"
              >
                Reset Password
              </button>
              <button
                onClick={() => setInputMessage('How do I access the VPN?')}
                className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-md"
              >
                VPN Access
              </button>
              <button
                onClick={() => setInputMessage('My computer is running slowly')}
                className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-md"
              >
                Performance Issues
              </button>
              <button
                onClick={() => setInputMessage('How do I install software?')}
                className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-md"
              >
                Software Installation
              </button>
              <button
                onClick={() => setInputMessage('What are the IT support hours?')}
                className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-md"
              >
                Support Hours
              </button>
            </div>
          </div>

          {/* Session Info */}
          {sessionId && (
            <div className="card p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Session Info</h3>
              <div className="space-y-2 text-sm text-gray-600">
                <div>Session ID: {sessionId.slice(0, 8)}...</div>
                <div>Messages: {messages.length}</div>
                <div>Started: {messages.length > 0 ? formatTimestamp(messages[0].timestamp) : 'N/A'}</div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChatbotDashboard;

