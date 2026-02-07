from components import Component, Stack, DateTimeComponent, WeatherComponent


def create_briefing_scene() -> Component:

	date_component = DateTimeComponent(format=DateTimeComponent.SIMPLE_DATE, case="lower", font_size=6)
	date_component.x = 1
	date_component.y = 1

	weekday_component = DateTimeComponent(format=DateTimeComponent.SIMPLE_WEEKDAY, case="upper", font_size=5, color='#0425cc')
	weekday_component.x = 1
	weekday_component.y = 10

	time_component = DateTimeComponent(format=DateTimeComponent.SIMPLE_TIME, font_size=6)
	time_component.x = 9
	time_component.y = 9

	weather_component = WeatherComponent()
	weather_component.x = 40
	weather_component.y = 1

	return Stack("horizontal",
		Stack("vertical",
			date_component,
			Stack("horizontal",
				weekday_component,
				time_component,
			),
		),
		weather_component,
	)
