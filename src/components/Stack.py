from . import Group, Component
from typing import Literal, Iterable
from PIL import Image


Direction = Literal['vertical', 'horizontal']
Alignment = Literal['left_top', 'left_center', 'left_bottom', 'center_top', 'center_center', 'center_bottom', 'right_top', 'right_center', 'right_bottom']

class Stack(Group):
	def __init__(self, direction: Direction, alignment: Alignment = 'center_center', spacing: float = 0.0, padding: float = 0.0, children: Iterable[Component] = [], name: str|None = None):
		super().__init__(name=name, children=children)
		self._direction = direction
		self._alignment = alignment
		self._spacing = spacing
		self._padding = padding

	def _calculate_children_constraints(self):
		main_axis, cross_axis = (0, 1) if self._direction == 'horizontal' else (1, 0)
		stack_size = self._render_properties.max_size
		pixels_spacing = round(self._spacing * stack_size[main_axis])
		pixels_padding = round(self._padding * stack_size[main_axis])
		
		max_cross_size: int = 0
		main_size_left: int = stack_size[main_axis] - pixels_spacing * (len(self.children) - 1) - pixels_padding * 2
		total_weight: float = 0.0

		# Pass 1: render already defined sizes and get stats for pass 2
		for child in self.children:
			child_main_size = child.placement.size[main_axis]
			child_cross_size = child.placement.size[cross_axis]
			pixels_max_cross_size = round(child_cross_size * stack_size[cross_axis]) if child_cross_size is not None else stack_size[cross_axis]
			pixels_max_main_size = round(child_main_size * stack_size[main_axis]) if child_main_size is not None else None			
			child_max_size = self._get_xy_from_maincross(pixels_max_main_size, pixels_max_cross_size)
			child._render_properties.max_size = child_max_size

			if not child._render_properties.is_max_size_axis_ready[main_axis]:
				total_weight += child.placement.weight

			if child._render_properties.is_max_size_ready:
				child.render()
				child_size = child._render_properties.size
				main_size_left -= child_size[main_axis]
				max_cross_size = max(max_cross_size, child_size[cross_axis])

		# Pass 2: render rest of components by weight
		for child in self.children:
			if child._render_properties.is_max_size_axis_ready[main_axis]:
				continue
			pixels_max_main_size = round(main_size_left * child.placement.weight / total_weight)
			pixels_max_cross_size = child._render_properties.max_height if self._direction == 'horizontal' else child._render_properties.max_width # avoid max_size getter (value on main axis is not ready yet)
			child._render_properties.max_size = self._get_xy_from_maincross(pixels_max_main_size, pixels_max_cross_size)
			child.render()
			max_cross_size = max(max_cross_size, child._render_properties.size[cross_axis])

		# Pass 3: calculate positions
		#TODO LAYOUT implement alignment
		main_position = pixels_padding
		for child in self.children:
			cross_position = 0
			child._render_properties.position = self._get_xy_from_maincross(main_position, cross_position)
			main_position += child._render_properties.size[main_axis] + pixels_spacing

	def _get_xy_from_maincross[T](self, main: T, cross: T) -> tuple[T, T]:
		return (main, cross) if self._direction == 'horizontal' else (cross, main)

	def _render_implementation(self) -> Image.Image:
		image = Image.new("RGBA", self._render_properties.max_size, self.background_color)
		width = height = 0
		for child in self.children:
			rendered_image = child._render_properties.rendered_image
			mask = rendered_image if rendered_image.mode == "RGBA" else None
			image.paste(rendered_image, child._render_properties.position, mask)
			width = max(width, child._render_properties.x + child._render_properties.width)
			height = max(height, child._render_properties.y + child._render_properties.height)
		image = image.crop((0, 0, width, height))
		return image
