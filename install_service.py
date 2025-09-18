"""
Install helper to register the Utility Suite agent as a Windows Service or Scheduled Task.

Responsibilities:
- Provide two install options:
    1) Install as a Windows Service (pywin32 recommended).
    2) Create a Scheduled Task (schtasks) to run the agent at login/startup.
- Validate administrative privileges before performing operations.
- Use utils.service_manager APIs to perform install actions and record manifests in config/modules.json and config/agent_config.json.
- Optionally perform a dry-run to preview actions.
- Log installation steps and errors via utils.logger.

Dependencies:
- Internal: utils.logger, utils.config_manager, utils.service_manager
- External: subprocess, ctypes (for admin checks), pywin32 (optional)

Safety:
- Confirm with user before making system changes.
- Do not start service automatically unless user explicitly opts-in.
"""
