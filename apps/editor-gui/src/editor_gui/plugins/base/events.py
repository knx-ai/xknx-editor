from collections import defaultdict
from collections.abc import Callable
from typing import Any


class EventBus:
    def __init__(self) -> None:
        self._typed_handlers: dict[type, list[Callable[[Any], None]]] = defaultdict(
            list
        )
        self._named_handlers: dict[str, list[Callable[..., Any]]] = defaultdict(list)

    def subscribe(
        self, event: type | str, handler: Callable[..., Any]
    ) -> Callable[[], None]:
        if isinstance(event, str):
            self._named_handlers[event].append(handler)
            return lambda: self._named_handlers[event].remove(handler)
        else:
            self._typed_handlers[event].append(handler)
            return lambda: self._typed_handlers[event].remove(handler)

    def unsubscribe(self, event_type: type, handler: Callable[[Any], None]) -> None:
        if event_type in self._typed_handlers:
            self._typed_handlers[event_type].remove(handler)

    def emit(self, event: object | str, *args: Any) -> None:
        if isinstance(event, str):
            for handler in self._named_handlers[event]:
                handler(*args)
        else:
            for handler in self._typed_handlers[type(event)]:
                handler(event)
