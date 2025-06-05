import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from services.weather_service import weather_service

def format_timestamp(timestamp: int) -> str:
    """Convert Unix timestamp to readable date and time."""
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def test_weather_service():
    """Test the weather service with a sample city using OpenWeatherMap 3.0 API."""
    # Load environment variables
    load_dotenv()
    
    # Check if API key is set
    if not os.getenv("OPENWEATHER_API_KEY"):
        print("ERROR: OPENWEATHER_API_KEY is not set in your .env file")
        print("Get your API key from: https://openweathermap.org/api")
        print("Then add this to your .env file:")
        print("OPENWEATHER_API_KEY=your_api_key_here")
        return
    
    # Test with a known city
    city = "London,GB"  # Adding country code for better accuracy
    print(f"Fetching weather for {city}...\n")
    
    try:
        # Get weather data
        result = weather_service.get_weather_by_city(city)
        
        # Print results
        if result['status'] == 'success':
            data = result['data']
            
            print("=== Weather Information ===")
            print(f"Location: {result['location']}")
            print(f"Current Time: {format_timestamp(data['timezone_offset'])}")
            print(f"Temperature: {data['temperature']:.1f}°C (Feels like {data['feels_like']:.1f}°C)")
            print(f"Conditions: {data['weather']} - {data['description']}")
            print(f"Humidity: {data['humidity']}%")
            print(f"Pressure: {data['pressure']} hPa")
            print(f"Wind: {data['wind_speed']} m/s at {data['wind_deg']}°")
            if 'wind_gust' in data and data['wind_gust']:
                print(f"Wind Gust: {data['wind_gust']} m/s")
            print(f"Cloud Cover: {data['clouds']}%")
            print(f"Visibility: {data['visibility']}m")
            print(f"UV Index: {data['uvi']}")
            print(f"Dew Point: {data['dew_point']}°C")
            print(f"Sunrise: {format_timestamp(data['sunrise'])}")
            print(f"Sunset: {format_timestamp(data['sunset'])}")
            print(f"Timezone: {data['timezone']}")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        if 'data' in locals():
            print(f"Response data: {data}")

if __name__ == "__main__":
    test_weather_service()
