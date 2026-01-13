from . import Component
from pathlib import Path
from PIL import Image, ImageColor
import tomllib
from datetime import datetime


class Icon(Component):
	def __init__(self, path: Path | str):
		super().__init__()
		self.path = path
		self._load_file()
		
	def _load_file(self):
		with open(self.path, "rb") as f:
			icon_data = tomllib.load(f)
			
		self.fps = icon_data['configuration']['fps']
	
		palette = {}
		for character, color in icon_data['palette'].items():
			palette[character] = ImageColor.getrgb(color)
		if " " not in palette:
			palette[" "] = (0, 0, 0, 0)
		
		self.frames = []
		for frame in icon_data['frames']:
			bitmap = frame['bitmap'].strip("\n").split("\n")
			self.frames.append(self._parse_frame_bitmap(bitmap, palette))

		self.frames_amount = len(self.frames)


	def _parse_frame_bitmap(self, bitmap, palette) -> Image.Image:
		height = len(bitmap)
		width = max(len(bitmap[i]) for i in range(len(bitmap)))
		frame = Image.new('RGBA', (width, height), (0, 0, 0, 0))
		for y, row in enumerate(bitmap):
			for x, pixel in enumerate(row):
				color = palette[pixel]
				frame.putpixel((x, y), color)
		return frame

	def update(self):
		pass

	def render(self) -> Image.Image:
		seconds = datetime.now().timestamp()
		frame_index = (seconds * self.fps) % self.frames_amount
		frame_index = int(frame_index)
		frame = self.frames[frame_index]
		return frame