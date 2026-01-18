from abc import ABCMeta, abstractmethod
from PIL.Image import Image


class DisplayTarget(metaclass=ABCMeta):
	
	@property
	@abstractmethod
	def width(self):
		pass
	
	@property
	@abstractmethod
	def height(self):
		pass
	
	@abstractmethod
	async def setup(self):
		pass
	
	@abstractmethod
	async def teardown(self):
		pass

	@abstractmethod
	async def display(self, image: Image):
		pass
		# TODO: Allow program stopping from this function.
		# TODO: For example, when user closes the window or bluetooth device disconnects.
