from . import Stack
from app import context
from helpers.weather import WeatherApi, WeatherLocation
from . import TextComponent
from . import Icon
from assets import get_asset_path


class WeatherComponent(Stack):
	def __init__(self, location: WeatherLocation|None = None):
		super().__init__("vertical")
		location = location or context.weather_location.get()
		self._weather_api: WeatherApi = WeatherApi(location)
		
		self.temperature_text = TextComponent("  ", font_size=5) # TODO: size
		self.temperature_text.x = 2
		self.temperature_text.y = 9
		self.add_child(self.temperature_text)
		
		self.type_icon = Icon(get_asset_path("weather/rain.icon.toml")) # TODO: size
		self.type_icon.x = 4
		self.type_icon.y = 0
		self.add_child(self.type_icon)
		
		# TODO: add precipitation icon, wind speed bar, and temperature text as separate components
		# TODO: add loading icon

	def update(self):
		super().update()
		weather = self._weather_api.latest_current
		is_loading = weather is None
		# TODO: show/hide components
		if is_loading:
			return

		self.temperature_text.text = f"{round(weather.temperature)}°C"
		# TODO: change other components' properties