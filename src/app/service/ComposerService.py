from . import Service
import datetime
from scenes import create_briefing_scene
from display_target import DisplayTarget
from helpers import Timer
import warnings # TODO!: use better logging system
import asyncio
import traceback


class ComposerService(Service):
	def __init__(self, display_target: DisplayTarget, fps: float, auto_reconnect: bool = True, debug_scene: bool = False, debug_render: bool = False, debug_placement: bool = False):
		super().__init__()

		# TODO!: Scene switching - come up with system! Group with enabled/disabled components? Something in ComposerService?
		# TODO! Implement root alignment! Scene with user_root and true_root components?????
		# TODO!: Initial scene should be passed as an argument
		self.scene = create_briefing_scene()

		self._restarting = False
		self.display_target = display_target
		if auto_reconnect:
			self.display_target.connect_unavailable(self._on_display_unavailable_sync)

		interval = datetime.timedelta(seconds=1.0/fps)
		self._timer = Timer(interval, self._tick)
		
		self.debug_scene = debug_scene or debug_render or debug_placement
		self.debug_render = debug_render
		self.debug_placement = debug_placement

	async def on_start(self):
		await self.display_target.setup()
		self._timer.start()

	async def on_restart(self):
		await self.on_stop()
		await self.on_start()

	async def on_stop(self):
		self._timer.stop()
		await self.display_target.teardown()

	async def _on_display_unavailable(self):
		if self._restarting:
			return
		self._restarting = True
		warnings.warn("Display target is unavailable, trying to reconnect...")
		attempt_amount = 0
		while not self.display_target.is_available:
			attempt_amount += 1
			print(f"Attempt to reconnect ({attempt_amount})...")
			try:
				await self.on_restart()
			except KeyboardInterrupt or CancelledError:
				raise
			except:
				warnings.warn(f"Error during restart: {traceback.format_exc()}")
			await asyncio.sleep(1.0)
		warnings.warn("Reconnected, continuing...")
		self._restarting = False

	def _on_display_unavailable_sync(self):
		asyncio.create_task(self._on_display_unavailable())

	async def _tick(self):
		self.scene.init_scene_root(self.display_target.width, self.display_target.height)
		self.scene.update()
		self.scene.update_sizing_mode()
		self.scene.render()
		await self.display_target.display(self.scene._render_properties.rendered_image)
		if self.debug_scene:
			self.scene.print_tree(include_placement_info=self.debug_placement, include_render_info=self.debug_render)
