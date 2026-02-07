from components import Component, Stack, DateTimeComponent, WeatherComponent


def create_briefing_scene() -> Component:

	date_component = DateTimeComponent(format=DateTimeComponent.SIMPLE_DATE, case="lower", font_size=6)
	date_component.placement.position_x = 1
	date_component.placement.position_y = 1

	weekday_component = DateTimeComponent(format=DateTimeComponent.SIMPLE_WEEKDAY, case="upper", font_size=5, color='#0425cc')
	weekday_component.placement.position_x = 1
	weekday_component.placement.position_y = 10

	time_component = DateTimeComponent(format=DateTimeComponent.SIMPLE_TIME, font_size=6)
	time_component.placement.position_x = 9
	time_component.placement.position_y = 9

	weather_component = WeatherComponent()
	weather_component.placement.position_x = 40
	weather_component.placement.position_y = 1

	return Stack("horizontal", "center_center",
		Stack("vertical", "left_center",
			date_component,
			Stack("horizontal", "left_bottom",
				weekday_component,
				time_component,
			),
		),
		weather_component,
	)
