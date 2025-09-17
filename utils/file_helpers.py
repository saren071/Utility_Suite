# utils/file_helpers.py
"""
File helper utilities for file operations.

Responsibilities:
- Common file and directory operations to reduce code duplication:
  - Recursive directory traversal.
  - Safe file copying and moving.
  - File hashing for duplicates/integrity checks.
  - Safe deletion with optional backup.
- Provide helper functions for modules like Disk Space Visualizer, Duplicate Finder, File Organizer.

Dependencies:
- External: `os`, `shutil`, `hashlib`.
- Internal: None.

Notes:
- Should NOT perform user interaction; return structured data for tools to consume.
- Ensure Windows-safe paths.
"""
