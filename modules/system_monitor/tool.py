# modules/system_monitor/tool.py
"""
System Resource Monitor module.

Responsibilities:
- Display live system statistics:
  - CPU per-core usage.
  - RAM usage.
  - Disk I/O read/write speeds.
  - Network bytes sent/received.
  - GPU utilization, VRAM usage, temperature.

Dependencies:
- Internal: `utils/formatting.py` for tables and progress bars.
- External: `psutil`, `GPUtil`, `time`.

Notes:
- Should refresh CLI at user-defined intervals.
- No permanent logging unless optional feature is enabled.
"""
