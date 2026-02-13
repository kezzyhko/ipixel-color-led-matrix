from abc import ABCMeta, abstractmethod
from PIL.Image import Image


class DisplayTarget(metaclass=ABCMeta):
	
	@property
	@abstractmethod
	def width(self) -> int:
		...
	
	@property
	@abstractmethod
	def height(self) -> int:
		...
	
	@abstractmethod
	async def setup(self):
		...
	
	@abstractmethod
	async def teardown(self):
		...

	@abstractmethod
	async def display(self, image: Image):
		...
		# TODO: Allow program stopping from this function.
		# TODO: For example, when user closes the window or bluetooth device disconnects.
