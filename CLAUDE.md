# ulauncher-i3

## Project Overview
CLI tool (`i3helper`) + ulauncher extension for controlling i3wm. CLI-first architecture — ulauncher wraps the same command layer as a GUI frontend.

## Architecture
- `i3_backend.py` — sole layer talking to i3 (i3ipc w/ subprocess fallback). All i3 interaction goes through here.
- `commands/` — subcommand modules. Each implements `Command` base class with `run_cli()`, `get_results()`, `execute_ulauncher()`.
- `commands/__init__.py` — registry mapping subcommand names to classes. Add new commands by importing and adding to `COMMANDS` dict.
- `i3helper` — CLI entry point (symlinked to `~/.local/bin/i3helper`)
- `main.py` — ulauncher entry point
- `manifest.json` + `versions.json` — ulauncher extension metadata

## Ulauncher UX
- Keyword is `i3`, name is "i3 Workspace Selector" — name must be descriptive for ulauncher's matching
- On activation: shows command menu (Workspace Selector, Move to Workspace)
- Selecting a command drills in via `SetUserQueryAction`, then shows results with fuzzy filtering
- Extension does its own fuzzy filtering (not relying on ulauncher's matching)

## Installed symlinks
- `~/.local/bin/i3helper` → `./i3helper`
- `~/.local/bin/i3-workspace` → `./scripts/i3-workspace` (original standalone script, may be deprecated)
- `~/.local/share/ulauncher/extensions/com.github.gns.ulauncher-i3` → this repo

## Plans
- Implementation plans live in `.claude/plans/`
- Use conventional commits
- GitHub remote: `git@github.com:gnsiva/ulauncher-i3.git`
