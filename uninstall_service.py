"""
Uninstall helper to remove the Utility Suite agent service or scheduled task.

Responsibilities:
- Detect installed service/task using config manifest and service_manager queries.
- Stop and remove the service (or delete scheduled task).
- Remove install metadata from config/modules.json and config/agent_config.json.
- Provide soft-uninstall (stop & disable) and full-uninstall (remove registration and optionally purge configs/logs).
- Log actions to utils.logger.

Dependencies:
- Internal: utils.logger, utils.config_manager, utils.service_manager
- External: subprocess, pywin32 (optional)

Safety:
- Request explicit confirmation for destructive actions.
- Preserve user data unless user requests full purge.
"""
