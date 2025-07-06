#!/bin/bash
# Docker Compose startup script for the weather MCP server

echo "🌤️  Starting Weather MCP Server with Docker Compose..."
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

# Test the weather service
echo "🧪 Testing weather service with your coordinates (52.237049, 21.017532)..."
sleep 5

# Test current weather
echo "Testing current weather endpoint..."
curl -s "http://localhost:8001/current/52.237049/21.017532" | jq -r '.current' 2>/dev/null || echo "Service starting up..."

echo ""
echo "✅ Docker Compose setup complete!"
echo ""
echo "📋 Available services:"
echo "   - n8n:              http://localhost:5678"
echo "   - Weather MCP:      http://localhost:8001"
echo "   - Mix Server:       http://localhost:8000"
echo ""
echo "🌤️  Weather API endpoints:"
echo "   - Current weather:  http://localhost:8001/current/52.237049/21.017532"
echo "   - Forecast:         http://localhost:8001/forecast/52.237049/21.017532"
echo "   - Health check:     http://localhost:8001/health"
echo ""
echo "🔧 To view logs: docker-compose logs -f"
echo "🛑 To stop all:  docker-compose down"
