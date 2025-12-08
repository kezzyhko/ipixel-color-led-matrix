import pypixelcolor
from bleak import BleakScanner
from bleak.exc import BleakDeviceNotFoundError

from .config import Config


class Controller:
	def __init__(self, config: Config):
		self.config: Config = config
		self.client = pypixelcolor.AsyncClient(self.config.mac_address)

	@staticmethod
	async def search_devices():
		devices = await BleakScanner.discover(timeout=5.0)
		return [
			device
			for device in devices
			if device.name and device.name.startswith("LED_BLE_")
		]

	@classmethod
	async def create(cls, config_path: str, auto_connect: bool = True) -> "Controller":
		config = Config(config_path)

		if config.mac_address == "search":
			devices = await Controller.search_devices()
			match len(devices):
				case 0:
					raise BleakDeviceNotFoundError("No devices found")
				case 1:
					print(f"Found device: {devices[0]}")
					print(f"Setting it explicitly in config will make connection faster")
					config.mac_address = devices[0].address
				case _:
					raise ValueError(f"Multiple devices found: {devices}")

		controller = cls(config)
		if auto_connect:
			await controller.connect()

		return controller

	async def connect(self) -> None:
		await self.client.connect()
