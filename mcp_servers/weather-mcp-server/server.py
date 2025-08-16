import argparse
from typing import Dict, Any
import requests

from fastmcp import FastMCP

# Create MCP server
mcp = FastMCP(
    name="WeatherServer",
    dependencies=["requests"]
)


# MET Norway API endpoint (no API key required)
MET_API_URL = "https://api.met.no/weatherapi/locationforecast/2.0/compact"

# OpenStreetMap Nominatim endpoint for geocoding
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"


def _get_current_weather_impl(city: str) -> Dict[str, Any]:
    """
    Implementation of get_current_weather function.
    Fetches current weather for the given city using MET Norway API (no API key required).
    Args:
        city: Name of the city to fetch weather for
    Returns:
        Dictionary containing weather data or error
    """

    # Geocode city name to lat/lon using OpenStreetMap Nominatim
    geocode_params = {"q": city, "format": "json", "limit": 1}
    try:
        geo_resp = requests.get(
            NOMINATIM_URL,
            params=geocode_params,
            headers={"User-Agent": "weather-mcp-server/1.0"},
        )
        geo_resp.raise_for_status()
        geo_data = geo_resp.json()
        if not geo_data:
            return {"error": f"City '{city}' not found."}
        lat = geo_data[0]["lat"]
        lon = geo_data[0]["lon"]
        # Fetch weather from MET Norway
        met_params = {"lat": lat, "lon": lon}
        met_resp = requests.get(
            MET_API_URL,
            params=met_params,
            headers={"User-Agent": "weather-mcp-server/1.0"},
        )
        met_resp.raise_for_status()
        met_data = met_resp.json()
        # Extract current weather (first timeseries entry)
        timeseries = met_data.get("properties", {}).get("timeseries", [])
        if not timeseries:
            return {"error": "No weather data available."}
        current = timeseries[0]["data"]["instant"]["details"]
        weather_data = {
            "city": city,
            "latitude": lat,
            "longitude": lon,
            "air_temperature": current.get("air_temperature"),
            "humidity": current.get("relative_humidity"),
            "pressure": current.get("air_pressure_at_sea_level"),
            "wind_speed": current.get("wind_speed"),
            "wind_direction": current.get("wind_from_direction"),
            "cloud_area_fraction": current.get("cloud_area_fraction"),
        }
        return weather_data
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_current_weather(city: str) -> Dict[str, Any]:
    """
    Fetches current weather for the given city using MET Norway API (no API key required).
    Args:
        city: Name of the city to fetch weather for
    Returns:
        Dictionary containing weather data or error
    """
    return _get_current_weather_impl(city)



def test_get_current_weather():
    """
    Simple test for get_current_weather. Prints result for a sample city.
    """
    city = "London"
    print(f"Testing get_current_weather for city: {city}")
    result = _get_current_weather_impl(city)
    print("Result:", result)

def main():
    parser = argparse.ArgumentParser(description="Weather MCP Server")
    parser.add_argument("--http", action="store_true", help="Run as HTTP server")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--test", action="store_true", help="Run test for get_current_weather")
    args = parser.parse_args()
    if args.test:
        test_get_current_weather()
        return
    if args.http:
        mcp.run(transport="http", host=args.host, port=args.port)
    else:
        print("Starting stdio server")
        mcp.run()

if __name__ == "__main__":
    main()
