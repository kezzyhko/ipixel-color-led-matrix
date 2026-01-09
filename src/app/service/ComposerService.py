from . import Service
from scenes import create_breifing_scene
from display_target import DisplayTarget
from multitimer import MultiTimer
import asyncio


class ComposerService(Service):
	def __init__(self, display_target: DisplayTarget, fps: int):
		super().__init__()
		self.scene = create_breifing_scene() # TODO: initial scene should be passed as argument
		self.display_target = display_target
		self._timer = MultiTimer(interval=1.0/fps, function=self._tick)

	async def on_start(self):
		await self.display_target.setup()
		self._timer.start()

	async def on_stop(self):
		self._timer.stop()
		await self.display_target.teardown()

	def _tick(self):
		asyncio.run(self._tick_async())

	async def _tick_async(self):
		self.scene.update()
		screen_buffer = self.scene.render()
		await self.display_target.display(screen_buffer)
		