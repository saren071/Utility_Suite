"""
Snapshot List feature.

Purpose:
- List available snapshots/backups in a backup repo.

API:
- run(args, ctx) -> dict
    - args: {"repo": str}
    - return: {"success": True, "data": [{"backup_path":..., "timestamp":...}], "message": None}

Implementation notes:
- Read backup folder structures and parse timestamps.
"""
