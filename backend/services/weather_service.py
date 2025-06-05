import os
import logging
from typing import Dict, Any, Optional
import requests
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class WeatherService:
    """Service for fetching weather data from OpenWeatherMap API."""
    
    def __init__(self):
        """Initialize the weather service with API key and base URLs."""
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/3.0/onecall"
        self.geo_url = "http://api.openweathermap.org/geo/1.0/direct"
        
        if not self.api_key:
            logger.warning("OPENWEATHER_API_KEY not found in environment variables")
    
    def _get_coordinates(self, city: str, country_code: Optional[str] = None) -> Optional[Dict[str, float]]:
        """
        Get latitude and longitude for a city using geocoding.
        
        Args:
            city: Name of the city
            country_code: Optional country code (e.g., 'US' for United States)
            
        Returns:
            Dict containing 'lat' and 'lon' or None if not found
        """
        try:
            params = {
                'q': f"{city},{country_code}" if country_code else city,
                'limit': 1,
                'appid': self.api_key
            }
            
            response = requests.get(self.geo_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if not data or not isinstance(data, list) or len(data) == 0:
                logger.error(f"Location not found: {city}")
                return None
                
            return {
                'lat': data[0].get('lat'),
                'lon': data[0].get('lon'),
                'name': data[0].get('name', city),
                'country': data[0].get('country', '')
            }
            
        except Exception as e:
            logger.error(f"Error in geocoding: {str(e)}")
            return None
            
    def get_weather_by_city(self, city: str, country_code: Optional[str] = None) -> Dict[str, Any]:
        """
        Get current weather data for a city using OpenWeatherMap 3.0 One Call API.
        
        Args:
            city: Name of the city
            country_code: Optional country code (e.g., 'US' for United States)
            
        Returns:
            Dict containing weather data or error information
        """
        if not self.api_key:
            return {
                'status': 'error',
                'error': 'OpenWeatherMap API key not configured'
            }
            
        try:
            # First, get coordinates for the city
            location = self._get_coordinates(city, country_code)
            if not location:
                return {
                    'status': 'error',
                    'error': f'Could not find coordinates for {city}'
                }
            
            # Build query parameters for One Call API 3.0
            params = {
                'lat': location['lat'],
                'lon': location['lon'],
                'appid': self.api_key,
                'units': 'metric',  # Get temperature in Celsius
                'lang': 'en',       # Get weather description in English
                'exclude': 'minutely,hourly,daily,alerts'  # We only want current weather
            }
            
            # Make API request to One Call API
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Format the location name
            location_name = f"{location['name']}, {location['country']}" if location.get('country') else location['name']
            
            # Extract and format weather data
            weather_data = self._format_weather_data(data, location_name)
            return {
                'status': 'success',
                'location': location_name,
                'data': weather_data
            }
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Error fetching weather data: {str(e)}"
            logger.error(error_msg)
            return {
                'status': 'error',
                'error': error_msg
            }
        except (KeyError, IndexError) as e:
            error_msg = f"Unexpected response format from weather API: {str(e)}"
            logger.error(f"{error_msg}\nResponse: {data if 'data' in locals() else 'No data'}")
            return {
                'status': 'error',
                'error': error_msg
            }
    
    def _format_weather_data(self, data: Dict[str, Any], location: str) -> Dict[str, Any]:
        """
        Format raw weather data from One Call API 3.0 into a more usable structure.
        
        Args:
            data: Raw weather data from the One Call API
            location: Location name
            
        Returns:
            Formatted weather data
        """
        try:
            current = data.get('current', {})
            weather = current.get('weather', [{}])[0] if current.get('weather') else {}
            
            return {
                'location': location,
                'temperature': current.get('temp'),
                'feels_like': current.get('feels_like'),
                'pressure': current.get('pressure'),
                'humidity': current.get('humidity'),
                'dew_point': current.get('dew_point'),
                'uvi': current.get('uvi'),  # UV index
                'clouds': current.get('clouds'),
                'visibility': current.get('visibility'),
                'wind_speed': current.get('wind_speed'),
                'wind_deg': current.get('wind_deg'),
                'wind_gust': current.get('wind_gust'),
                'weather': weather.get('main'),
                'description': weather.get('description', '').capitalize(),
                'sunrise': current.get('sunrise'),
                'sunset': current.get('sunset'),
                'timezone': data.get('timezone'),
                'timezone_offset': current.get('dt')
            }
        except Exception as e:
            logger.error(f"Error formatting weather data: {e}")
            return {}

# Create a singleton instance
weather_service = WeatherService()
