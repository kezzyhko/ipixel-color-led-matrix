from PIL import Image, ImageDraw
from . import Component
from helpers import AsciiBitmapFont
from .base import SizingMode


class TextComponent(Component):
	def __init__(self, text: str, color: tuple[int, int, int, int]|str = '#ffffff', font: AsciiBitmapFont = AsciiBitmapFont.DEFAULT):
		super().__init__()
		self.text = text
		self.color = color
		self.font = font

	def _calculate_sizing_mode(self) -> tuple[SizingMode, SizingMode]:
		return 'output', 'input'

	def update(self):
		pass

	def _render_implementation(self) -> Image.Image:
		height = self._render_properties.max_height
		font_implementation = self.font.get_implementation(height = height)
		width = font_implementation.getlength(self.text)
		
		img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
		draw = ImageDraw.Draw(img)
		draw.fontmode = "1"
		
		# Use anchor="lt" (left-top) to align from top-left instead of baseline
		# Note: May not work with bitmap fonts, but worth trying
		draw.text((0, 0), self.text, fill=self.color, font=font_implementation)
		return img
