"""
HTTP check feature.

Purpose:
- Perform a simple HTTP GET to a URL and return status code and timings.

API:
- run(args, ctx) -> dict
    - args: {"url": str, "timeout": float}
    - return: {"success": True, "data": {"status_code": int, "elapsed_ms": float}, "message": None}

Implementation notes:
- Use requests if available; else use urllib with strict timeouts.
- Respect robots/usage policies for remote servers (do not poll aggressively).

Dependencies:
- External: requests (optional), urllib
- Internal: utils.logger

Safety:
- Default to safe single-shot checks; no continuous polling unless requested.
"""
