"""
File Integrity Checker feature.

Purpose:
- Generate checksum manifests and verify files against them.

API:
- run(args: dict = None, ctx: dict = None) -> dict
    - args: {"path": str, "action":"generate"|"verify", "out": "checksums.json", "algorithm":"sha256"}
    - return: {"success": True, "data": {"mismatches": [...]} , "message": None}

Implementation notes:
- Use utils.file_helpers.file_hash for chunked hashing.
- Save and load manifests via ctx["config_manager"].atomic writes.

Dependencies:
- Internal: utils.file_helpers, utils.config_manager, utils.logger
- External: hashlib, json, os

Safety:
- Verification is read-only.
"""
