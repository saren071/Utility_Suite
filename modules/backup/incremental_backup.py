"""
Incremental Backup feature.

Purpose:
- Copy only changed/new files based on checksum manifests.

API:
- run(args, ctx) -> dict
    - args: {"source": str, "dest": str, "manifest": str|null}
    - return: {"success": True, "data": {"copied": [...]} , "message": None}

Implementation notes:
- Use file_integrity-like hashing to detect changed files.
- Save updated manifest via ctx["config_manager"].

Dependencies:
- Internal: utils.file_helpers, utils.config_manager, utils.logger
"""
