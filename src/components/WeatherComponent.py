from . import Stack, StackAlignment
from app import context
from helpers import AsciiBitmapFont
from helpers.weather import WeatherApi, WeatherLocation, WeatherTypeInfo
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
		self.temperature_text.text = f"{round(weather.temperature)}°C"
		icon_name = self._get_icon_name(weather.weathercode)
		self.type_icon.path = get_asset_path(f"weather/{icon_name}.icon.toml")

	def _get_icon_name(self, weathercode: int) -> str:
		weather_type_info = WeatherTypeInfo.from_code(weathercode)
		
		match weather_type_info.power:
			case p if p > 0.66:
				power_name = "heavy"
			case p if p > 0.33:
				power_name = "medium"
			case p if p > 0.00:
				power_name = "light"
			case _:
				power_name = None

		icon_name = weather_type_info.type
		if power_name:
			icon_name += f"_{power_name}"
		return icon_name
