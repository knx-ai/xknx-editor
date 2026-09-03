from __future__ import annotations


class Allocator:
    """KNX address allocator: resolves an unresolved arg to a concrete address for a given repeat index."""

    __slots__ = ("id", "max_inclusive", "start")

    def __init__(self, id: str, start: int, max_inclusive: int) -> None:
        self.id = id
        self.start = start
        self.max_inclusive = max_inclusive

    def resolve(
        self, position: int, allocates: int, alignment: int, base: int
    ) -> tuple[int, int]:
        """Return (address, next_position). Raises OverflowError if the allocation exceeds max_inclusive."""
        aligned = position
        if alignment > 1 and aligned % alignment != 0:
            aligned += alignment - (aligned % alignment)
        if aligned + allocates - 1 > self.max_inclusive:
            raise OverflowError(
                f"allocator {self.id!r} overflow: end {aligned + allocates - 1} > max {self.max_inclusive}"
            )
        return aligned + base, aligned + allocates
