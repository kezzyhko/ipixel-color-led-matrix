from contextvars import ContextVar
from helpers.weather import WeatherLocation


locale_code: ContextVar[str] = ContextVar('locale', default='en')
weather_location: ContextVar[WeatherLocation] = ContextVar('weather_location')
