from io import BytesIO
from PIL.Image import Image
import numpy as np
from numpy.typing import NDArray


def ensure_rgba(image: Image) -> Image:
	return image.convert("RGBA")

def get_rgba_pixels(image: Image) -> NDArray[np.uint8]:
	image = image.convert("RGBA")
	return np.asarray(image, dtype=np.uint8)

def convert_to_png_hex(image: Image) -> str:
	output = BytesIO()
	image.save(output, format="PNG")
	file_bytes = output.getvalue()
	hex = file_bytes.hex()
	return hex

def convert_to_hex(color: tuple[int, int, int, int]) -> str:
	return f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}{color[3]:02x}'