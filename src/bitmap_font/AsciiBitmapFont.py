from PIL import Image
from PIL.ImageFont import ImageFont
import tomllib
from pathlib import Path


class AsciiBitmapFont(ImageFont):

	DEFAULT_SPACING = 1

	@staticmethod
	def get_default_font(size: int) -> AsciiBitmapFont:
		path = Path(__file__).parent / "default.font.toml"
		return AsciiBitmapFont(path, size)

	def __init__(self, path: str | Path, size: int, spacing: int | None = None):
		super().__init__()
		self.path = path
		self.size = size
		self.spacing = spacing
		self.glyphs = {}
		self._load_file()

	def _load_file(self):
		with open(self.path, "rb") as f:
			font_data = tomllib.load(f)
		
		configuration = font_data.get('configuration', {})
		self.spacing = self.spacing or configuration.get('default_spacing') or AsciiBitmapFont.DEFAULT_SPACING

		for glyph in font_data['glyphs']:
			bitmap = glyph['bitmap'].strip("\n").split("\n")
			size = len(bitmap)
			if (size != self.size):
				continue # TODO: load and cache all file as a collection of fonts with different sizes
			for character in glyph['characters']:
				self.glyphs[character] = bitmap

	def getmask(self, text: str) -> Image.core.ImagingCore:
		w = self.width * len(text)
		h = self.height
		img = Image.new("1", (w, h), 0)

		x = 0
		for ch in text:
			rows = self.glyphs.get(ch)
			if not rows:
				x += self.width
				continue

			for y, row in enumerate(rows):
				for xx, bit in enumerate(row):
					if bit == "1":
						for sy in range(self.scale):
							for sx in range(self.scale):
								img.putpixel(
									(x + xx * self.scale + sx,
									 y * self.scale + sy),
									255
								)
			x += self.width

		return img.im
