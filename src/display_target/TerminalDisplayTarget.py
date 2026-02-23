from . import DisplayTarget
import colorama
from PIL.Image import Image
from helpers import image as image_helpers, terminal as terminal_helpers
import sys
from io import TextIOWrapper


class TerminalDisplayTarget(DisplayTarget):
	def __init__(self, width: int, height: int):
		super().__init__()
		self._width = width
		self._height = height
		self._is_available = True

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

	@property
	def is_available(self) -> bool:
		return self._is_available
	
	async def setup(self):
		if self._is_available:
			return
		print("Using terminal as display")
		terminal_helpers.set_alternate_screen(True, self.output)
		self._is_available = True
	
	async def teardown(self):
		if not self._is_available:
			return
		self._send_unavailable_event()
		self._is_available = False
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
