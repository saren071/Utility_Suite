"""
System Monitor feature.

Purpose:
- Provide snapshot or streaming resource metrics: CPU, per-core, RAM, disk I/O, network I/O, GPU.

API:
- run(args: dict = None, ctx: dict = None) -> dict
    - args: {"interval": float, "count": int, "log": bool}
    - return: {"success": True, "data": [{"timestamp":..., "cpu":..., "ram":..., "gpus":...}], "message": None}

Implementation notes:
- Use psutil for CPU/RAM/disk/network. Use GPUtil or NVML for GPU if present.
- For streaming, return incremental results or write to a temporary log file when running headless.

Dependencies:
- Internal: utils.formatting, utils.logger
- External: psutil, GPUtil (optional), time

Testing:
- Provide a short-run mode (count=1) for unit tests.
"""
