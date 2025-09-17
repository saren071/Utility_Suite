# modules/battery_monitor/tool.py
"""
Battery Monitor module (for laptops).

Responsibilities:
- Display current battery percentage, charging status, and time remaining.
- Optionally alert user if battery falls below a configurable threshold.

Dependencies:
- Internal: `utils/formatting.py`.
- External: `psutil`, `time`.

Notes:
- Only functional on laptops; skip or warn on desktops.
- Alerts can be CLI messages or optional system notifications.
"""
