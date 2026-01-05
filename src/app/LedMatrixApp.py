from display_target.DisplayTarget import DisplayTarget


class LedMatrixApp:
	def __init__(self, display_target: DisplayTarget, is_debug: bool = False, fps: int = 120):
		self.is_debug = is_debug
		# TODO: !!! create events, pass to all services
		# TODO: Implement services
		self.composer_service = ComposerService()
		self.display_service = DisplayService(display_target)
		self.cli_controller_service = CliControllerService()
		self.http_controller_service = HttpControllerService()

	async def run(self):
		self.composer_service.run()
		self.display_service.run()
		self.cli_controller_service.run()
		self.http_controller_service.run()
		# TODO: start with loop over an array of services
		# TODO: join all tasks? try/except?
		# TODO: connect events
