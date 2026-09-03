from enum import Enum


class TelegramSource(Enum):
    CONNECTION = "connection"
    PROXY = "proxy"
    VIRTUAL = "virtual"
