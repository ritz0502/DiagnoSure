@echo off
REM ====================================================
REM DiagnoSure - All-in-One Startup Script (Windows)
REM ====================================================
REM This script starts all services: database, backend, frontend, and more

setlocal enabledelayedexpansion

echo ======================================
echo  DiagnoSure System Startup
echo ======================================
echo.

REM Check if Docker is installed
echo Checking Docker installation...
docker --version > nul 2>&1
if %errorlevel% NEQ 0 (
    echo ERROR: Docker is not installed or not in PATH
    echo Please install Docker from https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo ✓ Docker is installed
echo.

REM Navigate to backend directory
cd /d "%~dp0backend"

REM Check if .env exists
if not exist ".env" (
    echo WARNING: .env file not found in backend/
    echo Creating from .env.example...
    if exist "..\env.example" (
        copy "..\env.example" ".env"
        echo ✓ Created .env from .env.example
        echo Please update .env with your configuration values
    )
)

echo.
echo ======================================
echo 1. Starting Database and Services
echo ======================================
echo.

REM Start Docker containers
echo Starting Docker containers...
docker-compose up -d

if %errorlevel% neq 0 (
    echo ERROR: Failed to start Docker containers
    echo Make sure Docker Desktop is running
    pause
    exit /b 1
)

echo ✓ Docker containers started
echo.

REM Wait for database to be ready
echo Waiting 15 seconds for database to initialize...
timeout /t 15 /nobreak

echo.
echo ======================================
echo 2. Running Database Migrations
echo ======================================
echo.

REM Run migrations inside the web container
docker-compose exec -T web python manage.py makemigrations
if %errorlevel% neq 0 (
    echo WARNING: makemigrations had issues
)

docker-compose exec -T web python manage.py migrate
if %errorlevel% neq 0 (
    echo ERROR: Migration failed
)

echo ✓ Migrations completed
echo.

REM Navigate to frontend directory
cd /d "%~dp0frontend"

echo ======================================
echo 3. Installing Frontend Dependencies
echo ======================================
echo.

if not exist "node_modules" (
    echo Installing npm packages...
    call npm install
    if %errorlevel% neq 0 (
        echo ERROR: npm install failed
        pause
        exit /b 1
    )
    echo ✓ npm packages installed
) else (
    echo ✓ node_modules already exists
)

echo.
echo ======================================
echo 4. Starting Application
echo ======================================
echo.

echo.
echo SERVICES STARTED:
echo ================================================================
echo.
echo ✓ Backend API:        http://localhost:8090
echo   - Home:             http://localhost:8090/api/home/
echo   - Symptom Checker:  http://localhost:8090/api/symptoms/check/ [POST]
echo   - Hospital Search:  http://localhost:8090/api/hospitals/search/ [GET]
echo   - Prescription Upload: http://localhost:8090/api/upload-prescription/ [POST]
echo.
echo ✓ PostgreSQL Database: localhost:5432
echo   - Database: healthcare
echo   - User: postgres
echo   - Password: postgres
echo.
echo ✓ Redis Cache:         localhost:6379
echo.
echo ✓ Frontend (Ready to start):
echo   Run in frontend folder: npm run dev
echo.
echo ================================================================
echo.
echo NEXT STEPS:
echo.
echo 1. Open a new terminal in the 'frontend' directory
echo 2. Run: npm run dev
echo 3. Open http://localhost:5173 in your browser
echo.
echo To view logs:
echo   - Backend: docker-compose logs web
echo   - All services: docker-compose logs -f
echo.
echo To stop all services:
echo   - Run: docker-compose down
echo.
echo ================================================================
echo.

pause
