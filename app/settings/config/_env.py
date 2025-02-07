import json
from pathlib import Path
from typing import Dict, List
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettingsFile(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore"
    )

    BOT_TOKEN: str
    CHAT_IDS: List[int]
    LINKS_JSON_PATH: str = "links.json"

    @property
    def services(self) -> Dict[str, str]:
        path = Path(self.LINKS_JSON_PATH)

        if not path.exists():
            raise FileNotFoundError(f"Links file '{path}' not found!")

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

                if not isinstance(data, dict):
                    raise ValueError("JSON root must be a dictionary!")

                for key, value in data.items():
                    if not isinstance(value, str):
                        raise ValueError(f"Value for '{key}' must be a string!")

                return data

        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in links file!")
