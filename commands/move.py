"""Move subcommand — move focused container to a workspace."""

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
    return query.lower() in text.lower()


class MoveCommand(Command):
    name = "move"
    display_name = "Move to Workspace"
    description = "Move focused container to a workspace"

    def run_cli(self, args):
        if args:
            self.backend.move_to_workspace(" ".join(args))
        else:
            workspaces = self.backend.get_workspaces()
            names = sorted(ws["name"] for ws in workspaces)
            if not names:
                print("No workspaces found", file=sys.stderr)
                return
            try:
                result = subprocess.run(
                    ["fzf", "--prompt=move to: ", "--print-query"],
                    input="\n".join(names),
                    capture_output=True,
                    text=True,
                )
                lines = result.stdout.strip().splitlines()
                selected = lines[-1] if lines else ""
                if selected:
                    self.backend.move_to_workspace(selected)
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
                "description": f"Move focused container to {ws['name']}",
                "on_enter": ExtensionCustomAction({
                    "command": "move",
                    "action": "move",
                    "workspace": ws["name"],
                }),
            })

        # Offer to move to a new workspace if query doesn't match existing
        if query and not any(ws["name"] == query for ws in workspaces):
            results.insert(0, {
                "name": f"Move to new workspace: {query}",
                "description": "Create workspace and move container there",
                "on_enter": ExtensionCustomAction({
                    "command": "move",
                    "action": "move",
                    "workspace": query,
                }),
            })

        return results

    def execute_ulauncher(self, data, **kwargs):
        if data.get("action") == "move" and data.get("workspace"):
            self.backend.move_to_workspace(data["workspace"])
            return HideWindowAction()
        return None
