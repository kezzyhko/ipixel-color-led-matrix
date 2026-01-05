from configargparse import ArgumentParser
from pathlib import Path
from app import LedMatrixApp
from display_target import TerminalDisplayTarget, IPixelColorMatrix
import asyncio


async def main():
	args = parse_arguments()
	if args.debug:
		display_target = TerminalDisplayTarget()
	else:
		display_target = IPixelColorMatrix()
	app = LedMatrixApp(display_target=display_target)
	await app.run()

def parse_arguments():
	parser = ArgumentParser(description="Led Matrix App")
	parser.add_argument('-c', '--config', required=False, is_config_file=True, help="Path to config file.")
	parser.add_argument('-d', '--debug', action="store_true", help="Enable debug mode. Uses terminal display instead of physical display.")
	parser.add_argument('--debug-size', type=int, nargs=2, default=(64, 32), help="Defines the size of the terminal display. Ignored if debug mode is disabled.") #TODO: use this argument
	args = parser.parse_args()
	return args


if __name__ == "__main__":
	asyncio.run(main())
