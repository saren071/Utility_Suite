"""
Duplicate Finder feature.

Purpose:
- Identify duplicate files by content hash and group them for reporting or optional movement/deletion.

API:
- run(args: dict = None, ctx: dict = None) -> dict
    - args: {"path": str, "algorithm": "md5"|"sha256", "min_size": int, "action": "report"|"move"|"delete", "target": str|null, "dry_run": bool}
    - return: {"success": True, "data": [{"hash": str, "files": [paths]}], "message": str}

Implementation notes:
- Use utils.file_helpers.file_hash() reading files in chunks.
- For move/delete, use utils.file_helpers.safe_move/send_to_trash and require confirm (dry_run default).
- Handle large directories with streaming and incremental grouping.

Dependencies:
- Internal: utils.file_helpers, utils.logger, utils.formatting
- External: hashlib, os, shutil, send2trash (optional)

Safety:
- Default action = "report". Do not delete files without explicit user confirmation.
"""
