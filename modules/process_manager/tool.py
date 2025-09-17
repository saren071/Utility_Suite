# modules/process_manager/tool.py
"""
Process Manager Lite module.

Responsibilities:
- List running processes with PID, CPU%, and RAM%.
- Support filtering by process name.
- Allow terminating processes by PID.
- Provide Windows-specific fallback using `taskkill` for restricted processes.

Dependencies:
- Internal: `utils/formatting.py` for table display.
- External: `psutil`, `subprocess`, `os`.

Notes:
- Must handle permission errors gracefully.
- Should not forcibly kill critical system processes.
"""
