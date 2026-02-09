from PIL import Image
from PIL.ImageFont import ImageFont
import tomllib
from assets import get_asset_path
from pathlib import Path
from typing import Any
import copy


class FontData:
	def __init__(self, height: int, global_configuration: dict[str, Any], size_specific_configuration: dict[str, Any]):
		self._global_configuration = global_configuration
		self._size_specific_configuration = size_specific_configuration

		self.height: int = height
		self.spacing: int = self._get_configuration_value('default_spacing')
		self.space_width: int = self._get_configuration_value('space_width')
		self.glyphs: dict[str, Image.Image] = {}

	def _get_configuration_value(self, key: str) -> Any:
		return self._size_specific_configuration.get(key, self._global_configuration.get(key))


#TODO: add types, check font file for errors when parsing
class AsciiBitmapFont():
	DEFAULT: AsciiBitmapFont

	def __init__(self, path: str | Path):
		super().__init__()
		self._path: str | Path = path
		self._font_data: dict[str, Any] = {}
		self._fonts: dict[int, FontData] = {}
		self._load_file()

	def get_implementation(self, height: int) -> AsciiBitmapFontImplementation:
		#TODO: allow configuration overwrites from file's defaults
		return AsciiBitmapFontImplementation(self._fonts[height])

	def _load_file(self):
		with open(self._path, "rb") as f:
			self.font_data = tomllib.load(f)
		global_configuration = self._font_data.get('configuration', {})

		for glyph in self.font_data['glyphs']:
			bitmap = glyph['bitmap'].strip("\n").split("\n")
			height = len(bitmap)
			if height not in self._fonts:
				size_specific_configuration = self._font_data.get(f'configuration_height{height}', {})
				self._fonts[height] = FontData(height, global_configuration, size_specific_configuration)

			for character in glyph['characters']:
				self._fonts[height].glyphs[character] = self._parse_glyph_bitmap(bitmap)

		for height in self._fonts:
			space_width = self._fonts[height].space_width
			self._fonts[height].glyphs[' '] = self._parse_glyph_bitmap([" " * space_width] * height)
			self._fonts[height].glyphs['�'] = self._parse_glyph_bitmap([["X" if (x+y)%2 == 0 else " " for x in range(space_width)] for y in range(height)]) # checkerboard pattern
			# TODO: support new line character and wrapping??
	
	def _parse_glyph_bitmap(self, bitmap) -> Image.Image:
		height = len(bitmap)
		width = max(len(bitmap[i]) for i in range(len(bitmap)))
		mask = Image.new('1', (width, height), 0)
		for y, row in enumerate(bitmap):
			for x, pixel in enumerate(row):
				if pixel not in [' ', '0']:
					mask.putpixel((x, y), 1)
		return mask

AsciiBitmapFont.DEFAULT = AsciiBitmapFont(get_asset_path("default.font.toml"))


class AsciiBitmapFontImplementation(ImageFont):

	def __init__(self, font_data: FontData):
		super().__init__()
		self._font_data: FontData

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