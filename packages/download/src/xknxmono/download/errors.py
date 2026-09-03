"""Exceptions raised while downloading data into a KNX device."""

from __future__ import annotations


class DownloadError(Exception):
    """Base class for all download errors."""


class LoadStateError(DownloadError):
    """A Load State Machine did not reach the expected state."""


class VerificationError(DownloadError):
    """Data read back from the device does not match the data written."""


class UnsupportedProcedureError(DownloadError):
    """The Load Procedure contains a step that is not supported."""


class ImageError(DownloadError):
    """The download image could not be assembled from the application data."""
