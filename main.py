# main.py
"""
Main entrypoint for the Utility Suite CLI.

Responsibilities:
- Initialize application and logging.
- Start the main CLI loop.
- Delegate loading and execution of tool modules to `module_loader.py`.
- Pass shared utilities (logger, formatting, etc.) to modules when they run.
- Handle graceful shutdown and cleanup when the user exits.

Dependencies:
- Internal: `utils/module_loader.py` for loading tool modules.
- External: `sys`.

Notes:
- This file does NOT implement any tool-specific logic.
- It should remain lightweight; heavy modules are loaded on-demand by `module_loader.py`.
- All CLI interaction and menu display logic occurs here.
"""
