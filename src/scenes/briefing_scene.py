from components import Group, Stack, DateTimeComponent, WeatherComponent


def create_briefing_scene() -> Group:

	weekday = DateTimeComponent(name="weekday", format=DateTimeComponent.SIMPLE_WEEKDAY, case='upper', color='#0425cc')
	weekday.placement.height = 0.8
	# TODO LAYOUT change placement params from constructor

	return Stack(
		name = "root",
		direction = 'horizontal',
		alignment = 'center_center',
		spacing = 3/32,
		padding = 1/32,
		children = [
			Stack(
				name = "datetime",
				direction = 'vertical',
				alignment = 'left_center',
				spacing = 2/16,
				padding = 1/16,
				children = [
					DateTimeComponent(name="date", format=DateTimeComponent.SIMPLE_DATE, case='lower'),
					Stack(
						name = "bottom_line",
						direction = 'horizontal',
						alignment = 'left_bottom',
						spacing = 1/32,
						children = [
							weekday,
							DateTimeComponent(name="time", format=DateTimeComponent.SIMPLE_TIME),
						],
					),
				],
			),
			WeatherComponent(name="weather"),
		],
	)
