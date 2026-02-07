from . import Component
from pathlib import Path
from PIL import Image
import tomllib
from datetime import datetime
from helpers import Color
from .base import SizingMode


class Icon(Component):
	def __init__(self, path: Path | str):
		super().__init__()
		self.path = path
		self._load_file()
		
		self._current_frame_index: float = 0
		self._last_frame_time = None
		
	def _load_file(self):
		with open(self.path, "rb") as f:
			icon_data = tomllib.load(f)
	
		palette = {}
		for character, color in icon_data['palette'].items():
			palette[character] = Color(color).rgba_tuple_int
		if " " not in palette:
			palette[" "] = (0, 0, 0, 0)
		
		self.frames = []
		for frame in icon_data['frames']:
			bitmap = frame['bitmap'].strip("\n").split("\n")
			self.frames.append(self._parse_frame_bitmap(bitmap, palette))

		self.frames_amount = len(self.frames)
		self.fps = icon_data['configuration']['fps']

	def _parse_frame_bitmap(self, bitmap, palette) -> Image.Image:
		height = len(bitmap)
		width = max(len(bitmap[i]) for i in range(len(bitmap)))
		frame = Image.new('RGBA', (width, height), (0, 0, 0, 0))
		for y, row in enumerate(bitmap):
			for x, pixel in enumerate(row):
				color = palette[pixel]
				frame.putpixel((x, y), color)
		return frame

	def get_sizing_mode(self) -> tuple[SizingMode, SizingMode]:
		return 'output', 'output'

	def update(self):
		current_time = datetime.now().timestamp()
		time_elapsed = (current_time - self._last_frame_time) if self._last_frame_time else 0
		self._current_frame_index += time_elapsed * self.fps
		self._current_frame_index %= self.frames_amount
		self._last_frame_time = current_time

	def render(self) -> Image.Image:
		return self.frames[int(self._current_frame_index)]
