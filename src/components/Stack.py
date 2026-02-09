from . import Group, Component
from typing import Literal
from PIL import Image


Direction = Literal['vertical', 'horizontal']
Alignment = Literal['left_top', 'left_center', 'left_bottom', 'center_top', 'center_center', 'center_bottom', 'right_top', 'right_center', 'right_bottom']

class Stack(Group):
	def __init__(self, direction: Direction, alignment: Alignment, *children: Component):
		super().__init__(*children)
		self._direction = direction
		self._alignment = alignment

	def calculate_children_constraints(self):
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
			render_buffer = child.render()
			mask = render_buffer if render_buffer.mode == "RGBA" else None
			image.paste(render_buffer, child._render_properties.position, mask)
		return image

	# TODO: implement