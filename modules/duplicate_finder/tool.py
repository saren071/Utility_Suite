# modules/duplicate_finder/tool.py
"""
Duplicate File Finder module.

Responsibilities:
- Scan a folder and hash all files (MD5/SHA256) to identify duplicates.
- Group files by identical hashes.
- Allow listing, moving, or deleting duplicates.

Dependencies:
- Internal: `utils/file_helpers.py` for hashing and file operations, `utils/formatting.py` for CLI display.
- External: `hashlib`, `os`, `shutil`.

Notes:
- Must handle large files efficiently (read in chunks).
- Optional deletion/move should ask for user confirmation.
"""
