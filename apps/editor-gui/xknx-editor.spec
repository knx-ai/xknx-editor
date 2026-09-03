# PyInstaller spec for XKNX Editor — build with:  tools/build_desktop.sh
#
# Packages the GUI into a standalone desktop app. imgui_bundle (native libs + fonts),
# fastmcp, xknx, xknxproject and our own xknxmono/editor_gui packages carry data files and
# do dynamic imports, so we collect them explicitly. Packaging imgui_bundle apps is known to
# work but is unofficial — expect to add hidden imports here if the frozen app misses a module.
# ruff: noqa
# type: ignore
import os
import sys

from PyInstaller.utils.hooks import collect_all, collect_data_files, collect_submodules

# Per-OS executable icon: macOS wants .icns (committed), Windows wants .ico (optional — build
# succeeds without it), Linux embeds none. Keeps the cross-platform release build from failing.
if sys.platform == "darwin":
    _icon = "icon.icns"
elif sys.platform == "win32":
    _icon = "icon.ico" if os.path.exists("icon.ico") else None
else:
    _icon = None

_datas = []
_binaries = []
_hiddenimports = []

# Third-party packages that ship native libraries and/or data (fonts, schemas, templates).
for _pkg in ("imgui_bundle", "fastmcp", "xknx", "xknxproject"):
    d, b, h = collect_all(_pkg)
    _datas += d
    _binaries += b
    _hiddenimports += h

# Our own namespace packages: dynamic imports (parser_v2, model adapters, plugins) + data
# (KNX XML schemas, i18n .mo locales, the app icon + fonts).
for _pkg in ("xknxmono", "editor_gui"):
    _hiddenimports += collect_submodules(_pkg)
    _datas += collect_data_files(_pkg, include_py_files=False)

# Trim collected data we never ship: imgui_bundle's demo playground + its assets (the app has its
# own fonts/icon), and .pyi type stubs (dev-only, not used at runtime). Saves ~6-7 MB.
_SKIP_DIRS = ("imgui_bundle/demos_python", "imgui_bundle/demos_assets")


def _keep(dst):
    norm = dst.replace("\\", "/")
    return not dst.endswith(".pyi") and not any(p in norm for p in _SKIP_DIRS)


# collect_all routes some of these (incl. .pyi stubs) into binaries, not datas — filter both.
_datas = [(src, dst) for (src, dst) in _datas if _keep(dst)]
_binaries = [(src, dst) for (src, dst) in _binaries if _keep(dst)]

block_cipher = None

a = Analysis(
    ["tools/desktop_entry.py"],
    pathex=[],
    binaries=_binaries,
    datas=_datas,
    hiddenimports=_hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=["pytest", "tkinter"],
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="XKNX Editor",
    strip=True,  # strip debug symbols from the bootloader/binaries (smaller, no functional change)
    upx=True,  # compresses the Windows build (.dll/.pyd); PyInstaller ignores UPX on macOS/Linux
    console=False,  # windowed app (no terminal)
    # Platform icon (macOS .icns / Windows .ico) — the XKNX logo. Regenerate the .icns with:
    #   sips -s format icns src/editor_gui/assets/app_settings/icon.png --out icon.icns
    icon=_icon,
)
# upx=True shrinks the Windows binaries; PyInstaller disables UPX on macOS/Linux automatically
# (compressed arm64 Mach-O libs fail to load / break code signing), so it is a no-op there.
coll = COLLECT(exe, a.binaries, a.datas, strip=True, upx=True, name="XKNX Editor")

# On macOS, wrap the result in a proper .app bundle (dock icon comes from the bundle icon).
app = BUNDLE(
    coll,
    name="XKNX Editor.app",
    icon="icon.icns",  # XKNX logo for the dock/Finder icon
    bundle_identifier="org.xknx.editor",
)
