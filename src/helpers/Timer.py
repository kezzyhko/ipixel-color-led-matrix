import asyncio
import datetime
import time
from typing import Callable
import traceback
import warnings


class Timer:
	def __init__(self, interval: datetime.timedelta, callback: Callable):
		self._interval: datetime.timedelta = interval
		self._running: bool = False
		self._task: asyncio.Task | None = None
		self._callback: Callable = callback
		self.reported_errors: list[Exception] = []

	def start(self):
		if self._running:
			raise RuntimeError("Timer is already running")
		self._running = True
		self._task = asyncio.create_task(self._loop())

	def stop(self):
		if not self._running:
			return
		if self._task:
			self._task.cancel()
		self._task = None
		self._running = False

	async def _loop(self):
		while self._running:
			start_time = time.monotonic()
			try:
				await self._callback()
			except Exception as error:
				self._report_error(error)
			end_time = time.monotonic()
			elapsed_time = end_time - start_time
			seconds_to_sleep = self._interval.total_seconds() - elapsed_time
			if seconds_to_sleep > 0:
				await asyncio.sleep(seconds_to_sleep)
			if seconds_to_sleep < 0:
				warnings.warn(f"Timer can not keep up: Time taken ({elapsed_time}s) > Interval ({self._interval.total_seconds()}s)")

	def _report_error(self, current_error: Exception):
		if self._was_error_already_reported(current_error):
			return
		self.reported_errors.append(current_error)
		start_line = "========== ERROR IN TIMER CALLBACK =========="
		end_line = "============================================="
		previous_errors_info = f"TIMER errors reported so far: {len(self.reported_errors)}"
		warning_text = f"\n{start_line}\n{traceback.format_exc()}\n{previous_errors_info}\n{end_line}"
		warnings.warn(warning_text)

	def _was_error_already_reported(self, current_error: Exception) -> bool:
		for reported_error in self.reported_errors:
			if type(reported_error) == type(current_error) and reported_error.args == current_error.args:
				return True
		return False