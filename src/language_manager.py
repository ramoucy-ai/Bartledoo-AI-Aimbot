"""Language management utilities for the GUI."""
from __future__ import annotations

import json
import os
from typing import Dict

from language_data import TRANSLATIONS


class LanguageManager:
    """Simple helper that wraps language translations and persistence."""

    DEFAULT_LANGUAGE = "zh_tw"
    CONFIG_FILE = "language_config.json"

    def __init__(self) -> None:
        self.translations: Dict[str, Dict[str, str]] = TRANSLATIONS
        self.current_language: str = self.DEFAULT_LANGUAGE
        self.load_language_config()

    def get_text(self, key: str, default: str = "") -> str:
        """Return translated text for the active language."""
        lang_table = self.translations.get(self.current_language, {})
        return lang_table.get(key, default or key)

    def set_language(self, language_code: str) -> bool:
        """Switch to a different language if available."""
        if language_code in self.translations:
            self.current_language = language_code
            self.save_language_config()
            return True
        return False

    def get_current_language(self) -> str:
        return self.current_language

    def get_available_languages(self) -> list[str]:
        return list(self.translations.keys())

    def save_language_config(self) -> None:
        try:
            config_data = {"language": self.current_language}
            with open(self.CONFIG_FILE, "w", encoding="utf-8") as handle:
                json.dump(config_data, handle, ensure_ascii=False, indent=2)
        except Exception as exc:  # pragma: no cover
            print(f"Failed to save language config: {exc}")

    def load_language_config(self) -> None:
        try:
            if os.path.exists(self.CONFIG_FILE):
                with open(self.CONFIG_FILE, "r", encoding="utf-8") as handle:
                    config_data = json.load(handle)
                    language = config_data.get("language", self.DEFAULT_LANGUAGE)
                    if language in self.translations:
                        self.current_language = language
        except Exception as exc:  # pragma: no cover
            print(f"Failed to load language config: {exc}")
            self.current_language = self.DEFAULT_LANGUAGE


def get_text(key: str, default: str = "") -> str:
    return language_manager.get_text(key, default)


def set_language(language_code: str) -> bool:
    return language_manager.set_language(language_code)


language_manager = LanguageManager()
