from abc import ABCMeta, abstractmethod
from PIL.Image import Image


class DisplayTarget(metaclass=ABCMeta):
	@abstractmethod
	def setup(self):
		pass
	
	@abstractmethod
	def teardown(self):
		pass

	@abstractmethod
	def display(self, image: Image):
		pass
