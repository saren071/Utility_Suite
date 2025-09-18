"""
Agent control orchestrator.

Purpose:
- Provide package-level meta and dispatch to features in modules/agent:
    features: ["agent_status","start_task","stop_task","list_scheduled_tasks","reload_config"]

Exports:
- meta and run(feature_id, args, ctx)

Implementation notes:
- Communicates with agent IPC (modules/agent/control_api.py) to send commands to the running agent/service.
- For service mode operations that require admin (start/stop service), use utils.service_manager.

Dependencies:
- Internal: modules/agent/control_api, utils.service_manager, utils.logger
"""
