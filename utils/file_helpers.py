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
import send2trash

def iterate_files(root, follow_symlinks=False):
    """
    Recursively iterate files from root, optionally following symlinks.
    """
    for dirpath, dirnames, filenames in os.walk(root, followlinks=follow_symlinks):
        for filename in filenames:
            yield os.path.join(dirpath, filename)


def folder_size(path, depth=None):
    """
    Calculate the total size of files under a path.
    """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if depth is not None and file_path.count(os.path.sep) > depth:
                continue
            total_size += os.path.getsize(file_path)
    return total_size

def file_hash(path, algorithm="sha256", chunk_size=65536):
    """
    Calculate the hash of a file.
    """
    hasher = hashlib.new(algorithm)
    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            hasher.update(chunk)
    return hasher.hexdigest()

def safe_copy(src, dst, overwrite=False):
    """
    Copy a file safely, optionally overwriting.
    """
    if not overwrite and os.path.exists(dst):
        return {"success": False, "message": "Destination exists"}
    shutil.copy2(src, dst)
    return {"success": True, "message": "File copied"}

def safe_move(src, dst, overwrite=False):
    """
    Move a file safely, optionally overwriting.
    """
    if not overwrite and os.path.exists(dst):
        return {"success": False, "message": "Destination exists"}
    shutil.move(src, dst)
    return {"success": True, "message": "File moved"}

def send_to_trash(path):
    """
    Send a file to the trash.
    """
    if not hasattr(send2trash, "send2trash"):
        return {"success": False, "message": "send2trash not available"}
    send2trash.send2trash(path)
    return {"success": True, "message": "File sent to trash"}

def atomic_write_json(path, data):
    """
    Write JSON data atomically to a file.
    """
    temp_path = f"{path}.tmp"
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.replace(temp_path, path)
    return {"success": True, "message": "JSON written"}
