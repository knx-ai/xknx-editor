#!/usr/bin/env bash
# Build the XKNX Editor as a standalone desktop app with PyInstaller.
#
#   apps/editor-gui/tools/build_desktop.sh
#
# Output: apps/editor-gui/dist/  ("XKNX Editor.app" on macOS, a folder elsewhere).
# PyInstaller is pulled in ephemerally (uv --with), so it is not a project dependency.
set -euo pipefail

cd "$(dirname "$0")/.."  # -> apps/editor-gui

# 1) Refresh the app icon (assets/app_settings/icon.png).
uv run --package xknxeditor-gui python tools/make_icon.py

# 2) Freeze the app from the spec.
uv run --package xknxeditor-gui --with pyinstaller \
    pyinstaller --noconfirm --clean xknx-editor.spec

echo
echo "Done. Result in: $(pwd)/dist/"
echo "Note: for a custom executable/dock icon, generate a .icns (macOS) / .ico (Windows)"
echo "from src/editor_gui/assets/app_settings/icon.png and set 'icon=' in xknx-editor.spec."
