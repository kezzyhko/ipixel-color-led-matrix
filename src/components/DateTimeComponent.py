from typing import Literal
from . import TextComponent
from datetime import datetime
from app import context
from helpers import TempLocale
import locale

class DateTimeComponent(TextComponent):
	SIMPLE_DATE = "%d %b"
	SIMPLE_TIME = "%H:%M"
	SIMPLE_WEEKDAY = "%a"
	SIMPLE_DATETIME = f"{SIMPLE_DATE} {SIMPLE_TIME}"
	FULL_DATE = "%Y-%m-%d"
	FULL_TIME = "%H:%M:%S"
	FULL_WEEKDAY = "%A"
	FULL_DATETIME = f"{FULL_DATE} {FULL_WEEKDAY} {FULL_TIME}"

	def __init__(self, format: str = SIMPLE_DATETIME, locale: str|None = None, case: Literal['default', 'upper', 'lower', 'title'] = 'default', **kwargs):
		self._locale = locale or context.locale_code.get() or "en"
		self._format = format
		self._case = case
		super().__init__(self._get_formated_datetime(), **kwargs)

	def update(self):
		self.text = self._get_formated_datetime()

	def _get_formated_datetime(self) -> str:
		now = datetime.now()
		with TempLocale(self._locale, locale.LC_ALL):
			formated_string = now.strftime(self._format)
		match self._case:
			case 'default':
				pass
			case 'upper':
				formated_string = formated_string.upper()
			case 'lower':
				formated_string = formated_string.lower()
			case 'title':
				formated_string = formated_string.title()
		if now.second % 2 == 0:
			formated_string = formated_string.replace(":", " ") # thin space
		return formated_string
