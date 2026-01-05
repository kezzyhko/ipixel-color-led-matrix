from abc import ABCMeta, abstractmethod


class Service(metaclass=ABCMeta):
	def __init__(self):
		self.is_running = False

	def start(self):
		if self.is_running:
			raise RuntimeError("Service is already running")
		self.is_running = True
		self.on_start()
		
	def stop(self):
		if not self.is_running:
			return
		self.on_stop()
		self.is_running = False
	
	@abstractmethod
	def on_start(self):
		pass
	
	@abstractmethod
	def on_stop(self):
		pass
