"""
File Integrity Checker feature.

Purpose:
- Generate checksum manifests and verify files against them.

API:
- run(args: dict = None, ctx: dict = None) -> dict
    - args: {"path": str, "action":"generate"|"verify", "out": str|None, "algorithm":"sha256"}
    - return: {"success": True, "data": {"mismatches": [...]} , "message": None}

Dependencies:
- Internal: utils.file_helpers, utils.config_manager, utils.logger
- External: hashlib, json, os

Safety:
- Verification is read-only.
"""

import os
from utils.file_helpers import FileHelpers
from utils.logger import get_logger


def run(args: dict | None = None, ctx: dict | None = None) -> dict:
    logger = get_logger(__name__)
    helpers = FileHelpers()

    args = args or {}
    path = args.get("path")
    action = args.get("action", "generate")
    algorithm = args.get("algorithm", "sha256")
    out = args.get("out")

    if not path or not os.path.isdir(path):
        return {"success": False, "data": None, "message": f"Invalid directory: {path}"}

    manifest: dict[str, str] = {}
    if action == "generate":
        for file_path in helpers.iterate_files(path):
            try:
                rel = os.path.relpath(file_path, start=path)
                manifest[rel] = helpers.file_hash(file_path, algorithm=algorithm)
            except Exception:
                logger.exception(f"Hash failed for {file_path}")
        # Determine output
        out_path = out if isinstance(out, str) and out else os.path.join(path, "checksums.json")
        res = helpers.atomic_write_json(out_path, manifest)
        if not res.get("success", False):
            return {"success": False, "data": None, "message": res.get("message", "write failed")}
        return {"success": True, "data": {"manifest": out_path, "count": len(manifest)}, "message": None}

    elif action == "verify":
        manifest_path = out if isinstance(out, str) and out else os.path.join(path, "checksums.json")
        if not os.path.isfile(manifest_path):
            return {"success": False, "data": None, "message": f"Manifest not found: {manifest_path}"}
        try:
            import json
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = json.load(f)
        except Exception as exc:
            return {"success": False, "data": None, "message": f"Failed to read manifest: {exc}"}

        mismatches: list[dict] = []
        for rel, expected in manifest.items():
            abs_path = os.path.join(path, rel)
            if not os.path.exists(abs_path):
                mismatches.append({"path": rel, "issue": "missing"})
                continue
            try:
                actual = helpers.file_hash(abs_path, algorithm=algorithm)
                if actual != expected:
                    mismatches.append({"path": rel, "issue": "hash_mismatch", "expected": expected, "actual": actual})
            except Exception:
                logger.exception(f"Hash failed for {abs_path}")
                mismatches.append({"path": rel, "issue": "hash_error"})

        return {"success": True, "data": {"mismatches": mismatches}, "message": None}

    else:
        return {"success": False, "data": None, "message": f"Unsupported action: {action}"}
