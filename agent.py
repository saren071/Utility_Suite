"""
Background agent for persistent tasks (user-mode or service-hosted).

Purpose:
- Execute scheduled and persistent tasks independent of the CLI/GUI.
- Provide an IPC interface (named pipe or localhost socket) for CLI/GUI to query and control the agent.

Responsibilities:
- Load schedules from config/agent_config.json and start tasks accordingly.
- Use utils.module_loader.load_package() to import features on-demand.
- Run tasks in threads or subprocesses (heavy tasks in subprocesses).
- Expose IPC for commands: status, start_task, stop_task, reload_config.
- Log runtime events using utils.logger. Use rotating file handlers.

Dependencies:
- Internal: utils.module_loader, utils.logger, utils.config_manager, utils.service_manager
- External: threading, socket or namedpipe, apscheduler (optional)

Design constraints:
- Lazy-import package code at execution time.
- Must handle and isolate task failures; agent should not crash from a single feature exception.
- Provide a debug/foreground mode (`--debug`) for development.

Security & permissions:
- Agent should run with minimum privileges; any admin-required task must escalate via explicit user action.
"""
