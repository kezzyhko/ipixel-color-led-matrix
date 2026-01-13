from PIL import ImageColor


RGBTupleInt = tuple[int, int, int]
RGBATupleInt = tuple[int, int, int, int]
RGBTupleFloat = tuple[float, float, float]
RGBATupleFloat = tuple[float, float, float, float]
HexString = str
ColorInput = str | RGBTupleInt | RGBATupleInt | RGBTupleFloat | RGBATupleFloat

class Color:
	def __init__(self, color: ColorInput):
		if isinstance(color, tuple) and isinstance(color[0], float):
			if len(color) == 3:
				color = (color[0] * 255, color[1] * 255, color[2] * 255)
			else:
				color = (color[0] * 255, color[1] * 255, color[2] * 255)
		rgba = ImageColor.getcolor(color, "RGBA")
		assert isinstance(rgba, tuple) and len(rgba) == 4
		self.r, self.g, self.b, self.a = rgba

	@property
	def rgb_tuple_int(self) -> RGBTupleInt:
		return (self.r, self.g, self.b)

	@property
	def rgba_tuple_int(self) -> RGBATupleInt:
		return (self.r, self.g, self.b, self.a)

	@property
	def rgb_tuple_float(self) -> RGBTupleFloat:
		return (self.r / 255, self.g / 255, self.b / 255)

	@property
	def rgba_tuple_float(self) -> RGBATupleFloat:
		return (self.r / 255, self.g / 255, self.b / 255, self.a / 255)

	@property
	def rgb_hex(self) -> HexString:
		return f"#{self.r:02X}{self.g:02X}{self.b:02X}"

	@property
	def rgba_hex(self) -> HexString:
		return f"#{self.r:02X}{self.g:02X}{self.b:02X}{self.a:02X}"

	@property
	def tk(self) -> HexString:
		return self.rgb_hex

	@property
	def matplotlib(self) -> RGBATupleFloat:
		return self.rgba_tuple_float

	def __repr__(self) -> str:
		return f"Color({self.rgba_hex})"
