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
        for file in ["agent_config.json", "modules.json"]:
            path = os.path.join(self.base_path, file)
            if not os.path.exists(path):
                with open(path, "w", encoding="utf-8") as f:
                    f.write("{}")  # empty JSON object


    def load_json(self, path, default=None):
        """
        Load JSON from a file, optionally providing a default value.
        """
        full_path = os.path.join(self.base_path, path)
        if not os.path.exists(full_path):
            if default is None:
                raise FileNotFoundError(f"Config file not found: {path}")
            return default
        with open(full_path, "r", encoding="utf-8") as f:
            return json.load(f)

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
