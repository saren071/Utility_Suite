"""
Disk Cleanup feature.

Purpose:
- Identify common cleanup candidates (temp files, browser caches) for review and optional cleanup.

API:
- run(args: dict = None, ctx: dict = None) -> dict
    - args: {"paths": [paths]|None, "targets": ["temp","browser_cache"], "dry_run": True}
    - return: {"success": True, "data": {"candidates": [paths]}, "message": None}

Implementation notes:
- Provide plugin points for app-specific cleaners (browser profiles).
- Always present a preview (dry_run default).

Dependencies:
- Internal: utils.file_helpers, utils.logger
- External: os, shutil

Safety:
- Avoid deleting anything without explicit confirmation. Prefer send2trash.
"""
