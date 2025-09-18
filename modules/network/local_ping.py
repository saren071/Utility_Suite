"""
Local Ping / connectivity check feature.

Purpose:
- Ping a target host or service to check connectivity (ICMP or TCP connect).

API:
- run(args: dict, ctx: dict) -> dict
    - args: {"host": str, "timeout": float, "method": "icmp"|"tcp"}
    - return: {"success": True, "data": {"latency_ms": float}, "message": None}

Implementation notes:
- Use socket connect for TCP; for ICMP, rely on system ping (subprocess) unless raw sockets are available.
- Bound timeouts and require explicit host for remote checks.

Dependencies:
- External: socket, subprocess
- Internal: utils.logger

Safety:
- Document that ICMP may require elevated privileges on some platforms.
"""
