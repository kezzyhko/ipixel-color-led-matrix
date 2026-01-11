from abc import ABCMeta, abstractmethod
from PIL.Image import Image
from . import Group


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
	def render(self) -> Image:
		pass
