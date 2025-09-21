import React from 'react';
import { Link } from 'react-router-dom';
import {
  Shield,
  Zap,
  Brain,
  BarChart3,
  Users,
  Clock,
  CheckCircle,
  ArrowRight,
  Star,
  Globe,
  Lock
} from 'lucide-react';

const LandingPage = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Navigation */}
      <nav className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Shield className="h-8 w-8 text-blue-600" />
              <span className="ml-2 text-xl font-bold text-gray-900">IT Support Pro</span>
            </div>
            <div className="flex items-center space-x-4">
              <Link
                to="/login"
                className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium"
              >
                Sign In
              </Link>
              <Link
                to="/register"
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
              Unified IT Support
              <span className="text-blue-600"> Made Simple</span>
            </h1>
            <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
              Enterprise-grade IT operations platform with AI-driven automation,
              real-time monitoring, and intelligent ticket management.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/register"
                className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-lg text-lg font-semibold flex items-center justify-center"
              >
                Start Free Trial
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
              <button className="border border-gray-300 hover:border-gray-400 text-gray-700 px-8 py-4 rounded-lg text-lg font-semibold">
                Watch Demo
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Everything You Need for IT Operations
            </h2>
            <p className="text-xl text-gray-600">
              Powerful features designed for modern IT teams
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* Real-time Monitoring */}
            <div className="bg-gray-50 p-6 rounded-xl hover:shadow-lg transition-shadow">
              <div className="flex items-center mb-4">
                <BarChart3 className="h-8 w-8 text-blue-600" />
                <h3 className="text-xl font-semibold text-gray-900 ml-3">Real-time Monitoring</h3>
              </div>
              <p className="text-gray-600">
                Monitor CPU, memory, disk usage, and system health with live dashboards and instant alerts.
              </p>
            </div>

            {/* AI-Powered Chatbot */}
            <div className="bg-gray-50 p-6 rounded-xl hover:shadow-lg transition-shadow">
              <div className="flex items-center mb-4">
                <Brain className="h-8 w-8 text-purple-600" />
                <h3 className="text-xl font-semibold text-gray-900 ml-3">AI Chatbot</h3>
              </div>
              <p className="text-gray-600">
                Intelligent FAQ bot with auto-escalation and 24/7 customer support capabilities.
              </p>
            </div>

            {/* Auto-Triage */}
            <div className="bg-gray-50 p-6 rounded-xl hover:shadow-lg transition-shadow">
              <div className="flex items-center mb-4">
                <Zap className="h-8 w-8 text-green-600" />
                <h3 className="text-xl font-semibold text-gray-900 ml-3">Auto-Triage</h3>
              </div>
              <p className="text-gray-600">
                Smart ticket classification and automatic assignment based on priority and expertise.
              </p>
            </div>

            {/* Role-Based Access */}
            <div className="bg-gray-50 p-6 rounded-xl hover:shadow-lg transition-shadow">
              <div className="flex items-center mb-4">
                <Users className="h-8 w-8 text-orange-600" />
                <h3 className="text-xl font-semibold text-gray-900 ml-3">Role-Based Access</h3>
              </div>
              <p className="text-gray-600">
                Secure access control for admins, agents, and customers with granular permissions.
              </p>
            </div>

            {/* SLA Tracking */}
            <div className="bg-gray-50 p-6 rounded-xl hover:shadow-lg transition-shadow">
              <div className="flex items-center mb-4">
                <Clock className="h-8 w-8 text-red-600" />
                <h3 className="text-xl font-semibold text-gray-900 ml-3">SLA Tracking</h3>
              </div>
              <p className="text-gray-600">
                Automated SLA monitoring with escalation and performance analytics.
              </p>
            </div>

            {/* Security */}
            <div className="bg-gray-50 p-6 rounded-xl hover:shadow-lg transition-shadow">
              <div className="flex items-center mb-4">
                <Lock className="h-8 w-8 text-indigo-600" />
                <h3 className="text-xl font-semibold text-gray-900 ml-3">Enterprise Security</h3>
              </div>
              <p className="text-gray-600">
                Bank-level security with encryption, audit logs, and compliance features.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 bg-blue-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 text-center text-white">
            <div>
              <div className="text-4xl font-bold mb-2">99.9%</div>
              <div className="text-blue-100">Uptime SLA</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">24/7</div>
              <div className="text-blue-100">AI Support</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">50%</div>
              <div className="text-blue-100">Faster Resolution</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">1000+</div>
              <div className="text-blue-100">Happy Customers</div>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Trusted by IT Teams Worldwide
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-gray-50 p-6 rounded-xl">
              <div className="flex items-center mb-4">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} className="h-5 w-5 text-yellow-400 fill-current" />
                ))}
              </div>
              <p className="text-gray-600 mb-4">
                "This platform transformed our IT operations. The AI chatbot alone reduced our support tickets by 60%."
              </p>
              <div className="font-semibold text-gray-900">Sarah Johnson</div>
              <div className="text-sm text-gray-500">CTO, TechCorp</div>
            </div>

            <div className="bg-gray-50 p-6 rounded-xl">
              <div className="flex items-center mb-4">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} className="h-5 w-5 text-yellow-400 fill-current" />
                ))}
              </div>
              <p className="text-gray-600 mb-4">
                "The real-time monitoring and auto-triage features are game-changers for our team."
              </p>
              <div className="font-semibold text-gray-900">Mike Chen</div>
              <div className="text-sm text-gray-500">IT Director, GlobalTech</div>
            </div>

            <div className="bg-gray-50 p-6 rounded-xl">
              <div className="flex items-center mb-4">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} className="h-5 w-5 text-yellow-400 fill-current" />
                ))}
              </div>
              <p className="text-gray-600 mb-4">
                "Best IT support platform we've used. The security features give us complete peace of mind."
              </p>
              <div className="font-semibold text-gray-900">Emily Rodriguez</div>
              <div className="text-sm text-gray-500">Security Manager, SecureIT</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gray-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            Ready to Transform Your IT Operations?
          </h2>
          <p className="text-xl text-gray-300 mb-8">
            Join thousands of IT teams already using our platform
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/register"
              className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-lg text-lg font-semibold"
            >
              Start Your Free Trial
            </Link>
            <button className="border border-gray-600 hover:border-gray-500 text-white px-8 py-4 rounded-lg text-lg font-semibold">
              Contact Sales
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-800 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center mb-4">
                <Shield className="h-6 w-6 text-blue-400" />
                <span className="ml-2 text-lg font-bold text-white">IT Support Pro</span>
              </div>
              <p className="text-gray-400">
                Enterprise IT operations platform with AI-driven automation and real-time monitoring.
              </p>
            </div>
            <div>
              <h3 className="text-white font-semibold mb-4">Product</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white">Features</a></li>
                <li><a href="#" className="hover:text-white">Pricing</a></li>
                <li><a href="#" className="hover:text-white">Security</a></li>
                <li><a href="#" className="hover:text-white">Integrations</a></li>
              </ul>
            </div>
            <div>
              <h3 className="text-white font-semibold mb-4">Company</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white">About</a></li>
                <li><a href="#" className="hover:text-white">Blog</a></li>
                <li><a href="#" className="hover:text-white">Careers</a></li>
                <li><a href="#" className="hover:text-white">Contact</a></li>
              </ul>
            </div>
            <div>
              <h3 className="text-white font-semibold mb-4">Support</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white">Help Center</a></li>
                <li><a href="#" className="hover:text-white">Documentation</a></li>
                <li><a href="#" className="hover:text-white">Status</a></li>
                <li><a href="#" className="hover:text-white">Community</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-700 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2025 IT Support Pro. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;




