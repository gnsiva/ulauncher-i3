"""Workspace subcommand — list, switch, create i3 workspaces."""

import subprocess
import sys

from commands.base import Command


class WorkspaceCommand(Command):
    name = "workspace"
    description = "Switch to or create an i3 workspace"

    def run_cli(self, args):
        if args:
            # Direct switch/create
            self.backend.switch_workspace(" ".join(args))
        else:
            # fzf picker
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
        results = []
        for ws in sorted(workspaces, key=lambda w: w["name"]):
            prefix = "→ " if ws["focused"] else ""
            results.append({
                "name": f"{prefix}{ws['name']}",
                "description": f"Output: {ws['output']}",
                "data": {"action": "switch", "workspace": ws["name"]},
            })
        # If query doesn't match any existing workspace, offer to create it
        if query and not any(ws["name"] == query for ws in workspaces):
            results.insert(0, {
                "name": f"Create workspace: {query}",
                "description": "Switch to new workspace",
                "data": {"action": "switch", "workspace": query},
            })
        return results

    def execute(self, data):
        self.backend.switch_workspace(data["workspace"])
