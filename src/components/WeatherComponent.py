from . import Stack, StackAlignment
from app import context
from helpers import AsciiBitmapFont
from helpers.weather import WeatherApi, WeatherLocation
from . import Icon, TextComponent, Placement
from assets import get_asset_path


class WeatherComponent(Stack):
	def __init__(self, location: WeatherLocation|None = None, alignment: StackAlignment = "center_center", temperature_color: tuple[int, int, int, int]|str = '#ffffff', temperature_font: AsciiBitmapFont = AsciiBitmapFont.DEFAULT, name: str|None = None, placement: Placement|None = None):
		location = location or context.weather_location.get()
		self._weather_api: WeatherApi = WeatherApi(location)
		
		self.type_icon = Icon(name="weather_type_icon", path=get_asset_path("loading.icon.toml"))
		self.temperature_text = TextComponent(name="temperature_text", text="", color=temperature_color, font=temperature_font)

		super().__init__(
			name = name,
			placement = placement,
			children = [self.type_icon, self.temperature_text],
			direction = 'vertical',
			alignment = alignment,
			spacing = 1/16,
			padding = 1/16,
		)
		
		# TODO: wind speed bar as separate component

	def update(self):
		super().update()
		weather = self._weather_api.latest_current
		if weather is None:
			self.temperature_text.placement.enabled = False
			self.type_icon.path = get_asset_path("loading.icon.toml")
			return

		self.temperature_text.placement.enabled = True
		self.type_icon.path = get_asset_path(f"weather/rain.icon.toml") # TODO: select actual icon
		self.temperature_text.text = f"{round(weather.temperature)}°C"