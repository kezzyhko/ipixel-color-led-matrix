from pathlib import Path


ASSETS_FOLDER_PATH = Path(__file__).parent

def get_asset_path(relative_path: str | Path) -> Path:
	return ASSETS_FOLDER_PATH / relative_path
