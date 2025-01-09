import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def fetch_weather(city, api_key):
    """Fetch weather data from OpenWeather API for a specific city."""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "imperial"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()  # Return full data from the API
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def main():
    # Load the API key from environment variables
    api_key = os.getenv('OPENWEATHER_API_KEY')
    if not api_key:
        print("Error: OPENWEATHER_API_KEY is not set in the environment.")
        return

    city = "Hilo"  # Target city for the weather data
    print(f"Fetching weather data for {city}...")

    # Fetch the weather data
    weather_data = fetch_weather(city, api_key)

    # Print the full API response
    if weather_data:
        print("\nFull Weather Data for Hilo:")
        print(weather_data)  # Prints all JSON data returned by the API
    else:
        print("Failed to fetch weather data for Hilo.")

if __name__ == "__main__":
    main()
