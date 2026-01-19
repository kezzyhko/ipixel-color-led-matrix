from components import Component, Group
from PIL.Image import Image

class Scene:
	def __init__(self, *children: Component):
		self._root = Group(*children)

	def update(self):
		self._root.update()

	def render() -> Image:
		return self._root.render()
