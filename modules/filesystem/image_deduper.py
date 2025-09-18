"""
Image Deduper feature (optional dependencies).

Purpose:
- Find visually duplicate images using perceptual hashing (PHash/AHash).

API:
- run(args: dict = None, ctx: dict = None) -> dict
    - args: {"path": str, "hash_method":"phash"|"ahash", "threshold": int, "dry_run": True}
    - return: {"success": True, "data": [{"group": [paths]}], "message": None}

Implementation notes:
- Try to import Pillow and imagehash; if not present, return a helpful error.
- Compute perceptual hashes and group by Hamming distance threshold.

Dependencies:
- Internal: utils.file_helpers, utils.logger
- External: Pillow, imagehash

Safety:
- Default to dry-run; do not delete/move images without confirmation.
"""
