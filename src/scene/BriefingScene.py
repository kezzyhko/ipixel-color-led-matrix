from scene import Scene


class BriefingScene(Scene):
	def __init__(self):
		super().__init__()
		self.add_component(DateTimeComponent())
