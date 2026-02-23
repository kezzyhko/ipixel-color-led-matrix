from components import Group, Stack, DateTimeComponent, WeatherComponent, Placement


def create_briefing_scene() -> Group:
	return Stack(
		name = "root",
		direction = 'horizontal',
		alignment = 'center',
		spacing = 5/64,
		padding = 1/64,
		children = [
			Stack(
				name = "datetime",
				direction = 'vertical',
				alignment = 'start',
				spacing = 2/16,
				padding = 1/16,
				children = [
					DateTimeComponent(name="date", format=DateTimeComponent.SIMPLE_DATE, case='lower'),
					Stack(
						name = "bottom_line",
						direction = 'horizontal',
						alignment = 'end',
						spacing = 1/64,
						children = [
							DateTimeComponent(name="weekday", format=DateTimeComponent.SIMPLE_WEEKDAY, case='upper', color='#0425cc', placement=Placement(height=5/6)),
							DateTimeComponent(name="time", format=DateTimeComponent.SIMPLE_TIME),
						],
					),
				],
			),
			WeatherComponent(name="weather"),
		],
	)
