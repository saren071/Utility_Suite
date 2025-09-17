# module_spec.md — Full Module & Feature Specification (Utility Suite)

> This specification defines the package and feature contract used by the Utility Suite's loader, CLI, agent, and UI. It documents metadata schema, argument schema, runtime context, capabilities, UI hints, security expectations, testing requirements, packaging guidance, and examples. Implementers must follow this to ensure package compatibility with the system.

---

## 1. Purpose & Scope

`module_spec.md` specifies:
- What constitutes a *package* (folder under `modules/`)
- Package-level metadata (`meta`) structure
- Feature-level contracts and argument schemas (so UI/CLI can auto-generate forms)
- The `run()` API, return shapes, error handling, streaming/progress patterns
- `ctx` runtime context that is injected by the caller (CLI/agent/UI)
- Security/capabilities flags, and how the UI/agent should behave for guarded operations
- Packaging, testing and distribution guidelines for third-party packages

This spec is intentionally detailed to allow the UI to auto-generate interfaces and to make package behavior predictable across CLI, agent, and GUI.

---

## 2. Package Layout

Minimum package folder layout (example):

    modules/
      your_package_id/
        __init__.py
        tool.py                 # required: package orchestrator & meta
        <feature1>.py          # required: feature file
        <feature2>.py
        assets/                 # optional: icons, preview images
          icon.svg
          preview.png
        docs/                   # optional: extended docs for package
          README.md
        tests/
          test_tool.py
          test_feature1.py
        meta.json               # optional: static metadata for discovery

Notes:
- `tool.py` must be present and export `meta` and `run()`.
- Feature files must provide `run()` and may optionally export feature-level `meta`.
- `meta.json` is optional; if present, module_loader can use it to discover packages without executing Python code.

---

## 3. Package-level `meta` Schema

`meta` is a Python dict (exported by `tool.py`) or a JSON object (meta.json) and must include:

- `id` (string): unique package id (lowercase, use hyphen or underscore as needed)
- `name` (string): human-friendly name
- `description` (string): short one-to-three sentence description
- `version` (string): semantic version (e.g., "0.1.0")
- `features` (list): list of feature descriptors (see below)
- Optional fields:
  - `author` (string)
  - `license` (string), e.g., "MIT"
  - `homepage` (string, URL)
  - `dependencies` (list of strings: optional runtime/optional deps)
  - `capabilities` (list: package-level capabilities like "needs_admin" or "modifies_files")

Each feature descriptor in `features` must have:

- `id` (string): feature identifier — must match the feature filename (without .py)
- `name` (string)
- `description` (string)
- `arg_schema` (object, optional): JSON Schema (subset) for feature arguments
- `capabilities` (list, optional): e.g., `["needs_admin","modifies_files"]`
- `ui` (object, optional): UI hints (icon path, form layout, widgets)

Example `meta` (Python-style):

    meta = {
      "id": "filesystem",
      "name": "Filesystem Tools",
      "description": "Disk and file utilities (disk space, duplicate finder, organizer).",
      "version": "0.2.0",
      "author": "YourName",
      "features": [
        {
          "id": "disk_space",
          "name": "Disk Space Visualizer",
          "description": "List largest files/folders under a path.",
          "arg_schema": {
            "type":"object",
            "properties": {
              "path": {"type":"string", "format":"path"},
              "top_n": {"type":"integer", "default":20},
              "depth": {"type":"integer", "default":1},
              "human_readable": {"type":"boolean", "default":true}
            },
            "required":["path"],
            "additionalProperties": false
          },
          "capabilities": ["read_only"]
        },
        {
          "id": "duplicate_finder",
          "name": "Duplicate Finder",
          "description": "Find duplicate files using content hashing.",
          "arg_schema": {
            "type":"object",
            "properties": {
              "path": {"type":"string", "format":"path"},
              "algorithm": {"type":"string", "enum":["md5","sha256"], "default":"sha256"},
              "min_size": {"type":"integer", "default":1024},
              "action": {"type":"string", "enum":["report","move_to_trash","delete"], "default":"report"},
              "dry_run": {"type":"boolean", "default":true}
            },
            "required":["path"],
            "additionalProperties": false
          },
          "capabilities": ["modifies_files"]
        }
      ],
      "dependencies": ["Pillow (optional)", "imagehash (optional)"]
    }

Guidelines:
- Keep `meta` minimal and static-friendly.
- Avoid heavy runtime imports in `tool.py` that would be required to build `meta`.

---

## 4. Feature Argument Schema (`arg_schema`)

Use a JSON Schema subset that supports:

Top-level:
- `type`: always `"object"` for arguments
- `properties`: mapping of arg name → schema
- `required`: list of required arg names
- `additionalProperties`: boolean, recommended `false`

Property schema keys supported:
- `type`: `"string" | "integer" | "number" | "boolean" | "array" | "object"`
- `title`, `description`: for human UI help
- `default`
- `enum`: list of allowed values
- `min`, `max`, `minLength`, `maxLength`
- `format`: recognized values include `"path"`, `"date"`, `"time"`, `"cron"`, `"duration"`, `"regex"`
- `items`: for arrays
- `ui`: optional object for UI hints (widget type, placeholder, order, group)

UI generation notes:
- `format: "path"` → UI renders a file/directory picker
- `enum` → select/dropdown
- `type: "boolean"` → toggle/checkbox
- `ui` may contain `widget` (e.g., `"directory_picker"`, `"password"`, `"cron_input"`), `order` (numeric), and `help_text`.

Example `arg_schema` for `duplicate_finder` (see meta example above).

---

## 5. Feature file contract (`run()`)

Each feature file (e.g., `duplicate_finder.py`) must implement:

    def run(args: dict = None, ctx: dict = None) -> dict:
        """
        Execute the feature.

        Args:
            args: arguments validated against `arg_schema`.
            ctx: runtime context dict (see Section 7).

        Returns:
            A dict with at least:
              - success: bool
              - data: arbitrary JSON-serializable payload
              - message: human-readable string or None
              - metadata: optional dict (timing, counts)
        """

Behavior & rules:
- Validate `args` against `arg_schema` (module_loader/UI may pre-validate; features should re-validate if critical).
- Do heavy imports inside `run()` (lazy import), not at module import time.
- Catch expected exceptions and return a structured failure dict:
      {"success": False, "message": "Permission denied", "data": {"error_type":"PermissionError"}}
- For unexpected exceptions, allow them to propagate so agent/loader can log and convert to error response.
- For long-running operations, return progress via the agent's progress API or provide streaming (task IDs with status).

---

## 6. Return value shape (standardized)

All feature `run()` implementations should return a dict with keys:

- `success`: boolean
- `data`: feature-specific JSON-serializable payload
- `message`: short human-readable text (nullable)
- `metadata`: optional dict for machine metadata (timing, files_processed, summary)
- `logs`: optional (list / incremental stream reference) for long-run tasks

Example successful return:

    {
      "success": True,
      "data": [ {"path":"C:\\bigfile.zip","size":12345678} ],
      "message": "Top 20 files listed",
      "metadata":{"duration_s": 1.23}
    }

Example failure return:

    {
      "success": False,
      "data": {"error":"PermissionError"},
      "message": "Permission denied writing to target directory",
      "metadata": null
    }

---

## 7. Runtime Context (`ctx`)

`ctx` is provided by the caller (main CLI, agent, or UI/backend) and includes:

- `ctx["logger"]`: a `logging.Logger` instance
- `ctx["format"]`: formatting helpers from `utils.formatting`
- `ctx["config_manager"]`: read/write JSON configs (safe atomic write helpers)
- `ctx["service_manager"]`: helpers for Windows service and scheduled task operations
- `ctx["constants"]`: project constants (paths)
- `ctx["agent"]`: if running in agent, a small API to report progress / register tasks
- `ctx["auth"]`: optional auth metadata for IPC context (token, user)

Feature implementations should:
- Use `ctx` if provided; otherwise, fallback to standard library operations.
- Not assume `ctx` contains functionality beyond the documented keys.

---

## 8. Capabilities & Security Flags

Capabilities are strings used to inform UI and agent about the feature's behavior & required privileges:

Common flags:
- `needs_admin` — action needs elevated privileges (UAC on Windows)
- `modifies_files` — will move/delete/modify files
- `network_access` — will make outbound/inbound network calls
- `long_running` — expected to take long time; UI shows progress controls
- `read_only` — feature is read-only
- `high_io` — may produce high disk/network I/O
- `requires_external_deps` — optional heavy deps (Pillow, NVML)

The UI/agent obeys these flags:
- `needs_admin`: UI prompts for elevation; agent will require running elevated or prompt user.
- `modifies_files`: UI shows explicit confirmation modal with preview.
- `long_running`: UI provides progress and cancel actions.

---

## 9. UI Hints & Auto-Generation

`ui` property (optional) in feature descriptor gives extra hints to UI for rendering:

- `icon`: path to asset (relative to package assets/)
- `preview`: preview image path
- `form_layout`: e.g., `{"columns":2}`
- `widgets`: mapping of field to widget override, e.g., `{"path":"directory_picker"}`
- `confirm_text`: custom confirmation dialog text

Example:

    "ui": {
      "icon":"assets/icon.svg",
      "preview":"assets/preview.png",
      "form_layout":{"columns":2},
      "widgets":{"path":"directory_picker"},
      "confirm_text":"This will move files — proceed?"
    }

The UI should:
- Use `arg_schema` to validate user input client-side.
- Generate form controls from `arg_schema` & `ui` hints.
- Re-validate on backend for security.

---

## 10. Lazy-import & side-effect rules

To keep discovery and startup fast and safe:

- **No side-effects at import time.**
  - Feature modules and `tool.py` must not:
    - start threads or timers
    - open network sockets
    - read significant disk state, or modify system state
- **Lazy imports**:
  - Heavy libraries (psutil, Pillow, NVML) must be imported inside `run()` or helper functions.

- **meta** should be static-friendly:
  - If `meta` computation requires heavy imports, provide a `meta.json` static file for discovery.

---

## 11. Admin / Privileged Actions

If a feature modifies registry, services, or system settings:
- Mark it with `needs_admin` in `capabilities`.
- UI should show explicit warnings and request elevation.
- Agent or install script handles privilege escalation; do not silently escalate.
- Provide backups/undo:
  - For registry edits, export key before change.
  - For file operations, provide `send2trash`/recycle option or manifest to undo moves.

---

## 12. Long-running tasks & progress reporting

Patterns:

- **Agent-managed tasks**: for heavy tasks, agent spawns subprocess and returns a task id. Agent streams progress via IPC (WebSocket).
- **In-process streaming**: for simple monitors, `run()` may return incremental results; caller should support streaming or short-run modes.
- **Abort/cancel**: features must support being asked to stop gracefully (agent context should provide a cancellation token in `ctx["agent"]` or similar).

Return progress example (agent):
- On start, return `{"success": True, "data":{"task_id":"abc123"}, "message":"Task started"}`
- Agent broadcasts progress events: `{ "task_id":"abc123", "progress": 40, "status":"scanning", "current":"C:\\..." }`
- On completion, agent sets final result and stores logs.

---

## 13. Logging

- Use `ctx["logger"]` for structured logging.
- Log levels: DEBUG, INFO, WARNING, ERROR.
- Keep verbose debug messages guarded behind log-level checks.
- Do not send logs externally by default.

---

## 14. Tests & CI

Package authors should include `tests/` with pytest-based unit tests:
- Use `tmp_path` fixtures for file operations.
- Mock system dependencies: psutil, GPUtil, winreg, subprocess.
- Do not require admin.
- CI pipeline should run tests on Windows runners for Windows-specific code.

Checklist before publishing:
- `meta` present and valid
- `tool.py` exports `meta` & `run()`
- All feature files export `run()`
- Tests present & pass
- Docs included (docs/README.md)
- Optional dependencies documented

---

## 15. Packaging & Distribution

Options:
- Distributable ZIP with package folder that users drop into `modules/`.
- Installer script that copies package folder into user's `modules/` dir.
- Pip package (if desired) that provides an installer to copy files to `modules/`.

Include:
- `meta.json` for discovery (optional but recommended)
- License (MIT recommended)
- README and changelog
- Tests & sample config

---

## 16. Example code skeletons (no triple-backticks; use indented blocks)

Package `tool.py` skeleton:

    meta = {
      "id":"example_pkg",
      "name":"Example Package",
      "description":"Example features",
      "version":"0.1.0",
      "features":[{"id":"do_thing","name":"Do Thing"}]
    }

    def run(feature_id, args=None, ctx=None):
        if feature_id == "do_thing":
            from . import do_thing
            return do_thing.run(args or {}, ctx or {})
        return {"success": False, "message": f"Unknown feature: {feature_id}"}

Feature file (`do_thing.py`) skeleton:

    def run(args=None, ctx=None):
        try:
            # lazy-import heavy libs if needed
            # perform work...
            return {"success": True, "data": {"result": 42}, "message": "Done"}
        except PermissionError:
            return {"success": False, "data": {"error":"PermissionError"}, "message":"Permission denied"}

Example `arg_schema` snippet:

    {
      "type":"object",
      "properties":{
        "path":{"type":"string","format":"path","title":"Directory"},
        "dry_run":{"type":"boolean","default":true}
      },
      "required":["path"],
      "additionalProperties": false
    }

---

## 17. UI mapping guidance (how to auto-generate forms)

- Map JSON Schema to form controls:
  - `string` + `format:path` → directory/file picker
  - `enum` → dropdown
  - `boolean` → toggle
  - `integer`/`number` → numeric input (min/max if provided)
  - `array` → multi-select or repeated entry inputs
- Use `ui` hints for custom widgets and layout.
- Validate on client and server.

---

## 18. Security checklist for package authors

- Avoid shelling out to execute raw user input.
- Validate file paths to avoid `..` traversal where not intended.
- For network features: set timeouts and limit retries.
- For admin features: backup and document changes; require explicit consent.

---

## 19. Release & versioning notes

- Follow semver: MAJOR.MINOR.PATCH.
- Breaking `meta` or `arg_schema` changes should bump MAJOR.
- Document migration steps for UI/agent when schema changes.

---

## 20. Publishing to plugin marketplace (future)

- Provide `meta.json` plus packaged folder.
- Include `assets/`, `docs/`, `tests/`.
- Provide an install script that verifies `meta`, copies files to `modules/`, and optionally registers package in manifest.

---

## 21. Troubleshooting & debugging

- For feature debug, support `--dry-run` and `--debug` flags in CLI.
- Provide verbose logs when `ctx["logger"].level` is DEBUG.
- Agent should support a `--mock` or `--dev` mode that uses mock services for UI dev.

---

## 22. Checklist before merge/publish

- [ ] meta exists and valid
- [ ] tool.py exports meta & run
- [ ] all features export run
- [ ] no heavy imports at module import time
- [ ] tests included and pass
- [ ] docs/README.md provided
- [ ] license included (MIT recommended)
- [ ] capabilities annotated correctly

---

## 23. Contact & Contribution

- For inclusion in the official repo or marketplace: open PR with package folder, pass CI, and include docs.
- For questions about module_spec extension or UI needs, submit an issue with use-case.

---

### End of module_spec.md
