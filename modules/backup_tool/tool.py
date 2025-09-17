# modules/backup_tool/tool.py
"""
Simple Backup Tool module.

Responsibilities:
- Copy a folder to a backup location.
- Name backups with timestamp.
- Optionally compress backups into zip files.
- Restore from backup when requested.

Dependencies:
- Internal: `utils/file_helpers.py`.
- External: `os`, `shutil`, `zipfile`, `datetime`.

Notes:
- Should check disk space before backup.
- CLI should display progress.
"""
