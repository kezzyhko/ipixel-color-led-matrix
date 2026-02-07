from . import Group, Component
from typing import Literal


Direction = Literal['vertical', 'horizontal']
Alignment = Literal['left_top', 'left_center', 'left_bottom', 'center_top', 'center_center', 'center_bottom', 'right_top', 'right_center', 'right_bottom']

class Stack(Group):
	def __init__(self, direction: Direction, alignment: Alignment, *children: Component):
		super().__init__(*children)
		self._direction = direction
		self._alignment = alignment

	# def update(self):
	# 	pass

	# def render(self) -> Image.Image:
	# 	pass

	# TODO: implement