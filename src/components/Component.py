from abc import ABCMeta, abstractmethod
from PIL.Image import Image


class Component(metaclass=ABCMeta):
	def __init__(self):
		self.x = 0
		self.y = 0
		self.parent: Component|None = None

	@abstractmethod
	def update(self):
		pass

	@abstractmethod
	def render(self) -> Image:
		pass
