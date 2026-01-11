from components import HStack, VStack, DateTimeComponent, WeatherComponent
from . import Scene


def create_briefing_scene() -> Scene:

	date_component = DateTimeComponent(DateTimeComponent.SIMPLE_DATE, case="upper")
	date_component.x = 1
	date_component.y = 1

	time_component = DateTimeComponent(f"{DateTimeComponent.SIMPLE_WEEKDAY} {DateTimeComponent.SIMPLE_TIME}", case="upper")
	time_component.x = 1
	time_component.y = 9

	return Scene(
		HStack(
			VStack(
				date_component,
				time_component,
			),
			WeatherComponent()
		)
	)
