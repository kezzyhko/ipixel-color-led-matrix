from . import DisplayTarget
import colorama
from PIL.Image import Image
from helpers import image as image_helpers, terminal as terminal_helpers
import sys
from io import TextIOWrapper


class TerminalDisplayTarget(DisplayTarget):
	def __init__(self, width: int, height: int):
		self._width = width
		self._height = height

		output = sys.stdout
		if sys.platform == "win32":
			output = colorama.AnsiToWin32(output).stream
		output = TextIOWrapper(output.buffer, encoding='utf-8', line_buffering=False)
		self.output: terminal_helpers.WriteableStream = output

	@property
	def width(self) -> int:
		return self._width
	
	@property
	def height(self) -> int:
		return self._height
	
	async def setup(self):
		print("Using terminal as display")
		terminal_helpers.set_alternate_screen(True, self.output)
	
	async def teardown(self):
		terminal_helpers.set_alternate_screen(False, self.output)
		print("Exiting display emulator mode")

	async def display(self, image: Image):
		terminal_helpers.clear_window(self.output)
		pixels = image_helpers.get_rgba_pixels(image)
		for y in range(self._height):
			for x in range(self._width):
				r, g, b, _ = pixels[y, x] if x < image.width and y < image.height else (0, 0, 0, 0)
				terminal_helpers.change_color(r, g, b, self.output)
				self.output.write("●")
			self.output.write("\n")
		terminal_helpers.clear_formatting(self.output)
		self.output.flush()
