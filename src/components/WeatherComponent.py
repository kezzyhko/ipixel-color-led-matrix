from . import Stack
from app import context
from helpers import AsciiBitmapFont
from helpers.weather import WeatherApi, WeatherLocation, WeatherTypeInfo, CurrentWeather
from . import Icon, TextComponent, Placement
from assets import get_asset_path
from datetime import datetime


class WeatherComponent(Stack):
	def __init__(self, location: WeatherLocation|None = None, temperature_color: tuple[int, int, int, int]|str = '#ffffff', temperature_font: AsciiBitmapFont = AsciiBitmapFont.DEFAULT, name: str|None = None, placement: Placement|None = None):
		location = location or context.weather_location.get()
		self._weather_api: WeatherApi = WeatherApi(location)
		
		self.type_icon = Icon(name="weather_type_icon", path=get_asset_path("loading.icon.toml"))
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
		
		# TODO: wind speed bar as separate component

	def update(self):
		super().update()
		weather = self._weather_api.latest_current
		if weather is None:
			self.temperature_text.placement.enabled = False
			self.type_icon.path = get_asset_path("loading.icon.toml")
			return

		self.temperature_text.placement.enabled = True
		self.temperature_text.text = f"{round(weather.temperature)}°C"
		icon_name = self._get_icon_name(weather)
		self.type_icon.path = get_asset_path(f"weather/{icon_name}.icon.toml")

	def _get_icon_name(self, weather: CurrentWeather) -> str:
		weather_type_info = WeatherTypeInfo.from_code(weather.weathercode)

		# Determine celestial body (sun/moon)
		hour = datetime.fromisoformat(weather.time).hour
		is_night_time = hour < 6 or hour >= 19 # TODO: Use time of the actual sunrise/sunset
		celestial_body = 'moon' if is_night_time else 'sun'
		#TODO: Include lunar phase? Detect rotation of moon based on location??
		
		# Choose power name
		match weather_type_info.power:
			case p if p > 0.66:
				power_name = 'severe'
			case p if p < 0.33:
				power_name = 'light'
			case _:
				power_name = 'moderate'

		# Choose and return icon name
		if weather_type_info.type == 'clear':
			return f"{weather_type_info.type}_{celestial_body}"
		else:
			return f"{weather_type_info.type}_{power_name}"
