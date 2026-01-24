from abc import ABCMeta, abstractmethod
from PIL import Image


class Component(metaclass=ABCMeta):
	def __init__(self):
		self.x = 0
		self.y = 0
		self._parent: Group|None = None

	@property
	def parent(self) -> Group|None:
		return self._parent

	@parent.setter
	def parent(self, new_parent: Group|None):
		del self.parent
		if not new_parent:
			return
		self._parent = new_parent
		new_parent.add_child(self)

	@parent.deleter
	def parent(self):
		if not self._parent:
			return
		self._parent.remove_child(self)
		self._parent = None

	@abstractmethod
	def update(self):
		pass

	@abstractmethod
	def render(self) -> Image.Image:
		pass


class Group(Component):
	def __init__(self, *children: Component):
		super().__init__()
		self.children: list[Component] = []
		for child in children:
			self.add_child(child)
		self.background_color = (0, 0, 0, 0)

	def update(self):
		for child in self.children:
			child.update()

	def render(self) -> Image.Image:
		image = Image.new("RGBA", (64, 16), self.background_color) #TODO: size
		for child in self.children:
			render_buffer = child.render()
			mask = render_buffer if render_buffer.mode == "RGBA" else None
			image.paste(render_buffer, (child.x, child.y), mask)
		return image

	def add_child(self, child: Component):
		if child in self.children:
			return
		self.children.append(child)
		child.parent = self

	def remove_child(self, child: Component):
		if child not in self.children:
			return
		child.parent = None
