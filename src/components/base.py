from abc import ABCMeta, abstractmethod
from PIL import Image
from typing import Literal


SizingMode = Literal['input', 'output']


class Placement:
	def __init__(self, x: float = 0.0, y: float = 0.0, width: float|None = None, height: float|None = None, weight: float = 1.0):
		self.x: float = 0.0
		self.y: float = 0.0
		self.width: float|None = None
		self.height: float|None = None
		self.weight: float = 1.0

	@property
	def position(self) -> tuple[float, float]:
		return (self.x, self.y)

	@position.setter
	def position(self, new_position: tuple[float, float]):
		self.x, self.y = new_position

	@property
	def size(self) -> tuple[float|None, float|None]:
		return (self.width, self.height)

	@size.setter
	def size(self, new_size: tuple[float|None, float|None]):
		self.width, self.height = new_size


class Component(metaclass=ABCMeta):
	def __init__(self):
		self.placement = Placement()
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
	def get_sizing_mode(self) -> tuple[SizingMode, SizingMode]:
		...

	@abstractmethod
	def update(self):
		...

	@abstractmethod
	def render(self) -> Image.Image:
		...


class Group(Component):
	def __init__(self, *children: Component):
		super().__init__()
		self.children: list[Component] = []
		for child in children:
			self.add_child(child)
		self.background_color = (0, 0, 0, 0)
		
	def get_sizing_mode(self) -> tuple[SizingMode, SizingMode]:
		children_sizing_modes = [child.get_sizing_mode() for child in self.children]
		def _get_sizing_mode(index: int):
			return 'input' if any(child_sizing_modes[index] == 'input' for child_sizing_modes in children_sizing_modes) else 'output'
		return _get_sizing_mode(0), _get_sizing_mode(1)

	def update(self):
		for child in self.children:
			child.update()

	def render(self) -> Image.Image:
		image = Image.new("RGBA", (64, 16), self.background_color) #TODO: size
		for child in self.children:
			render_buffer = child.render()
			mask = render_buffer if render_buffer.mode == "RGBA" else None
			x = round(child.placement.x * image.width); #TODO: size
			y = round(child.placement.y * image.height); #TODO: size
			image.paste(render_buffer, (x, y), mask)
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
