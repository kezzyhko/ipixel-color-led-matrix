from weather.weather import GeocodingClient, OpenMeteoClient, TTLCacheDecorator, CurrentWeather, DailyForecast, HistoricalWeather, WeatherData
from pydantic import BaseModel
import datetime
import asyncio
from typing import Callable, Type, Optional, Literal


class WeatherApi:
	def __init__(
		self,
		location: WeatherLocation,
		update_interval: datetime.timedelta = datetime.timedelta(minutes=5)
	):
		self._cache_ttl = int(update_interval.total_seconds())
		self._client = OpenMeteoClient(location.latitude, location.longitude)
		
		self._current_cache = self.create_cache_decorator()
		self._forecast_cache = self.create_cache_decorator()
		self._historical_cache = self.create_cache_decorator()
		
		self._latest_current: Optional[CurrentWeather] = None
		self._latest_forecast: Optional[DailyForecast] = None
		self._latest_historical: Optional[HistoricalWeather] = None

	def create_cache_decorator(self) -> Callable[[Callable], Callable]:
		if self._cache_ttl <= 0:
			return lambda func: func
		return TTLCacheDecorator(ttl=self._cache_ttl)

	async def _get_data[TResult: BaseModel](self, cache_decorator: Callable, actual_function: Callable, cls: Type[TResult]) -> TResult:
		dict_data = await cache_decorator(actual_function)()
		return cls(**dict_data)

	@property
	async def current(self) -> CurrentWeather:
		self._latest_current = await self._get_data(self._current_cache, self._client.get_current_weather, CurrentWeather)
		return self._latest_current

	@property
	async def forecast(self) -> DailyForecast:
		self._latest_forecast = await self._get_data(self._forecast_cache, self._client.get_forecast, DailyForecast)
		return self._latest_forecast

	@property
	async def historical(self) -> HistoricalWeather:
		self._latest_historical = await self._get_data(self._historical_cache, self._client.get_historical_weather, HistoricalWeather)
		return self._latest_historical

	@property
	async def all_weather(self) -> WeatherData:
		return WeatherData(
			current=await self.current,
			forecast=await self.forecast,
			historical=await self.historical
		)
	
	@property
	def latest_current(self) -> Optional[CurrentWeather]:
		asyncio.create_task(self.current)
		return self._latest_current

	@property
	def latest_forecast(self) -> Optional[DailyForecast]:
		asyncio.create_task(self.forecast)
		return self._latest_forecast

	@property
	def latest_historical(self) -> Optional[HistoricalWeather]:
		asyncio.create_task(self.historical)
		return self._latest_historical

	@property
	def latest_all_weather(self) -> WeatherData:
		return WeatherData(
			current=self._latest_current,
			forecast=self._latest_forecast,
			historical=self._latest_historical
		)


class WeatherLocation():
	def __init__(self, latitude: float, longitude: float):
		self.latitude = latitude
		self.longitude = longitude
		
	_geocoding_client = GeocodingClient()

	@staticmethod
	async def from_city(city: str):
		coordinates = await WeatherLocation._geocoding_client.get_coordinates(city)
		instance = WeatherLocation(coordinates['latitude'], coordinates['longitude'])
		return instance

	@staticmethod
	async def from_optional(latitude: float|None, longitude: float|None, city: str|None = None):
		if latitude and longitude:
			return WeatherLocation(latitude, longitude)

		if not city:
			raise ValueError("Either latitude and longitude or city must be provided")

		coordinates = await WeatherLocation._geocoding_client.get_coordinates(city)
		return WeatherLocation(
			latitude or coordinates['latitude'],
			longitude or coordinates['longitude']
		)


WeatherType = Literal['clear', 'clouds', 'fog', 'rain', 'snowrain', 'snow', 'thunderstorm_hail']

class WeatherTypeInfo:
	def __init__(self, code: int, type: WeatherType, power: float, description: str):
		if power < 0.0 or power > 1.0:
			raise ValueError("Power must be between 0.0 and 1.0")
		self.code: int = code
		self.description: str = description
		self.type: WeatherType = type
		self.power: float = power

	WEATHER_CODES: dict[int, WeatherTypeInfo]
	
	@staticmethod
	def from_code(code: int) -> WeatherTypeInfo:
		return WeatherTypeInfo.WEATHER_CODES[code]
	
WeatherTypeInfo.WEATHER_CODES = {
	 0: WeatherTypeInfo( 0,             'clear', 0.00, "Clear sky"),
	 1: WeatherTypeInfo( 1,            'clouds', 0.25, "Mainly clear"),
	 2: WeatherTypeInfo( 2,            'clouds', 0.50, "Partly cloudy"),
	 3: WeatherTypeInfo( 3,            'clouds', 1.00, "Overcast"),
	45: WeatherTypeInfo(45,               'fog', 0.50, "Fog"),
	48: WeatherTypeInfo(48,               'fog', 1.00, "Depositing rime fog"),
	51: WeatherTypeInfo(51,              'rain', 0.15, "Light drizzle"),
	53: WeatherTypeInfo(53,              'rain', 0.35, "Moderate drizzle"),
	55: WeatherTypeInfo(55,              'rain', 0.50, "Dense drizzle"),
	56: WeatherTypeInfo(56,          'snowrain', 0.25, "Light freezing drizzle"),
	57: WeatherTypeInfo(57,          'snowrain', 0.50, "Dense freezing drizzle"),
	61: WeatherTypeInfo(61,              'rain', 0.40, "Slight rain"),
	63: WeatherTypeInfo(63,              'rain', 0.65, "Moderate rain"),
	65: WeatherTypeInfo(65,              'rain', 0.90, "Heavy rain"),
	66: WeatherTypeInfo(66,          'snowrain', 0.60, "Light freezing rain"),
	67: WeatherTypeInfo(67,          'snowrain', 0.95, "Heavy freezing rain"),
	71: WeatherTypeInfo(71,              'snow', 0.25, "Slight snow fall"),
	73: WeatherTypeInfo(73,              'snow', 0.50, "Moderate snow fall"),
	75: WeatherTypeInfo(75,              'snow', 0.90, "Heavy snow fall"),
	77: WeatherTypeInfo(77,          'snowrain', 0.35, "Snow grains"),
	80: WeatherTypeInfo(80,              'rain', 0.45, "Slight rain showers"),
	81: WeatherTypeInfo(81,              'rain', 0.70, "Moderate rain showers"),
	82: WeatherTypeInfo(82,              'rain', 1.00, "Violent rain showers"),
	85: WeatherTypeInfo(85,              'snow', 0.40, "Slight snow showers"),
	86: WeatherTypeInfo(86,              'snow', 1.00, "Heavy snow showers"),
	95: WeatherTypeInfo(95, 'thunderstorm_hail', 0.10, "Thunderstorm"),
	96: WeatherTypeInfo(96, 'thunderstorm_hail', 0.50, "Thunderstorm with slight hail"),
	99: WeatherTypeInfo(99, 'thunderstorm_hail', 1.00, "Thunderstorm with heavy hail"),
}
