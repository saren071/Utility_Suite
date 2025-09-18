# utils/formatting.py
"""
Formatting helpers for CLI output.

Responsibilities:
- Provide pure functions for formatting:
    - human_readable_size(bytes, precision=1)
    - format_table(rows, headers=None)
    - format_seconds(seconds)
    - truncate_middle(text, maxlen)
- Support optional `rich` integration if available; fallback to plain text.

Dependencies:
- External (optional): rich, colorama
- Internal: None

Notes:
- Return strings only; do not print directly.
"""

import tabulate

class Formatting:
    def __init__(self):
        pass
    
    def human_readable_size(self, bytes, precision=1):
        """
        Convert bytes to a human readable size.
        """
        if bytes == 0:
            return "0B"
        size_names = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
        i = 0
        while bytes >= 1024 and i < len(size_names) - 1:
            bytes /= 1024
            i += 1
        return f"{bytes:.{precision}f}{size_names[i]}"
    
    def format_table(self, rows, headers=None):
        """
        Format a table of rows and headers.
        """
        return tabulate.tabulate(rows, headers=headers, tablefmt="grid") if headers else tabulate.tabulate(rows, tablefmt="grid")
    
    def format_seconds(self, seconds):
        """
        Format seconds to a human readable time.
        """
        return f"{seconds:.2f}s"
    
    def truncate_middle(self, text, maxlen):
        """
        Truncate a text in the middle.
        """
        if len(text) <= maxlen:
            return text
        return f"{text[:maxlen//2]}...{text[-maxlen//2:]}"
