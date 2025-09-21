# Setup Instructions

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- Docker and Docker Compose (optional)
- Git

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd unified_it_support
   ```

2. **Run the setup script**
   ```bash
   python setup.py
   ```

3. **Configure environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

4. **Start the application**
   ```bash
   docker-compose up
   ```

## Manual Setup

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**
   ```bash
   export DATABASE_URL="sqlite:///./it_support.db"
   export OPENAI_API_KEY="your-openai-api-key"
   export JWT_SECRET_KEY="your-secret-key"
   ```

5. **Run the backend**
   ```bash
   python main.py
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set environment variables**
   ```bash
   export REACT_APP_API_URL="http://localhost:8000"
   ```

4. **Run the frontend**
   ```bash
   npm start
   ```

## Environment Variables

### Required Variables

- `DATABASE_URL`: Database connection string
- `OPENAI_API_KEY`: OpenAI API key for chatbot
- `JWT_SECRET_KEY`: Secret key for JWT tokens

### Optional Variables

- `SMTP_SERVER`: SMTP server for email notifications
- `SMTP_PORT`: SMTP port (default: 587)
- `SMTP_USERNAME`: SMTP username
- `SMTP_PASSWORD`: SMTP password
- `SLACK_WEBHOOK_URL`: Slack webhook for notifications
- `DEBUG`: Enable debug mode (default: False)

## Database Setup

The application uses SQLite by default for development. For production, use PostgreSQL:

1. **Install PostgreSQL**
2. **Create database**
   ```sql
   CREATE DATABASE it_support;
   ```
3. **Update DATABASE_URL**
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/it_support
   ```

## Docker Setup

1. **Build and start containers**
   ```bash
   docker-compose up --build
   ```

2. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Default Users

After first run, create users through the registration interface or use the admin panel.

## Troubleshooting

### Common Issues

1. **Port already in use**
   - Change ports in docker-compose.yml
   - Or stop existing services using those ports

2. **Database connection issues**
   - Check DATABASE_URL format
   - Ensure database server is running
   - Verify credentials

3. **OpenAI API issues**
   - Verify API key is correct
   - Check API quota and billing

4. **Frontend build issues**
   - Clear node_modules and reinstall
   - Check Node.js version compatibility

### Logs

- Backend logs: Check console output or Docker logs
- Frontend logs: Check browser console
- Database logs: Check PostgreSQL logs if using PostgreSQL

## Production Deployment

1. **Use PostgreSQL for production**
2. **Set secure JWT secret key**
3. **Configure proper SMTP settings**
4. **Set up reverse proxy (nginx)**
5. **Enable HTTPS**
6. **Set up monitoring and logging**
7. **Configure backup strategy**

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API documentation at /docs
3. Check the GitHub issues
4. Contact the development team

