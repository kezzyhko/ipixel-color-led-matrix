from typing import TypeGuard, cast
from . import DisplayTarget
from PIL.Image import Image
from bleak import BleakScanner, BleakClient
from bleak.backends.client import BaseBleakClient
from bleak.backends.device import BLEDevice
from bleak.exc import BleakDeviceNotFoundError
from pypixelcolor import AsyncClient # TODO!: use other (maybe custom) wrapper instead of pypixelcolor
from pypixelcolor.lib.device_session import DeviceSession
from helpers import image as image_helpers


class IPixelColorMatrix(DisplayTarget):
	def __init__(self, mac_address: str | None = None):
		super().__init__()
		self._requested_mac_address = mac_address
		self._client: AsyncClient|None = None

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

	@staticmethod
	def _is_connected(client: AsyncClient | None) -> TypeGuard[AsyncClient]:
		return client is not None and client._session.is_connected  # pyright: ignore[reportAttributeAccessIssue]

	@property
	def is_available(self) -> bool:
		return IPixelColorMatrix._is_connected(self._client)

	@property
	def client(self) -> AsyncClient:
		if not IPixelColorMatrix._is_connected(self._client):
			raise ConnectionError("Not connected to device")
		return self._client

	@client.setter
	def client(self, new_client: AsyncClient):
		self._client = new_client

	def _check_connection(self):
		if not self.is_available:
			raise ConnectionError("Not connected to device")
	
	@property
	def width(self) -> int:
		self._check_connection()
		return self.client.get_device_info().width
	
	@property
	def height(self) -> int:
		self._check_connection()
		return self.client.get_device_info().height

	def _set_ble_disconnect_callback(self, client: AsyncClient):
		"""Hook into pypixelcolor's underlying BleakClient so we get unsolicited disconnect events.
		AsyncClient does not expose a disconnect event; DeviceSession uses one internally only.
		"""
		session = cast(DeviceSession, client._session) # pyright: ignore[reportAttributeAccessIssue]
		bleak_client = cast(BleakClient, session._client)
		bleak_backend = cast(BaseBleakClient, bleak_client._backend)
		def _on_ble_disconnect():
			session._on_disconnect(bleak_client)
			self._send_unavailable_event()
		bleak_backend.set_disconnected_callback(_on_ble_disconnect)

	async def setup(self):
		if not self._client:
			mac_address = self._requested_mac_address or await IPixelColorMatrix.get_single_device()
			self._client = AsyncClient(address=mac_address)
		if not self.is_available:
			await self._client.connect()
			self._set_ble_disconnect_callback(self._client)
		await self._client.set_fun_mode(True)

	async def teardown(self):
		if not self.is_available:
			self._client = None
			return
		await self.client.set_fun_mode(False)
		await self.client.disconnect()
		self._client = None

	async def display(self, image: Image):
		self._check_connection()
		png_hex = image_helpers.convert_to_png_hex(image)
		await self.client.send_image_hex(png_hex, ".png")
