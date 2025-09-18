"""
Productivity package orchestrator.

Purpose:
- Expose productivity features and dispatch to:
    ["clipboard_monitor","snippet_manager","quick_launcher"]

Exports:
- meta and run(feature_id, args, ctx)

Design:
- Each feature lives in its own file (clipboard_monitor.py etc.) and is imported on demand.
"""
