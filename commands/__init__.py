"""Command registry for i3helper."""

from commands.workspace import WorkspaceCommand

COMMANDS = {
    WorkspaceCommand.name: WorkspaceCommand,
}


def get_command(name, backend):
    cls = COMMANDS.get(name)
    if cls:
        return cls(backend)
    return None


def all_command_names():
    return list(COMMANDS.keys())
