
# Weather MCP Server

MCP server for fetching current weather data for a specified city using the MET Norway API (no API key required).

## Features

- Fetch current weather for any city worldwide
- Uses free MET Norway API (no API key required)
- Geocoding via OpenStreetMap Nominatim
- Returns temperature, humidity, pressure, wind speed, and more

## Requirements

- Python 3.12 or newer
- No API key required

## Installation

1. Navigate to the weather-mcp-server directory:

```bash
cd mcp_servers/weather-mcp-server
```

2. Install dependencies:

```bash
uv pip install -e .
```

## Usage

### Test the weather function

```bash
uv run server.py --test
```

### As stdio server (default)

```bash
uv run server.py
```

### As HTTP server (FastAPI + FastMCP)

```bash
uv run server.py --http
```

After starting the HTTP server, the API will be available at: `http://127.0.0.1:8000/mcp`

## Available MCP Tools

### get_current_weather

Fetches current weather for the specified city using MET Norway API.

**Parameters:**
- `city` (string): City name (e.g., "London", "New York", "Warsaw")

**Returns:**
- `city`: City name
- `latitude`: Geographic latitude
- `longitude`: Geographic longitude  
- `air_temperature`: Temperature in Celsius
- `humidity`: Relative humidity percentage
- `pressure`: Air pressure at sea level (hPa)
- `wind_speed`: Wind speed (m/s)
- `wind_direction`: Wind direction (degrees)
- `cloud_area_fraction`: Cloud coverage percentage

**Example usage in n8n:**

```javascript
// In a Code node in n8n
return await $mcp.call("WeatherServer", "get_current_weather", {
  city: "London"
});
```

## Integration with n8n

To integrate this MCP server with n8n:

1. Start the server in HTTP mode: `uv run server.py --http`
2. Configure the MCP connection in n8n with the server address: `http://127.0.0.1:8000/mcp`
3. Use the `get_current_weather` tool in Code nodes in n8n

## Data Sources

- **Weather Data**: [MET Norway API](https://api.met.no/) - Free weather data from the Norwegian Meteorological Institute
- **Geocoding**: [OpenStreetMap Nominatim](https://nominatim.openstreetmap.org/) - Free geocoding service

## License

MIT