"""i3 backend — abstraction over i3ipc / i3-msg subprocess."""

import json
import subprocess

try:
    import i3ipc
    _HAS_I3IPC = True
except ImportError:
    _HAS_I3IPC = False


class I3Backend:
    def __init__(self):
        self._conn = i3ipc.Connection() if _HAS_I3IPC else None

    def get_workspaces(self):
        """Return list of dicts with keys: name, focused, num, output."""
        if self._conn:
            return [
                {"name": ws.name, "focused": ws.focused, "num": ws.num, "output": ws.output}
                for ws in self._conn.get_workspaces()
            ]
        raw = subprocess.check_output(["i3-msg", "-t", "get_workspaces"], text=True)
        return [
            {"name": ws["name"], "focused": ws["focused"], "num": ws["num"], "output": ws["output"]}
            for ws in json.loads(raw)
        ]

    def command(self, cmd):
        """Run an i3 command string."""
        if self._conn:
            return self._conn.command(cmd)
        subprocess.check_call(["i3-msg", cmd])

    def switch_workspace(self, name):
        self.command(f"workspace {name}")

    def move_to_workspace(self, name):
        self.command(f"move container to workspace {name}")
