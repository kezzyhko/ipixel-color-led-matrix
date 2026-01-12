from weather.weather import GeocodingClient, OpenMeteoClient, TTLCacheDecorator, CurrentWeather, DailyForecast, HistoricalWeather, WeatherData
from pydantic import BaseModel
import datetime
import asyncio
from typing import Callable, Type, Optional


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
