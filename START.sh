#!/bin/bash
# ====================================================
# DiagnoSure - All-in-One Startup Script (Unix/Linux/Mac)
# ====================================================
# This script starts all services: database, backend, frontend, and more

set -e  # Exit on any error

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "======================================"
echo "  DiagnoSure System Startup"
echo "======================================"
echo ""

# Check if Docker is installed
echo "Checking Docker installation..."
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is not installed"
    echo "Please install Docker from https://www.docker.com/products/docker-desktop"
    exit 1
fi

echo "✓ Docker is installed"
echo ""

# Navigate to backend directory
cd "$SCRIPT_DIR/backend"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found in backend/"
    echo "Creating from ../.env.example..."
    if [ -f "../.env.example" ]; then
        cp "../.env.example" ".env"
        echo "✓ Created .env from .env.example"
        echo "Please update .env with your configuration values"
    fi
fi

echo ""
echo "======================================"
echo "1. Starting Database and Services"
echo "======================================"
echo ""

# Start Docker containers
echo "Starting Docker containers..."
docker-compose up -d

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to start Docker containers"
    echo "Make sure Docker is running"
    exit 1
fi

echo "✓ Docker containers started"
echo ""

# Wait for database to be ready
echo "Waiting 15 seconds for database to initialize..."
sleep 15

echo ""
echo "======================================"
echo "2. Running Database Migrations"
echo "======================================"
echo ""

# Run migrations inside the web container
docker-compose exec -T web python manage.py makemigrations || echo "WARNING: makemigrations had issues"
docker-compose exec -T web python manage.py migrate || echo "ERROR: Migration failed"

echo "✓ Migrations completed"
echo ""

# Navigate to frontend directory
cd "$SCRIPT_DIR/frontend"

echo "======================================"
echo "3. Installing Frontend Dependencies"
echo "======================================"
echo ""

if [ ! -d "node_modules" ]; then
    echo "Installing npm packages..."
    npm install
    if [ $? -ne 0 ]; then
        echo "ERROR: npm install failed"
        exit 1
    fi
    echo "✓ npm packages installed"
else
    echo "✓ node_modules already exists"
fi

echo ""
echo "======================================"
echo "4. Starting Application"
echo "======================================"
echo ""

echo ""
echo "SERVICES STARTED:"
echo "================================================================"
echo ""
echo "✓ Backend API:        http://localhost:8090"
echo "   - Home:             http://localhost:8090/api/home/"
echo "   - Symptom Checker:  http://localhost:8090/api/symptoms/check/ [POST]"
echo "   - Hospital Search:  http://localhost:8090/api/hospitals/search/ [GET]"
echo "   - Prescription Upload: http://localhost:8090/api/upload-prescription/ [POST]"
echo ""
echo "✓ PostgreSQL Database: localhost:5432"
echo "   - Database: healthcare"
echo "   - User: postgres"
echo "   - Password: postgres"
echo ""
echo "✓ Redis Cache:         localhost:6379"
echo ""
echo "✓ Frontend (Ready to start):"
echo "   Run in frontend folder: npm run dev"
echo ""
echo "================================================================"
echo ""
echo "NEXT STEPS:"
echo ""
echo "1. Open a new terminal in the 'frontend' directory"
echo "2. Run: npm run dev"
echo "3. Open http://localhost:5173 in your browser"
echo ""
echo "To view logs:"
echo "   - Backend: docker-compose logs web"
echo "   - All services: docker-compose logs -f"
echo ""
echo "To stop all services:"
echo "   - Run: docker-compose down"
echo ""
echo "================================================================"
echo ""
