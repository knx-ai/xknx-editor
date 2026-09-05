"""A fake Programmer for testing the DALI protocol without a bus.

Reads: per property id, either a constant ``bytes`` (returned whole on each read) or a FIFO list of
chunks (popped per read — for poll sequences / chunked reads). Writes are recorded.
"""

from __future__ import annotations


class FakeProgrammer:
    def __init__(self) -> None:
        self.writes: list[dict[str, object]] = []
        self._reads: dict[int, bytes | list[bytes]] = {}

    def set_read(self, property_id: int, data: bytes) -> None:
        self._reads[property_id] = data

    def queue_read(self, property_id: int, *chunks: bytes) -> None:
        bucket = self._reads.setdefault(property_id, [])
        assert isinstance(bucket, list)
        bucket.extend(chunks)

    async def read_property(
        self,
        object_index: int,
        property_id: int,
        *,
        count: int = 1,
        start_index: int = 1,
    ) -> bytes:
        r = self._reads.get(property_id)
        if isinstance(r, list):
            return r.pop(0) if r else b""
        if isinstance(r, (bytes, bytearray)):
            return bytes(r)
        return b""

    async def write_property(
        self,
        object_index: int,
        property_id: int,
        data: bytes,
        *,
        count: int = 1,
        start_index: int = 1,
    ) -> bytes:
        self.writes.append(
            {
                "object_index": object_index,
                "property_id": property_id,
                "data": bytes(data),
                "count": count,
                "start_index": start_index,
            }
        )
        return bytes(data)

    def writes_for(self, property_id: int) -> list[dict[str, object]]:
        return [w for w in self.writes if w["property_id"] == property_id]
