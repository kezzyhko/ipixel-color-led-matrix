from . import Group, Component
from typing import Literal
from PIL import Image


Direction = Literal['vertical', 'horizontal']
Alignment = Literal['left_top', 'left_center', 'left_bottom', 'center_top', 'center_center', 'center_bottom', 'right_top', 'right_center', 'right_bottom']

class Stack(Group):
	def __init__(self, *children: Component, direction: Direction, alignment: Alignment, spacing: float = 0.0):
		super().__init__(*children)
		self._direction = direction
		self._alignment = alignment
		self._spacing = spacing

	def calculate_children_constraints(self):
		main_axis, cross_axis = (0, 1) if self._direction == 'horizontal' else (1, 0)
		stack_size = self._render_properties.max_size
		
		max_cross_size: int = 0
		main_size_left: int = stack_size[main_axis]
		total_weight: float = 0.0

		# Pass 1: render already defined sizes and get stats for pass 2
		for child in self.children:
			child_main_size = child.placement.size[main_axis]
			child_cross_size = child.placement.size[cross_axis]
			pixels_max_cross_size = round(child_cross_size * stack_size[cross_axis]) if child_cross_size is not None else stack_size[cross_axis]
			pixels_max_main_size = round(child_main_size * stack_size[main_axis]) if child_main_size is not None else None			
			child_max_size = self._get_xy_from_maincross(pixels_max_main_size, pixels_max_cross_size)
			child._render_properties.max_size = child_max_size

			if child_main_size is None and child._render_properties.sizing_mode[main_axis] == 'input':
				total_weight += child.placement.weight

			if child._render_properties.is_max_size_ready:
				child.render()
				child_size = child._render_properties.size
				main_size_left -= child_size[main_axis]
				max_cross_size = max(max_cross_size, child_size[cross_axis])

		# Pass 2: render rest of components by weight
		for child in self.children:
			if child._render_properties.max_size[main_axis] is not None:
				continue
			pixels_max_main_size = round(main_size_left * child.placement.weight / total_weight)
			child._render_properties.max_size = self._get_xy_from_maincross(pixels_max_main_size, child._render_properties.max_size[cross_axis])
			child.render()

	def _get_xy_from_maincross(self, main: int|None, cross: int|None) -> tuple[int|None, int|None]:
		return (main, cross) if self._direction == 'horizontal' else (cross, main)

	def _render_implementation(self) -> Image.Image:
		size = (self._render_properties.max_width, self._render_properties.max_height) # TODO: shrink if necessary
		image = Image.new("RGBA", size, self.background_color)
		for child in self.children:
			rendered_image = child._render_properties.rendered_image
			mask = rendered_image if rendered_image.mode == "RGBA" else None
			image.paste(rendered_image, child._render_properties.position, mask)
		return image

	# TODO: implement