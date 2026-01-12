from . import VStack
import python_weather
from app import context
from helpers import WeatherApi


class WeatherComponent(VStack):
	def __init__(self):
		super().__init__()
		self._weather_api: WeatherApi = context.weather_api.get()
		# TODO: add precipitation icon, wind speed bar, and temperature text as separate components
		# TODO: add loading icon

	def update(self):
		super().update()
		forecast = self._weather_api.forecast
		is_loading = forecast is None
		# TODO: show/hide components
		if is_loading:
			return
		print(forecast.temperature, forecast.precipitation, forecast.wind_speed) # TODO: change components' properties
