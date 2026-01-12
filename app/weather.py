"""
Weather tool for the chatbot using Open-Meteo free API (no API key required)
"""
import requests
from langchain.tools import tool


@tool
def get_weather(location: str) -> str:
    """
    Get the current weather for a given location.
    
    Args:
        location: City name or location (e.g., "Madrid", "New York", "London")
    
    Returns:
        A string with the weather information
    """
    try:
        # Get coordinates for the location using Open-Meteo geocoding API
        geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_params = {
            "name": location,
            "count": 1,
            "language": "en",
            "format": "json"
        }
        
        geo_response = requests.get(geocoding_url, params=geo_params)
        geo_data = geo_response.json()
        
        if not geo_data.get("results"):
            return f"Could not find location: {location}"
        
        result = geo_data["results"][0]
        latitude = result["latitude"]
        longitude = result["longitude"]
        place_name = f"{result['name']}, {result.get('country', '')}"
        
        # Get weather for the coordinates
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,weather_code,wind_speed_10m,relative_humidity_2m",
            "timezone": "auto"
        }
        
        weather_response = requests.get(weather_url, params=weather_params)
        weather_data = weather_response.json()
        
        current = weather_data["current"]
        
        # Map WMO weather codes to descriptions
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail"
        }
        
        weather_desc = weather_codes.get(current["weather_code"], "Unknown")
        temp = current['temperature_2m']
        humidity = current['relative_humidity_2m']
        wind_speed = current['wind_speed_10m']
        
        # Return concise, conversational weather data for the LLM to integrate
        result_text = (
            f"In {place_name}, it's currently {temp}°C with {weather_desc.lower()}. "
            f"The humidity is {humidity}% and wind speed is {wind_speed} km/h."
        )
        return result_text
        
    except Exception as e:
        return f"Error fetching weather data: {str(e)}"


# Example usage (for testing)
if __name__ == "__main__":
    print(get_weather("Madrid"))
    print(get_weather("London"))
