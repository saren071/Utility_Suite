"""
System package orchestrator (tool.py).

Purpose:
- Expose system-level features and dispatch to feature files:
    features: ["system_monitor","system_info","process_manager","services_viewer","startup_checker","battery_monitor"]

Exports:
- meta and run(feature_id, args, ctx)

Responsibilities:
- Validate features and import the feature module dynamically.
- Provide structured error handling and consistent return shapes.

Dependencies:
- Internal: utils.logger, utils.module_loader, utils.formatting

Safety:
- Actions that modify system state (services, startup registry) require admin checks and confirmations.
"""
