"""
Restore feature.

Purpose:
- Restore a backup from a snapshot or backup archive.

API:
- run(args, ctx) -> dict
    - args: {"backup_path": str, "restore_to": str, "preview": bool}
    - return: {"success": True, "data": {"restored": [...]} , "message": None}

Implementation notes:
- Provide dry-run preview and confirm step.
- Use safe move/copy helpers.

Dependencies:
- Internal: utils.file_helpers, utils.logger
"""
