from components import Group, Stack, DateTimeComponent, WeatherComponent


def create_briefing_scene() -> Group:
	return Stack("horizontal", "center_center",
		Stack("vertical", "left_center",
			DateTimeComponent(format=DateTimeComponent.SIMPLE_DATE, case="lower"),
			Stack("horizontal", "left_bottom",
				DateTimeComponent(format=DateTimeComponent.SIMPLE_WEEKDAY, case="upper", color='#0425cc'),
				DateTimeComponent(format=DateTimeComponent.SIMPLE_TIME),
			),
		),
		WeatherComponent(),
	)
