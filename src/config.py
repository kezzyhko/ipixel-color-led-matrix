from configparser import ConfigParser


class Config:
	REQUIRED_KEYS: list[str] = [
		"mac_address",
		"write_characteristic",
		"notify_characteristic"
	]

	def __init__(self, config_path: str):
		self._read_config(config_path)
		self._validate_config()
		self._set_attributes()

	def _read_config(self, config_path: str):
		self.parser: ConfigParser = ConfigParser()
		with open(config_path, "r") as config_file:
			self.parser.read_file(config_file)

	def _validate_config(self):
		missing_keys: list[str] = []
		for key in self.REQUIRED_KEYS:
			if not self.parser.has_option("DEFAULT", key):
				missing_keys.append(key)
		if missing_keys:
			raise ValueError(f"Missing required keys: {missing_keys}")

		all_keys = set(self.parser.options("DEFAULT"))
		required_keys_set = set(self.REQUIRED_KEYS)
		unrecognized_keys = all_keys - required_keys_set
		if unrecognized_keys:
			raise ValueError(f"Unrecognized keys: {unrecognized_keys}")

		sections = self.parser.sections()
		if sections:
			raise ValueError(
				f"Config should not contain sections. Found: {', '.join(sections)}"
			)

	def _set_attributes(self):
		self.mac_address: str = self.parser.get("DEFAULT", "mac_address")
		self.write_characteristic: str = self.parser.get("DEFAULT", "write_characteristic")
		self.notify_characteristic: str = self.parser.get("DEFAULT", "notify_characteristic")
