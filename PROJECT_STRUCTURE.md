# IT Support System - Project Structure

## 📁 Project Overview
This is a unified IT support system with AI-powered chatbot, ticket management, and real-time monitoring capabilities.

## 🏗️ Directory Structure

```
unified_it_support/
├── 📁 backend/                          # Backend API and services
│   ├── 📁 api/                          # API route definitions
│   │   └── routes/
│   │       ├── auth.py                  # Authentication endpoints
│   │       ├── tickets.py               # Ticket management endpoints
│   │       ├── dashboard.py             # Dashboard endpoints
│   │       └── chatbot.py               # Chatbot endpoints
│   ├── 📁 database/                     # Database models and connections
│   │   ├── models/                      # SQLAlchemy models
│   │   ├── prisma_client.py             # Prisma database client
│   │   └── connection.py                # Database connection setup
│   ├── 📁 services/                     # Business logic services
│   │   ├── auth_service.py              # Authentication service
│   │   ├── chatbot_service.py           # AI chatbot service
│   │   ├── auto_triage.py               # Auto-triage service
│   │   ├── rbac.py                      # Role-based access control
│   │   └── realtime_monitor.py          # System monitoring
│   ├── 📁 tests/                        # Test files (organized)
│   │   ├── auth/                        # Authentication tests
│   │   │   ├── test_auth_fix.py         # Auth persistence tests
│   │   │   └── test_aditi_user.py       # User-specific tests
│   │   ├── api/                         # API endpoint tests
│   │   │   └── test_health.py           # Health check tests
│   │   └── integration/                 # Integration tests
│   │       └── test_backend.py          # Full backend tests
│   ├── 📁 prisma/                       # Prisma schema and migrations
│   │   ├── schema.prisma                # Database schema
│   │   └── generated/                   # Generated Prisma client
│   ├── main_dynamic.py                  # 🚀 MAIN SERVER (Database-backed)
│   ├── working_server.py                # Alternative server (In-memory)
│   ├── simple_main_enhanced.py          # Enhanced server (In-memory)
│   ├── init_database.py                 # Database initialization
│   ├── migrate_to_database.py           # Migration script
│   └── requirements.txt                 # Python dependencies
├── 📁 frontend/                         # React frontend application
│   ├── 📁 src/
│   │   ├── 📁 components/               # React components
│   │   │   ├── auth/                    # Authentication components
│   │   │   ├── dashboard/               # Dashboard components
│   │   │   ├── chatbot/                 # Chatbot components
│   │   │   └── layout/                  # Layout components
│   │   ├── 📁 contexts/                 # React contexts
│   │   │   ├── AuthContext.js           # Authentication context
│   │   │   └── DashboardContext.js      # Dashboard context
│   │   ├── 📁 services/                 # API services
│   │   │   └── api.js                   # API client
│   │   ├── 📁 pages/                    # Page components
│   │   └── App.js                       # Main app component
│   └── package.json                     # Node.js dependencies
├── 📁 docs/                             # Documentation
│   ├── API.md                           # API documentation
│   ├── FEATURES.md                      # Feature documentation
│   └── SETUP.md                         # Setup instructions
├── 📄 docker-compose.yml                # Docker configuration
├── 📄 nginx.conf                        # Nginx configuration
├── 📄 MIGRATION_GUIDE.md                # Migration guide
├── 📄 PROJECT_STRUCTURE.md              # This file
└── 📄 README.md                         # Main README
```

## 🚀 Quick Start

### Option 1: Database-Backed System (Recommended)
```bash
# Start the main system with persistent storage
start_dynamic_system.bat
```

### Option 2: Manual Setup
```bash
# Backend
cd backend
python main_dynamic.py

# Frontend (new terminal)
cd frontend
npm start
```

### Option 3: In-Memory System (Testing)
```bash
# Backend
cd backend
python working_server.py

# Frontend (new terminal)
cd frontend
npm start
```

## 🧪 Testing

### Run Authentication Tests
```bash
cd backend/tests/auth
python test_auth_fix.py
python test_aditi_user.py
```

### Run API Tests
```bash
cd backend/tests/api
python test_health.py
```

### Run Integration Tests
```bash
cd backend/tests/integration
python test_backend.py
```

## 🔧 Server Types

| Server File | Type | Storage | Port | Use Case |
|-------------|------|---------|------|----------|
| `main_dynamic.py` | Database | Persistent | 8001 | Production |
| `working_server.py` | In-memory | Temporary | 8002 | Testing |
| `simple_main_enhanced.py` | In-memory | Temporary | 8001 | Development |

## 🗄️ Database

- **Type**: SQLite (development) / PostgreSQL (production)
- **ORM**: Prisma
- **Schema**: `backend/prisma/schema.prisma`
- **Migration**: `python migrate_to_database.py`

## 🔑 Default Credentials

- **Admin**: admin / admin123
- **Agent**: agent / agent123
- **Customer**: customer / customer123

## 📝 Key Features

- ✅ **Persistent Ticket Storage** - Tickets saved to database
- ✅ **Real-time Updates** - WebSocket support
- ✅ **Role-based Access** - Full RBAC system
- ✅ **Auto-triage** - AI-powered categorization
- ✅ **SLA Tracking** - Automatic monitoring
- ✅ **Analytics** - Comprehensive reporting
- ✅ **System Monitoring** - Real-time health metrics

## 🐛 Troubleshooting

### Tickets Disappearing on Reload
- **Cause**: Using in-memory server instead of database server
- **Fix**: Use `main_dynamic.py` or run `migrate_to_database.py`

### Demo User Appearing
- **Cause**: Hardcoded demo user in server endpoints
- **Fix**: Updated authentication to use proper token validation

### Port Conflicts
- **8001**: Main database server
- **8002**: Alternative server
- **3000**: Frontend development server

## 📚 Documentation

- [API Documentation](docs/API.md)
- [Features](docs/FEATURES.md)
- [Setup Guide](docs/SETUP.md)
- [Migration Guide](MIGRATION_GUIDE.md)

## 🔄 Migration from In-Memory to Database

1. Run migration script: `python migrate_to_database.py`
2. Switch to database server: `python main_dynamic.py`
3. Verify persistence: Login, create ticket, reload page

This structure provides a clean, organized, and maintainable codebase for the IT support system.
