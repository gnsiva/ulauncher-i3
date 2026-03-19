"""Ulauncher extension entry point for i3helper."""

import os
import sys

# Ensure repo root is on path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.SetUserQueryAction import SetUserQueryAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

from i3_backend import I3Backend
from commands import get_command, all_command_names

ICON_PATH = os.path.join(os.path.dirname(__file__), "images", "icon.png")


def _keyword(event):
    """Get the keyword that triggered this event."""
    return event.get_keyword()


class I3HelperExtension(Extension):
    def __init__(self):
        super().__init__()
        self.backend = I3Backend()
        self.subscribe(KeywordQueryEvent, QueryListener())
        self.subscribe(ItemEnterEvent, EnterListener())


class QueryListener(EventListener):
    def on_event(self, event, extension):
        keyword = _keyword(event)
        raw_arg = event.get_argument() or ""
        query = raw_arg.strip()
        parts = query.split(maxsplit=1)
        subcmd_name = parts[0] if parts else ""
        subcmd_query = parts[1] if len(parts) > 1 else ""

        cmd = get_command(subcmd_name, extension.backend)

        # Subcommand matched and user has typed past it (space after subcommand)
        if cmd and (len(parts) > 1 or raw_arg.endswith(" ")):
            results = cmd.get_results(subcmd_query)
            return RenderResultListAction([
                ExtensionResultItem(
                    icon=ICON_PATH,
                    name=r["name"],
                    description=r.get("description", ""),
                    on_enter=r["on_enter"]
                )
                for r in results
            ])

        # Top level — show available commands, fuzzy filtered by what's typed
        items = []
        for name in all_command_names():
            c = get_command(name, extension.backend)
            display = c.display_name
            if query and query.lower() not in display.lower():
                continue
            items.append(ExtensionResultItem(
                icon=ICON_PATH,
                name=display,
                description=c.description,
                on_enter=SetUserQueryAction(f"{keyword} {name} ")
            ))
        return RenderResultListAction(items)


class EnterListener(EventListener):
    def on_event(self, event, extension):
        data = event.get_data()
        subcmd_name = data.pop("command", None)
        cmd = get_command(subcmd_name, extension.backend)
        if cmd:
            return cmd.execute_ulauncher(data, _keyword=event)
        return HideWindowAction()


if __name__ == "__main__":
    I3HelperExtension().run()
