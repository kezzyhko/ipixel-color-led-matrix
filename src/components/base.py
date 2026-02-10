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


class RenderProperties:
	def __init__(self):
		self._sizing_mode_x: SizingMode = 'output'
		self._sizing_mode_y: SizingMode = 'output'
		self._x: int|None = None
		self._y: int|None = None
		self._max_width: int|None = None
		self._max_height: int|None = None
		self._width: int
		self._height: int
		self._rendered_image: Image.Image|None = None

	@property
	def position(self) -> tuple[int, int]:
		if self._x is None or self._y is None:
			raise ValueError(f"Position is not set (x={self._x}, y={self._y})")
		return (self._x, self._y)

	@property
	def max_width(self) -> int:
		if self._max_width is None:
			raise ValueError(f"Width is not set (width={self._max_width})")
		return self._max_width

	@property
	def max_height(self) -> int:
		if self._max_height is None:
			raise ValueError(f"Height is not set (height={self._max_height})")
		return self._max_height

	@property
	def max_size(self) -> tuple[int, int]:
		return (self.max_width, self.max_height)

	@max_size.setter
	def max_size(self, new_max_size: tuple[int|None, int|None]):
		self._max_width, self._max_height = new_max_size

	@property
	def size(self) -> tuple[int, int]:
		return (self._width, self._height)

	@size.setter
	def size(self, new_size: tuple[int, int]):
		self._width, self._height = new_size

	@property
	def sizing_mode(self) -> tuple[SizingMode, SizingMode]:
		return (self._sizing_mode_x, self._sizing_mode_y)

	@sizing_mode.setter
	def sizing_mode(self, new_sizing_mode: tuple[SizingMode, SizingMode]):
		self._sizing_mode_x, self._sizing_mode_y = new_sizing_mode

	@property
	def is_max_size_ready(self) -> bool:
		is_max_width_ready = self._sizing_mode_x == 'output' or self._max_width is not None
		is_max_height_ready = self._sizing_mode_y == 'output' or self._max_height is not None
		return is_max_width_ready and is_max_height_ready

	@property
	def rendered_image(self) -> Image.Image:
		if self._rendered_image is None:
			raise ValueError(f"Component was not rendered yet")
		return self._rendered_image

	@rendered_image.setter
	def rendered_image(self, new_rendered_image: Image.Image):
		self._rendered_image = new_rendered_image


class Component(metaclass=ABCMeta):
	def __init__(self):
		self.placement = Placement()
		self._render_properties: RenderProperties
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

	def init_render_pass(self):
		self._render_properties = RenderProperties()

	@abstractmethod
	def update(self):
		...

	def update_sizing_mode(self):
		self._render_properties.sizing_mode = self._calculate_sizing_mode()

	@abstractmethod
	def _calculate_sizing_mode(self) -> tuple[SizingMode, SizingMode]:
		...

	@abstractmethod
	def _render_implementation(self) -> Image.Image:
		...

	def render(self):
		if self._render_properties.rendered_image is not None:
			return
		image = self._render_implementation()
		self._render_properties.rendered_image = image
		self._render_properties.size = image.size


class Group(Component):
	def __init__(self, *children: Component):
		super().__init__()
		self.children: list[Component] = []
		for child in children:
			self.add_child(child)
		self.background_color = (0, 0, 0, 0)

	def init_render_pass(self):
		super().init_render_pass()
		for child in self.children:
			child.init_render_pass()

	def update(self):
		for child in self.children:
			child.update()
		
	def _calculate_sizing_mode(self) -> tuple[SizingMode, SizingMode]:
		sizing_mode_x = sizing_mode_y = 'output'
		for child in self.children:
			child.update_sizing_mode()
			if child._render_properties._sizing_mode_x == 'input':
				sizing_mode_x = 'input'
			if child._render_properties._sizing_mode_y == 'input':
				sizing_mode_y = 'input'
		return (sizing_mode_x, sizing_mode_y)

	def update_children_constraints(self):
		max_width = self._render_properties.max_width
		max_height = self._render_properties.max_height
		
		for child in self.children:
			if child._render_properties._sizing_mode_x == 'input' and child.placement.width is None:
				raise ValueError(f"Width is not set for Group's child")
			if child._render_properties._sizing_mode_y == 'input' and child.placement.height is None:
				raise ValueError(f"Height is not set for Group's child")
			child._render_properties._x = round(child.placement.x * max_width)
			child._render_properties._y = round(child.placement.y * max_height)
			child._render_properties._max_width = round((child.placement.width or 1) * max_width)
			child._render_properties._max_height = round((child.placement.height or 1) * max_height)

	def _render_implementation(self) -> Image.Image:
		size = (self._render_properties.max_width, self._render_properties.max_height) # TODO: shrink if necessary
		image = Image.new("RGBA", size, self.background_color)
		for child in self.children:
			child.render()
			rendered_image = child._render_properties.rendered_image
			mask = rendered_image if rendered_image.mode == "RGBA" else None
			image.paste(rendered_image, child._render_properties.position, mask)
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
