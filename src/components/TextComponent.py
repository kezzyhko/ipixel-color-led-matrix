from PIL import Image, ImageDraw
from . import Component
from helpers import AsciiBitmapFont
from .base import SizingMode


class TextComponent(Component):
	def __init__(self, text: str, font_size: int, color: tuple[int, int, int, int]|str = '#ffffff'): #TODO: size
		super().__init__()
		self.text = text
		self.color = color
		self.font = AsciiBitmapFont.get_default_font(size=font_size)

	def _calculate_sizing_mode(self) -> tuple[SizingMode, SizingMode]:
		return 'output', 'input'

	def update(self):
		pass

	def _render_implementation(self) -> Image.Image:
		# TODO: size
		height = 16
		width = 64
		
		img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
		draw = ImageDraw.Draw(img)
		draw.fontmode = "1"
		
		# Use anchor="lt" (left-top) to align from top-left instead of baseline
		# Note: May not work with bitmap fonts, but worth trying
		draw.text((0, 0), self.text, fill=self.color, font=self.font)
		return img
