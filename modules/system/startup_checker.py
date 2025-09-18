"""
Startup Checker feature.

Purpose:
- Enumerate startup entries (registry Run keys and startup folders) and optionally disable/enable them.

API:
- run(args: dict = None, ctx: dict = None) -> dict
    - args: {"action":"list"|"disable"|"enable", "key": str|null, "dry_run": True}

Implementation notes:
- Use winreg for HKCU/HKLM reads. For disables, prefer to move entry to a backup key or record in config instead of deleting.
- Log registry exports before changing.

Dependencies:
- Internal: utils.logger, utils.config_manager, utils.service_manager
- External: winreg (Windows builtin), pywin32 (optional)

Safety:
- Always back up registry entries before modifying them.
"""
