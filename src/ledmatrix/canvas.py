class Dimension:
	def __init__(self, width: int, height: int):
		if width < 0 or height < 0:
			raise ValueError("Dimensions must be non-negative")
		self.width = width
		self.height = height


class Canvas:
	def __init__(self, size: Dimension):
		self.size = size
		self._layers = []
	
	def create_layer(self) -> Layer:
		layer = Layer(self.size)
		self._layers.append(layer)
		return layer
	
	def remove_layer(self, layer: Layer):
		self._layers.remove(layer)


class Layer:
	def __init__(self, size: Dimension):
		self.size = size
