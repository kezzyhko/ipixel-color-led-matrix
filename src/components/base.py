from abc import ABCMeta, abstractmethod
from PIL import Image
from typing import Literal, Iterable
from helpers import terminal as terminal_helpers


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
	
	def _get_tree_lines(self) -> Iterable[str]:
		yield f"Position: {self.position}"
		yield f"Size: {self.size}"
		yield f"Weight: {self.weight}"


class RenderProperties:
	def __init__(self, component: Component):
		self._component: Component = component
		self._sizing_mode_x: SizingMode = 'output'
		self._sizing_mode_y: SizingMode = 'output'
		self._x: int|None = None
		self._y: int|None = None
		self._max_width: int|None = None
		self._max_height: int|None = None
		self._width: int|None = None
		self._height: int|None = None
		self._rendered_image: Image.Image|None = None


	def _value_if_set[T](self, value: T|None, name: str) -> T:
		if value is None:
			raise ValueError(f"{name} is not set: {self._component.get_full_path()}")
		return value

	@property
	def x(self) -> int:
		return self._value_if_set(self._x, "X")

	@property
	def y(self) -> int:
		return self._value_if_set(self._y, "Y")

	@property
	def position(self) -> tuple[int, int]:
		return (self.x, self.y)

	@position.setter
	def position(self, new_position: tuple[int, int]):
		self._x, self._y = new_position

	@property
	def max_width(self) -> int:
		if self._max_width is not None:
			return self._max_width
		elif self._sizing_mode_x == 'input':
			raise ValueError(f"Max width was not set: {self._component.get_full_path()}")
		elif self._component.parent is not None:
			return self._component.parent._render_properties.max_width
		else:
			raise ValueError(f"Max width was not set, and component has no parent: {self._component.get_full_path()}")

	@property
	def max_height(self) -> int:
		if self._max_height is not None:
			return self._max_height
		elif self._sizing_mode_y == 'input':
			raise ValueError(f"Max height was not set: {self._component.get_full_path()}")
		elif self._component.parent is not None:
			return self._component.parent._render_properties.max_height
		else:
			raise ValueError(f"Max height was not set, and component has no parent: {self._component.get_full_path()}")

	@property
	def max_size(self) -> tuple[int, int]:
		return (self.max_width, self.max_height)

	@max_size.setter
	def max_size(self, new_max_size: tuple[int|None, int|None]):
		self._max_width, self._max_height = new_max_size

	@property
	def width(self) -> int:
		return self._value_if_set(self._width, "Width")

	@property
	def height(self) -> int:
		return self._value_if_set(self._height, "Height")

	@property
	def size(self) -> tuple[int, int]:
		return (self.width, self.height)

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
	def is_max_size_axis_ready(self) -> tuple[bool, bool]:
		is_max_width_ready = self._sizing_mode_x == 'output' or self._max_width is not None
		is_max_height_ready = self._sizing_mode_y == 'output' or self._max_height is not None
		return (is_max_width_ready, is_max_height_ready)

	@property
	def is_max_size_ready(self) -> bool:
		return all(self.is_max_size_axis_ready)

	@property
	def rendered_image(self) -> Image.Image:
		return self._value_if_set(self._rendered_image, "Rendered image")

	@rendered_image.setter
	def rendered_image(self, new_rendered_image: Image.Image):
		self._rendered_image = new_rendered_image

	@property
	def is_rendered(self) -> bool:
		return self._rendered_image is not None

	def _get_tree_lines(self) -> Iterable[str]:
		yield f"Position: {self.position}"
		yield f"Size: {self.size}"


class Component(metaclass=ABCMeta):
	def __init__(self, name: str|None = None, placement: Placement = Placement()):
		self.name = name if name is not None else f"{type(self).__name__}_{id(self)}"
		self.placement = placement
		self._render_properties: RenderProperties
		self._parent: Group|None = None

	def get_full_path(self):
		parent_path = self.parent.get_full_path() if self.parent else ""
		return f"{parent_path}/{self.name}"

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
		self._render_properties = RenderProperties(self)

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
		if self._render_properties.is_rendered:
			return
		image = self._render_implementation()
		self._render_properties.rendered_image = image
		self._render_properties.size = image.size

	def print_tree(self, description: str = "", include_placement_info: bool = False, include_render_info: bool = False):
		print("===== TREE START =====")
		if description != "":
			print(f"Description: {description}")
			print()
		for line in self._get_tree_lines(include_placement_info, include_render_info):
			print(line)
		print("===== TREE END =====")

	def _get_tree_lines(self, include_placement_info: bool = False, include_render_info: bool = False) -> Iterable[str]:
		yield f"{self.name}"
		if include_placement_info:
			yield from terminal_helpers.add_indent(self.placement._get_tree_lines())
		if include_placement_info and include_render_info:
			yield ""
		if include_render_info and self.parent is not None:
			yield from terminal_helpers.add_indent(self._render_properties._get_tree_lines())


class Group(Component):
	def __init__(self, name: str|None = None, placement: Placement = Placement(), children: Iterable[Component] = []):
		super().__init__(name=name, placement=placement)
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
			if child._render_properties._sizing_mode_x == 'input' or child.placement.width is not None:
				sizing_mode_x = 'input'
			if child._render_properties._sizing_mode_y == 'input' or child.placement.height is not None:
				sizing_mode_y = 'input'
		return (sizing_mode_x, sizing_mode_y)

	def _calculate_children_constraints(self):
		max_width = self._render_properties.max_width
		max_height = self._render_properties.max_height
		
		for child in self.children:
			if child._render_properties._sizing_mode_x == 'input' and child.placement.width is None:
				raise ValueError(f"Width is not set for Group's child: {child.get_full_path()}")
			if child._render_properties._sizing_mode_y == 'input' and child.placement.height is None:
				raise ValueError(f"Height is not set for Group's child: {child.get_full_path()}")
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

	def render(self):
		if self._render_properties.is_rendered:
			return
		self._calculate_children_constraints()
		super().render()

	def _get_tree_lines(self, include_placement_info: bool = False, include_render_info: bool = False) -> Iterable[str]:
		yield from super()._get_tree_lines(include_placement_info, include_render_info)
		if include_render_info or include_placement_info:
			yield ""
		for child in self.children:
			yield from terminal_helpers.add_indent(child._get_tree_lines(include_placement_info, include_render_info))
			yield ""
			

	def add_child(self, child: Component):
		if child in self.children:
			return
		self.children.append(child)
		child.parent = self

	def remove_child(self, child: Component):
		if child not in self.children:
			return
		child.parent = None
