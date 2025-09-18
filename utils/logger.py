# utils/logger.py
"""
Centralized logging utility.

Responsibilities:
- Configure and provide a `logging.Logger` instance named "utility_suite".
- Set up console and rotating file handlers (logs/utility_suite.log).
- Provide helper function get_logger(name) for module-specific loggers.
- Ensure logs/ directory exists at import time.

Dependencies:
- External: logging, logging.handlers, os
- Internal: utils.constants

Testing:
- Provide a reconfigure_for_tests(temp_dir) helper to divert logs to temp in tests.
"""

import logging
from logging.handlers import RotatingFileHandler
import os
import sys
from utils.constants import Constants

class LoggerManager:
    def __init__(self):
        self.logger = logging.getLogger(Constants.LOGGER_NAME)
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        if not os.path.exists(Constants.LOG_DIR):
            os.makedirs(Constants.LOG_DIR, exist_ok=True)
        self._ensure_file_handler()
        self._ensure_console_handler()

    def _ensure_file_handler(self):
        abs_target = os.path.abspath(Constants.LOG_FILE)
        for h in self.logger.handlers:
            if isinstance(h, RotatingFileHandler):
                if getattr(h, 'baseFilename', None) == abs_target:
                    return
            if isinstance(h, logging.FileHandler) and getattr(h, 'baseFilename', None) == abs_target:
                return

        fh = RotatingFileHandler(Constants.LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=5, encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)
        fh.name = f"file::{abs_target}"
        self.logger.addHandler(fh)

    def _ensure_console_handler(self):
        for h in self.logger.handlers:
            if isinstance(h, logging.StreamHandler):
                return

        ch = logging.StreamHandler(stream=sys.stdout)
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formatter)
        ch.name = "console"
        self.logger.addHandler(ch)

    def get_logger(self, name: str):
        """
        Return a child logger for `name`. Example: get_logger(__name__)
        Child loggers inherit handlers from utility_suite but show their own name
        """
        return self.logger.getChild(name)

    def shutdown(self):
        """
        Close and remove handlers safely. After shutdown, the manager's logger
        no longer has handlers if you need to re-enable logging, re-instantiate LoggerManager.
        """
        handlers = list(self.logger.handlers)  # copy to avoid modification during iteration
        for h in handlers:
            try:
                h.flush()
            except Exception:
                pass
            try:
                h.close()
            except Exception:
                pass
            try:
                self.logger.removeHandler(h)
            except Exception:
                pass
        self.logger.propagate = False

_manager = LoggerManager()

def get_logger(name: str):
    return _manager.get_logger(name)

def shutdown_logger():
    _manager.shutdown()