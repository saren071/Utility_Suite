# utils/logger.py
"""
Centralized logging utility for the Utility Suite.

Responsibilities:
- Provide a single logger instance shared across all modules.
- Log messages to both console and file (`logs/utility_suite.log`).
- Support different log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL.
- Include timestamps and module names in logs.

Dependencies:
- External: `logging`, `os`.

Usage:
- Import logger in any module: `from utils.logger import logger`
- Use like: `logger.info("Message")` or `logger.error("Error message")`.

Notes:
- Ensure `logs/` directory exists; create if missing at runtime.
- Avoid file I/O directly in modules; use this logger for all messages.
"""
