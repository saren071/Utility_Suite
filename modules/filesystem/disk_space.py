"""
Disk Space Visualizer feature.

Purpose:
- Compute sizes of files/folders under a path and return a sorted list of top N largest items.

API:
- meta (optional): {"id":"disk_space", "name":"Disk Space Visualizer"}
- run(args: dict = None, ctx: dict = None) -> dict
    - args: {"path": str, "top_n": int = 20, "depth": int|None, "human_readable": bool}
    - ctx: runtime context with logger, formatting, config_manager, service_manager, constants
    - return: {"success": True, "data": [{"path": str, "size": int, "size_hr": str}], "message": None}

Dependencies:
- Internal: utils.file_helpers, utils.formatting, utils.logger
- External: os

Safety:
- Read-only operation only.
"""

import os
from utils.file_helpers import FileHelpers
from utils.logger import get_logger

meta = {"id": "disk_space", "name": "Disk Space Visualizer"}


def run(args: dict | None = None, ctx: dict | None = None) -> dict:
    logger = get_logger(__name__)
    helpers = FileHelpers()
    formatting = ctx.get("format") if isinstance(ctx, dict) else None

    args = args or {}
    path = args.get("path", ".")
    top_n = int(args.get("top_n", 20))
    depth = args.get("depth")
    human_readable = bool(args.get("human_readable", True))

    if not os.path.isdir(path):
        return {"success": False, "data": None, "message": f"Invalid directory: {path}"}

    items: list[tuple[str, int]] = []

    try:
        with os.scandir(path) as it:
            for entry in it:
                try:
                    size = 0
                    if entry.is_file(follow_symlinks=False):
                        size = entry.stat().st_size
                    elif entry.is_dir(follow_symlinks=False):
                        size = helpers.folder_size(entry.path, depth=depth)
                    items.append((entry.path, size))
                except Exception:
                    logger.exception(f"Failed to stat/size {entry.path}")
    except Exception as exc:
        return {"success": False, "data": None, "message": str(exc)}

    items.sort(key=lambda t: t[1], reverse=True)
    items = items[:top_n]

    result_rows: list[dict] = []
    for p, s in items:
        row = {"path": p, "size": s}
        if human_readable and formatting:
            try:
                row["size_hr"] = formatting.human_readable_size(s)
            except Exception:
                row["size_hr"] = None
        result_rows.append(row)

    return {"success": True, "data": result_rows, "message": None}
