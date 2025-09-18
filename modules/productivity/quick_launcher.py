"""
Quick Launcher feature.

Purpose:
- Launch configured shortcuts/scripts quickly from CLI/GUI.

API:
- run(args, ctx) -> dict
    - args: {"action":"list"|"run", "id": str|null}
    - return: {"success": True, "data": [...], "message": None}

Implementation notes:
- Index shortcuts via a config-managed JSON; execute via subprocess with careful quoting.
- Provide preview and dry-run for risky commands.

Dependencies:
- Internal: utils.config_manager, utils.logger
- External: subprocess

Safety:
- Dangerous commands must have confirm flag; do not execute arbitrary input without validation.
"""
