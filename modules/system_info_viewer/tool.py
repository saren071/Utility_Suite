# modules/system_info_viewer/tool.py
"""
System Info Viewer module.

Responsibilities:
- Aggregate and display key system details in one screen:
  - CPU info (model, cores, threads).
  - RAM total and available.
  - Disk partitions and sizes.
  - GPU names, VRAM, driver info.
  - OS version, architecture.

Dependencies:
- Internal: `utils/system_info.py` for gathering data, `utils/formatting.py` for CLI display.
- External: `psutil`, `cpuinfo`, `platform`, `GPUtil`.

Notes:
- CLI-only display; do not modify system state.
"""
