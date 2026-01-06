from . import Service
from scenes import create_breifing_scene
from display_target import DisplayTarget
from multitimer import MultiTimer



class ComposerService(Service):
	def __init__(self, display_target: DisplayTarget, fps: int):
		super().__init__()
		self.scene = create_breifing_scene() # TODO: initial scene should be passed as argument
		self.display_target = display_target
		self._timer = MultiTimer(interval=1.0/fps, function=self.tick)

	def on_start(self):
		self.display_target.setup()
		self._timer.start()

	def on_stop(self):
		self._timer.stop()
		self.display_target.teardown()

	def tick(self):
		self.scene.update()
		screen_buffer = self.scene.render()
		self.display_target.display(screen_buffer)
		