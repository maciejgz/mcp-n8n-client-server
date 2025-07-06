@echo off
echo Starting n8n with MCP servers...
echo.

rem Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not running. Please start Docker Desktop first.
    pause
    exit /b 1
)

rem Start services
echo Building and starting services...
docker-compose up --build -d

rem Wait a moment for services to start
echo Waiting for services to start...
timeout /t 10 /nobreak >nul

rem Check service status
echo.
echo Checking service status...
docker-compose ps

rem Show logs
echo.
echo Recent logs:
docker-compose logs --tail=20

echo.
echo Services started successfully!
echo n8n is available at: http://localhost:5678
echo MCP Mix Server is available at: http://localhost:8000
echo Weather MCP Server is available at: http://localhost:8001
echo.
echo To stop services: docker-compose down
echo To view logs: docker-compose logs -f
echo.
pause
