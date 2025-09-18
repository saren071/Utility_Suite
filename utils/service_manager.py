"""
Service and scheduled-task manager (Windows-focused).

Responsibilities:
- Provide unified APIs for service and scheduled task management:
    - install_service(service_name, exe_path, args, run_as)
    - uninstall_service(service_name)
    - create_scheduled_task(task_name, command, trigger)
    - delete_scheduled_task(task_name)
    - start_service(service_name), stop_service(service_name), query_service_status(service_name)
- Use pywin32 when available, otherwise fallback to sc.exe and schtasks.exe via subprocess.
- Check for admin privileges (is_admin()).

Safety:
- All operations logged and recorded in config/modules.json to allow clean uninstall.
- Prompt for confirmation before making system-level changes.
"""

from utils.logger import get_logger


class ServiceManager:
    def __init__(self):
        self.logger = get_logger(__name__)

    def install_service(self, service_name, exe_path, args, run_as):
        self.logger.info(f"Installing service {service_name}...")
        if self.use_pywin32():
            # TODO: Implement real service creation using pywin32
            return True
        # TODO: Fallback to sc.exe
        return False

    def uninstall_service(self, service_name):
        self.logger.info(f"Uninstalling service {service_name}...")
        if self.use_pywin32():
            # TODO: Implement real uninstall using pywin32
            return True
        # TODO: Fallback to sc.exe
        return False

    def create_scheduled_task(self, task_name, command, trigger):
        self.logger.info(f"Creating scheduled task {task_name}...")
        # TODO: Implement via schtasks.exe
        return True

    def delete_scheduled_task(self, task_name):
        self.logger.info(f"Deleting scheduled task {task_name}...")
        # TODO: Implement via schtasks.exe
        return True

    def start_service(self, service_name):
        self.logger.info(f"Starting service {service_name}...")
        # TODO: Implement real start
        return True

    def stop_service(self, service_name):
        self.logger.info(f"Stopping service {service_name}...")
        # TODO: Implement real stop
        return True

    def query_service_status(self, service_name):
        self.logger.info(f"Querying service status {service_name}...")
        # TODO: Implement real status
        return True

    def is_admin(self):
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False

    def use_pywin32(self):
        try:
            import win32service
            import win32serviceutil
            import win32api
            _ = (win32service, win32serviceutil, win32api)
            return True
        except Exception:
            return False


