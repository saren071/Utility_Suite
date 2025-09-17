# modules/port_scanner/tool.py
"""
Network Port Scanner module (localhost).

Responsibilities:
- Scan local or specified IP for open ports.
- Map ports to owning processes.
- Optionally identify common services (HTTP, SSH, etc.).

Dependencies:
- Internal: `utils/formatting.py`.
- External: `psutil`, `socket`.

Notes:
- Must handle permissions for low ports (<1024).
- Avoid aggressive scanning; this is for localhost or small networks only.
"""
