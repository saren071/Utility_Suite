# main.py
"""
Main entrypoint and runtime orchestrator for Utility Suite.

Responsibilities:
- Ensure environment readiness:
    - Create config/ and logs/ directories if missing (use utils.config_manager).
    - Initialize centralized logger (utils.logger).
- Fast package discovery via utils.module_loader.discover_packages().
- Present CLI:
    - Show packages and their features.
    - Accept selection; load package and run selected feature with args.
- Provide runtime context `ctx` to features:
    ctx = {"logger", "format", "config_manager", "service_manager", "constants"}
- Graceful shutdown.
"""

from __future__ import annotations

import json
import sys
import traceback
from typing import Any

from utils.formatting import Formatting
from utils.service_manager import ServiceManager
from utils.constants import Constants
from utils.module_loader import ModuleLoader
from utils.config_manager import ConfigManager
from utils.logger import get_logger, shutdown_logger

from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class Main:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.formatting = Formatting()
        self.config_manager = ConfigManager()
        self.service_manager = ServiceManager()
        self.constants = Constants()
        self.module_loader = ModuleLoader()
        self.console = Console()
        self.is_initialized = False

    def initialize(self):
        self.logger.info("Initializing...")
        self.config_manager.setup()
        self.is_initialized = True
        self.logger.info("Initialize complete")

    def run(self):
        if not self.is_initialized:
            self.initialize()
        try:
            self._run_cli()
        except KeyboardInterrupt:
            self.console.print("\n[red]Interrupted[/red]")
        except Exception as e:
            self.logger.error(f"Error running CLI: {e}")
            self.logger.error(traceback.format_exc())
        finally:
            self._shutdown()

    def _ctx(self) -> dict:
        return {
            "logger": self.logger,
            "format": self.formatting,
            "config_manager": self.config_manager,
            "service_manager": self.service_manager,
            "constants": self.constants,
        }

    def _run_cli(self):
        while True:
            self.console.print(Panel("[bold purple]Utility Suite[/bold purple]\nSelect an option:"))
            self.console.print("[cyan]1.[/cyan] List & Run Packages")
            self.console.print("[cyan]2.[/cyan] Project Info")
            self.console.print("[cyan]3.[/cyan] Exit")
            choice = self.console.input("\n[bold yellow]Enter choice:[/bold yellow] ").strip()
            if choice == "1":
                self._menu_packages()
            elif choice == "2":
                self._show_project_info()
            elif choice == "3":
                break
            else:
                self.console.print("[red]Invalid choice[/red]\n")

    def _menu_packages(self):
        packages = self.module_loader.discover_packages()
        if not packages:
            self.console.print("[red]No packages found.[/red]")
            return

        # List packages
        table = Table(title="Packages")
        table.add_column("#", justify="right")
        table.add_column("ID")
        table.add_column("Name")
        table.add_column("Version")
        table.add_column("Features")
        for idx, pkg in enumerate(packages, start=1):
            features = ", ".join([f.get("id", "?") for f in pkg.get("features", [])])
            table.add_row(str(idx), pkg.get("id", ""), pkg.get("name", ""), pkg.get("version", ""), features)
        self.console.print(table)

        sel = self.console.input("Select package # (or blank to return): ").strip()
        if not sel:
            return
        try:
            pidx = int(sel) - 1
            if pidx < 0 or pidx >= len(packages):
                raise ValueError
        except Exception:
            self.console.print("[red]Invalid selection[/red]")
            return

        pkg_meta = packages[pidx]
        pkg_id_val = pkg_meta.get("id")
        if not isinstance(pkg_id_val, str) or not pkg_id_val:
            self.console.print("[red]Invalid package id[/red]")
            return
        pkg_id: str = pkg_id_val
        module = self.module_loader.load_package(pkg_id)
        if module is None:
            self.console.print(f"[red]Failed to load package {pkg_id}[/red]")
            return

        feats = module.meta.get("features", [])
        if not feats:
            self.console.print("[yellow]No features found for this package[/yellow]")
            return

        # Feature selection
        table = Table(title=f"Features — {pkg_meta.get('name', pkg_id)}")
        table.add_column("#", justify="right")
        table.add_column("Feature ID")
        table.add_column("Name")
        for idx, f in enumerate(feats, start=1):
            table.add_row(str(idx), f.get("id", ""), f.get("name", ""))
        self.console.print(table)

        sel = self.console.input("Select feature # (or blank to return): ").strip()
        if not sel:
            return
        try:
            fidx = int(sel) - 1
            if fidx < 0 or fidx >= len(feats):
                raise ValueError
        except Exception:
            self.console.print("[red]Invalid selection[/red]")
            return

        feature_id_val = feats[fidx].get("id")
        if not isinstance(feature_id_val, str) or not feature_id_val:
            self.console.print("[red]Invalid feature id[/red]")
            return
        feature_id: str = feature_id_val

        # Args input
        self.console.print("Enter args as JSON (e.g., {\"path\": \"C:\\temp\"}) or blank for {}:")
        args_s = self.console.input("> ").strip()
        args: dict[str, Any] = {}
        if args_s:
            try:
                args = json.loads(args_s)
                if not isinstance(args, dict):
                    raise ValueError
            except Exception:
                self.console.print("[red]Invalid JSON args. Using {}[/red]")
                args = {}

        # Execute
        self.console.print(Panel(f"Running {pkg_id}.{feature_id} ...", style="green"))
        result = module.run(feature_id, args=args, ctx=self._ctx())
        self._render_result(result)

    def _render_result(self, result: dict):
        success = result.get("success")
        message = result.get("message")
        data = result.get("data")
        status = "SUCCESS" if success else "FAIL"
        self.console.print(Panel(f"Status: {status}\nMessage: {message}", title="Result"))
        try:
            pretty = json.dumps(data, indent=2, ensure_ascii=False)
            self.console.print(pretty)
        except Exception:
            self.console.print(str(data))

    def _show_project_info(self):
        self.console.print(Panel("Utility Suite — Modular utilities for Windows. (v0.1.0)", title="About"))

    def _shutdown(self):
        self.logger.info("Shutting down...")
        shutdown_logger()
        self.is_initialized = False
        # Do not sys.exit here to allow embedding


if __name__ == "__main__":
    app = Main()
    app.initialize()
    app.run()