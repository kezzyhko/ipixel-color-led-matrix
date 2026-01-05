from abc import ABCMeta, abstractmethod
from PIL.Image import Image


class DisplayTarget(metaclass=ABCMeta):
	@abstractmethod
	def display(self, image: Image):
		pass
