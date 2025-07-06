# n8n Multi-Language Automation Workspace

This workspace provides a robust environment for building, running, and integrating automation workflows using n8n, Python, and Node.js. It includes:
- n8n workflow automation (Docker-based)
- Python scripts and tools for data processing
- MCP (Model Context Protocol) servers for advanced data and AI workflows
- Example workflows and configuration for rapid prototyping
- Utilities for local and cloud deployment


---

## Project Structure

```
├── compose.yaml                # Docker Compose configuration for n8n and MCP servers
├── Dockerfile.n8n              # Dockerfile for n8n customizations
├── js_scripts/                 # Node.js scripts for automation
├── local-files/                # Local data and files (gitignored)
├── mcp_servers/                # MCP (Model Context Protocol) servers
│   ├── mix-server/             # Example: Mix server (Python)
│   └── weather/                # Weather MCP server (Python, FastAPI)
├── nginx-config/               # Nginx configuration for reverse proxy
├── python_scripts/             # Standalone Python scripts (e.g., stock fetcher)
├── workflows/                  # Example n8n workflow JSON files
├── start_compose.sh            # Shell script to start all services (Linux/macOS)
├── start_n8n.bat               # Batch script to start all services (Windows)
└── README.md                   # This file
```

## How to Run the Project

### 1. Prerequisites
- Docker and Docker Compose installed
- (Optional) Python 3.12+ for running scripts directly

### 2. Start All Services (Recommended)

#### On Windows
Run in PowerShell or Command Prompt:
```bat
start_n8n.bat
```

#### On Linux/macOS
```bash
./start_compose.sh
```

#### Manual Start (Any OS)
```bash
docker-compose up -d
```

Access n8n at: http://localhost:5678

### 3. Running Python Scripts
Navigate to `python_scripts/` and run:
```bash
python orlen_stock_fetcher.py
```

### 4. Running MCP Servers Directly
Navigate to the desired MCP server directory (e.g., `mcp_servers/weather/`) and follow the instructions in its `README.md` or usage guide.

## Key Files and Scripts

- `compose.yaml`: Main Docker Compose configuration
- `start_n8n.bat` / `start_compose.sh`: Scripts to start all services
- `mcp_servers/weather/README.md`, `MCP_USAGE_GUIDE.md`: Weather MCP server usage and API
- `python_scripts/orlen_stock_fetcher.py`: Example Python script for stock data
- `workflows/`: Example n8n workflow JSON files for import

## Example Workflow

Import example workflows from the `workflows/` directory into n8n to get started quickly. For weather automation, see `workflows/weather_mcp_example.json`.

---

See below for setup and configuration instructions.

---

### Run n8n locally in the main directory
```bash
docker-compose up -d 
```

Access n8n at http://localhost:5678


### Configuration of the mikrus.xyz server
New unix accounts:
```bash
sudo passwd root
sudo adduser mgzik
sudo usermod -aG sudo mgzik

w pliku /etc/ssh/sshd_config:
PermitRootLogin no

sudo systemctl restart sshd
```


Generate a self-signed SSL certificate for the domain xyz
```bash
## create self-signed SSL certificate
sudo openssl genrsa -out /etc/ssl/private/xyz.key 2048
sudo openssl req -new -x509 -key /etc/ssl/private/xyz.key -out /etc/ssl/certs/xyz.crt -days 760


## Create nginx configuration file for n8n
```bash
sudo vim /etc/nginx/sites-available/n8n
sudo ln -s /etc/nginx/sites-available/n8n /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl reload nginx
```
