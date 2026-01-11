from contextvars import ContextVar
from typing import Literal
import contextlib
import locale

locale_code: ContextVar[str] = ContextVar('locale', default='en')
weather_city: ContextVar[str | None] = ContextVar('weather_city', default=None)
weather_units: ContextVar[Literal['metric', 'imperial']] = ContextVar('weather_units', default='metric')


@contextlib.contextmanager
def temporary_locale(loc, category: int = locale.LC_ALL):
    """Context manager to temporarily change locale"""
    old_locale = locale.getlocale(category)
    try:
        locale.setlocale(category, loc)
        yield
    finally:
        locale.setlocale(category, old_locale)
