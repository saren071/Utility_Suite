"""
Network package orchestrator.

Purpose:
- Expose network features and dispatch to feature files:
    features: ["port_scanner","local_ping","package_manager_viewer","http_check"]

Exports:
- meta and run(feature_id, args, ctx)

Safety:
- Network scanning limited to localhost by default; remote scans require opt-in.
"""
