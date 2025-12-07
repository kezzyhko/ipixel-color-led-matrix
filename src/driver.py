from bleak import BleakScanner
from bleak.backends.device import BLEDevice

from src.config import Config


class Driver:
	def __init__(self, config: Config):
		self.config: Config = config

	async def connect(self):
		if not self.config.mac_address:
			devices: list[BLEDevice] = await self.search_devices()
				raise Exception(f"Please specify a mac address in the config file. Found devices: {devices}")
		return None

	async def search_devices(self):
		devices = await BleakScanner.discover(timeout=15.0)
		return [
			device
			for device in devices
			if device.name and device.name.startswith("LED_BLE_")
		]