from abc import ABCMeta, abstractmethod


class Service(metaclass=ABCMeta):
	@abstractmethod
	def run(self):
		pass