**---KEY---**
- [x] Complete
- [ ] Not Started
- [~] In Progress

## Project Bring-up Checklist (end-to-end)

### Core Utilities and Structure
- [x] Create `utils/logger.py` with console + rotating file handler
- [x] Create `utils/constants.py` centralizing paths
- [x] Create `utils/config_manager.py` with safe JSON and defaults (agent_config, modules, file_organizer)
- [x] Create `utils/file_helpers.py` for hashing, safe moves/copies, trash, atomic writes
- [x] Create `utils/formatting.py` with human_readable_size and table helpers
- [x] Ensure `logs/` and `config/` are created at startup

### Module System
- [x] Implement `utils/module_loader.py` to discover packages and load tool modules
- [x] Define package contract: `meta` and `run(feature_id, args, ctx)`
- [x] Persist discovery manifest to `config/modules.json`

### Filesystem Package (features)
- [x] `modules/filesystem/tool.py` with `meta` and dispatcher
- [x] `disk_space` — list top-N largest items with optional human-readable sizes
- [x] `duplicate_finder` — hash-based grouping with optional move/delete (dry-run default)
- [x] `file_organizer` — move by extension rules from `config/file_organizer.json`
- [x] `auto_renamer` — batch rename with collision handling (already present)
- [x] `file_integrity` — checksum manifest generate/verify
- [x] `image_deduper` — perceptual hashing via Pillow+imagehash (optional)
- [x] `disk_cleanup` — temp candidates and optional trash (dry-run default)

### CLI (main)
- [x] Initialize config/logs and logger
- [x] Discover packages and display menus with features
- [x] Prompt for JSON args and execute feature via `run()`
- [x] Pretty-print structured results
- [x] Graceful shutdown

### Agent & Service (stubs sufficient for MVP)
- [x] `utils/service_manager.py` lazy pywin32 detection, safe stubs
- [ ] Implement real Windows Service install/uninstall via pywin32
- [ ] Implement Scheduled Task create/delete via `schtasks.exe`

### UI Backend (FastAPI)
- [x] `ui/backend/server.py` FastAPI app with `/health`, `/packages`, `/run`
- [x] `ui/backend/requirements-ui.txt` with `fastapi`, `uvicorn`
- [ ] Add CORS config if serving frontend separately
- [ ] Packaging script to run backend with agent

### UI Frontend (React + Vite + TS)
- [x] `ui/frontend/package.json`, `tsconfig.json`, `vite.config.ts`
- [x] `ui/frontend/src/main.tsx`, `src/App.tsx`, `public/index.html`
- [ ] Add pages/components for richer UX (tables, filters, feature-specific forms)
- [ ] Build/publish pipeline for UI assets

### Testing
- [ ] Add pytest tests for `utils/file_helpers`
- [ ] Add tests for `modules/filesystem` features using temp dirs
- [ ] CI workflow (lint, type-check, tests) on Windows runner

### Packaging & Distribution
- [ ] PyInstaller spec for CLI and service runner
- [ ] Optional Chocolatey/winget package definitions

### Security & Safety
- [ ] Admin elevation checks before registry/service changes
- [ ] Optional IPC token for agent control
- [ ] Confirmations for destructive actions in UI/CLI

### Documentation
- [x] README reviewed and aligned
- [ ] Developer guide updates for adding new packages
- [ ] API docs for UI backend endpoints

### How to Run (local dev)
- [x] `pip install -r requirements.txt`
- [x] `python main.py` to launch CLI
- [x] Backend UI: `pip install -r ui/backend/requirements-ui.txt` then `uvicorn ui.backend.server:app --reload`
- [x] Frontend UI: `cd ui/frontend && npm install && npm run dev`










