import locale


class TempLocale:
	def __init__(self, locale_code: str, category: int = locale.LC_ALL):
		self.changed_category = category
		self.new_locale = locale_code
		self.old_locales: dict[int, str] = {}

	ALL_CATEGORIES = [
		{
			'name': name,
			'value': getattr(locale, name),
		}
		for name in dir(locale)
		if name.startswith("LC_") and name != "LC_ALL"
	]

	def __enter__(self):
		for category_definition in self.ALL_CATEGORIES:
			category = category_definition['value']
			does_category_match = self.changed_category == category or self.changed_category == locale.LC_ALL
			new_locale = self.new_locale if does_category_match else None
			self.old_locales[category] = locale.setlocale(category, new_locale)
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		for category_definition in self.ALL_CATEGORIES:
			category = category_definition['value']
			old_locale = self.old_locales[category]
			locale.setlocale(category, old_locale)
