from display_target.DisplayTarget import DisplayTarget
from PIL.Image import Image


class IPixelColorMatrix(DisplayTarget):
	def __init__(self):
		pass

	def display(self, image: Image):
		raise NotImplementedError("IPixelColorMatrix is not implemented yet") #TODO: Implement
