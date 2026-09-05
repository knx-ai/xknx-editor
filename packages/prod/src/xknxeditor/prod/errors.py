class ArchiveError(Exception):
    """Invalid or unreadable knxprod archive."""


class VersionError(Exception):
    """KNX version undetectable or unsupported."""


class ParseError(Exception):
    """XML parsing failed."""
