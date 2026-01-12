from . import DisplayTarget
from PIL.Image import Image
from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.exc import BleakDeviceNotFoundError
from pypixelcolor import AsyncClient
from helpers import image as image_helpers


class IPixelColorMatrix(DisplayTarget):
	def __init__(self, mac_address: str | None = None):
		self._requested_mac_address = mac_address
		self._client: AsyncClient|None = None
		self._client_connected = False

	@staticmethod
	async def search_devices(timeout: float = 5.0) -> list[BLEDevice]:
		print("Searching for devices...")
		devices = await BleakScanner.discover(timeout=timeout)
		devices = filter(IPixelColorMatrix.device_filter, devices)
		devices = list(devices)
		print("Found devices: ", devices)
		return devices

	@staticmethod
	def device_filter(device: BLEDevice) -> bool:
		return device.name is not None and device.name.startswith("LED_BLE_")

	@staticmethod
	async def get_single_device() -> str:
		devices = await IPixelColorMatrix.search_devices()
		match len(devices):
			case 0:
				raise BleakDeviceNotFoundError("No devices found")
			case 1:
				print(f"Using single found device: {devices[0]}")
				print(f"Setting it explicitly in config will make connection faster")
				return devices[0].address
			case _:
				raise BleakDeviceNotFoundError(f"Multiple devices found: {devices}")

	async def setup(self):
		if self._client_connected:
			await self._client.set_fun_mode(False)
			return
		mac_address = self._requested_mac_address or await IPixelColorMatrix.get_single_device()
		self._client = AsyncClient(address=mac_address)
		await self._client.connect()
		self._client_connected = True
		await self._client.set_fun_mode(True)

	async def teardown(self):
		if not self._client_connected:
			return
		await self._client.set_fun_mode(False)
		await self._client.disconnect()
		self._client_connected = False

	async def display(self, image: Image):
		if not self._client:
			raise ConnectionError("Not connected to device")
		
		png_hex = image_helpers.convert_to_png_hex(image)
		await self._client.send_image_hex(png_hex, ".png")
