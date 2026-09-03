# Changelog

All notable changes to `xknx-download` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Initial device download package.
- `download()` high level entry point driving a full download over a
  point-to-point connection.
- `build_image()` assembling a `DownloadImage` from a parsed application program.
- `LoadProcedureRunner` interpreting Load Procedures into bus operations.
- `DeviceProgrammer` with chunked memory writes, property access, interface
  object location and property based Load State Machine control.
- Load event encodings per KNX Standard 3/5/2 (including data relative
  allocation, subtype 0x0B).
- Load Procedure resolution (`resolve_download_controls`) for product, default
  and merged procedure styles, splicing application fragments into the mask
  version's default procedure by merge id.
- Connection lifecycle following the procedure's Connect/Disconnect/Restart
  controls (open per Connect, close per Disconnect, tear down + cooldown after
  Restart, auto-connect before any bus control) via a `ConnectionManager`.
- Relative memory controls (`WriteRelMem`/`CompareRelMem`/`LoadImageRelMem`) with
  table-reference base resolution; image-backed `WriteMem`/`WriteProp`;
  element-aware property chunking; per-block memory verify.
- Partial downloads via `DownloadScope` (parameters / group communication).
- `program_individual_address` for commissioning a device's individual address.
- `project_data` adapters turning a configured device into parameter values and
  group communication links.
