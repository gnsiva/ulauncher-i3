# i3helper — CLI + Ulauncher Extension

## Goal
CLI tool (`i3helper`) and ulauncher extension for i3wm control. CLI is the core; ulauncher wraps it as a GUI frontend.

## Architecture
```
i3helper <subcommand> [args]       # CLI usage
i3helper workspace                 # fzf picker (CLI) / list all (ulauncher)
i3helper workspace <name>          # switch/create workspace
i3helper move <workspace>          # future
i3helper layout <mode>             # future
```

Both CLI and ulauncher share the same command layer — ulauncher just provides results instead of using fzf.

## Directory Structure
```
ulauncher-i3/
├── manifest.json              # ulauncher extension metadata
├── main.py                    # ulauncher entry point, routes to commands
├── i3helper                   # CLI entry point (symlinked to ~/.local/bin)
├── i3_backend.py              # i3 interaction (i3ipc w/ subprocess fallback)
├── commands/
│   ├── __init__.py            # command registry
│   ├── base.py                # base command interface
│   └── workspace.py           # workspace subcommand
├── images/
│   └── icon.png
├── scripts/
│   └── i3-workspace           # original standalone script (kept for now)
└── .claude/plans/
```

## Implementation Steps

### Phase 1: CLI core
- [x] `i3_backend.py` — wrapper around i3ipc/i3-msg for querying workspaces and running commands
- [x] `commands/base.py` — base command interface: `name`, `run_cli(args)`, `get_results(query)`, `execute(data)`
- [x] `commands/workspace.py`:
  - `i3helper workspace` → fzf picker over current workspaces
  - `i3helper workspace <name>` → switch/create
- [x] `commands/__init__.py` — registry, maps subcommand names to command classes
- [x] `i3helper` CLI entry point — sys.argv, dispatches to command registry
- [x] Symlink `i3helper` to `~/.local/bin/`

### Phase 2: Ulauncher extension
- [x] `manifest.json` — keyword `i3`, preferences
- [x] `main.py` — on KeywordQueryEvent, parse input as `<subcommand> [args]`, call command's `get_results(query)` to build result items; on ItemEnterEvent, call `execute(data)`
- [x] Workspace command returns result items for ulauncher (no fzf, ulauncher does the filtering)

### Phase 3: Polish
- [ ] Icon
- [ ] README with install instructions for both CLI and ulauncher
- [ ] Deprecate/remove `scripts/i3-workspace` once `i3helper workspace` covers it

## Future subcommands (not in scope yet)
- `i3helper move <workspace>` — move focused container
- `i3helper layout <tabbed|split|stacking>` — change layout
- `i3helper scratch` — toggle scratchpad
- `i3helper float` — toggle floating
- `i3helper kill` — close focused window
- `i3helper rename <name>` — rename current workspace

## Dependencies
- `i3ipc` (optional, recommended) — `pip install i3ipc`
- `fzf` (CLI only, for interactive picking)
- ulauncher v5+ (extension only)

## Notes
- Commands are CLI-first, independently usable without ulauncher
- Each command implements both CLI (fzf/stdout) and ulauncher (result items) interfaces
- `i3_backend.py` is the only layer that talks to i3
