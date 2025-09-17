# utils/module_loader.py
"""
Dynamic module/package loader for the Utility Suite.

Responsibilities:
- Discover all tool modules in the `/modules/` directory.
  - Each tool resides in its own folder with a `tool.py` entrypoint.
- Read each module's `meta` dictionary to extract:
  - Name
  - Description
  - Author
  - Version
- Import tool modules dynamically without loading them all at startup.
  - Keeps memory usage low and improves initial load time.
- Provide a standardized interface for `main.py` to:
  - Retrieve available tools and their metadata.
  - Load a specific tool on-demand.
  - Pass shared utilities and logger to the module.
- Handle errors gracefully if a module is missing required `meta` or `run()`.

Dependencies:
- Internal: `utils/logger.py` for logging, optionally `utils/formatting.py`.
- External: `importlib`, `os`, `sys`, `types`.

Usage:
- `modules = module_loader.discover_modules()`
- `tool_instance = module_loader.load_module("disk_space")`
- Returns the module object, ready to call `tool_instance.run()`.

Notes:
- This file does NOT execute any tools by itself.
- Keeps startup lightweight by only importing metadata initially.
- Ensures consistency and error-checking before main application loop runs.
"""
