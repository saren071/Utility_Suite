"""
Global constants for the project.

Responsibilities:
- Centralize important paths and defaults:
    LOGGER_NAME = "utility_suite"
    LOG_DIR = "logs"
    LOG_FILE = "logs/utility_suite.log"
    CONFIG_DIR = "config"
    MODULES_DIR = "modules"
    AGENT_CONFIG = "config/agent_config.json"
    MODULES_MANIFEST = "config/modules.json"
    DEFAULT_SCHEDULE_MAX_CONCURRENT = 2
- Avoid runtime logic; pure constants only.

Notes:
- If runtime overrides are needed, config_manager should handle them.
"""
class Constants:
    LOGGER_NAME = "utility_suite"
    LOG_DIR = "logs"
    LOG_FILE = "logs/utility_suite.log"
    CONFIG_DIR = "config"
    MODULES_DIR = "modules"
    AGENT_CONFIG = "config/agent_config.json"
    MODULES_MANIFEST = "config/modules.json"
    DEFAULT_SCHEDULE_MAX_CONCURRENT = 2





