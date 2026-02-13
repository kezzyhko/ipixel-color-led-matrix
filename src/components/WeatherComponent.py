from . import Stack
from app import context
from helpers import AsciiBitmapFont
from helpers.weather import WeatherApi, WeatherLocation
from . import Icon, TextComponent, Placement
from assets import get_asset_path


class WeatherComponent(Stack):
	def __init__(self, location: WeatherLocation|None = None, temperature_color: tuple[int, int, int, int]|str = '#ffffff', temperature_font: AsciiBitmapFont = AsciiBitmapFont.DEFAULT, name: str|None = None, placement: Placement|None = None):
		location = location or context.weather_location.get()
		self._weather_api: WeatherApi = WeatherApi(location)
		
		self.type_icon = Icon(name="weather_type_icon", path=get_asset_path("weather/rain.icon.toml"))
		self.temperature_text = TextComponent(name="temperature_text", text="", color=temperature_color, font=temperature_font)

		super().__init__(
			name = name,
			placement = placement,
			children = [self.type_icon, self.temperature_text],
			direction = 'vertical',
			alignment = 'center',
			spacing = 1/16,
			padding = 1/16,
		)
		
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