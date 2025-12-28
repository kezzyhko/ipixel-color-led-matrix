from configparser import ConfigParser, UNNAMED_SECTION
from pathlib import Path
from warnings import warn


class Config:
	EXPECTED_KEYS: list[str] = [
		"mac_address",
	]

	def _set_attributes(self):
		self.mac_address: str = self.parser.get(UNNAMED_SECTION, "mac_address", fallback="search")

	def __init__(self, config_path: Path):
		self._read_config(config_path)
		self._validate_config()
		self._set_attributes()

	def _read_config(self, config_path: Path):
		self.parser: ConfigParser = ConfigParser(allow_unnamed_section = True)
		with open(config_path, "r") as config_file:
			self.parser.read_file(config_file)

	def _validate_config(self):
		missing_keys: list[str] = []
		for key in self.EXPECTED_KEYS:
			if not self.parser.has_option(UNNAMED_SECTION, key):
				missing_keys.append(key)
		if missing_keys:
			warn(f"Missing required keys: {missing_keys}")

		existing_keys = set(self.parser.options(UNNAMED_SECTION))
		expected_keys_set = set(self.EXPECTED_KEYS)
		unrecognized_keys = existing_keys - expected_keys_set
		if unrecognized_keys:
			warn(f"Unrecognized keys: {unrecognized_keys}")

		sections = self.parser.sections()
		sections.remove(UNNAMED_SECTION)
		if sections:
			warn(f"Config should not contain sections. Found: {sections}")
