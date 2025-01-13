import os
import json
import boto3
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class WeatherDashboard:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.bucket_name = os.getenv('AWS_BUCKET_NAME')
        self.s3_client = boto3.client('s3')

    def create_bucket_if_not_exists(self):
        """Create S3 bucket if it doesn't exist"""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            print(f"Bucket {self.bucket_name} exists")
        except:
            print(f"Creating bucket {self.bucket_name}")
        try:
            self.s3_client.create_bucket(Bucket=self.bucket_name)
            print(f"Successfully created bucket {self.bucket_name}")
        except Exception as e:
            print(f"Error creating bucket: {e}")

    def fetch_weather(self, city):
        """Fetch weather data from OpenWeather API"""
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "imperial"
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None

    def save_to_s3(self, weather_data):
        """Save aggregated weather data to S3 bucket"""
        if not weather_data:
            return False

        # Generate a timestamp for uniqueness
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        file_name = f"weather-data/daily-summary-{timestamp}.json"

        try:
            # Save the file to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_name,
                Body=json.dumps(weather_data),
                ContentType='application/json'
            )
            print(f"Successfully saved aggregated weather data to S3: {file_name}")
            return True
        except Exception as e:
            print(f"Error saving to S3: {e}")
            return False

def main():
    dashboard = WeatherDashboard()

    # Create bucket if needed
    dashboard.create_bucket_if_not_exists()

    cities = ["Honolulu", "Helsinki", "Houston", "Hilo"]
    aggregated_data = {}

    for city in cities:
        print(f"\nFetching weather for {city}...")
        weather_data = dashboard.fetch_weather(city)
        if weather_data:
            temp = weather_data['main']['temp']
            feels_like = weather_data['main']['feels_like']
            humidity = weather_data['main']['humidity']
            description = weather_data['weather'][0]['description']
            wind_speed_mph = weather_data['wind']['speed']
            sunrise_timestamp = weather_data['sys']['sunrise']
            sunset_timestamp = weather_data['sys']['sunset']
            timezone_offset = weather_data['timezone']

            # Convert sunrise and sunset timestamps to readable format
            sunrise = datetime.utcfromtimestamp(sunrise_timestamp + timezone_offset).strftime('%Y-%m-%d %H:%M:%S')
            sunset = datetime.utcfromtimestamp(sunset_timestamp + timezone_offset).strftime('%Y-%m-%d %H:%M:%S')

            # Print weather data to screen
            print(f"Temperature: {temp}°F")
            print(f"Feels like: {feels_like}°F")
            print(f"Humidity: {humidity}%")
            print(f"Conditions: {description}")
            print(f"Wind Speed: {wind_speed_mph} mph")
            print(f"Sunrise: {sunrise}")
            print(f"Sunset: {sunset}")

            # Add data to aggregated dictionary
            aggregated_data[city] = {
                "temperature": f"{temp}°F",
                "feels_like": f"{feels_like}°F",
                "humidity": f"{humidity}%",
                "conditions": description,
                "wind_speed": f"{wind_speed_mph} mph",
                "sunrise": sunrise,
                "sunset": sunset
            }
        else:
            print(f"Failed to fetch weather data for {city}")

    # Save aggregated data to S3
    if aggregated_data:
        success = dashboard.save_to_s3(aggregated_data)
        if success:
            print("\nAggregated weather data saved to S3!")
        else:
            print("\nFailed to save aggregated weather data.")

if __name__ == "__main__":
    main()

