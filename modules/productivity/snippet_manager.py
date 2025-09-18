"""
Snippet Manager feature.

Purpose:
- Manage saved snippets with tags, timestamps, and quick retrieval.

API:
- run(args, ctx) -> dict
    - args: {"action":"add"|"list"|"search"|"delete", "snippet": str, "tags": [str]}
    - return: {"success": True, "data": [...], "message": None}

Implementation notes:
- Persist snippets via ctx["config_manager"] in a JSON DB.
- Provide quick copy-to-clipboard via pyperclip when requested.

Dependencies:
- Internal: utils.config_manager, utils.logger
- External: pyperclip (optional)

Safety:
- Local-only storage; provide export/import options.
"""
