import json
import os


class ConfigManager:
    def __init__(self, path: str | None = None):
        if path is None:
            current = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(current, "config.json")

        with open(path, "r", encoding="utf-8") as f:
            self._data = json.load(f)


    @property
    def base_url(self) -> str:
        return self._data.get("base_url", "")

    @property
    def contact_name(self) -> str:
        return self._data.get("contact_form", {}).get("name", "")

    @property
    def contact_email(self) -> str:
        return self._data.get("contact_form", {}).get("email", "")

    @property
    def contact_message_template(self) -> str:
        return self._data.get("contact_form", {}).get("message_template", "")
