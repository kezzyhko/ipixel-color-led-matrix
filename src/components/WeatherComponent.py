from . import VStack
from app import context
from helpers.weather import WeatherApi, WeatherLocation


class WeatherComponent(VStack):
	def __init__(self, location: WeatherLocation|None = None):
		super().__init__()
		location = location or context.weather_location.get()
		self._weather_api: WeatherApi = WeatherApi(location)
		# TODO: add precipitation icon, wind speed bar, and temperature text as separate components
		# TODO: add loading icon

	def update(self):
		super().update()
		weather = self._weather_api.latest_current
		is_loading = weather is None
		# TODO: show/hide components
		if is_loading:
			print("Loading weather data...") # TODO: remove
			return
		
		print(weather) # TODO: change other components' properties