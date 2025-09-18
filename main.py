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

import traceback
from utils.formatting import Formatting
from utils.service_manager import ServiceManager
from utils.constants import Constants
from utils.module_loader import ModuleLoader
from utils.config_manager import ConfigManager
from utils.logger import get_logger, shutdown_logger
import sys
from rich.console import Console
from rich.panel import Panel

class Main:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.formatting = Formatting()
        self.config_manager = ConfigManager()
        self.service_manager = ServiceManager()
        self.constants = Constants()
        self.module_loader = ModuleLoader()
        self.is_initialized = False
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

    def initialize(self):
        self.logger.info("Initializing...")
        # TODO: Implement initialize
        # this is currently a placeholder
        self._setup_environment()
        self.is_initialized = True
        self.logger.info("Initialize complete")

    def run(self):
        while self.is_initialized:
            try:
                initial_load_choice = input("Would you like to use the CLI? (y/n): ")
                if initial_load_choice.lower() == "y":
                    self._run_cli()
                elif initial_load_choice.lower() == "n":
                    self._run_ui()
                else:
                    print("Invalid choice")
                    self.logger.error("Invalid choice")
                    continue
            except Exception as e:
                self.logger.error(f"Error running CLI: {e}")
                self.logger.error(traceback.format_exc())
                self.logger.error("Shutting down...")
                self._shutdown()

    def _run_cli(self):
        self.logger.info("Running CLI...")
        console = Console()
        while True:
            console.print(Panel(f"[bold purple]Welcome to the Utility Suite![/bold purple]\n[bold red]Please select an option:[/bold red]"))
            for choice in self.menu_choices:
                console.print(f"[cyan]{choice}[/cyan]")

            choice = console.input("\n[bold yellow]Enter your choice:[/bold yellow] ")
            if choice in self.menu_choices_mapped:
                self.menu_choices_mapped[choice]()
            else:
                console.print("[red]Invalid choice[/red]\n")

    def _run_ui(self):
        self.logger.info("Running UI...")
        # TODO: Implement run ui
        # this is currently a placeholder
        self.logger.info("UI run complete")
        self.logger.info("UI is not implemented yet")
        self.logger.info("Shutting down...")
        self._shutdown()

    def _show_packages(self):
        self.logger.info("Showing packages...")
        self.module_loader.run()

    def _show_options(self):
        # TODO: Implement show options
        # this is currently a placeholder
        self.logger.info("Showing options...")
        print("Show Options")

    def _show_project_info(self):
        # TODO: Implement show project info
        # this is currently a placeholder
        self.logger.info("Showing project info...")
        print("Show Project Info")

    def _setup_environment(self):
        self.logger.info("Setting up environment...")
        self.config_manager.setup()
        # self.service_manager.setup() # TODO: Add service manager setup
        # self.constants.setup() # TODO: Add constants setup
        # self.module_loader.setup() # TODO: Add module loader setup
        self.logger.info("Environment setup complete")

    def _shutdown(self):
        self.logger.info("Shutting down...")
        # TODO: Implement shutdown
        # this is currently a placeholder
        self.logger.info("Shutdown complete")
        shutdown_logger()
        self.is_initialized = False
        sys.exit(0)

if __name__ == "__main__":
    main = Main()
    main.initialize()
    main.run()