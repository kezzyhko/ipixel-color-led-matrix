from abc import ABCMeta, abstractmethod
from PIL import Image
from . import Component


class TextComponent(Component, metaclass=ABCMeta):
	def __init__(self, text: str):
		super().__init__()
		self.text = text

	def update(self):
		pass

	def render(self) -> Image.Image:
		return Image.new("RGB", (10, 10), (0, 0, 255)) # TODO: use self.text #TODO: size
