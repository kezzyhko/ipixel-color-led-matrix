from . import DisplayTarget
from PIL.Image import Image


class IPixelColorMatrix(DisplayTarget):
	def setup(self):
		pass
	
	def teardown(self):
		pass

	def display(self, image: Image):
		raise NotImplementedError("IPixelColorMatrix is not implemented yet") #TODO: Implement
