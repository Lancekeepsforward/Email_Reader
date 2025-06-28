from pathlib import Path
import json

CONFIG_DIR = Path(__file__).parent / "config"

def _get_config_dir(name: str) -> Path:
    path = CONFIG_DIR / name
    if not path.exists():
        print(f"[CREATING '{path}', EXISTS: '{path.exists()}']")
        raise FileNotFoundError(f"Config directory '{path}' does not exist")
    return path

def get_config_file(name: str) -> Path:
    """
    !!! IMPORTANT !!!
    Get the content of a config file.
    """
    path = _get_config_dir(name)
    with open(path, "r") as f:
        try:
            content = json.load(f)
        except json.JSONDecodeError:
            if path.suffix != ".json":
                raise ValueError(f"File '{path}' is not a valid JSON file")
            if path.stat().st_size == 0:
                raise json.JSONDecodeError(f"File '{path}' is empty", path.read_text(), 0)
    return content

if __name__ == "__main__":
    print(get_config_file(input("Enter the name of the config file: ")))