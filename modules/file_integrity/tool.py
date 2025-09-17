# modules/file_integrity/tool.py
"""
File Integrity Checker module.

Responsibilities:
- Generate checksums (MD5, SHA1, SHA256) for specified files/folders.
- Save checksums to JSON for later verification.
- Verify files against saved checksums to detect corruption or tampering.

Dependencies:
- Internal: `utils/file_helpers.py` for hashing.
- External: `hashlib`, `json`, `os`.

Notes:
- CLI should display verification results clearly.
- Avoid modifying files during verification.
"""
