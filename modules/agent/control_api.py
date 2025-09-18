"""
Agent IPC helper (control API).

Purpose:
- Provide a small client library to communicate with the running agent:
    - connect(), send_command(cmd_dict), receive_response(timeout)
- Support named pipes on Windows and TCP localhost fallback.

Responsibilities:
- Serialize commands/responses as JSON.
- Implement simple auth token support (optional) for local-only security.

Dependencies:
- External: socket, json
- Internal: utils.logger

Testing:
- Provide a mock server for unit tests.
"""
