# modules/services_viewer/tool.py
"""
Windows Services Viewer module.

Responsibilities:
- List all Windows services with name, description, and current status.
- Optionally allow starting/stopping services from CLI.

Dependencies:
- Internal: `utils/formatting.py`.
- External: `psutil`.

Notes:
- Must handle permissions errors when starting/stopping services.
- Should not allow stopping critical system services.
"""
