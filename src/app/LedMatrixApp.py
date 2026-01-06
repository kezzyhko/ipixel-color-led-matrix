import asyncio
from app.service import ComposerService
from display_target import DisplayTarget


class LedMatrixApp:
	def __init__(self, display_target: DisplayTarget, fps: int = 120, is_debug: bool = False):
		self.is_debug = is_debug
		# TODO: create events, pass to all services??
		# TODO: Implement services
		self._stop_event = asyncio.Event()
		self.composer_service = ComposerService(display_target, fps) # TODO: pass fps from config
		# self.cli_controller_service = CliControllerService()
		# self.http_controller_service = HttpControllerService()

	async def run(self):
		self.composer_service.start()
		# self.cli_controller_service.start()
		# self.http_controller_service.start()
		# TODO: start with loop over an array of services
		# TODO: connect events?
		await self._stop_event.wait()

	async def end(self):
		self.composer_service.stop()
		# TODO: stop with loop over an array of services
		self._stop_event.set()
