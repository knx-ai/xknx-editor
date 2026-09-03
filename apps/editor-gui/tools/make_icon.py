"""Generate the app icon with pure stdlib (no Pillow).

Draws a white "XKNX" wordmark on a black rounded square and writes:
  - src/editor_gui/assets/app_settings/icon.png  (512px, runtime window icon)
  - icon.ico                                      (multi-size, Windows .exe icon; see the spec)

Re-run to regenerate:

    uv run --package editor-gui python apps/editor-gui/tools/make_icon.py
"""

from __future__ import annotations

import struct
import zlib
from pathlib import Path

SIZE = 512  # 512x512 recommended for a crisp app/window icon (hello_imgui / packaging)
_S = SIZE / 256.0  # design was authored on a 256 grid; scale all metrics by this
BG = (17, 17, 17, 255)  # near-black
FG = (255, 255, 255, 255)  # white


def _blank() -> list[list[tuple[int, int, int, int]]]:
    return [[BG for _ in range(SIZE)] for _ in range(SIZE)]


def _round_corners(px: list[list[tuple[int, int, int, int]]], radius: int) -> None:
    """Make the black square a rounded square by clearing the corners to transparent."""
    for cy, cx, sy, sx in (
        (radius, radius, -1, -1),
        (radius, SIZE - radius - 1, -1, 1),
        (SIZE - radius - 1, radius, 1, -1),
        (SIZE - radius - 1, SIZE - radius - 1, 1, 1),
    ):
        for y in range(radius):
            for x in range(radius):
                if x * x + y * y > radius * radius:
                    px[cy + sy * y][cx + sx * x] = (0, 0, 0, 0)


def _stroke(
    px: list[list[tuple[int, int, int, int]]],
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    half: int,
) -> None:
    """Draw a thick line from (x0,y0) to (x1,y1) by stamping a square brush along it."""
    steps = int(max(abs(x1 - x0), abs(y1 - y0)) * 2) + 1
    for i in range(steps + 1):
        t = i / steps
        cx = round(x0 + (x1 - x0) * t)
        cy = round(y0 + (y1 - y0) * t)
        for yy in range(cy - half, cy + half + 1):
            for xx in range(cx - half, cx + half + 1):
                if 0 <= xx < SIZE and 0 <= yy < SIZE:
                    px[yy][xx] = FG


def _draw_glyph(
    px: list[list[tuple[int, int, int, int]]], ch: str, left: float, half: int
) -> None:
    """Draw one letter of the wordmark in a fixed cell (top, bottom, width in px)."""
    top, bot, w = 96.0 * _S, 168.0 * _S, 40.0 * _S
    r = left + w
    if ch == "X":
        _stroke(px, left, top, r, bot, half)
        _stroke(px, r, top, left, bot, half)
    elif ch == "K":
        _stroke(px, left, top, left, bot, half)
        _stroke(px, r, top, left, (top + bot) / 2, half)
        _stroke(px, left, (top + bot) / 2, r, bot, half)
    elif ch == "N":
        _stroke(px, left, bot, left, top, half)
        _stroke(px, left, top, r, bot, half)
        _stroke(px, r, bot, r, top, half)


def build(size: int = 512) -> bytes:
    global SIZE, _S
    SIZE, _S = size, size / 256.0
    px = _blank()
    _round_corners(px, round(48 * _S))
    half = round(5 * _S)
    gap = 12.0 * _S
    w = 40.0 * _S
    total = 4 * w + 3 * gap
    x = (SIZE - total) / 2
    for ch in "XKNX":
        _draw_glyph(px, ch, x, half)
        x += w + gap
    # encode PNG (RGBA, 8-bit)
    raw = bytearray()
    for row in px:
        raw.append(0)  # filter type 0
        for r, g, b, a in row:
            raw += bytes((r, g, b, a))

    def chunk(tag: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + tag
            + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        )

    ihdr = struct.pack(">IIBBBBB", SIZE, SIZE, 8, 6, 0, 0, 0)
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
        + chunk(b"IEND", b"")
    )


def build_ico(sizes: tuple[int, ...] = (256, 48, 32, 16)) -> bytes:
    """Pack the rendered logo at several sizes into a Windows .ico (PNG-compressed entries).

    PNG-in-ICO is valid on Windows Vista+ and embedded as-is by PyInstaller's resource injector.
    ICONDIRENTRY encodes the size (0 == 256), so the icon loader doesn't parse the image header."""
    images = [(s, build(s)) for s in sizes]
    header = struct.pack(
        "<HHH", 0, 1, len(images)
    )  # reserved, type=1 (icon), image count
    entries, data = b"", b""
    offset = 6 + 16 * len(images)
    for s, png in images:
        dim = 0 if s >= 256 else s
        # bWidth, bHeight, bColorCount, bReserved, wPlanes, wBitCount, dwBytesInRes, dwImageOffset
        entries += struct.pack("<BBBBHHII", dim, dim, 0, 0, 1, 32, len(png), offset)
        data += png
        offset += len(png)
    return header + entries + data


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    png_path = root / "src" / "editor_gui" / "assets" / "app_settings" / "icon.png"
    png_path.parent.mkdir(parents=True, exist_ok=True)
    png_path.write_bytes(build(512))
    print(f"wrote {png_path} ({png_path.stat().st_size} bytes)")

    ico_path = (
        root / "icon.ico"
    )  # next to xknx-editor.spec (build CWD), used for the Windows .exe
    ico_path.write_bytes(build_ico())
    print(f"wrote {ico_path} ({ico_path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
