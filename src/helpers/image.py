from io import BytesIO
from PIL import Image
import numpy as np
from numpy.typing import NDArray


def ensure_rgba(image: Image.Image) -> Image.Image:
	return image.convert("RGBA")

def get_rgba_pixels(image: Image.Image) -> NDArray[np.uint8]:
	image = image.convert("RGBA")
	return np.asarray(image, dtype=np.uint8)

def convert_to_png_hex(image: Image.Image) -> str:
	output = BytesIO()
	image.save(output, format="PNG")
	file_bytes = output.getvalue()
	hex = file_bytes.hex()
	return hex

EMPTY_IMAGE: Image.Image = Image.new("RGBA", (0, 0), (0, 0, 0, 0))
