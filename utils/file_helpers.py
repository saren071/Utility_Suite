# utils/file_helpers.py
"""
Filesystem helpers used across packages.

Responsibilities:
- Provide safe, efficient file operations:
    - iterate_files(root, follow_symlinks=False) -> generator[str]
    - folder_size(path, depth=None) -> int (bytes)
    - file_hash(path, algorithm="sha256", chunk_size=65536) -> str
    - safe_copy(src, dst, overwrite=False)
    - safe_move(src, dst, overwrite=False)
    - send_to_trash(path) (uses send2trash if available)
    - atomic_write_json(path, data)
- Read large files in chunks for hashing and copying.

Dependencies:
- External: os, shutil, hashlib, send2trash (optional)
- Internal: utils.logger

Safety:
- Do not prompt for confirmation here; return structured results for caller to act upon.
"""

import hashlib
import os
import shutil
import json
from utils.logger import get_logger


class FileHelpers:
    def __init__(self):
        self.logger = get_logger(__name__)

    def iterate_files(self, root, follow_symlinks=False):
        """
        Recursively iterate files from root, optionally following symlinks.
        """
        for dirpath, dirnames, filenames in os.walk(root, followlinks=follow_symlinks):
            for filename in filenames:
                yield os.path.join(dirpath, filename)

    def folder_size(self, path, depth=None):
        """
        Calculate the total size of files under a path.
        If depth is provided (int), limit traversal depth relative to `path`.
        depth=0 means only direct files in `path`, depth=1 includes one level of subfolders, etc.
        """
        total_size = 0
        base_depth = path.rstrip(os.sep).count(os.sep)
        for dirpath, dirnames, filenames in os.walk(path):
            if depth is not None:
                current_depth = dirpath.rstrip(os.sep).count(os.sep) - base_depth
                if current_depth > depth:
                    # prune deeper traversal
                    dirnames[:] = []
                    continue
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(file_path)
                except Exception:
                    # Skip unreadable files
                    continue
        return total_size

    def file_hash(self, path, algorithm="sha256", chunk_size=65536):
        """
        Calculate the hash of a file.
        """
        hasher = hashlib.new(algorithm)
        with open(path, "rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                hasher.update(chunk)
        return hasher.hexdigest()

    def safe_copy(self, src, dst, overwrite=False):
        """
        Copy a file safely, optionally overwriting.
        """
        if not overwrite and os.path.exists(dst):
            return {"success": False, "message": "Destination exists"}
        os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
        shutil.copy2(src, dst)
        return {"success": True, "message": "File copied"}

    def safe_move(self, src, dst, overwrite=False):
        """
        Move a file safely, optionally overwriting.
        """
        if not overwrite and os.path.exists(dst):
            return {"success": False, "message": "Destination exists"}
        os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
        shutil.move(src, dst)
        return {"success": True, "message": "File moved"}

    def send_to_trash(self, path):
        """
        Send a file to the trash.
        """
        try:
            from send2trash import send2trash as _send2trash
        except Exception:
            return {"success": False, "message": "send2trash not available"}
        try:
            _send2trash(path)
            return {"success": True, "message": "File sent to trash"}
        except Exception as exc:
            return {"success": False, "message": f"send2trash failed: {exc}"}

    def atomic_write_json(self, path, data):
        """
        Write JSON data atomically to a file.
        """
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        temp_path = f"{path}.tmp"
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        os.replace(temp_path, path)
        return {"success": True, "message": "JSON written"}
