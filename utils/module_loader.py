"""
Dynamic package discovery and on-demand loader.

Responsibilities:
- Quickly discover package metadata under modules/ without importing heavy code:
    - If package contains meta.json, read it.
    - Otherwise, inspect tool.py for a `meta` dict using importlib.util.spec_from_file_location but avoid executing side-effect code.
- Persist discovery results to config/modules.json for faster startup.
- Provide APIs:
    - discover_packages() -> list[meta_dict]
    - load_package(package_id) -> module object loaded from modules/<package>/tool.py (full import)
    - enable_package(package_id, enabled: bool)
- Validate loaded package implements:
    - meta (dict) and run(feature_id: str, args: dict = None, ctx: dict = None) -> dict

Dependencies:
- External: importlib, importlib.util, os, json, types
- Internal: utils.logger, utils.config_manager, utils.constants

Security:
- Warn if a package meta declares `needs_admin` capability; do not auto-run such features without confirmation and privilege checks.
"""

import json
import os
from utils.logger import get_logger
from utils.config_manager import ConfigManager
from utils.constants import Constants

class ModuleLoader:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.config_manager = ConfigManager()
        self.constants = Constants()
    
    def run(self):
        self.logger.info("Discovering packages...")
        packages = self._discover_packages()
        for package in packages:
            valid, meta = self._validate_package(package)
            if not valid:
                continue
            if meta is None:
                self.logger.error(f"Package {package} does not contain a meta")
                continue
            if meta["name"] is None:
                self.logger.error(f"Package {meta['name']} does not contain a name")
                continue
            self.logger.info(f"Loading package {meta['name']}...")
            valid, meta = self._load_package(meta["name"])
            if not valid:
                continue
            if meta is None:
                self.logger.error(f"Package {package} does not contain a meta")
                continue
            if meta["name"] is None:
                self.logger.error(f"Package {meta['name']} does not contain a name")
                continue
            self.logger.info(f"Package {meta['name']} loaded")
            print(f"Package {meta['name']} loaded")
        self.logger.info("Packages loaded")

    def _discover_packages(self):
        """
        Discover packages under Constants.MODULES_DIR
        Returns a list of full paths.
        """
        modules_dir = os.path.abspath(Constants.MODULES_DIR)
        packages = []
        for tool in os.listdir(modules_dir):
            package_path = os.path.join(modules_dir, tool)
            if os.path.isdir(package_path):
                packages.append(package_path)
        return packages

    def _load_package(self, package_id):
        """
        Load a package.
        """
        for package_path in self._discover_packages():
            valid, meta = self._validate_package(package_path)
            if not valid:
                continue
            if meta["name"] == package_id if meta else None:
                return True, meta
        self.logger.error(f"Package {package_id} does not contain a valid meta.json")
        return False, None

    
    def _unload_package(self, package_id):
        """
        Unload a package.
        """
        packages = self._discover_packages()
        for package in packages:
            valid, meta = self._validate_package(package)
            if not valid:
                continue
            if package_id == meta["name"] if meta else None:
                return True, meta
        return False, None

    def _validate_package(self, package_path):
        """
        Validate a package.
        """
        meta_path = os.path.join(package_path, "meta.json")
        if not os.path.exists(meta_path):
            return False, None
        with open(meta_path, "r") as f:
            meta = json.load(f)
        required_fields = ["name", "description", "author", "version", "requires", "capabilities"]
        for field in required_fields:
            if field not in meta or meta[field] is None:
                return False, None
        return True, meta

    def _enable_package(self, package_id, enabled):
        """
        Enable a package.
        """
        valid, meta = self._load_package(package_id)
        if not valid:
            return False
        return True, meta if meta else None
    
    def _disable_package(self, package_id):
        """
        Disable a package.
        """
        valid, meta = self._unload_package(package_id)
        if not valid:
            return False
        return True, meta if meta else None
