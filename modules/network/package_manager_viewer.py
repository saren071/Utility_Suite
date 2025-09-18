"""
Package Manager Viewer feature.

Purpose:
- Show installed packages from winget/choco/pip (best-effort) for quick inventory.

API:
- run(args, ctx) -> dict
    - args: {"backend": "winget"|"choco"|"pip"|"all"}
    - return: {"success": True, "data": [{"name":...,"version":...}], "message": None}

Implementation notes:
- Use subprocess to call backend CLIs. Handle absence gracefully with informative messages.

Dependencies:
- External: subprocess
- Internal: utils.logger

Safety:
- No changes performed; read-only.
"""
