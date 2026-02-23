from abc import ABCMeta, abstractmethod
from PIL.Image import Image
from blinker import Signal
from typing import Callable


class DisplayTarget(metaclass=ABCMeta):
	
	def __init__(self):
		self._unavailable = Signal()

	def _send_unavailable_event(self):
		self._unavailable.send(self)

	def connect_unavailable(self, callback: Callable[[], None]):
		self._unavailable.connect(lambda sender: callback(), weak=False)
	
	@property
	@abstractmethod
	def is_available(self) -> bool:
		...
	
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
