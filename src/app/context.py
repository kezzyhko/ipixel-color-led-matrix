from contextvars import ContextVar
from typing import Literal
import locale
from helpers import WeatherApi


locale_code: ContextVar[str] = ContextVar('locale', default='en')
weather_api: ContextVar[WeatherApi] = ContextVar('weather_api')
