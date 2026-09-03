# Project Persistence Architecture

## Overview

A project is one SQLite document (`.xknx` file) using event sourcing: every edit is an `Event`
object, applied against the live tables and appended to an `events` log, so undo/redo just walks
that log rather than diffing state.

Like the catalog, this is **not** GUI code: it's the standalone `xknx-project` package
(`packages/project/src/xknxmono/project/`). The GUI wraps it in `plugins/project/service.py`, which
adds the GUI-only concerns (resolving devices against the catalog, caching the resolved
`Application`, pub/sub for panels, selection state).

## Database Schema

SQLAlchemy models live in `xknxmono/project/models.py`. Tree: `Installation → Area → Line → Segment
→ Device`; group addresses live in a separate recursive `GroupRange` tree. Schema is
auto-created (`Base.metadata.create_all`), no migrations.

| Table | Purpose |
|-------|---------|
| `projects` | Single metadata row: name, `group_address_style` (e.g. `"ThreeLevel"`) |
| `installations` | One row per installation (`index` is the user-facing 0-based installation number) |
| `areas` / `lines` / `segments` | Topology tree; `segments.medium_type` carries e.g. `MT-0` (TP) / `MT-5` (IP) |
| `devices` | `address` (0–255 octet, unique within its line), `product_ref_id` (catalog product), `hardware2program_ref_id` (catalog `HardwareProgram.id`, resolves the `Application`) |
| `module_instances` | Top-level module instances on a device (`instance_id`, `ref_id`) |
| `parameters` | Parameter overrides: `(device_id, ref_id) -> value` |
| `com_objects` | Com-object instance overrides: `ref_id`, `channel_id`, and `*_flag` columns (`None` = inherit the product/application default, a bool forces enabled/disabled) |
| `group_ranges` | Recursive group-address range tree (main → middle in ThreeLevel style) |
| `group_addresses` | Leaf addresses, with an optional `datapoint_type` override |
| `com_object_links` | Links a com-object to a group address; `is_sending` marks the (at most one) transmit link |
| `events` | The undo/redo history: `type`, `data` (JSON payload), `timestamp`, `reverted` |

## Event Sourcing

### Event Types

All defined in `xknxmono/project/core/events.py`:

- **Topology**: `AddInstallation`, `CreateArea`, `CreateLine`, `CreateSegment`
- **Devices**: `AddDevice`, `SetParameter`, `SetDeviceName`, `MoveDevice` (segment + address)
- **Group addresses / links**: `CreateGroupAddress` (also finds-or-creates its containing range
  chain as one undoable step), `LinkComObject`, `SetComObjectFlag`, `SetComObjectSending`,
  `SetGroupAddressDatapointType`
- **Reversible deletes** (snapshot-and-restore, see below): `RemoveDevice`, `RemoveArea`,
  `RemoveLine`, `RemoveSegment`, `RemoveGroupAddress`, `UnlinkComObject`
- **Renames**: `RenameArea`, `RenameLine`

Every event is a dataclass implementing `apply(session)`, `revert(session)`, `to_dict()`,
`from_dict()`. Row ids created by `apply()` are captured on the event itself (the `if self.x_id is
not None: obj.id = self.x_id` idiom), so a redo re-inserts with the *same* ids and any foreign keys
elsewhere in the JSON payload stay valid.

### Reversible Deletes

`RemoveDevice`/`RemoveArea`/etc. are all `_SubtreeDelete`: `apply()` walks every cascade-owned
descendant of the target row via SQLAlchemy relationship introspection, serializes each one to a
plain dict (`_snapshot_subtree`), stores that list on the event, then deletes the row (cascade
handles the rest). `revert()` just re-inserts every captured row (`_restore_rows`), parents first.
This means deleting a device also captures and can restore its parameters, com objects, and module
instances — no per-field revert logic needed for deletes.

### EventStore (undo/redo)

`xknxmono/project/core/event_store.py`. A cursor tracks the id of the highest non-reverted event.

- `append(event)` — if the cursor isn't at the end, deletes every event after it (discards the redo
  branch), applies the new event, inserts its row, commits, moves the cursor to it.
- `undo()` — reverts the event at the cursor, marks it `reverted=True`, moves the cursor to the
  previous non-reverted event.
- `redo()` — finds the next `reverted=True` event after the cursor, re-applies it, marks it
  `reverted=False`, moves the cursor forward.
- `jump_to(id)` — repeated undo/redo until the cursor reaches the target.

No rows are ever deleted by undo/redo itself (only `append` after a branch prunes forward history),
so `history()` (newest first) always reflects the full log, reverted or not.

## GUI Facade (`plugins/project/service.py`)

The GUI's `ProjectService` wraps `xknxmono.project.ProjectService` and adds:

- **Device resolution**: turns a `devices` row + its `parameters`/`com_objects`/`module_instances`
  into a `editor_gui.types.Device` by resolving `hardware2program_ref_id` to an `Application` through
  the catalog (`CatalogService.get_application`), with the resolved `Application` cached by program
  ref (`_app_cache`) since parsing is the expensive part.
- **Lazy rebuild via version counter**: every mutating call bumps `self._version`; property reads
  like `.devices`/`.group_addresses` rebuild only if `self._cache_version != self._version`. There's
  no explicit "reload from DB" — undo/redo just bump the version like any other edit.
- **Pub/sub**: `subscribe(event, handler) -> unsubscribe_fn` for `"device_selected"` and similar UI
  events, orthogonal to the persistence event log above.
- **History labels**: `_history_label()` renders a human-readable string per event type for the
  History panel — presentation lives in the GUI, not the project package.

## File Format

Project files use the `.xknx` extension and are plain SQLite3 databases:

```bash
sqlite3 project.xknx "SELECT type, data FROM events ORDER BY id;"
```

## Limitations

### Devices with a missing catalog entry
A project device only stores `product_ref_id`/`hardware2program_ref_id` — references into the
catalog, not the application data itself. If the catalog doesn't have that program (a fresh or
emptied `catalog.db`, or a product that was never (re-)imported), `ProjectService._build_device()`
logs a warning and the device is silently dropped from `.devices` until the catalog is repopulated
with a matching import. It is not deleted from the project database.

### Catalog changes aren't versioned
If an application's parameter/com-object definitions change between catalog imports (e.g. a
manufacturer ships an updated `.knxprod` under the same `hardware2program_ref_id`), existing project
overrides are re-applied against the new definition with no compatibility check.
