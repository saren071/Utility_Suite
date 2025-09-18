"""
Disk Cleanup feature.

Purpose:
- Identify common cleanup candidates (temp files, browser caches) for review and optional cleanup.

API:
- run(args: dict = None, ctx: dict = None) -> dict
    - args: {"paths": list[str]|None, "targets": list[str], "dry_run": bool}
    - return: {"success": True, "data": {"candidates": [paths], "deleted": [paths]}, "message": None}

Dependencies:
- Internal: utils.file_helpers, utils.logger
- External: os, shutil, tempfile

Safety:
- Avoid deleting anything without explicit confirmation. Prefer send2trash.
"""

import os
import tempfile
from utils.file_helpers import FileHelpers
from utils.logger import get_logger


KNOWN_TARGETS = {
    "temp": lambda: [tempfile.gettempdir()],
}


def _collect_candidates(paths: list[str]) -> list[str]:
    files: list[str] = []
    for root in paths:
        if not os.path.isdir(root):
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            for name in filenames:
                files.append(os.path.join(dirpath, name))
    return files


def run(args: dict | None = None, ctx: dict | None = None) -> dict:
    logger = get_logger(__name__)
    helpers = FileHelpers()

    args = args or {}
    paths = args.get("paths")
    targets = args.get("targets", ["temp"]) or ["temp"]
    dry_run = bool(args.get("dry_run", True))

    resolved_paths: list[str] = []
    if isinstance(paths, list) and paths:
        resolved_paths.extend([p for p in paths if isinstance(p, str)])
    for t in targets:
        fn = KNOWN_TARGETS.get(t)
        if fn:
            try:
                resolved_paths.extend([p for p in fn() if isinstance(p, str)])
            except Exception:
                logger.exception(f"Failed to resolve target {t}")

    candidates = _collect_candidates(resolved_paths)
    deleted: list[str] = []

    if not dry_run:
        for p in candidates:
            try:
                res = helpers.send_to_trash(p)
                if res.get("success"):
                    deleted.append(p)
            except Exception:
                logger.exception(f"Failed to trash {p}")

    return {"success": True, "data": {"candidates": candidates, "deleted": deleted}, "message": None}
