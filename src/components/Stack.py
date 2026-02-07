from . import Group, Component
from typing import Literal


StackDirection = Literal['vertical', 'horizontal']

class Stack(Group):
	def __init__(self, direction: StackDirection, *children: Component):
		super().__init__(*children)
		self._direction = direction

	# def update(self):
	# 	pass

	# def render(self) -> Image.Image:
	# 	pass

	# TODO: implement