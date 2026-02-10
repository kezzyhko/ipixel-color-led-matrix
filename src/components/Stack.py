from . import Group, Component
from typing import Literal
from PIL import Image


Direction = Literal['vertical', 'horizontal']
Alignment = Literal['left_top', 'left_center', 'left_bottom', 'center_top', 'center_center', 'center_bottom', 'right_top', 'right_center', 'right_bottom']

class Stack(Group):
	def __init__(self, direction: Direction, alignment: Alignment, spacing: float = 0.0, *children: Component):
		super().__init__(*children)
		self._direction = direction
		self._alignment = alignment
		self._spacing = spacing

	def calculate_children_constraints(self):
		main_axis, cross_axis = (0, 1) if self._direction == 'horizontal' else (1, 0)
		stack_size = self._render_properties.max_size
		
		for child in self.children:
			child_main_size = child.placement.size[main_axis]
			child_cross_size = child.placement.size[cross_axis]
			pixels_cross_size = round(child_cross_size * stack_size[cross_axis]) if child_cross_size is not None else stack_size[cross_axis]
			pixels_main_size = round(child_main_size * stack_size[main_axis]) if child_main_size is not None else None			
			child_size = (pixels_main_size, pixels_cross_size) if self._direction == 'horizontal' else (pixels_cross_size, pixels_main_size)

			child._render_properties.max_size = child_size
			if child._render_properties.is_max_size_ready:
				child.render()
			# child._render_properties._x = round(child.placement.x * max_width)
			# child._render_properties._y = round(child.placement.y * max_height)
			# child._render_properties._max_width = round((child.placement.width or 1) * max_width)
			# child._render_properties._max_height = round((child.placement.height or 1) * max_height)

	def _render_implementation(self) -> Image.Image:
		size = (self._render_properties.max_width, self._render_properties.max_height) # TODO: shrink if necessary
		image = Image.new("RGBA", size, self.background_color)
		for child in self.children:
			render_buffer = child.render()
			mask = render_buffer if render_buffer.mode == "RGBA" else None
			image.paste(render_buffer, child._render_properties.position, mask)
		return image

	# TODO: implement