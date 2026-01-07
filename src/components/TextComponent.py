from abc import ABCMeta, abstractmethod
import platform
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from . import Component
from bitmap_font import AsciiBitmapFont


class TextComponent(Component, metaclass=ABCMeta):
	def __init__(self, text: str):
		super().__init__()
		self.text = text

	def update(self):
		pass

	def render(self) -> Image.Image:
		# TODO: size
		height = 16
		width = 64
		fontsize = 5
		
		font = AsciiBitmapFont.get_default_font(size=fontsize)
		
		img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
		draw = ImageDraw.Draw(img)
		draw.fontmode = "1"
		
		# Use anchor="lt" (left-top) to align from top-left instead of baseline
		# Note: May not work with bitmap fonts, but worth trying
		draw.text((0, 0), self.text, fill=(255, 255, 255, 255), font=font)#, anchor="lt")
		return img
