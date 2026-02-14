from . import Stack, StackAlignment
from app import context
from helpers import AsciiBitmapFont
from helpers.weather import WeatherApi, WeatherLocation, WeatherTypeInfo, CurrentWeather
from . import Icon, TextComponent, Placement
from assets import get_asset_path
from datetime import datetime


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
		self.temperature_text.text = f"{round(weather.temperature)}°C"
		icon_name = self._get_icon_name(weather)
		self.type_icon.path = get_asset_path(f"weather/{icon_name}.icon.toml")

	def _get_icon_name(self, weather: CurrentWeather) -> str:
		weather_type_info = WeatherTypeInfo.from_code(weather.weathercode)

		# Special case for clear sky - depends on more stuff
		base_icon_name = weather_type_info.type
		if base_icon_name == 'clear':
			hour = datetime.fromisoformat(weather.time).hour # TODO: Use time for actual sunrise/sunset
			is_night_time = hour < 6 or hour >= 19
			base_icon_name = "moon" if is_night_time else "sun" #TODO: Include lunar phase? Detect rotation of moon based on location??
		
		# Choose power name
		match weather_type_info.power:
			case p if p > 0.66:
				power_name = "severe"
			case p if p > 0.33:
				power_name = "moderate"
			case p if p > 0.00:
				power_name = "light"
			case _:
				power_name = None

		# Choose and return icon name
		icon_name = base_icon_name
		if power_name:
			icon_name += f"_{power_name}"
		return icon_name
