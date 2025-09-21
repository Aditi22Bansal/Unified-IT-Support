# 🚀 IT Support Pro - Unified IT Support System

A comprehensive, enterprise-grade IT operations platform with AI-driven automation, real-time monitoring, and intelligent ticket management.

## ✨ Features

### 🏠 Professional Landing Page
- Modern, responsive design with gradient backgrounds
- Feature showcase with real-time monitoring, AI chatbot, and auto-triage
- Statistics section with performance metrics
- Customer testimonials and success stories
- Clear call-to-action buttons

### 🔐 Secure Authentication System
- **Advanced Login/Registration** with real-time validation
- **Password Security** with strength indicators and requirements
- **Account Protection** with brute force protection and lockout
- **Google OAuth Ready** with integration points
- **Form Validation** with comprehensive error handling

### 🛡️ Cybersecurity Features
- **Password Requirements**: 8+ characters, uppercase, lowercase, numbers, special characters
- **Account Lockout**: 5 failed attempts = 15-minute lockout
- **Rate Limiting**: API and login rate limiting
- **Security Headers**: XSS protection, content security policy
- **Input Validation**: Client and server-side validation
- **Secure Storage**: JWT tokens, encrypted passwords

### 📊 IT Operations Dashboard
- **Real-time Monitoring**: CPU, memory, disk usage, system health
- **Live Dashboards**: Charts and graphs with instant alerts
- **Threshold Alerts**: Configurable alerts for system metrics
- **Historical Data**: 24-hour trend analysis

### 🤖 AI-Powered Chatbot
- **Intelligent FAQ Bot** with auto-escalation
- **24/7 Customer Support** capabilities
- **OpenRouter Integration** for advanced AI responses
- **Formatted Responses** with markdown rendering
- **Session Management** for conversation continuity

### 🎫 Auto-Triage System
- **Smart Ticket Classification** based on priority and expertise
- **Automatic Assignment** to appropriate agents
- **SLA Tracking** with escalation and performance analytics
- **Real-time Updates** via WebSocket connections

### 👥 Role-Based Access Control
- **Admin**: Full system access and management
- **Agent**: Ticket management and customer support
- **Customer**: Self-service and ticket creation
- **Granular Permissions** for secure access control

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- Docker and Docker Compose (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd unified_it_support
   ```

2. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

3. **Install dependencies**
   ```bash
   # Backend
   cd backend
   pip install -r requirements.txt

   # Frontend
   cd ../frontend
   npm install
   ```

4. **Run the application**
   ```bash

   # Option 1: Manual
   # Terminal 1 - Backend
   cd backend
   python main_dynamic.py

   # Terminal 2 - Frontend
   cd frontend
   npm start
   ```

## 🌐 Access Information

- **Landing Page**: http://localhost:3000
- **Login**: http://localhost:3000/login
- **Register**: http://localhost:3000/register
- **Dashboard**: http://localhost:3000/dashboard (after login)
- **API Documentation**: http://localhost:8001/docs

## 🔑 Default Credentials

- **Admin**: `admin` / `admin123`
- **Agent**: `agent` / `agent123`
- **Customer**: `customer` / `customer123`

## 🛠️ Technology Stack

### Frontend
- **React 18** with modern hooks
- **Tailwind CSS** for styling
- **Lucide React** for icons
- **React Router** for navigation
- **Axios** for API calls
- **React Hot Toast** for notifications

### Backend
- **FastAPI** with async support
- **Python 3.11** with type hints
- **OpenRouter API** for AI integration
- **WebSocket** for real-time updates
- **JWT** for authentication
- **SQLite** for data storage

### Security
- **Password Hashing** with bcrypt
- **JWT Tokens** for session management
- **Rate Limiting** for API protection
- **CORS** configuration
- **Input Validation** and sanitization

## 📁 Project Structure

```
unified_it_support/
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── pages/           # Landing, Login, Register pages
│   │   ├── components/      # Reusable components
│   │   ├── services/        # API services
│   │   └── contexts/        # React contexts
│   ├── Dockerfile
│   └── package.json
├── backend/                 # Python backend
│   ├── simple_main_enhanced.py
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml       # Multi-service setup
├── nginx.conf              # Reverse proxy config
├── deploy.bat              # Windows deployment
├── deploy.sh               # Linux/Mac deployment
└── README.md
```

## 🔧 Configuration

### Environment Variables
```bash
# OpenAI/OpenRouter API Key
OPENAI_API_KEY=your_openrouter_api_key_here

# Database
DATABASE_URL=sqlite:///./dev.db

# JWT Secret
JWT_SECRET=your-super-secret-jwt-key

# Google OAuth (Optional)
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

## 🚀 Deployment

### Docker Deployment (Recommended)
```bash
# Windows
deploy.bat

# Linux/Mac
chmod +x deploy.sh
./deploy.sh
```

### Manual Deployment
```bash
# Backend
cd backend
python main_dynamic.py

# Frontend
cd frontend
npm start
```

## 🧪 Testing

### Run All Tests
```bash
cd backend
python tests/run_tests.py
```

### Run Specific Test Categories
```bash
# Authentication tests
cd backend/tests/auth
python test_auth_fix.py

# API tests
cd backend/tests/api
python test_health.py

# Integration tests
cd backend/tests/integration
python test_backend.py
```

See [Test Documentation](backend/tests/README.md) for detailed testing information.

## 📊 Features Overview

| Feature | Status | Description |
|---------|--------|-------------|
| Landing Page | ✅ | Professional marketing page |
| Authentication | ✅ | Secure login/registration |
| Password Security | ✅ | Strength checking & requirements |
| Account Protection | ✅ | Brute force protection |
| Google OAuth | 🔄 | Integration points ready |
| Real-time Monitoring | ✅ | System health metrics |
| AI Chatbot | ✅ | OpenRouter integration |
| Auto-triage | ✅ | Smart ticket classification |
| Role-based Access | ✅ | Admin/Agent/Customer roles |
| WebSocket Updates | ✅ | Real-time notifications |
| Docker Support | ✅ | Containerized deployment |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the troubleshooting section

---

**Built with ❤️ for modern IT operations**




