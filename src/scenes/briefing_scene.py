from components import HStack, VStack, DateTimeComponent, WeatherComponent
from . import Scene


def create_briefing_scene() -> Scene:
	comp = DateTimeComponent(f"{DateTimeComponent.SIMPLE_WEEKDAY} {DateTimeComponent.SIMPLE_TIME}")
	comp.y = 8
	return Scene(
		HStack(
			VStack(
				DateTimeComponent(DateTimeComponent.SIMPLE_DATE),
				comp,
			),
			WeatherComponent()
		)
	)
