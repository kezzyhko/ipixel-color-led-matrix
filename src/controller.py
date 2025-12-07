import asyncio
import pypixelcolor
from .config import Config


class Controller:
	def __init__(self, config: Config):
		self.config: Config = config
		self.client = pypixelcolor.AsyncClient(self.config.mac_address)

	@classmethod
	async def create_async(cls, config_path: str, auto_connect: bool = True) -> "Controller":
		config = Config(config_path)
		controller = cls(config)
		if auto_connect:
			await controller.connect()
		return controller

	async def connect(self) -> None:
		await self.client.connect()
