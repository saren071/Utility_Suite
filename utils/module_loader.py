"""
Dynamic package discovery and on-demand loader.

Responsibilities:
- Discover package metadata under modules/ quickly.
  Prefer reading meta from modules.<package>.tool.meta; fall back to meta.json.
- Persist discovery results to config/modules.json for faster startup.
- Provide APIs:
  - discover_packages() -> list[dict]
  - load_package(package_id) -> imported tool module
  - enable_package(package_id, enabled: bool) -> persist flag in manifest

Notes:
- Keep imports light; but for simplicity we import tool modules which are expected to be lightweight per project rules.
"""

from __future__ import annotations

import json
import os
import time
import importlib
from types import ModuleType
from utils.logger import get_logger
from utils.config_manager import ConfigManager
from utils.constants import Constants


class ModuleLoader:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.config_manager = ConfigManager()
        self.modules_dir = Constants.MODULES_DIR

    def discover_packages(self) -> list[dict]:
        packages: list[dict] = []
        if not os.path.isdir(self.modules_dir):
            self.logger.error(f"Modules directory not found: {self.modules_dir}")
            return packages

        for entry in os.listdir(self.modules_dir):
            pkg_dir = os.path.join(self.modules_dir, entry)
            if not os.path.isdir(pkg_dir):
                continue
            try:
                meta = self._read_meta_from_tool(entry)
                if not meta:
                    meta = self._read_meta_json(pkg_dir)
                if not meta:
                    continue
                # Normalize
                meta.setdefault("id", entry)
                meta.setdefault("name", entry)
                meta.setdefault("version", "0.0")
                meta.setdefault("description", "")
                meta.setdefault("features", [])
                packages.append(meta)
            except Exception as exc:
                self.logger.exception(f"Failed discovering package {entry}: {exc}")

        manifest = {
            "updated_at": int(time.time()),
            "packages": packages,
        }
        try:
            self.config_manager.save_manifest(manifest)
        except Exception:
            self.logger.exception("Failed to save modules manifest")

        return packages

    def load_package(self, package_id: str) -> ModuleType | None:
        try:
            module = importlib.import_module(f"modules.{package_id}.tool")
            # Validate exports
            if not hasattr(module, "meta") or not hasattr(module, "run"):
                self.logger.error(f"Package {package_id} missing meta or run()")
                return None
            return module
        except Exception as exc:
            self.logger.exception(f"Failed to load package {package_id}: {exc}")
            return None

    def enable_package(self, package_id: str, enabled: bool) -> bool:
        try:
            manifest = self.config_manager.load_manifest() or {}
            packages = manifest.get("packages", [])
            found = False
            for pkg in packages:
                if pkg.get("id") == package_id:
                    pkg["enabled"] = bool(enabled)
                    found = True
                    break
            if not found:
                packages.append({"id": package_id, "enabled": bool(enabled)})
            manifest["packages"] = packages
            manifest["updated_at"] = int(time.time())
            self.config_manager.save_manifest(manifest)
            return True
        except Exception:
            self.logger.exception("Failed to update manifest enable flag")
            return False

    def _read_meta_from_tool(self, package_folder_name: str) -> dict | None:
        try:
            module = importlib.import_module(f"modules.{package_folder_name}.tool")
            meta = getattr(module, "meta", None)
            if isinstance(meta, dict):
                return meta.copy()
            return None
        except Exception:
            return None

    def _read_meta_json(self, pkg_dir: str) -> dict | None:
        meta_path = os.path.join(pkg_dir, "meta.json")
        if not os.path.isfile(meta_path):
            return None
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Map legacy fields to expected
            out = {
                "id": os.path.basename(pkg_dir),
                "name": data.get("name") or os.path.basename(pkg_dir),
                "description": data.get("description", ""),
                "version": data.get("version", "0.0"),
                # no features in legacy meta.json
                "features": [],
            }
            return out
        except Exception as exc:
            self.logger.error(f"Invalid meta.json at {meta_path}: {exc}")
            return None
