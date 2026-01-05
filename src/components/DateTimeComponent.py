from . import TextComponent
from datetime import datetime


class DateTimeComponent(TextComponent):
	def __init__(self, format: str = "%Y-%m-%d %H:%M:%S"):
		self.format = format
		super().__init__(self._get_formated_datetime())

	def update(self):
		self.text = self._get_formated_datetime()

	def _get_formated_datetime(self) -> str:
		return datetime.now().strftime(self.format)
