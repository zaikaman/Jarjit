import base64
import json
import os
from pathlib import Path


class Settings:
    def __init__(self):
        self.settings_file_path = self.get_settings_directory_path() + 'settings.json'
        os.makedirs(os.path.dirname(self.settings_file_path), exist_ok=True)
        self.settings = self.load_settings_from_file()

    def get_settings_directory_path(self):
        return str(Path.home()) + '/.open-interface/'

    def get_dict(self) -> dict[str, str]:
        return self.settings

    def save_settings_to_file(self, settings_dict) -> None:
        settings = {}
        if os.path.exists(self.settings_file_path):
            with open(self.settings_file_path, 'r') as file:
                try:
                    settings = json.load(file)
                except:
                    settings = {}

        for key, value in settings_dict.items():
            if value is not None:
                settings[key] = value

        os.makedirs(os.path.dirname(self.settings_file_path), exist_ok=True)
        with open(self.settings_file_path, 'w+') as file:
            json.dump(settings, file, indent=4)

    def load_settings_from_file(self):
        if os.path.exists(self.settings_file_path):
            try:
                with open(self.settings_file_path, 'r') as file:
                    settings = json.load(file)
                    return settings
            except Exception as e:
                print(f"Error loading settings: {e}")
        return {}
