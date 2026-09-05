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
    # hello_imgui and its backends are C++: they write errors to the OS-level stdout/stderr file
    # descriptors, not Python's sys.stderr, so their messages never reached this log (which is why a
    # failing DirectX11 window setup looked completely silent). Point fd 1/2 at the log too, so native
    # errors are captured.
    try:
        _fd = _log.fileno()
        os.dup2(_fd, 1)
        os.dup2(_fd, 2)
    except (OSError, ValueError):
        pass
    # Catch hard native crashes (access violations in C++ backends like DirectX11) and dump the Python
    # stack at the fault point into the log — otherwise such crashes are completely silent.
    try:
        import faulthandler

        faulthandler.enable(file=_log)
    except Exception:
        pass

# The "compat" build ships this marker plus Mesa's opengl32.dll next to the exe. Force the softpipe
# gallium driver: pure C, NO LLVM JIT, so it renders on the CPU even in a GPU-less VM (UTM/QEMU on a
# Mac, Windows-on-ARM x64 emulation) where llvmpipe's JIT would crash. Harmless in the normal build
# (no marker -> not set, so the system/GPU OpenGL driver is used).
if getattr(sys, "frozen", False):
    _here = os.path.dirname(sys.executable)
    # Mesa software-OpenGL compat build (bundled opengl32.dll next to the exe). Pick the gallium driver
    # by architecture: on native ARM64, llvmpipe's LLVM JIT emits native ARM64 code and is fast; on x64
    # it stays softpipe (pure C) because x64 llvmpipe crashes under ARM64 emulation. Override via
    # GALLIUM_DRIVER. Harmless in the normal build (no marker -> not set, system/GPU OpenGL is used).
    if os.path.exists(os.path.join(_here, "software_gl.marker")):
        import platform

        _driver = "llvmpipe" if platform.machine() == "ARM64" else "softpipe"
        os.environ.setdefault("GALLIUM_DRIVER", _driver)
        os.environ.setdefault("MESA_GL_VERSION_OVERRIDE", "3.3")
        # Tell the app it is running on a CPU rasterizer so it can throttle the frame rate (main.py).
        os.environ.setdefault("XKNX_SOFTWARE_GL", "1")

from editor_gui.main import main

if __name__ == "__main__":
    main()
