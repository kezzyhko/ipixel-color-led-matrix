from PIL import Image
from PIL.ImageFont import ImageFont
import tomllib
from pathlib import Path


#TODO: add types, check font file for errors when parsing
class AsciiBitmapFont(ImageFont):

	@staticmethod
	def get_default_font(size: int) -> AsciiBitmapFont:
		path = Path(__file__).parent / "default.font.toml"
		return AsciiBitmapFont(path, size)

	def __init__(self, path: str | Path, size: int, spacing: int | None = None):
		super().__init__()
		self.path: str | Path = path
		self.size: int = size

		# will be filled later in _load_file
		self.spacing: int = 0
		self.glyphs = {}
		self._load_file(spacing)

	def _load_file(self, requested_spacing: int | None):
		with open(self.path, "rb") as f:
			font_data = tomllib.load(f)
		
		configuration = font_data.get('configuration', {})
		self.spacing = requested_spacing or configuration.get('default_spacing')

		for glyph in font_data['glyphs']:
			bitmap = glyph['bitmap'].strip("\n").split("\n")
			size = len(bitmap)
			if (size != self.size):
				continue # TODO: load and cache all file as a collection of fonts with different sizes

			for character in glyph['characters']:
				self.glyphs[character] = self._parse_glyph_bitmap(bitmap)

		# special glyphs
		space_width = configuration['space_width']
		self.glyphs[' '] = self._parse_glyph_bitmap([" " * space_width] * self.size)
		self.glyphs['�'] = self._parse_glyph_bitmap([["X" if (x+y)%2 == 0 else " " for x in range(space_width)] for y in range(self.size)]) # checkerboard pattern

	# TODO: implement characters with height different from font size for letters like "Q" or "Й"

	def _parse_glyph_bitmap(self, bitmap) -> Image.Image:
		width = max(len(bitmap[i]) for i in range(len(bitmap)))
		mask = Image.new('1', (width, self.size), 0)
		for y, row in enumerate(bitmap):
			for x, pixel in enumerate(row):
				if pixel not in [' ', '0']:
					mask.putpixel((x, y), 1)
		return mask

	def getmetrics(self):
		return self.size, 0

	def getbbox(self, text: str, *args, **kwargs) -> tuple[int, int, int, int]:
		length = self.getlength(text)
		return (0, 0, length, self.size)

	def getlength(self, text: str, *args, **kwargs) -> int:
		length: int = 0
		for character in text:
			glyph = self.glyphs.get(character)
			if not glyph:
				glyph = self.glyphs['�']
			length += glyph.width
		length += self.spacing * (len(text) - 1)
		return length

	def getmask2(self, text: str, mode='1', *args, **kwargs) -> tuple[Image.core.ImagingCore, tuple[int, int]]:
		if mode != '1':
			raise ValueError("For now, only mode '1' is supported") # TODO: implement other modes (L for antialiasing and RGBA for characters with color)

		length = self.getlength(text, *args, **kwargs)
		mask = Image.new(mode, (length, self.size), 0)

		x = 0
		for character in text:
			glyph = self.glyphs.get(character)
			if not glyph:
				glyph = self.glyphs['�']
			mask.paste(1, (x, 0), glyph)
			x += glyph.width + self.spacing

		return mask.im, (0, 0)