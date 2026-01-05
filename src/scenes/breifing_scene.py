from components import HStack, DateTimeComponent, WeatherComponent
from . import Scene


def create_breifing_scene() -> Scene:
	return Scene(DateTimeComponent())
	return Scene(
		HStack(
			DateTimeComponent(),
			WeatherComponent()
		)
	)
