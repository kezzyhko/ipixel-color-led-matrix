from configargparse import ArgumentParser
from pathlib import Path
from app import LedMatrixApp
from display_target import TerminalDisplayTarget, IPixelColorMatrix
import asyncio
import locale


async def main():
	args = parse_arguments()

	locale.setlocale(locale.LC_ALL, args.locale)
	
	if args.debug:
		display_target = TerminalDisplayTarget()
	else:
		display_target = IPixelColorMatrix(args.mac_address)
	app = LedMatrixApp(display_target=display_target, fps=args.fps)
	try:
		await app.run()
	finally:
		await app.cleanup()

def parse_arguments():
	parser = ArgumentParser(description="Led Matrix App", add_help=False)
	parser.add_argument('--help', '-h', action="help", help="Show this help message and exit.")
	parser.add_argument('--config', '-c', metavar='PATH', required=False, is_config_file=True, help="Path to config file.")
	parser.add_argument('--debug', '-d', action="store_true", help="Enable debug mode. Uses terminal display instead of physical display.")
	parser.add_argument('--debug-size', metavar=('WIDTH', 'HEIGHT'), type=int, nargs=2, default=(64, 32), help="Defines the size of the terminal display. Ignored if debug mode is disabled.") #TODO: use this argument
	parser.add_argument('--mac-address', type=str, default=None, help="MAC address of the iPixel Color Matrix. Ignored if debug mode is enabled. Default - search for device and use it if only one device is found.")
	parser.add_argument('--locale', '-l', type=str, default="en_EN", help="Locale to use (for example, for date formatting)")
	parser.add_argument('--fps', type=float, default=30, help="Update frequency")
	args = parser.parse_args()
	return args


if __name__ == "__main__":
	asyncio.run(main())
