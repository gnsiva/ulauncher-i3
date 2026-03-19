"""Workspace subcommand — list, switch, create i3 workspaces."""

import subprocess
import sys

from commands.base import Command

try:
    from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
    from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
    _HAS_ULAUNCHER = True
except ImportError:
    _HAS_ULAUNCHER = False


def _fuzzy_match(query, text):
    """Simple case-insensitive substring match."""
    return query.lower() in text.lower()


class WorkspaceCommand(Command):
    name = "workspace"
    display_name = "Workspace Selector"
    description = "Switch to or create an i3 workspace"

    def run_cli(self, args):
        if args:
            self.backend.switch_workspace(" ".join(args))
        else:
            workspaces = self.backend.get_workspaces()
            names = sorted(ws["name"] for ws in workspaces)
            if not names:
                print("No workspaces found", file=sys.stderr)
                return
            try:
                result = subprocess.run(
                    ["fzf", "--prompt=workspace: ", "--print-query"],
                    input="\n".join(names),
                    capture_output=True,
                    text=True,
                )
                lines = result.stdout.strip().splitlines()
                selected = lines[-1] if lines else ""
                if selected:
                    self.backend.switch_workspace(selected)
            except FileNotFoundError:
                print("fzf not found, listing workspaces:", file=sys.stderr)
                for name in names:
                    print(name)

    def get_results(self, query):
        workspaces = self.backend.get_workspaces()
        query = query.strip()
        results = []

        for ws in sorted(workspaces, key=lambda w: w["name"]):
            if query and not _fuzzy_match(query, ws["name"]):
                continue
            prefix = "→ " if ws["focused"] else ""
            results.append({
                "name": f"{prefix}{ws['name']}",
                "description": f"Output: {ws['output']}",
                "on_enter": ExtensionCustomAction({
                    "command": "workspace",
                    "action": "switch",
                    "workspace": ws["name"],
                }),
            })

        # Always show "Create New Workspace" at the bottom
        results.append({
            "name": "Create New Workspace",
            "description": f'Create and switch to "{query}"' if query else "Type a name for the new workspace",
            "on_enter": ExtensionCustomAction({
                "command": "workspace",
                "action": "create",
                "workspace": query,
            }) if query else ExtensionCustomAction({
                "command": "workspace",
                "action": "create_prompt",
            }),
        })

        return results

    def execute_ulauncher(self, data, **kwargs):
        action = data.get("action")
        if action == "switch":
            self.backend.switch_workspace(data["workspace"])
            return HideWindowAction()
        if action == "create" and data.get("workspace"):
            self.backend.switch_workspace(data["workspace"])
            return HideWindowAction()
        # create_prompt or create with no name — keep ulauncher open, user needs to type more
        return None
