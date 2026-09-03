class ArchiveError(Exception):
    """Raised when a knxprod archive is invalid or cannot be read."""


class VersionError(Exception):
    """Raised when a KNX version cannot be detected or is unsupported."""


class ParseError(Exception):
    """Raised when XML parsing fails."""
