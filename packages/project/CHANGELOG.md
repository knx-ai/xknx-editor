# Changelog

All notable changes to `xknx-project` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- KNX project state management on top of `xknx-models`.
- `import_knxproj()` — import an ETS `.knxproj` archive into a new project (topology, group
  addresses with DPTs, devices, and com-object links), parsed via `xknxproject`.
- Typed read/write access to group addresses, topology, and device configuration.
