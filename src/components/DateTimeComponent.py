from . import TextComponent
from datetime import datetime


class DateTimeComponent(TextComponent):
	SIMPLE_DATE = "%d %b"
	SIMPLE_TIME = "%H:%M"
	SIMPLE_DATETIME = f"{SIMPLE_DATE} {SIMPLE_TIME}"
	FULL_DATE = "%Y-%m-%d"
	FULL_TIME = "%H:%M:%S"
	FULL_DATETIME = f"{FULL_DATE} {FULL_TIME}"

	def __init__(self, format: str = SIMPLE_DATETIME):
		self.format = format
		super().__init__(self._get_formated_datetime())

	def update(self):
		self.text = self._get_formated_datetime()

	def _get_formated_datetime(self) -> str:
		return datetime.now().strftime(self.format)
