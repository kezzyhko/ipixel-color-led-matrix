from PIL.Image import Image
import numpy as np
from numpy.typing import NDArray


def ensure_rgba(image: Image) -> Image:
	return image.convert("RGBA")


def get_rgba_pixels(image: Image) -> NDArray[np.uint8]:
	image = image.convert("RGBA")
	return np.asarray(image, dtype=np.uint8)
