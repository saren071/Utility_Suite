# modules/disk_space/tool.py
"""
Disk Space Visualizer module.

Responsibilities:
- Scan a user-specified directory recursively.
- Calculate folder and file sizes.
- Sort and return a list of largest items.
- Optionally limit depth and display human-readable sizes.

Dependencies:
- Internal: `utils/file_helpers.py` for traversal and size calculations, `utils/formatting.py` for display.
- External: `os`.

Notes:
- Should NOT delete or modify any files.
- CLI output handled in `run()`; core logic can return structured data.
"""
