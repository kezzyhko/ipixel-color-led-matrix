from configargparse import ArgumentParser
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

	display_target = GUIDisplayTarget(*args.debug_size) if args.debug else IPixelColorMatrix(args.mac_address)
	app = LedMatrixApp(display_target=display_target, fps=args.fps)

	try:
		await app.run()
	finally:
		await app.cleanup()

def parse_arguments():
	parser = ArgumentParser(description="Led Matrix App", add_help=False)

	general = parser.add_argument_group('General')
	general.add_argument('--help', '-h', action="help", help="Show this help message and exit.")
	general.add_argument('--config', '-c', metavar='PATH', required=False, is_config_file=True, help="Path to config file.")
	general.add_argument('--debug', '-d', action="store_true", help="Enable debug mode. Uses GUI display instead of physical display.")

	display = parser.add_argument_group('Display')
	display.add_argument('--debug-size', metavar=('WIDTH', 'HEIGHT'), type=int, nargs=2, default=(64, 32), help="Defines the size of the terminal display. Ignored if debug mode is disabled.") #TODO: use this argument
	display.add_argument('--mac-address', type=str, default=None, help="MAC address of the iPixel Color Matrix. Ignored if debug mode is enabled. Default - search for device and use it if only one device is found.")
	display.add_argument('--fps', type=float, default=10.0, help="Update frequency")

	locale = parser.add_argument_group('Locale')
	locale.add_argument('--locale', type=str, default="en", help="Locale to use (for example, for date formatting)")
	weather = locale.add_mutually_exclusive_group(required=True)
	weather.add_argument('--city', type=str, help="City to get weather data from.")
	weather.add_argument('--weather-coordinates', metavar=('LATITUDE', 'LONGITUDE'), type=float, nargs=2, default=[None, None], help="Coordinates to get weather data from.")

	args = parser.parse_args()
	return args


if __name__ == "__main__":
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		print("Keyboard interrupt, stopping...")
