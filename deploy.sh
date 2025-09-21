#!/bin/bash

# IT Support System Deployment Script
echo "🚀 Deploying IT Support System..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    print_warning ".env file not found. Creating from template..."
    cp env.example .env
    print_warning "Please edit .env file with your configuration before continuing."
    read -p "Press Enter to continue after editing .env file..."
fi

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p ssl
mkdir -p logs

# Build and start services
print_status "Building and starting services..."
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Wait for services to be ready
print_status "Waiting for services to start..."
sleep 30

# Check service health
print_status "Checking service health..."

# Check backend
if curl -f http://localhost:8001/health > /dev/null 2>&1; then
    print_success "Backend service is running on http://localhost:8001"
else
    print_error "Backend service is not responding"
fi

# Check frontend
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    print_success "Frontend service is running on http://localhost:3000"
else
    print_error "Frontend service is not responding"
fi

# Check nginx
if curl -f http://localhost > /dev/null 2>&1; then
    print_success "Nginx proxy is running on http://localhost"
else
    print_warning "Nginx proxy is not responding (this is optional)"
fi

# Show service status
print_status "Service Status:"
docker-compose ps

echo ""
print_success "🎉 Deployment completed!"
echo ""
echo "📋 Access Information:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8001"
echo "   API Docs: http://localhost:8001/docs"
echo "   Nginx Proxy: http://localhost (if enabled)"
echo ""
echo "🔑 Default Login Credentials:"
echo "   Admin: admin / admin123"
echo "   Agent: agent / agent123"
echo "   Customer: customer / customer123"
echo ""
echo "📊 Features Available:"
echo "   ✅ Real-time system monitoring"
echo "   ✅ AI-powered chatbot"
echo "   ✅ Auto-triage system"
echo "   ✅ Role-based access control"
echo "   ✅ WebSocket real-time updates"
echo "   ✅ Secure authentication"
echo ""
echo "🛠️ Management Commands:"
echo "   View logs: docker-compose logs -f"
echo "   Stop services: docker-compose down"
echo "   Restart services: docker-compose restart"
echo "   Update services: docker-compose pull && docker-compose up -d"
echo ""
print_success "Your IT Support System is now live! 🚀"


