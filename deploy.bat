@echo off
echo ========================================
echo  IT Support System Deployment
echo ========================================
echo.

echo [1/6] Checking Docker installation...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not installed or not in PATH
    echo Please install Docker Desktop first
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker Compose is not installed or not in PATH
    echo Please install Docker Compose first
    pause
    exit /b 1
)

echo Docker and Docker Compose are installed ✓
echo.

echo [2/6] Checking environment configuration...
if not exist .env (
    echo WARNING: .env file not found. Creating from template...
    copy env.example .env
    echo.
    echo Please edit .env file with your configuration:
    echo - OPENAI_API_KEY: Your OpenRouter API key
    echo - JWT_SECRET: A secure secret key
    echo - Other settings as needed
    echo.
    pause
)

echo Environment configuration ready ✓
echo.

echo [3/6] Creating necessary directories...
if not exist ssl mkdir ssl
if not exist logs mkdir logs
echo Directories created ✓
echo.

echo [4/6] Stopping existing services...
docker-compose down
echo Existing services stopped ✓
echo.

echo [5/6] Building and starting services...
echo This may take a few minutes...
docker-compose build --no-cache
if %errorlevel% neq 0 (
    echo ERROR: Failed to build services
    pause
    exit /b 1
)

docker-compose up -d
if %errorlevel% neq 0 (
    echo ERROR: Failed to start services
    pause
    exit /b 1
)

echo Services built and started ✓
echo.

echo [6/6] Waiting for services to initialize...
timeout /t 30 /nobreak >nul

echo.
echo ========================================
echo  Deployment Complete!
echo ========================================
echo.
echo 🌐 Access Information:
echo    Frontend: http://localhost:3000
echo    Backend API: http://localhost:8001
echo    API Documentation: http://localhost:8001/docs
echo    Nginx Proxy: http://localhost (if enabled)
echo.
echo 🔑 Default Login Credentials:
echo    Admin: admin / admin123
echo    Agent: agent / agent123
echo    Customer: customer / customer123
echo.
echo ✨ Features Available:
echo    ✅ Professional landing page
echo    ✅ Secure authentication with Google OAuth
echo    ✅ Real-time system monitoring
echo    ✅ AI-powered chatbot
echo    ✅ Auto-triage system
echo    ✅ Role-based access control
echo    ✅ WebSocket real-time updates
echo    ✅ Cybersecurity features
echo.
echo 🛠️ Management Commands:
echo    View logs: docker-compose logs -f
echo    Stop services: docker-compose down
echo    Restart services: docker-compose restart
echo    Update services: docker-compose pull ^&^& docker-compose up -d
echo.
echo 🚀 Your IT Support System is now live!
echo.
pause




