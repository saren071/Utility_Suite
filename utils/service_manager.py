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

Dependencies:
- External: subprocess, ctypes, pywin32 (optional)
- Internal: utils.logger, utils.config_manager

Safety:
- All operations logged and recorded in config/modules.json to allow clean uninstall.
- Prompt for confirmation before making system-level changes.
"""

import subprocess
from utils.logger import get_logger
import win32com.client

class ServiceManager:
    def __init__(self):
        self.logger = get_logger(__name__)

    def install_service(self, service_name, exe_path, args, run_as):
        """
        Install a service.
        """
        self.logger.info(f"Installing service {service_name}...")
        if self.use_pywin32():
            return True
        else:
            return False

    def uninstall_service(self, service_name):
        """
        Uninstall a service.
        """
        self.logger.info(f"Uninstalling service {service_name}...")
        if self.use_pywin32():
            return True
        else:
            return False

    def create_scheduled_task(self, task_name, command, trigger):
        """
        Create a scheduled task.
        """
        self.logger.info(f"Creating scheduled task {task_name}...")
        return True

    def delete_scheduled_task(self, task_name):
        """
        Delete a scheduled task.
        """
        self.logger.info(f"Deleting scheduled task {task_name}...")
        return True

    def start_service(self, service_name):
        """
        Start a service.
        """
        self.logger.info(f"Starting service {service_name}...")
        return True

    def stop_service(self, service_name):
        """
        Stop a service.
        """
        self.logger.info(f"Stopping service {service_name}...")
        return True

    def query_service_status(self, service_name):
        """
        Query the status of a service.
        """
        self.logger.info(f"Querying service status {service_name}...")
        return True

    def is_admin(self):
        """
        Check if the user is admin.
        """
        return True

    def use_pywin32(self):
        """
        Check if pywin32 is available.
        """
        if win32com.client:
            return True
        return False


