import configargparse as argparse
from app import LedMatrixApp
from display_target import GUIDisplayTarget, IPixelColorMatrix
import asyncio
from app import context
from helpers.weather import WeatherLocation


async def main():
	args = parse_arguments()

	context.locale_code.set(args.locale)
	context.weather_location.set(await WeatherLocation.from_optional(
		*args.weather_coordinates, city=args.city
	))

	display_target = GUIDisplayTarget(*args.emulator_size) if args.emulator else IPixelColorMatrix(args.mac_address)
	app = LedMatrixApp(display_target=display_target, fps=args.fps, debug_system=args.debug_system)

	try:
		await app.run()
	finally:
		await app.cleanup()


class HelpFormatter(argparse.HelpFormatter):
	"""Help message formatter which adds default values to argument help.

	Only the name of this class is considered a public API. All the methods
	provided by the class are considered an implementation detail.
	"""

	def _get_help_string(self, action):
		help = action.help or ''


		if help[-1] != '.':
			help += '.'
			
		if ('%(default)' not in help) and (action.default is not argparse.SUPPRESS) and (action.option_strings or action.nargs in [argparse.OPTIONAL, argparse.ZERO_OR_MORE]):
			help += ' Default: %(default)s.'

		if ('%(choices)' not in help) and (action.choices is not None):
			help += ' Choices: %(choices)s.'

		if (isinstance(action.nargs, int) and action.nargs > 0) or (isinstance(action.nargs, str) and action.nargs in [argparse.ONE_OR_MORE, argparse.ZERO_OR_MORE]):
			help += ' Multiple values allowed.'

		return help


def parse_arguments():
	parser = argparse.ArgumentParser(description="Led Matrix App", add_help=False, formatter_class=HelpFormatter)
	# TODO: add --rtl flag to enable right-to-left layout

	general = parser.add_argument_group('General')
	general.add_argument('--help', '-h', action="help", help="Show this help message and exit")
	general.add_argument('--config', '-c', metavar='PATH', required=False, is_config_file=True, help="Path to config file")
	general.add_argument('--debug-system', '-d', metavar='SYSTEM_NAME', nargs=argparse.ONE_OR_MORE, default=[], choices=['scene', 'render', 'placement'], help="System to show debug info from")

	display = parser.add_argument_group('Display')
	display.add_argument('--emulator', '-e', action="store_true", help="Use GUI display instead of physical display")
	display.add_argument('--emulator-size', metavar=('WIDTH', 'HEIGHT'), type=int, nargs=2, default=(64, 32), help="Defines the size of the terminal display. Ignored if --emulator is not specified.")
	display.add_argument('--mac-address', type=str, default=None, help="MAC address of the iPixel Color Matrix. Ignored if --emulator is specified. Default: %(default)s - search for device and use it if only one device is found.")
	display.add_argument('--fps', type=float, default=10.0, help="Update frequency.")

	locale = parser.add_argument_group('Locale')
	locale.add_argument('--locale', '-l', type=str, default="en", help="Locale to use (for example, for date formatting).")
	weather = locale.add_mutually_exclusive_group(required=True)
	weather.add_argument('--city', type=str, help="City to get weather data from. Can not be used together with --weather-coordinates.")
	weather.add_argument('--weather-coordinates', metavar=('LATITUDE', 'LONGITUDE'), type=float, nargs=2, default=[None, None], help="Coordinates to get weather data from. Two values: latitude and longitude. Can not be used together with --city.")

	args = parser.parse_args()
	return args


if __name__ == "__main__":
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		print("Keyboard interrupt, stopping...")
