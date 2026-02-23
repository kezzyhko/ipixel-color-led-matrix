from . import DisplayTarget
from PIL import Image, ImageTk
from helpers import image as image_helpers
import tkinter as tk
from helpers import Color


class GUIDisplayTarget(DisplayTarget):
	def __init__(self, width: int, height: int, pixel_size: int = 20):
		super().__init__()
		self._width = width
		self._height = height
		self._pixel_size = pixel_size
		# TODO: add spacing and make pixels circular
		self._create_window()

	@property
	def width(self) -> int:
		return self._width
	
	@property
	def height(self) -> int:
		return self._height

	@property
	def is_available(self) -> bool:
		try:
			return self._window.winfo_exists()
		except tk.TclError:
			return False

	@property
	def is_window_hidden(self) -> bool:
		return self._window.state() == "withdrawn"

	def _create_window(self):
		self._window = tk.Tk()
		self._window.withdraw()
		self._window.resizable(False, False)
		self._window.title("LED Matrix Emulator")
		self._window.protocol("WM_DELETE_WINDOW", self._on_window_closed)
		self._image = tk.Label(self._window)
		self._image.pack()
		self._window.deiconify()

	def __del__(self):
		if not self.is_available:
			return
		self._window.destroy()

	def _on_window_closed(self):
		self._window.destroy()
		self._send_unavailable_event()

	async def setup(self):
		if self.is_available:
			if self.is_window_hidden:
				self._window.deiconify()
			return
		self._create_window()
	
	async def teardown(self):
		self.__del__()

	async def display(self, image: Image.Image):
		if not self.is_available:
			raise RuntimeError("Window is closed")

		image = image.crop((0, 0, self._width, self._height))
		new_size = (image.width * self._pixel_size, image.height * self._pixel_size)
		image = image.resize(new_size, Image.Resampling.NEAREST)
		tk_image = ImageTk.PhotoImage(image)
		self._image.configure(image=tk_image, bg=Color("black").tk)
		self._window.update()
