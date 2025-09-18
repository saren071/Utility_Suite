"""
Backup package orchestrator.

Purpose:
- Expose backup-related features:
    ["full_backup","incremental_backup","restore","snapshot_list"]

Exports:
- meta and run(feature_id, args, ctx)

Design:
- Heavy operations should be invoked as subprocesses in agent/service mode.
"""
