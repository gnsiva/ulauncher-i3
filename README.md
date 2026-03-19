# ulauncher-i3

Ulauncher extension for controlling i3wm — switch between workspaces, create new ones, and more.

Also includes a standalone CLI tool (`i3helper`) for terminal-based workflows.

## Install

### Ulauncher Extension
1. Open Ulauncher Preferences
2. Go to **Extensions** → **Add extension**
3. Paste: `https://github.com/gnsiva/ulauncher-i3`

### CLI Tool
```bash
git clone https://github.com/gnsiva/ulauncher-i3.git
ln -s "$(pwd)/ulauncher-i3/i3helper" ~/.local/bin/i3helper
```

Requires `fzf` for the interactive picker. Optionally install `i3ipc` for faster i3 communication:
```bash
pip install i3ipc
```

## Usage

### Ulauncher
1. Open Ulauncher and type `i3`
2. Select **i3 Workspace Selector**
3. Your open workspaces are listed — type to fuzzy filter
4. Press Enter on a workspace to switch to it
5. Select **Create New Workspace** to create and switch to a new one

### CLI
```bash
# Interactive workspace picker (uses fzf)
i3helper workspace

# Switch to or create a workspace by name
i3helper workspace myproject
```

## Requirements
- i3wm
- Ulauncher v5+ (for the extension)
- `fzf` (CLI only)
- `i3ipc` (optional, falls back to `i3-msg`)
