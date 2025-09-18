"""
Image Deduper feature (optional dependencies).

Purpose:
- Find visually duplicate images using perceptual hashing (PHash/AHash).

API:
- run(args: dict = None, ctx: dict = None) -> dict
    - args: {"path": str, "hash_method":"phash"|"ahash", "threshold": int, "dry_run": True}
    - return: {"success": True, "data": [{"group": [paths]}], "message": None}

Dependencies:
- Internal: utils.file_helpers, utils.logger
- External: Pillow, imagehash

Safety:
- Default to dry-run; do not delete/move images without confirmation.
"""

import os
from typing import Any
from utils.logger import get_logger
from utils.file_helpers import FileHelpers


def run(args: dict | None = None, ctx: dict | None = None) -> dict:
    logger = get_logger(__name__)
    helpers = FileHelpers()

    args = args or {}
    path = args.get("path")
    method = args.get("hash_method", "phash")
    threshold = int(args.get("threshold", 5))

    if not path or not os.path.isdir(path):
        return {"success": False, "data": None, "message": f"Invalid directory: {path}"}

    try:
        from PIL import Image  # type: ignore
        import imagehash  # type: ignore
    except Exception:
        return {"success": False, "data": None, "message": "Pillow and imagehash are required for image_deduper"}

    def compute_hash(file_path: str):
        try:
            with Image.open(file_path) as img:
                if method == "ahash":
                    return imagehash.average_hash(img)
                else:
                    return imagehash.phash(img)
        except Exception:
            logger.exception(f"Hashing failed for {file_path}")
            return None

    # Collect images
    exts = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}
    img_files = [p for p in helpers.iterate_files(path) if os.path.splitext(p)[1].lower() in exts]

    hashes: list[tuple[str, Any]] = []
    for p in img_files:
        h = compute_hash(p)
        if h is not None:
            hashes.append((p, h))

    # Group by near-duplicates using threshold on Hamming distance
    groups: list[list[str]] = []
    used = set()
    for i in range(len(hashes)):
        if i in used:
            continue
        base_path, base_hash = hashes[i]
        group = [base_path]
        used.add(i)
        for j in range(i + 1, len(hashes)):
            if j in used:
                continue
            other_path, other_hash = hashes[j]
            try:
                dist = base_hash - other_hash  # imagehash defines distance via subtraction
            except Exception:
                dist = 999
            if dist <= threshold:
                group.append(other_path)
                used.add(j)
        if len(group) > 1:
            groups.append(group)

    return {"success": True, "data": [{"group": g} for g in groups], "message": None}
