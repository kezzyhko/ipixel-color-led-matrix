from abc import ABCMeta, abstractmethod


class Service(metaclass=ABCMeta):
	def __init__(self):
		self.is_running = False

	async def start(self):
		if self.is_running:
			raise RuntimeError("Service is already running")
		self.is_running = True
		await self.on_start()
		
	async def stop(self):
		if not self.is_running:
			return
		await self.on_stop()
		self.is_running = False
	
	@abstractmethod
	async def on_start(self):
		...
	
	@abstractmethod
	async def on_stop(self):
		...
