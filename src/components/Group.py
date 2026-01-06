from . import Component
from PIL import Image


class Group(Component):
	def __init__(self, *children: Component):
		super().__init__()
		self.children: list[Component] = []
		for child in children:
			self.add_child(child)

	def update(self):
		for child in self.children:
			child.update()

	def render(self) -> Image.Image:
		image = Image.new("RGBA", (64, 16), (0, 0, 0, 0)) #TODO: size
		for child in self.children:
			render_buffer = child.render()
			mask = render_buffer if render_buffer.mode == "RGBA" else None
			image.paste(render_buffer, (child.x, child.y), mask)
		return image

	def add_child(self, child: Component):
		self.children.append(child)
		child.parent = self

	def remove_child(self, child: Component):
		self.children.remove(child)
		child.parent = None
