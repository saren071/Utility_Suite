"""
Filesystem package orchestrator (tool.py).

Exports:
- meta: package metadata with id, name, description, version, features
- run(feature_id: str, args: dict | None = None, ctx: dict | None = None) -> dict

Design:
- Import feature modules lazily inside run()
- Standard return shape for all features
"""

from importlib import import_module
from typing import Any

meta = {
    "id": "filesystem",
    "name": "Filesystem Tools",
    "description": "Disk and file utilities",
    "version": "0.1",
    "features": [
        {"id": "disk_space", "name": "Disk Space Visualizer"},
        {"id": "duplicate_finder", "name": "Duplicate Finder"},
        {"id": "file_organizer", "name": "File Organizer"},
        {"id": "auto_renamer", "name": "Auto Renamer"},
        {"id": "file_integrity", "name": "File Integrity"},
        {"id": "image_deduper", "name": "Image Deduper"},
        {"id": "disk_cleanup", "name": "Disk Cleanup"},
    ],
}


def _result(success: bool, data: dict | list | None = None, message: str | None = None) -> dict:
    return {"success": success, "data": data, "message": message}


def run(feature_id: str, args: dict | None = None, ctx: dict | None = None) -> dict:
    if not feature_id:
        return _result(False, None, "feature_id is required")

    try:
        module = import_module(f"modules.filesystem.{feature_id}")
    except ModuleNotFoundError:
        return _result(False, None, f"Unknown feature: {feature_id}")
    except Exception as exc:  # defensive: import errors
        message = f"Failed to import feature {feature_id}: {exc}"
        if ctx and ctx.get("logger"):
            ctx["logger"].error(message)
        return _result(False, None, message)

    if not hasattr(module, "run"):
        return _result(False, None, f"Feature module {feature_id} missing run()")

    try:
        return module.run(args=args, ctx=ctx)
    except Exception as exc:
        message = f"Feature {feature_id} raised an exception: {exc}"
        if ctx and ctx.get("logger"):
            ctx["logger"].exception(message)
        return _result(False, None, message)