"""
Configuration manager and JSON utilities.

Responsibilities:
- Ensure config directory exists (ensure_config_dirs()).
- Read and write JSON config files with atomic writes:
    - load_json(path, default)
    - save_json(path, data)
- Provide helpers specifically for:
    - load_manifest() / save_manifest() for config/modules.json
    - load_agent_config() / save_agent_config()
- Cache frequently used configs in memory with explicit save() semantics.

Dependencies:
- External: json, os, tempfile
- Internal: utils.constants, utils.logger

Testing:
- Allow overriding base config directory path for tests (parameterize or env var).
"""

import json
from utils.constants import Constants
import os
from utils.logger import get_logger

class ConfigManager:
    def __init__(self, base_path=None):
        self.logger = get_logger(__name__)
        self.base_path = base_path or Constants.CONFIG_DIR
        self.cache = {}

    def setup(self):
        """
        Setup the config manager.
        """
        self.ensure_config_dirs()
        self.logger.info(f"Config manager setup complete in {self.base_path}")

    def ensure_config_dirs(self):
        """
        Ensure config directory exists.
        """
        os.makedirs(self.base_path, exist_ok=True)

        # Ensure default config files exist (empty if needed)
        defaults: dict[str, str] = {
            "agent_config.json": "{}\n",
            "modules.json": "{}\n",
            "file_organizer.json": (
                "{\n"
                "  \"jpg\": \"Images\",\n"
                "  \"jpeg\": \"Images\",\n"
                "  \"png\": \"Images\",\n"
                "  \"gif\": \"Images\",\n"
                "  \"pdf\": \"Documents\",\n"
                "  \"docx\": \"Documents\",\n"
                "  \"xlsx\": \"Documents\",\n"
                "  \"zip\": \"Archives\",\n"
                "  \"7z\": \"Archives\",\n"
                "  \"rar\": \"Archives\",\n"
                "  \"mp3\": \"Audio\",\n"
                "  \"wav\": \"Audio\",\n"
                "  \"mp4\": \"Video\",\n"
                "  \"mkv\": \"Video\"\n"
                "}\n"
            ),
        }
        for file_name, content in defaults.items():
            path = os.path.join(self.base_path, file_name)
            if not os.path.exists(path) or os.path.getsize(path) == 0:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)


    def load_json(self, path, default=None):
        """
        Load JSON from a file, optionally providing a default value.
        Returns default if file missing or invalid JSON.
        """
        full_path = os.path.join(self.base_path, path)
        if not os.path.exists(full_path):
            if default is None:
                raise FileNotFoundError(f"Config file not found: {path}")
            return default
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content == "":
                    return default if default is not None else {}
                return json.loads(content)
        except Exception as exc:
            self.logger.error(f"Failed to read JSON from {full_path}: {exc}")
            return default if default is not None else {}

    def save_json(self, path, data):
        """
        Save JSON data to a file.
        """
        full_path = os.path.join(self.base_path, path)
        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load_manifest(self):
        """
        Load the modules manifest.
        """
        return self.load_json(Constants.MODULES_MANIFEST, default={})

    def save_manifest(self, data):
        """
        Save the modules manifest.
        """
        return self.save_json(Constants.MODULES_MANIFEST, data)

    def load_agent_config(self):
        """
        Load the agent config.
        """
        return self.load_json(Constants.AGENT_CONFIG, default={})
    
    def save_agent_config(self, data):
        """
        Save the agent config.
        """
        return self.save_json(Constants.AGENT_CONFIG, data)
    
    def cache_config(self, key, data):
        """
        Cache a config value.
        """
        self.cache[key] = data
        return data
    
    def get_cached_config(self, key):
        """
        Get a cached config value.
        """
        return self.cache.get(key)
    
    def save_cached_config(self):
        """
        Save all cached configs to files.
        """
        for key, data in self.cache.items():
            self.save_json(key, data)

    def clear_cache(self):
        """
        Clear the cache.
        """
        self.cache.clear()

    def get_config_path(self, path):
        """
        Get the full path to a config file.
        """
        return os.path.join(self.base_path, path)
