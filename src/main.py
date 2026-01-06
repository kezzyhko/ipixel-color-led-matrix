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
		display_target = IPixelColorMatrix()
	app = LedMatrixApp(display_target=display_target)
	try:
		await app.run()
	finally:
		app.cleanup()

def parse_arguments():
	parser = ArgumentParser(description="Led Matrix App", add_help=False)
	parser.add_argument('--help', '-h', action="help", help="Show this help message and exit.")
	parser.add_argument('--config', '-c', metavar='PATH', required=False, is_config_file=True, help="Path to config file.")
	parser.add_argument('--debug', '-d', action="store_true", help="Enable debug mode. Uses terminal display instead of physical display.")
	parser.add_argument('--debug-size', metavar=('WIDTH', 'HEIGHT'), type=int, nargs=2, default=(64, 32), help="Defines the size of the terminal display. Ignored if debug mode is disabled.") #TODO: use this argument
	parser.add_argument('--locale', '-l', type=str, default="en_EN", help="Locale to use (for example, for date formatting)")
	args = parser.parse_args()
	return args


if __name__ == "__main__":
	asyncio.run(main())
