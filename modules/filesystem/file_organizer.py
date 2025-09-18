"""
File Organizer feature.

Purpose:
- Organize files in a directory into subfolders based on extension rules defined in config/file_organizer.json.

API:
- run(args: dict = None, ctx: dict = None) -> dict
    - args: {"path": str, "config": str|null, "dry_run": bool}
    - return: {"success": True, "data": {"moved": [{"src":dst}]}, "message": None}

Implementation notes:
- Load rules via ctx["config_manager"].
- Use utils.file_helpers.safe_move for file operations.
- Provide dry-run preview by default and require confirm True to perform moves.

Dependencies:
- Internal: utils.file_helpers, utils.config_manager, utils.formatting, utils.logger
- External: os, shutil

Safety:
- Never overwrite files unless overwrite arg set and confirmed.
"""
