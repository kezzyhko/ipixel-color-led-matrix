from abc import ABC, abstractmethod
from PIL.Image import Image


class DisplayTarget(ABC):
	@abstractmethod
	def display(self, image: Image):
		pass
