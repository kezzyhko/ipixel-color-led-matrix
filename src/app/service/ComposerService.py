from . import Service
import datetime
from scenes import create_briefing_scene
from display_target import DisplayTarget
from helpers import Timer


class ComposerService(Service):
	def __init__(self, display_target: DisplayTarget, fps: float):
		super().__init__()
		self.scene = create_briefing_scene() # TODO: initial scene should be passed as argument
		self.display_target = display_target
		interval = datetime.timedelta(seconds=1.0/fps)
		self._timer = Timer(interval, self._tick)

	async def on_start(self):
		await self.display_target.setup()
		self._timer.start()

	async def on_stop(self):
		self._timer.stop()
		await self.display_target.teardown()

	async def _tick(self):
		self.scene.init_render_pass()
		self.scene._render_properties._max_width = self.display_target.width
		self.scene._render_properties._max_height = self.display_target.height
		self.scene.update()
		self.scene.update_sizing_mode()
		self.scene.update_children_constraints()
		screen_buffer = self.scene.render()
		await self.display_target.display(screen_buffer)
		