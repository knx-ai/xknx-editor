"""Frozen-app entry point (referenced by xknx-editor.spec).

PyInstaller analyses this module as the program's start script; it just launches the GUI.
"""

from editor_gui.main import main

if __name__ == "__main__":
    main()
