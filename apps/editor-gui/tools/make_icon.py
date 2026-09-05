"""Regenerate the committed app icons — run MANUALLY, never during the build.

The build ships pre-made icons as-is (no image processing in CI):
  - src/editor_gui/assets/app_settings/icon.png  (512 px window icon)
  - icon.ico                                     (Windows .exe icon, multi-size)
  - icon.icns                                    (macOS .app icon, multi-size; regenerated on macOS only)

Re-run after changing the design (needs Pillow, and iconutil for the .icns on macOS):

    uv run --with pillow python apps/editor-gui/tools/make_icon.py

The wordmark "XKNX" is drawn with a real bold font at 32 px and up; the 16/24 px mini sizes fall back
to a single "X" because four letters are an unreadable smear that small.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BG = (17, 17, 17, 255)  # near-black rounded square
FG = (255, 255, 255, 255)  # white wordmark

# Bold, geometric sans fonts to try in order (first that exists wins).
_FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/System/Library/Fonts/Helvetica.ttc",
    "/Library/Fonts/Arial Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]


def _font_path() -> str:
    for f in _FONT_CANDIDATES:
        if Path(f).exists():
            return f
    raise SystemExit(
        "no bold TTF found; edit _FONT_CANDIDATES in tools/make_icon.py for your OS"
    )


def build(size: int) -> Image.Image:
    """Render the icon at `size` px as an RGBA image (rounded square + centered wordmark)."""
    text = "X" if size <= 24 else "XKNX"
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=int(size * 0.22), fill=BG)

    # Fit the font so the text spans ~84% (wordmark) / ~64% (single X) of the width.
    target = size * (0.64 if text == "X" else 0.84)
    fp = _font_path()
    fs = size
    for _ in range(40):
        if d.textlength(text, font=ImageFont.truetype(fp, fs)) <= target or fs <= 4:
            break
        fs = max(
            4, int(fs * target / d.textlength(text, font=ImageFont.truetype(fp, fs)))
        )
    font = ImageFont.truetype(fp, fs)
    bb = d.textbbox((0, 0), text, font=font)
    x = (size - (bb[2] - bb[0])) / 2 - bb[0]
    y = (size - (bb[3] - bb[1])) / 2 - bb[1]
    d.text((x, y), text, font=font, fill=FG)
    return im


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    png_path = root / "src" / "editor_gui" / "assets" / "app_settings" / "icon.png"
    png_path.parent.mkdir(parents=True, exist_ok=True)
    build(512).save(png_path)
    print(f"wrote {png_path}")

    # Windows .ico with the sizes Explorer/taskbar actually use.
    ico_path = root / "icon.ico"
    ico_sizes = [16, 24, 32, 48, 64, 128, 256]
    build(256).save(
        ico_path,
        format="ICO",
        sizes=[(s, s) for s in ico_sizes],
        append_images=[build(s) for s in ico_sizes],
    )
    print(f"wrote {ico_path}")

    # macOS .icns via iconutil (macOS only). Mini slots (16 pt) keep the single "X".
    if sys.platform == "darwin":
        iconset = root / "icon.iconset"
        iconset.mkdir(exist_ok=True)
        for name, s in {
            "icon_16x16": 16,
            "icon_16x16@2x": 24,
            "icon_32x32": 32,
            "icon_32x32@2x": 64,
            "icon_128x128": 128,
            "icon_128x128@2x": 256,
            "icon_256x256": 256,
            "icon_256x256@2x": 512,
            "icon_512x512": 512,
            "icon_512x512@2x": 1024,
        }.items():
            build(s).save(iconset / f"{name}.png")
        subprocess.run(
            ["iconutil", "-c", "icns", str(iconset), "-o", str(root / "icon.icns")],
            check=True,
        )
        print(f"wrote {root / 'icon.icns'}")
    else:
        print("skipping icon.icns (run on macOS to regenerate it)")


if __name__ == "__main__":
    main()
