from . import TextComponent
from datetime import datetime


class DateTimeComponent(TextComponent):
	SIMPLE_DATE = "%d %b"
	SIMPLE_TIME = "%H:%M"
	SIMPLE_WEEKDAY = "%a"
	SIMPLE_DATETIME = f"{SIMPLE_DATE} {SIMPLE_TIME}"
	FULL_DATE = "%Y-%m-%d"
	FULL_TIME = "%H:%M:%S"
	FULL_WEEKDAY = "%A"
	FULL_DATETIME = f"{FULL_DATE} {FULL_WEEKDAY} {FULL_TIME}"
	# TODO: add day of week

	def __init__(self, format: str = SIMPLE_DATETIME):
		self.format = format
		super().__init__(self._get_formated_datetime())

	def update(self):
		self.text = self._get_formated_datetime()

	def _get_formated_datetime(self) -> str:
		now = datetime.now()
		formated_string = now.strftime(self.format)
		formated_string = formated_string.upper()
		if now.second % 2 == 0:
			formated_string = formated_string.replace(":", " ") # thin space
		return formated_string
