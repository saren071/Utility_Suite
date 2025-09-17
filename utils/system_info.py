# utils/system_info.py
"""
System information utilities.

Responsibilities:
- Retrieve Windows system information for multiple modules:
  - CPU model, cores, threads.
  - RAM total/available.
  - Disk partitions, capacity, and usage.
  - GPU information (name, VRAM, temperature) using `GPUtil`.
  - OS version and architecture.

Dependencies:
- External: `psutil`, `platform`, `cpuinfo`, `GPUtil`.
- Internal: None.

Notes:
- Should only return structured data (dicts, lists); formatting for display is handled elsewhere.
- No CLI output in this file.
"""
