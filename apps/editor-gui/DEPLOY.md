# Desktop deployment

Package the XKNX Editor into a standalone desktop app (no Python install needed for users),
using [PyInstaller](https://pyinstaller.org/). Based on the imgui_bundle desktop-deploy guide.

## Build

```bash
apps/editor-gui/tools/build_desktop.sh
```

This regenerates the app icon and runs PyInstaller from [`xknx-editor.spec`](xknx-editor.spec).
Output lands in `apps/editor-gui/dist/` — `XKNX Editor.app` on macOS, an `XKNX Editor/` folder
(with the executable + dependencies) on Windows/Linux. PyInstaller is fetched ephemerally via
`uv --with`, so it is not added to the project dependencies.

## What the spec bundles

- **imgui_bundle** — native libraries + its bundled fonts (via `collect_all`).
- **fastmcp / xknx / xknxproject** — data files + submodules.
- **xknxeditor / editor_gui** — our packages: dynamic imports (parser_v2, model adapters, plugins)
  plus data (generated model bindings, i18n `.mo` locales, the app icon + fonts under `assets/`).

## Icons

- **Window icon** (Windows/Linux, and the in-app icon): `src/editor_gui/assets/app_settings/icon.png`
  (512×512), loaded via `hello_imgui.set_assets_folder(...)` in `main.py`.
- **Executable / dock icon**: PyInstaller needs a platform icon — `.icns` on macOS, `.ico` on
  Windows. Generate one from the PNG and set `icon=` in `xknx-editor.spec`. On macOS:

  ```bash
  cd apps/editor-gui/src/editor_gui/assets/app_settings
  mkdir icon.iconset
  for s in 16 32 128 256 512; do
    sips -z $s $s icon.png --out icon.iconset/icon_${s}x${s}.png >/dev/null
    sips -z $((s*2)) $((s*2)) icon.png --out icon.iconset/icon_${s}x${s}@2x.png >/dev/null
  done
  iconutil -c icns icon.iconset -o icon.icns && rm -r icon.iconset
  ```

## Note

Packaging imgui_bundle apps is known to work but is **unofficial**. If the frozen app fails with
`ModuleNotFoundError` at startup, add the missing module to `hiddenimports` in the spec (a common
need for dynamically imported plugins/backends). Run the built app from a terminal once to see any
such errors.
