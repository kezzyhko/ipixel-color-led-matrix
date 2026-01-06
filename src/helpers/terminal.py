import sys
from typing import Protocol


ESCAPE_CODE = "\033["


class WriteableStream(Protocol):
	def write(self, s: str, /) -> int | None:
		"""Write a string to the stream. Returns the number of characters written, or None."""
		...

	def flush(self) -> None:
		"""Flush the stream's internal buffer."""
		...


def change_color(r: int, g: int, b: int, stream: WriteableStream = sys.stdout):
	stream.write(f"{ESCAPE_CODE}38;2;{r};{g};{b}m")

def clear_formatting(stream: WriteableStream = sys.stdout):
	stream.write(f"{ESCAPE_CODE}0m")

def set_alternate_screen(is_enabled: bool, stream: WriteableStream = sys.stdout, flush: bool = True):
	letter = "h" if is_enabled else "l"
	stream.write(f"{ESCAPE_CODE}?1049{letter}")
	if flush:
		stream.flush()

def clear_window(stream: WriteableStream = sys.stdout):
	stream.write(f"{ESCAPE_CODE}2J{ESCAPE_CODE}H")
