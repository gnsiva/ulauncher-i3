"""Base command interface for i3helper."""

from abc import ABC, abstractmethod


class Command(ABC):
    """Base class for i3helper subcommands."""

    name: str  # subcommand name, e.g. "workspace"
    description: str  # short description for help text

    def __init__(self, backend):
        self.backend = backend

    @abstractmethod
    def run_cli(self, args):
        """Run from CLI. args is the list of arguments after the subcommand name."""
        ...

    @abstractmethod
    def get_results(self, query):
        """Return list of result dicts for ulauncher: [{name, description, icon, data}]."""
        ...

    @abstractmethod
    def execute(self, data):
        """Execute an action from ulauncher item selection. data is the dict from get_results."""
        ...
