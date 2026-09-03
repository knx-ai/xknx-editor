# Changelog

All notable changes to `xknx-product` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Read `.knxprod` archives (ZIP files) and validate their internal structure.
- Parse manufacturer, catalog, hardware, and application program XMLs via `xknx-models`.
- Typed access to product catalog metadata and application program definitions.
