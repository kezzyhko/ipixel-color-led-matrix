from . import VStack
from typing import Literal
import python_weather
from python_weather.constants import _Unit as MeasurementUnits
import datetime
from helpers import Timer
from helpers import context


class WeatherComponent(VStack):
	def __init__(
		self, city: str | None = None,
		units: Literal['metric', 'imperial'] | None = None,
		update_interval: datetime.timedelta = datetime.timedelta(minutes=5)
	):
		super().__init__()

		city = city or context.weather_city.get()
		if not city:
			raise ValueError("City is required, either as param or as contextvar. Example: `context.weather_city.set('Amsterdam')`.")
		self._city = city

		units_str: Literal['metric', 'imperial'] = units or context.weather_units.get() or 'metric'
		self._weather_client = python_weather.Client(unit=WeatherComponent.UNITS[units_str])
		self.last_update = 0

		self._timer = Timer(update_interval, self._update_weather_info)
		self._timer.start()
		self._forecast: python_weather.Forecast | None = None
		
	UNITS = {
		'metric': python_weather.METRIC,
		'imperial': python_weather.IMPERIAL,
	}

	def update(self):
		super().update()
		pass # Updating from API is done in async way

	async def _update_weather_info(self):
		self._forecast = await self._weather_client.get(self._city)
