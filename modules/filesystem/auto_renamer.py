"""
Auto-Renamer feature.

Purpose:
- Batch rename files by applying rules: replace spaces, add date prefix, normalize case, etc.

API:
- run(args: dict = None, ctx: dict = None) -> dict
    - args: {"path": str, "rule": "spaces_to_underscores"|"prefix_date"|"lowercase", "dry_run": True}
    - return: {"success": True, "data": {"renamed": [{"old": "new"}]}, "message": None}

Implementation notes:
- Use utils.file_helpers.safe_move to rename files safely.
- Detect collisions and append counters to avoid overwrites, or report collisions in dry-run.

Dependencies:
- Internal: utils.file_helpers, utils.formatting, utils.logger
- External: os, datetime

Safety:
- Default to dry-run.
"""

import os
import datetime
from utils.formatting import Formatting
from utils.logger import get_logger
from utils.file_helpers import FileHelpers

class AutoRenamer:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.file_helpers = FileHelpers()
        self.formatting = Formatting()

    def run(self, args: dict | None, ctx: dict | None) -> dict:
        """
        Run the Auto Renamer.
        Args are optional, and will default to False if not provided.
        Args are validated against the possible_args dictionary.
        """
        if args is None or not isinstance(args, dict):
            args = {}
        if ctx is None or not isinstance(ctx, dict):
            ctx = {}

        path = args.get("path")
        rule = args.get("rule")
        dry_run = args.get("dry_run", True)

        if not path or not os.path.isdir(path):
            return {"success": False, "data": {}, "message": f"Invalid path: {path}"}

        if rule not in {"spaces_to_underscores", "prefix_date", "lowercase"}:
            return {"success": False, "data": {}, "message": f"Invalid rule: {rule}"}

        renamed_files = []

        for fname in os.listdir(path):
            old_path = os.path.join(path, fname)
            if not os.path.isfile(old_path):
                continue

            new_path = self._generate_new_path(old_path, rule)

            if old_path != new_path:
                if dry_run:
                    self.logger.info(f"[DRY RUN] Would rename: {old_path} -> {new_path}")
                else:
                    self._perform_rename(old_path, new_path, args)
                renamed_files.append({old_path: new_path})

        return {"success": True, "data": {"renamed": renamed_files}, "message": None}

    def _generate_new_path(self, file_path: str, rule: str | None) -> str:
        """
        Generate the new file path according to the rule, handling collisions.
        """
        dir_name = os.path.dirname(file_path)
        base_name = os.path.basename(file_path)
        new_name = self.formatting.apply_rule(base_name, rule) if rule else base_name

        if rule == "prefix_date":
            today = datetime.datetime.now().strftime("%Y-%m-%d_")
            new_name = today + new_name

        new_path = os.path.join(dir_name, new_name)

        # Handle collisions by appending _1, _2, etc.
        counter = 1
        base, ext = os.path.splitext(new_name)
        while os.path.exists(new_path):
            new_name = f"{base}_{counter}{ext}"
            new_path = os.path.join(dir_name, new_name)
            counter += 1

        return new_path

    def _perform_rename(self, old_path: str, new_path: str, args: dict):
        """
        Rename a file safely using FileHelpers, with optional backup.
        """
        self.file_helpers.safe_move(old_path, new_path)

        if args.get("backup"):
            backup_dir = os.path.join(os.path.dirname(old_path), "backup")
            os.makedirs(backup_dir, exist_ok=True)
            self.file_helpers.safe_copy(new_path, os.path.join(backup_dir, os.path.basename(new_path)))
