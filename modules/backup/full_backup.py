"""
Full Backup feature.

Purpose:
- Create a full copy (optionally compressed) of a source directory.

API:
- run(args, ctx) -> dict
    - args: {"source": str, "dest": str, "compress": bool}
    - return: {"success": True, "data": {"backup_path": str}, "message": None}

Implementation notes:
- Check disk space before starting.
- Use utils.file_helpers.safe_copy and zipfile for compression.

Dependencies:
- Internal: utils.file_helpers, utils.logger
- External: zipfile, shutil

Safety:
- Do not delete source files; confirm before overwriting dest.
"""
