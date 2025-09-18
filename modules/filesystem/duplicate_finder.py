"""
Duplicate Finder feature.

Purpose:
- Identify duplicate files by content hash and group them for reporting or optional movement/deletion.

API:
- run(args: dict = None, ctx: dict = None) -> dict
    - args: {"path": str, "algorithm": "md5"|"sha256", "min_size": int, "action": "report"|"move"|"delete", "target": str|None, "dry_run": bool}
    - return: {"success": True, "data": [{"hash": str, "files": [paths]}], "message": str}

Dependencies:
- Internal: utils.file_helpers, utils.logger, utils.formatting
- External: hashlib, os, shutil, send2trash (optional)

Safety:
- Default action = "report". Do not delete files without explicit user confirmation.
"""

import os
from collections import defaultdict
from utils.file_helpers import FileHelpers
from utils.logger import get_logger


def run(args: dict | None = None, ctx: dict | None = None) -> dict:
    logger = get_logger(__name__)
    helpers = FileHelpers()

    args = args or {}
    path = args.get("path")
    algorithm = args.get("algorithm", "sha256")
    min_size = int(args.get("min_size", 1))
    action = args.get("action", "report")
    target_in = args.get("target")
    dry_run = bool(args.get("dry_run", True))

    if not path or not os.path.isdir(path):
        return {"success": False, "data": None, "message": f"Invalid directory: {path}"}
    if algorithm not in {"sha256", "md5"}:
        return {"success": False, "data": None, "message": f"Unsupported algorithm: {algorithm}"}
    if action not in {"report", "move", "delete"}:
        return {"success": False, "data": None, "message": f"Unsupported action: {action}"}

    target: str | None = None
    if action == "move":
        if not isinstance(target_in, str) or not target_in:
            return {"success": False, "data": None, "message": "Target directory is required for move action"}
        target = target_in
        os.makedirs(target, exist_ok=True)

    hash_to_files: dict[str, list[str]] = defaultdict(list)

    for file_path in helpers.iterate_files(path):
        try:
            if os.path.getsize(file_path) < min_size:
                continue
            file_hash = helpers.file_hash(file_path, algorithm=algorithm)
            hash_to_files[file_hash].append(file_path)
        except Exception:
            logger.exception(f"Failed hashing {file_path}")

    groups = [{"hash": h, "files": files} for h, files in hash_to_files.items() if len(files) > 1]

    # Apply actions on duplicates (keep first, act on rest)
    acted: list[dict] = []
    if action in {"move", "delete"} and groups:
        for group in groups:
            # Skip the first file, act on the rest
            for file_path in group["files"][1:]:
                try:
                    if action == "move" and target is not None:
                        dst = os.path.join(target, os.path.basename(file_path))
                        if dry_run:
                            logger.info(f"[DRY RUN] Would move {file_path} -> {dst}")
                            acted.append({"move": {file_path: dst}})
                        else:
                            res = helpers.safe_move(file_path, dst)
                            acted.append({"move": {file_path: dst, "ok": res.get("success", False)}})
                    elif action == "delete":
                        if dry_run:
                            logger.info(f"[DRY RUN] Would send to trash {file_path}")
                            acted.append({"trash": file_path})
                        else:
                            res = helpers.send_to_trash(file_path)
                            acted.append({"trash": {file_path: res.get("success", False)}})
                except Exception:
                    logger.exception(f"Action failed for {file_path}")

    return {
        "success": True,
        "data": {"groups": groups, "actions": acted},
        "message": None,
    }
