"""
Disk Space Visualizer feature.

Purpose:
- Compute sizes of files/folders under a path and return a sorted list of top N largest items.

API:
- meta (optional): {"id":"disk_space", "name":"Disk Space Visualizer"}
- run(args: dict = None, ctx: dict = None) -> dict
    - args: {"path": str, "top_n": int = 20, "depth": int|null, "human_readable": bool}
    - ctx: runtime context with logger, formatting, config_manager, service_manager, constants
    - return: {"success": True, "data": [{"path": str, "size": int, "size_hr": str}], "message": None}

Implementation notes:
- Use utils.file_helpers.folder_size() and iterate_files() for efficiency.
- Support depth-limited traversal.
- For display, caller may use utils.formatting.human_readable_size on returned sizes.

Dependencies:
- Internal: utils.file_helpers, utils.formatting, utils.logger
- External: os

Safety:
- Read-only operation only.
"""
