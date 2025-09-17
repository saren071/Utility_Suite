# utils/formatting.py
"""
Shared formatting utility functions.

Responsibilities:
- Provide consistent CLI output formatting across all tools.
- Support features like:
  - Tables for listing items.
  - Colored text for warnings/errors/info.
  - Human-readable byte sizes (KB, MB, GB).
  - Progress bars for operations.

Dependencies:
- External: `colorama` (for colored output).
- Internal: None.

Notes:
- Should NOT perform file I/O or system queries.
- All functions are pure utilities for formatting strings and CLI display.
"""
