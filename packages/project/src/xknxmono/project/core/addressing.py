"""Group-address representation: one 16-bit integer, three ways to render it.

A KNX group address is a single 16-bit value; the project's :class:`GroupAddressStyle` only decides
how that value is split into a string and how deep the named ``GroupRange`` tree is. The address int
is canonical and style-independent — formatting/parsing/ranging are pure functions of (value, style).
"""

from enum import StrEnum


class GroupAddressStyle(StrEnum):
    FREE = "Free"
    TWO_LEVEL = "TwoLevel"
    THREE_LEVEL = "ThreeLevel"


def format_ga(address: int, style: GroupAddressStyle) -> str:
    """Render a group-address value as a string in the given style."""
    if style is GroupAddressStyle.FREE:
        return str(address)
    if style is GroupAddressStyle.TWO_LEVEL:
        return f"{address >> 11}/{address & 0x7FF}"
    return f"{address >> 11}/{(address >> 8) & 0x7}/{address & 0xFF}"


def parse_ga(text: str, style: GroupAddressStyle) -> int:
    """Parse a group-address string in the given style back to its 16-bit value."""
    parts = [int(p) for p in text.split("/")]
    if style is GroupAddressStyle.FREE:
        return parts[0]
    if style is GroupAddressStyle.TWO_LEVEL:
        main, sub = parts
        return (main << 11) | sub
    main, middle, sub = parts
    return (main << 11) | (middle << 8) | sub


def format_ia(area: int, line: int, device: int) -> str:
    """Render an individual address from its topology parts as ``area.line.device`` (e.g. ``1.1.5``)."""
    return f"{area}.{line}.{device}"


def parse_ia(text: str) -> tuple[int, int, int]:
    """Parse an ``area.line.device`` individual-address string into its three numbers."""
    area, line, device = text.split(".")
    return int(area), int(line), int(device)


def ranges_for(address: int, style: GroupAddressStyle) -> list[tuple[int, int, str]]:
    """The named ``GroupRange`` chain (top → leaf) that should contain ``address`` in this style.

    Each entry is ``(range_start, range_end, name)``. ThreeLevel yields a main + middle range,
    TwoLevel a single main range, and Free a single catch-all range (so a group address always sits
    under a range). Address 0 is reserved, so the first range starts at 1 (matching ETS)."""
    main = address >> 11
    if style is GroupAddressStyle.FREE:
        return [(1, 0xFFFF, "Group addresses")]
    if style is GroupAddressStyle.TWO_LEVEL:
        main_base = main << 11
        return [(max(1, main_base), main_base + 0x7FF, f"Main group {main}")]
    middle = (address >> 8) & 0x7
    main_base = main << 11
    middle_base = main_base + (middle << 8)
    return [
        (max(1, main_base), main_base + 0x7FF, f"Main group {main}"),
        (max(1, middle_base), middle_base + 0xFF, f"Middle group {main}/{middle}"),
    ]
