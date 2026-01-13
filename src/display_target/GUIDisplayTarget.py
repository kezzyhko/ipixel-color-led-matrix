from . import DisplayTarget
from PIL import Image, ImageTk
from helpers import image as image_helpers
import tkinter as tk
from helpers import Color


class GUIDisplayTarget(DisplayTarget):
	def __init__(self, pixel_size: int = 20, spacing: int = 10):
		self._pixel_size = pixel_size
		self._spacing = spacing
		
		self._window = tk.Tk()
		self._window.withdraw()
		self._window.resizable(False, False)
		self._window.title("LED Matrix Emulator")
		self._image = tk.Label(self._window)
		self._image.pack()

	def __del__(self):
		self._window.destroy()

	@property
	def is_window_available(self) -> bool:
		try:
			self._window.winfo_exists()
			return True
		except tk.TclError:
			return False

	@property
	def is_window_hidden(self) -> bool:
		return self._window.state() == "withdrawn"
	
	async def setup(self):
		if not self.is_window_available:
			raise RuntimeError("Window is closed")
		if not self.is_window_hidden:
			return
		self._window.deiconify()
	
	async def teardown(self):
		if self.is_window_hidden or not self.is_window_available:
			return
		self._window.quit()

	async def display(self, image: Image.Image):
		if not self.is_window_available:
			raise RuntimeError("Window is closed")

		new_size = (image.width * self._pixel_size, image.height * self._pixel_size)
		resized = image.resize(new_size, Image.Resampling.NEAREST)
		tk_image = ImageTk.PhotoImage(resized)
		self._image.configure(image=tk_image, bg=Color("black").tk)
		self._window.update()
