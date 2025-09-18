"""
Services Viewer feature.

Purpose:
- List Windows services and optionally start/stop them.

API:
- run(args: dict = None, ctx: dict = None) -> dict
    - args: {"action":"list"|"start"|"stop", "service_name": str|null}

Implementation notes:
- Listing via psutil.win_service_iter(). Start/stop via pywin32 or sc.exe wrapper.
- Require admin for start/stop operations and confirm before stopping services.

Dependencies:
- Internal: utils.logger, utils.formatting, utils.service_manager
- External: psutil, pywin32 (optional)

Safety:
- Maintain a list of protected/critical services and prevent stopping them.
"""
