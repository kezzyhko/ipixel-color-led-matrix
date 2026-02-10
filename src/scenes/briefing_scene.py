from components import Group, Stack, DateTimeComponent, WeatherComponent


def create_briefing_scene() -> Group:
	return Stack(
		Stack(
			DateTimeComponent(format=DateTimeComponent.SIMPLE_DATE, case='lower'),
			Stack(
				DateTimeComponent(format=DateTimeComponent.SIMPLE_WEEKDAY, case='upper', color='#0425cc'),
				DateTimeComponent(format=DateTimeComponent.SIMPLE_TIME),
			direction='horizontal', alignment='left_bottom'),
		direction='vertical', alignment='left_center'),
		WeatherComponent(),
	direction='horizontal', alignment='center_center')
