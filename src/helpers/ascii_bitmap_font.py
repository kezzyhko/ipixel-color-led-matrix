from PIL import Image
from PIL.ImageFont import ImageFont
import tomllib
from assets import get_asset_path
from pathlib import Path
from collections.abc import Sequence
from typing import Any
import warnings


AsciiBitmap = Sequence[Sequence[str]]


class FontData:
	def __init__(self, height: int, global_configuration: dict[str, Any], size_specific_configuration: dict[str, Any]):
		self._global_configuration = global_configuration
		self._size_specific_configuration = size_specific_configuration

		self.height: int = height
		self.spacing: int = self._get_configuration_value('spacing')
		self.space_width: int = self._get_configuration_value('space_width')
		self.glyphs: dict[str, Image.Image] = {}
		self.add_glyphs([' '], FontData._get_empty_askii_bitmap(self.space_width, self.height))
		self.add_glyphs(['�'], FontData._get_checkerboard_askii_bitmap(self.space_width, self.height))
		# TODO: support new line character and wrapping??

	@staticmethod
	def create_stub(height: int, global_configuration: dict[str, Any]) -> FontData:
		fallback_configuration = {
			'spacing': int(height**0.5 / 2),
			'space_width': int(height / 2),
		}
		return FontData(height, fallback_configuration, global_configuration)

	@staticmethod
	def _get_empty_askii_bitmap(width: int, height: int) -> AsciiBitmap:
		return [" " * width] * height

	@staticmethod
	def _get_checkerboard_askii_bitmap(width: int, height: int) -> AsciiBitmap:
		return [["X" if (x+y)%2 == 0 else " " for x in range(width)] for y in range(height)]

	def add_glyphs(self, characters: list[str], bitmap: AsciiBitmap):
		glyph_mask = self._parse_askii_bitmap(bitmap)
		for character in characters:
			self.glyphs[character] = glyph_mask

	def _get_configuration_value(self, key: str) -> Any:
		return self._size_specific_configuration.get(key, self._global_configuration.get(key))
	
	def _parse_askii_bitmap(self, bitmap: AsciiBitmap) -> Image.Image:
		height = len(bitmap)
		width = max(len(bitmap[i]) for i in range(len(bitmap)))
		mask = Image.new('1', (width, height), 0)
		for y, row in enumerate(bitmap):
			for x, pixel in enumerate(row):
				if pixel not in [' ', '0']:
					mask.putpixel((x, y), 1)
		return mask


#TODO: add types, check font file for errors when parsing
class AsciiBitmapFont():
	DEFAULT: AsciiBitmapFont

	def __init__(self, path: str | Path):
		super().__init__()
		self._path: str | Path = path
		self._font_data: dict[str, Any] = {}
		self._fonts: dict[int, FontData] = {}
		self._global_configuration: dict[str, Any] = {}
		self._load_file()

	def get_implementation(self, height: int) -> AsciiBitmapFontImplementation:
		#TODO: allow configuration overwrites from file's defaults
		if height not in self._fonts:
			warnings.warn(f"Font data for height {height} not found, creating stub")
			return AsciiBitmapFontImplementation(FontData.create_stub(height, self._global_configuration))
		return AsciiBitmapFontImplementation(self._fonts[height])

	def _load_file(self):
		with open(self._path, "rb") as f:
			self._font_data = tomllib.load(f)
		self._global_configuration = self._font_data.get('configuration', {})

		for glyph in self._font_data['glyphs']:
			bitmap = glyph['bitmap'].strip("\n").split("\n")
			height = len(bitmap)
			if height not in self._fonts:
				size_specific_configuration = self._font_data.get(f'configuration_height{height}', {})
				self._fonts[height] = FontData(height, self._global_configuration, size_specific_configuration)
			self._fonts[height].add_glyphs(glyph['characters'], bitmap)

AsciiBitmapFont.DEFAULT = AsciiBitmapFont(get_asset_path("default.font.toml"))


class AsciiBitmapFontImplementation(ImageFont):

	def __init__(self, font_data: FontData):
		super().__init__()
		self._font_data: FontData = font_data

	# TODO: implement characters with height different from font size for letters like "Q" or "Й"?
	# TODO: support new line character and wrapping??

	def getmetrics(self):
		return self._font_data.height, 0

	def getbbox(self, text: str, *args, **kwargs) -> tuple[int, int, int, int]:
		length = self.getlength(text)
		return (0, 0, length, self._font_data.height)

	def getlength(self, text: str, *args, **kwargs) -> int:
		length: int = 0
		for character in text:
			glyph = self._font_data.glyphs.get(character)
			if not glyph:
				glyph = self._font_data.glyphs['�']
			length += glyph.width
		
		characters_amount = len(text)
		if characters_amount > 1:
			length += self._font_data.spacing * (characters_amount - 1)
		return length

	def getmask2(self, text: str, mode='1', *args, **kwargs) -> tuple[Image.core.ImagingCore, tuple[int, int]]:
		if mode != '1':
			raise ValueError("For now, only mode '1' is supported")
			# TODO: implement other modes (L for antialiasing and RGBA for characters with color)
			# TODO: make '�' character bright pink

		length = self.getlength(text, *args, **kwargs)
		mask = Image.new(mode, (length, self._font_data.height), 0)

		x = 0
		for character in text:
			glyph = self._font_data.glyphs.get(character)
			if not glyph:
				glyph = self._font_data.glyphs['�']
			mask.paste(1, (x, 0), glyph)
			x += glyph.width + self._font_data.spacing

		return mask.im, (0, 0)