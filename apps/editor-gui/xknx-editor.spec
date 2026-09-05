# PyInstaller spec for XKNX Editor — build with:  tools/build_desktop.sh
#
# Packages the GUI into a standalone desktop app. imgui_bundle (native libs + fonts),
# fastmcp, xknx, xknxproject and our own xknxeditor/editor_gui packages carry data files and
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

# Third-party packages that ship native libraries and/or data (fonts, schemas, templates) or do
# dynamic imports PyInstaller's static analysis misses. `mcp` and `uvicorn` are collected in full
# because fastmcp's server (uvicorn's protocol/loop backends, mcp's submodules) imports parts of
# them by name at runtime. NOTE: the earlier "FastMCP server support is not installed" failure was a
# symptom of the Windows OpenSSL load failure (fastmcp's server import chain imports ssl), not of
# missing modules — it is fixed by shipping python.org's OpenSSL, not by over-collecting here.
for _pkg in ("imgui_bundle", "fastmcp", "mcp", "uvicorn", "xknx", "xknxproject"):
    d, b, h = collect_all(_pkg)
    _datas += d
    _binaries += b
    _hiddenimports += h

# Our own namespace packages: dynamic imports (parser_v2, model adapters, plugins) + data
# (KNX XML schemas, i18n .mo locales, the app icon + fonts).
for _pkg in ("xknxeditor", "editor_gui"):
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
# Drop ONLY the bundled ucrtbase.dll. A/B-confirmed on the target: when the bundled ucrtbase.dll is
# present the PyInstaller bootloader pre-loads it and then FAILS to load python313.dll ("Failed to
# load Python DLL … FormatMessageW failed"); when it is absent python313.dll loads fine against the
# system UCRT. Keep the api-ms-win-crt-*.dll forwarders — python313.dll/_ssl.pyd/libcrypto-3.dll
# import them by name and they just forward to whatever ucrtbase.dll is loaded (the system one).
# NOTE: this is unrelated to the separate libcrypto-3.dll problem — setup-python's OpenSSL fails to
# load on some machines and is replaced with python.org's official build in the desktop-build workflow
# (post-packaging overlay step), not here.
import os as _os

a.binaries = [
    b for b in a.binaries if _os.path.basename(b[0]).lower() != "ucrtbase.dll"
]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="XKNX-Editor",
    # strip is DISABLED: on Windows PyInstaller runs GNU `strip` (present via Git-for-Windows on the
    # runner) over the collected DLLs, which corrupts python3xx.dll -> "Failed to load Python DLL …
    # FormatMessageW failed". PyInstaller itself warns strip is unsafe on Windows.
    strip=False,
    upx=False,  # also disabled: UPX likewise corrupted the Windows python DLL / MSVC runtime.
    console=False,  # windowed app (no terminal)
    # Platform icon (macOS .icns / Windows .ico) — the XKNX logo. Regenerate the .icns with:
    #   sips -s format icns src/editor_gui/assets/app_settings/icon.png --out icon.icns
    icon=_icon,
)
# UPX disabled (see EXE above): it corrupted the bundled python3xx.dll / MSVC runtime on Windows,
# so the app failed to start. macOS/Linux ignored UPX anyway.
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=False, name="XKNX-Editor")

# On macOS, wrap the result in a proper .app bundle (dock icon comes from the bundle icon).
app = BUNDLE(
    coll,
    name="XKNX-Editor.app",
    icon="icon.icns",  # XKNX logo for the dock/Finder icon
    bundle_identifier="org.xknx.editor",
)
