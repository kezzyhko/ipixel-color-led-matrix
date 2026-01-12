import datetime
from typing import Literal
import locale
import python_weather
from .Timer import Timer
from .TempLocale import TempLocale


class WeatherApi:

	_UNITS_MAP = {
		'metric': python_weather.METRIC,
		'imperial': python_weather.IMPERIAL,
	}
	UNIT_KEYS = list(_UNITS_MAP.keys())
	DEFAULT_UNITS = 'metric'

	def __init__(
		self,
		city: str,
		units: Literal['metric', 'imperial'] = DEFAULT_UNITS,
		update_interval: datetime.timedelta = datetime.timedelta(minutes=5)
	):
		self._city = city # TODO: support full address
		self._units_type = self._UNITS_MAP[units]
		self._timer = Timer(update_interval, self._update_weather_info)
		self.forecast: python_weather.Forecast | None = None

	async def __aenter__(self):
		self._weather_client = python_weather.Client(unit=self._units_type)
		self._timer.start()
		return self
	
	async def __aexit__(self, exc_type, exc_value, traceback):
		self._timer.stop()
		await self._weather_client.close()

	async def _update_weather_info(self):
		# Use English locale for weather API parsing (it expects English datetime formats)
		with TempLocale('en_US.UTF-8', locale.LC_TIME):
			self.forecast = await self._weather_client.get(self._city)
