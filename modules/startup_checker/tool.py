# modules/startup_checker/tool.py
"""
Startup Program Checker module.

Responsibilities:
- List programs that run on Windows startup.
- Read registry keys from:
  - HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run
  - HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run
- Optionally disable startup programs by removing registry entries.

Dependencies:
- Internal: `utils/formatting.py`.
- External: `winreg`.

Notes:
- Must request confirmation before deleting registry entries.
- Only run on Windows; error if attempted on other OS.
"""
