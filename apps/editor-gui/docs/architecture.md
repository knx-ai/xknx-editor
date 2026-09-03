# KNX GUI Architecture

## Overview

The application follows a template/instance pattern: immutable application templates come from the
catalog (`xknxmono.catalog`, backed by `xknxmono.product`), and are instantiated into configurable
devices inside a project (`xknxmono.project`). Both are standalone packages, not part of the GUI —
`apps/editor-gui` only holds thin adapters (`plugins/catalog/service.py`, `plugins/project/service.py`)
plus the GUI-only runtime view (`editor_gui.types.Device`).

## Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                          CATALOG                                  │
│  xknxmono.catalog — SQLite (default: config/catalog.xknxcatalog)            │
│                                                                    │
│  Hardware / HardwareProgram / Application rows, built by          │
│  importing .knxprod archives (xknxmono.product parses the XML).   │
│  Schema auto-created (SQLAlchemy metadata.create_all), no         │
│  migrations. Never modified except by import.                     │
│  See docs/catalog.md.                                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ CatalogService.get_application(application_id)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Application                               │
│  (xknxmono.product, IR-backed — xknxmono.models.intermediate)     │
│                                                                    │
│  Parsed once per application_id from the stored XML, then         │
│  cached by the GUI's ProjectService (`_app_cache`). Contains ALL   │
│  com objects and parameters plus the DynamicUI/dynamic tree that  │
│  computes visibility from current parameter values.                │
│  Immutable. Treated as the "blueprint" for devices.                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                          PROJECT                                  │
│  xknxmono.project — one SQLite document per project (.xknx file)  │
│  Event-sourced: every edit is an Event with apply()/revert(),     │
│  logged to an `events` table for undo/redo. Live state (devices,  │
│  parameters, com_objects, group_addresses, ...) IS the relational │
│  tables — there's no separate replay-on-load step.                │
│                                                                    │
│  Device row                                                       │
│    ├── id, segment_id, address (individual-address octet)         │
│    ├── product_ref_id (catalog product) + hardware2program_ref_id │
│    │   (catalog HardwareProgram — resolves the Application)       │
│    └── name                                                       │
│                                                                    │
│  Parameter / ComObject rows (children of Device)                  │
│    ├── ref_id (into the application's parameter/com-object refs)  │
│    └── value / flag_* (overrides only — None means "inherit")     │
│                                                                    │
│  See docs/project.md.                                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ ProjectService (plugins/project/service.py) — GUI facade
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DEVICE (runtime)                             │
│  editor_gui.types.Device                                             │
│                                                                    │
│  Device                                                            │
│    ├── node_id: int (= project Device.id)                          │
│    ├── name, individual_address: str                              │
│    ├── app: Application (immutable reference, resolved via catalog)│
│    ├── parameter_instance_refs / module_instances /                │
│    │   com_object_instance_refs (the raw overrides, IR dataclasses)│
│    └── com_objects: list[ComObject] (materialized from app +       │
│        overrides in __post_init__, via DynamicUI)                  │
│                                                                    │
│  Visibility is computed on demand from the DynamicUI tree, not     │
│  cached at the Device level (the com_objects list itself is        │
│  already the "visible-if-computed" set for the current params).    │
└─────────────────────────────────────────────────────────────────┘
```

## Key Principles

1. **Catalog is immutable**: raw application XML from imported `.knxprod` files is stored as-is and
   only ever read back through `xknxmono.catalog`/`xknxmono.product`.

2. **Project stores references + overrides only**: a device row references a catalog product/program
   (`product_ref_id`, `hardware2program_ref_id`); parameters and com-object flags are overrides that
   differ from the application's defaults. The rest is resolved at read time.

3. **`ProjectService.devices` is a lazily-rebuilt view, not a cache you reload from disk**: every
   mutating call (including undo/redo) bumps an internal version counter; the next read of
   `.devices`/`.group_addresses`/etc. rebuilds from the live SQLite tables if the version changed.
   There is no separate "reload project" step.

4. **Devices are skipped, not crashed, when their catalog entry is missing**: `_build_device()` in
   `plugins/project/service.py` resolves `hardware2program_ref_id` back to an `Application` via the
   catalog; if that product/program was never imported (or the catalog file was reset), the device is
   logged and dropped from `.devices` until the catalog is repopulated. See "Limitations" in
   `docs/project.md`.

5. **Undo/redo is generic, not per-field**: most edits are small `Event` subclasses
   (`xknxmono.project.core.events`) with their own `apply`/`revert`; deletes (`RemoveDevice`,
   `RemoveArea`, ...) instead snapshot the entire deleted subtree as rows and reinsert them verbatim
   on undo, so cascade-deleted children come back with their original ids.

## Loading a Device from a Project

```python
def load_device(project_service, catalog_service, device_row):
    # 1. Resolve the catalog application via the device's program ref
    products = {
        p.hardware2program_ref_id: p.application_id
        for p in catalog_service.get_products()
    }
    app_id = products[device_row.hardware2program_ref_id]
    app = catalog_service.get_application(app_id)

    # 2. Build the runtime Device: overrides applied inside __post_init__ via DynamicUI
    device = Device(
        node_id=device_row.id,
        name=device_row.name,
        app=app,
        individual_address=project_service.individual_address(device_row.id),
        parameter_instance_refs=[...],  # from device_row.parameters
        module_instances=[...],  # from device_row.module_instances
        com_object_instance_refs=[...],  # from device_row.com_objects
    )
    return device
```

## Event Sourcing

See `packages/project/src/xknxmono/project/core/events.py` for the full list; the current event
types are: `AddInstallation`, `CreateArea`, `CreateLine`, `CreateSegment`, `AddDevice`,
`SetParameter`, `CreateGroupAddress`, `LinkComObject`, `SetComObjectFlag`,
`SetGroupAddressDatapointType`, `SetComObjectSending`, `RenameArea`, `RenameLine`, `SetDeviceName`,
`MoveDevice`, and the subtree deletes `RemoveDevice`/`RemoveArea`/`RemoveLine`/`RemoveSegment`/
`RemoveGroupAddress`/`UnlinkComObject`. `EventStore` (`core/event_store.py`) tracks a cursor over the
`events` table; `undo`/`redo` flip each event's `reverted` flag and walk the cursor rather than
deleting rows, so history survives a close/reopen.
