# modules/log_analyzer/tool.py
"""
Log File Analyzer module.

Responsibilities:
- Parse `.log` files and summarize entries.
- Count number of ERROR/WARNING/INFO lines.
- Extract most frequent messages.
- Optionally group logs by timestamp intervals (hour/day).

Dependencies:
- Internal: `utils/formatting.py`.
- External: `re`, `os`, `datetime`.

Notes:
- Should not modify log files.
- Supports large files by reading line-by-line.
"""
