import asyncio
import datetime
import time
from typing import Callable
import traceback


class Timer:
	def __init__(self, interval: datetime.timedelta, callback: Callable):
		self._interval: datetime.timedelta = interval
		self._running: bool = False
		self._task: asyncio.Task | None = None
		self._callback: Callable = callback

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
			except Exception as e:
				print(f"Error in Timer callback")
				print(traceback.format_exc())
			end_time = time.monotonic()
			elapsed_time = end_time - start_time
			seconds_to_sleep = self._interval.total_seconds() - elapsed_time
			if seconds_to_sleep > 0:
				await asyncio.sleep(seconds_to_sleep)
