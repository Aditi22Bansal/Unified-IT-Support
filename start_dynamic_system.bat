@echo off
echo ========================================
echo  Dynamic IT Support System Startup
echo ========================================
echo.

echo [1/4] Starting Backend Services...
cd backend
echo Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error installing Python dependencies
    pause
    exit /b 1
)

echo Setting up Prisma database...
prisma generate
if %errorlevel% neq 0 (
    echo Error generating Prisma client
    pause
    exit /b 1
)

prisma db push
if %errorlevel% neq 0 (
    echo Error setting up database
    pause
    exit /b 1
)

echo Initializing database with sample data...
python init_database.py
if %errorlevel% neq 0 (
    echo Error initializing database
    pause
    exit /b 1
)

echo Starting backend server...
start "Backend Server" cmd /k "python main_dynamic.py"

echo.
echo [2/4] Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo.
echo [3/4] Starting Frontend Services...
cd ..\frontend
echo Installing Node.js dependencies...
npm install
if %errorlevel% neq 0 (
    echo Error installing Node.js dependencies
    pause
    exit /b 1
)

echo Starting frontend development server...
start "Frontend Server" cmd /k "npm start"

echo.
echo [4/4] System Status Check...
timeout /t 10 /nobreak > nul

echo.
echo ========================================
echo  System Startup Complete!
echo ========================================
echo.
echo 🌐 Frontend: http://localhost:3000
echo 🔧 Backend API: http://127.0.0.1:8001
echo 📚 API Docs: http://127.0.0.1:8001/docs
echo.
echo 🔑 Default Login Credentials:
echo    Admin: admin / admin123
echo    Agent: agent / agent123
echo    Customer: customer / customer123
echo.
echo ✨ Features Enabled:
echo    - Real-time system monitoring
echo    - Auto-triage and SLA tracking
echo    - Role-based access control
echo    - AI-powered chatbot
echo    - WebSocket real-time updates
echo    - Dynamic dashboards
echo.
echo Press any key to close this window...
pause > nul


