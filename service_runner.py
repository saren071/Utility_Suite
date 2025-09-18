"""
Windows service bootstrap entrypoint.

Purpose:
- Provide the service lifecycle adapter that Windows Service Control Manager invokes.
- Start the agent in service mode and map service start/stop to agent lifecycle events.

Responsibilities:
- Initialize logging and a minimal environment.
- Invoke agent in a non-interactive mode appropriate for services.
- Handle stop signals, ensure agent state saved, and close resources.
- Offer a foreground/debug mode when run directly for development.

Dependencies:
- Internal: utils.logger, agent, utils.module_loader
- External: pywin32 (win32serviceutil, win32service, win32event) recommended; fallback to sc.exe wrapper if pywin32 unavailable.

Notes:
- No interactive console I/O when running as a system service.
- Packaged EXE is recommended for production service to avoid Python path issues.
"""
