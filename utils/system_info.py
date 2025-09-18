# utils/system_info.py
"""
System information utilities (Windows-optimized).

Responsibilities:
- Provide data retrieval functions:
    - get_os_info()
    - get_cpu_info()
    - get_memory_info()
    - get_disks_info()
    - get_gpu_info()  (GPUtil/NVML optional)
    - get_battery_info()
- Return clean dicts for formatting/display.

Dependencies:
- External: psutil (required), GPUtil (optional), platform, cpuinfo (optional)
- Internal: utils.logger

Notes:
- Perform lazy imports inside functions to avoid heavy startup cost.
"""

# from utils.logger import Logger


class SystemInfo:
    def __init__(self):
        # self.logger = Logger().logger
        pass

    def get_os_info(self):
        import platform
        return {
            "os_name": platform.system(),
            "os_version": platform.release(),
            "os_architecture": platform.machine(),
        }

    def get_cpu_info(self):
        import psutil
        import cpuinfo
        return {
            "cpu_name": cpuinfo.get_cpu_info()["brand_raw"],
            "cpu_count": psutil.cpu_count(),
            "cpu_threads": psutil.cpu_count(logical=False),
            "cpu_frequency": psutil.cpu_freq().current
        }

    def get_memory_info(self):
        import psutil
        return {
            "total_memory": psutil.virtual_memory().total,
            "available_memory": psutil.virtual_memory().available,
            "used_memory": psutil.virtual_memory().used,
            "free_memory": psutil.virtual_memory().free,
        }

    def get_disks_info(self):
        import psutil
        return {
            "disks": psutil.disk_partitions(),
            "disk_usage": psutil.disk_usage(psutil.disk_partitions()[0].mountpoint),
        }

    def get_gpu_info(self):
        import GPUtil
        return {
            "gpu_name": GPUtil.getGPUs()[0].name,
            "gpu_vram": GPUtil.getGPUs()[0].memoryTotal,
            "gpu_temperature": GPUtil.getGPUs()[0].temperature,
        }

    def get_battery_info(self):
        import psutil
        if psutil.sensors_battery() is None:
            return {
                "battery_percentage": None,
                "battery_status": None,
            }
        return {
            "battery_percentage": psutil.sensors_battery().percent,
            "battery_status": psutil.sensors_battery().power_plugged,
        }