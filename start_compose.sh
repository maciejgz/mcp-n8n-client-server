#!/bin/bash
# Docker Compose startup script

echo "🚀 Starting n8n with Docker Compose..."
echo "================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "compose.yaml" ]; then
    echo "❌ compose.yaml not found. Please run this script from the n8n workspace root."
    exit 1
fi

# Build and start the services
echo "🏗️  Building and starting all services..."
docker-compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service status
echo "🔍 Checking service status..."
docker-compose ps

# No endpoint tests needed

echo ""
echo "✅ Docker Compose setup complete!"
echo ""
echo "📋 Available services:"
echo "   - n8n:              http://localhost:5678"
echo "   - Mix Server:       http://localhost:8000"
echo ""
echo "🔧 To view logs: docker-compose logs -f"
echo "🛑 To stop all:  docker-compose down"
