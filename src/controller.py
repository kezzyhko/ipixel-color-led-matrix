from src.config import Config
from src.driver import Driver


class Controller:
	def __init__(self, config: Config):
		self.config: Config = config
		self.driver: Driver = Driver(config)

	@classmethod
	async def create(cls, config: Config, auto_connect: bool = True) -> "Controller":
		controller = cls(config)
		if auto_connect:
			await controller.connect()
		return controller

	async def connect(self) -> None:
		await self.driver.connect()
