"""Frozen-app entry point (referenced by xknx-editor.spec).

PyInstaller analyses this module as the program's start script; it just launches the GUI.
"""

import os
import sys

# A frozen windowed app (PyInstaller console=False) has no console, so sys.stdout/sys.stderr are
# None. Any print() or library that writes to them (e.g. structlog's PrintLogger) then crashes at
# startup. Redirect both to a log file before anything else runs; it also aids diagnosing the build.
if sys.stdout is None or sys.stderr is None:
    import tempfile

    _log = open(  # noqa: SIM115 - kept open for the process lifetime by design
        os.path.join(tempfile.gettempdir(), "xknx-editor.log"),
        "a",
        encoding="utf-8",
        buffering=1,
    )
    if sys.stdout is None:
        sys.stdout = _log
    if sys.stderr is None:
        sys.stderr = _log

# The "software-OpenGL" build ships a Mesa llvmpipe opengl32.dll next to the exe plus this marker
# file; force Mesa onto its CPU llvmpipe driver so the app renders in VMs (UTM/QEMU) and hosts with
# no GPU/OpenGL driver. Harmless in the normal build (no marker -> not set).
if getattr(sys, "frozen", False):
    _marker = os.path.join(os.path.dirname(sys.executable), "software_gl.marker")
    if os.path.exists(_marker):
        os.environ.setdefault("GALLIUM_DRIVER", "llvmpipe")

from editor_gui.main import main

if __name__ == "__main__":
    main()
