# main.py
"""
Main entrypoint and runtime orchestrator for Utility Suite.

Responsibilities:
- Ensure environment readiness:
    - Create config/ and logs/ directories if missing (use utils.config_manager).
    - Initialize centralized logger (utils.logger).
    - Load persisted user settings and manifest (utils.config_manager).
- Load lightweight package metadata via utils.module_loader.discover_packages() to build CLI menus quickly.
- Present CLI to user:
    - Show packages and their features.
    - Accept selection of package -> feature.
    - When a feature is selected, call utils.module_loader.load_package(package_id) and then package.run(feature_id, args, ctx).
- Provide runtime context `ctx` injected into packages/features:
    ctx = {
        "logger": logger,
        "format": formatting,
        "config_manager": config_manager,
        "service_manager": service_manager,
        "constants": constants
    }
- Coordinate starting/stopping the background agent on user request.
- Graceful shutdown: request running tasks to stop, flush logs, save state.

Design constraints:
- Keep imports lightweight at module import time (lazy import heavy libs inside functions).
- main.py must not implement package-specific logic.

Dependencies:
- Internal: utils.module_loader, utils.logger, utils.formatting, utils.config_manager, utils.service_manager
- External: sys, signal, threading

Testing:
- Factor CLI loop into testable functions to allow pytest-driven simulation of user choices.
"""

from utils import formatting, config_manager, service_manager, constants, module_loader
from utils.logger import Logger
import sys

class Main:
    def __init__(self):
        self.logger = Logger()
        self.formatting = formatting
        self.config_manager = config_manager
        self.service_manager = service_manager
        self.constants = constants
        self.module_loader = module_loader
        self.menu_choices = [
            "1. Show Packages",
            "2. Show Options",
            "3. Show Project Info",
            "4. Exit"
        ]
        self.menu_choices_mapped = {
            "1": self._show_packages,
            "2": self._show_options,
            "3": self._show_project_info,
            "4": self._shutdown
        }

    def run(self):
        self._setup_environment()
        self._run_cli() # Optional, main ui will be used unless user wants to use cli, provide a choice to use cli

    def _run_cli(self):
        while True:
            # TODO: Implement cli
            # this is currently a placeholder
            cli_display = """
            Welcome to the Utility Suite!
            Please select an option:
            """
            menu_choice_display = ""
            for choice in self.menu_choices:
                menu_choice_display += f"{choice}\n"
            print(cli_display + menu_choice_display)
            choice = input("Enter your choice: ")
            if choice in self.menu_choices_mapped:
                self.menu_choices_mapped[choice]()
            else:
                print("Invalid choice")
                continue

    def _show_packages(self):
        # TODO: Implement show packages
        # this is currently a placeholder
        print("Show Packages")

    def _show_options(self):
        # TODO: Implement show options
        # this is currently a placeholder
        print("Show Options")

    def _show_project_info(self):
        # TODO: Implement show project info
        # this is currently a placeholder
        print("Show Project Info")

    def _setup_environment(self):
        self.logger.logger.info("Setting up environment...")
        # self.config_manager.setup() # TODO: Add config manager setup
        # self.service_manager.setup() # TODO: Add service manager setup
        # self.constants.setup() # TODO: Add constants setup
        # self.module_loader.setup() # TODO: Add module loader setup
        self.logger.logger.info("Environment setup complete")

    def _shutdown(self):
        self.logger.logger.info("Shutting down...")
        # TODO: Implement shutdown
        # this is currently a placeholder
        self.logger.logger.info("Shutdown complete")
        self.logger.shutdown()
        sys.exit(0)

if __name__ == "__main__":
    main = Main()
    main.run()