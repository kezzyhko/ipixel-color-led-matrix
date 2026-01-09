from abc import ABCMeta, abstractmethod
from PIL.Image import Image


class DisplayTarget(metaclass=ABCMeta):
	@abstractmethod
	async def setup(self):
		pass
	
	@abstractmethod
	async def teardown(self):
		pass

	@abstractmethod
	async def display(self, image: Image):
		pass
