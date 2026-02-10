from components import Group, Stack, DateTimeComponent, WeatherComponent


def create_briefing_scene() -> Group:
	return Stack(
		name = "root",
		direction = 'horizontal',
		alignment = 'center_center',
		children = [
			Stack(
				name = "datetime",
				direction = 'vertical',
				alignment = 'left_center',
				children = [
					DateTimeComponent(name="date", format=DateTimeComponent.SIMPLE_DATE, case='lower'),
					Stack(
						name = "bottom_line",
						direction = 'horizontal',
						alignment = 'left_bottom',
						children = [
							DateTimeComponent(name="weekday", format=DateTimeComponent.SIMPLE_WEEKDAY, case='upper', color='#0425cc'),
							DateTimeComponent(name="time", format=DateTimeComponent.SIMPLE_TIME),
						],
					),
				],
			),
			WeatherComponent(name="weather"),
		],
	)
