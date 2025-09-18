"""
Port Scanner feature.

Purpose:
- Discover listening ports and map them to PIDs/process names on the local host.

API:
- run(args: dict = None, ctx: dict = None) -> dict
    - args: {"ip": "127.0.0.1", "port_range": [min,max] | None, "protocol": "tcp"|"udp"}
    - return: {"success": True, "data": [{"port": int, "pid": int, "process": str}], "message": None}

Implementation notes:
- Use psutil.net_connections(kind='inet') and filter by laddr/ip.
- For remote scans, use socket with strict timeouts and require explicit user consent.

Dependencies:
- Internal: utils.formatting, utils.logger
- External: psutil, socket

Safety:
- Avoid aggressive remote scanning; default to localhost.
"""
