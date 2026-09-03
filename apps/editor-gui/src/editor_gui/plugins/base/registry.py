from collections.abc import Callable
from dataclasses import dataclass
from importlib.metadata import entry_points
from typing import ClassVar, Protocol

from editor_gui.plugins.base.api import PluginAPI


class Panel(Protocol):
    def render(self) -> None: ...


class Service(Protocol):
    def refresh(self) -> None: ...


@dataclass
class PanelDefinition:
    name: str
    label: str
    dock: str
    render: Callable[[], None]


class Plugin(Protocol):
    name: str

    @property
    def panels(self) -> list[PanelDefinition]: ...
    def on_load(self) -> None: ...
    def on_unload(self) -> None: ...


PluginFactory = Callable[[PluginAPI], Plugin]


class PluginRegistry:
    _factories: ClassVar[dict[str, PluginFactory]] = {}

    @classmethod
    def register(cls, name: str) -> Callable[[PluginFactory], PluginFactory]:
        def decorator(factory: PluginFactory) -> PluginFactory:
            cls._factories[name] = factory
            return factory

        return decorator

    @classmethod
    def get(cls, name: str) -> PluginFactory | None:
        return cls._factories.get(name)

    @classmethod
    def all(cls) -> dict[str, PluginFactory]:
        return cls._factories.copy()

    @classmethod
    def discover(cls) -> None:
        for ep in entry_points(group="editor_gui.plugins"):
            cls._factories[ep.name] = ep.load()
