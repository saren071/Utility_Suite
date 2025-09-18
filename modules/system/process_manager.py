"""
Process Manager feature.

Purpose:
- List processes and optionally terminate a selected process safely.

API:
- run(args: dict = None, ctx: dict = None) -> dict
    - args: {"action": "list"|"kill", "filter": str|null, "pid": int|null, "force": bool}
    - return: {"success": True, "data": [...], "message": None}

Implementation notes:
- Use psutil.process_iter() for listings and handle AccessDenied exceptions.
- For kill, check permissions, disallow killing system-critical PIDs, and use utils.service_manager.taskkill fallback on Windows if needed.

Dependencies:
- Internal: utils.logger, utils.formatting, utils.service_manager
- External: psutil, subprocess

Safety:
- Always prompt or require confirm flag for destructive actions.
"""
