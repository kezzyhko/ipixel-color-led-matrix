from . import DisplayTarget
import colorama
from PIL.Image import Image
from helpers import get_rgba_pixels


class TerminalDisplayTarget(DisplayTarget):
	def __init__(self):
		colorama.just_fix_windows_console()

	def display(self, image: Image):
		pixels = get_rgba_pixels(image)
		for y in range(image.height):
			for x in range(image.width):
				r, g, b, _ = pixels[y, x]
				self._change_color(r, g, b)
				print("●", end="")
			print()
		self._clear_formatting()

	def _change_color(self, r: int, g: int, b: int):
		print(f"\033[38;2;{r};{g};{b}m", end="")

	def _clear_formatting(self):
		print("\033[0m", end="")
