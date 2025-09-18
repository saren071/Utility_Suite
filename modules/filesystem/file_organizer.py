"""
File Organizer feature.

Purpose:
- Organize files in a directory into subfolders based on extension rules defined in config/file_organizer.json.

API:
- run(args: dict = None, ctx: dict = None) -> dict
    - args: {"path": str, "config": str|None, "dry_run": bool, "overwrite": bool}
    - return: {"success": True, "data": {"moved": [{"src":dst}]}, "message": None}

Dependencies:
- Internal: utils.file_helpers, utils.config_manager, utils.formatting, utils.logger
- External: os, shutil

Safety:
- Never overwrite files unless overwrite arg set and confirmed.
"""

import os
from utils.file_helpers import FileHelpers
from utils.logger import get_logger


def run(args: dict | None = None, ctx: dict | None = None) -> dict:
    logger = get_logger(__name__)
    helpers = FileHelpers()

    args = args or {}
    path = args.get("path")
    config_name = args.get("config", "file_organizer.json")
    dry_run = bool(args.get("dry_run", True))
    overwrite = bool(args.get("overwrite", False))

    if not path or not os.path.isdir(path):
        return {"success": False, "data": None, "message": f"Invalid directory: {path}"}

    # Load rules
    rules = {}
    if isinstance(ctx, dict) and ctx.get("config_manager"):
        try:
            rules = ctx["config_manager"].load_json(config_name, default={})
        except Exception as exc:
            logger.error(f"Failed to load organizer rules: {exc}")
            rules = {}

    moved = []
    for entry in os.listdir(path):
        src = os.path.join(path, entry)
        if not os.path.isfile(src):
            continue
        ext = os.path.splitext(entry)[1].lstrip(".").lower()
        if not ext or ext not in rules:
            continue
        folder = rules[ext]
        dest_dir = os.path.join(path, folder)
        dest = os.path.join(dest_dir, entry)
        os.makedirs(dest_dir, exist_ok=True)
        if dry_run:
            logger.info(f"[DRY RUN] Would move {src} -> {dest}")
            moved.append({src: dest})
        else:
            res = helpers.safe_move(src, dest, overwrite=overwrite)
            if res.get("success"):
                moved.append({src: dest})
            else:
                logger.warning(f"Skip move {src}: {res.get('message')}")

    return {"success": True, "data": {"moved": moved}, "message": None}
