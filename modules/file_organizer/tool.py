# modules/file_organizer/tool.py
"""
Configurable File Organizer module.

Responsibilities:
- Organize files into folders based on extension or rules in `config.json`.
- Support dry-run preview mode before moving files.
- Move or copy files according to configuration rules.

Dependencies:
- Internal: `utils/file_helpers.py` for moving/copying files, `utils/formatting.py` for CLI output.
- External: `os`, `shutil`, `json`.

Notes:
- Should never overwrite files unless explicitly allowed.
- Dry-run mode is strongly recommended before first use.
"""
