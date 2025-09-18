"""
Battery Monitor feature.

Purpose:
- Report battery status and optionally notify on thresholds.

API:
- run(args: dict = None, ctx: dict = None) -> dict
    - args: {"interval": float, "threshold": int, "notify": bool}
    - return: {"success": True, "data": {"percent": int, "plugged": bool, "secs_left": int}, "message": None}

Implementation notes:
- Use psutil.sensors_battery(). For notifications, optional win10toast.
- For agent mode, run as persistent task with small interval.

Dependencies:
- Internal: utils.logger, utils.formatting
- External: psutil, win10toast (optional)

Safety:
- Detect absence of battery gracefully and report that feature is unavailable on desktops.
"""
