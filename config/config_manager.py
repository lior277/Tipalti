import json
import os


class ConfigManager:
    def __init__(self, path: str | None = None):
        if path is None:
            current = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(current, "config.json")

        with open(path, "r", encoding="utf-8") as f:
            self._data = json.load(f)

    # ---------- core ----------
    @property
    def base_url(self) -> str:
        try:
            return self._data["base_url"]
        except KeyError:
            raise RuntimeError("Missing 'base_url' in config.json")

    @property
    def ui_timeout_ms(self) -> int:
        return int(self._data.get("ui_timeout_ms", 5000))
