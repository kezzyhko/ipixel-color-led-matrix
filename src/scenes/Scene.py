from components import Component, Group
from PIL.Image import Image

class Scene:
	def __init__(self, *children: Component):
		self.root = Group(*children)

	def update(self):
		self.root.update()

	def render(self) -> Image:
		return self.root.render()
