from . import Service
from scenes import create_breifing_scene
from display_target import DisplayTarget
import asyncio
import time


class ComposerService(Service):
	def __init__(self, display_target: DisplayTarget, fps: float):
		super().__init__()
		self.scene = create_breifing_scene() # TODO: initial scene should be passed as argument
		self.display_target = display_target
		self._fps = fps
		self._task: asyncio.Task | None = None

	async def on_start(self):
		await self.display_target.setup()
		self._running = True	
		self._task = asyncio.create_task(self._loop())

	async def on_stop(self):
		self._running = False
		if self._task:
			await self._task
		await self.display_target.teardown()

	async def _loop(self):
		interval = 1.0 / self._fps
		while self._running:
			start_time = time.monotonic_ns()
			try:
				await self._tick()
			except Exception as e:
				print(f"Error in ComposerService tick: {e}")
			end_time = time.monotonic_ns()
			elapsed_time = end_time - start_time
			if elapsed_time < interval:
				await asyncio.sleep(interval - elapsed_time)

	async def _tick(self):
		self.scene.update()
		screen_buffer = self.scene.render()
		await self.display_target.display(screen_buffer)
		