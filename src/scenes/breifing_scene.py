from components import HStack, DateTimeComponent, WeatherComponent
from . import Scene


def create_breifing_scene() -> Scene:
	return Scene(
		DateTimeComponent(format=DateTimeComponent.SIMPLE_DATETIME),
	)
	return Scene(
		HStack(
			DateTimeComponent(),
			WeatherComponent()
		)
	)
