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

import logging


class Logger:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._configure_logging_level()
        self._configure_logging_format()
        self._configure_logging_file()
        self._configure_logging_console()

    def _configure_logging_level(self):
        self.logger.setLevel(logging.DEBUG)

    def _configure_logging_format(self):
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def _configure_logging_file(self):
        file_handler = logging.FileHandler('logs/utility_suite.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)

    def _configure_logging_console(self):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(self.formatter)
        self.logger.addHandler(console_handler)

    def shutdown(self):
        for handler in self.logger.handlers:
            handler.close()
        self.logger.handlers.clear()
        self.logger.propagate = False
        for handler in self.logger.handlers:
            self.logger.removeHandler(handler)
        self.logger.handlers.clear()
        self.logger.propagate = False