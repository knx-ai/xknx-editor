"""Sign a ``.knxproj`` directory the way the KNX tooling expects on import.

Each folder in a ``.knxproj`` archive (the project folder ``P-XXXX`` and each
manufacturer folder ``M-XXXX``) is accompanied by a ``<folder>.signature`` file
at the archive root. The signature is an RSA-PKCS#1 v1.5 signature over a SHA-1
digest of the folder's contents:

1. for every file in the folder (recursively), compute ``base64(sha1(content))``;
2. build the string ``"relpath:hash,relpath:hash,..."`` with the entries sorted by relative path
   and joined by commas. ETS orders paths with ``StringComparer.InvariantCulture``; ETS 6 is
   .NET Framework, so that is the **Windows NLS collation** (not ICU/UCA). We reproduce it with an
   embedded per-character NLS sort-key table (:mod:`_nls_sortkeys`), which was verified to yield
   byte-identical folder digests for real manufacturer folders. Relative paths use ``\\`` (the
   Windows separator ETS runs with);
3. the digest is ``sha1(utf-8(that string))``;
4. the signature is ``RSA-PKCS#1v1.5(sha1)`` of that digest, base64 encoded.

The signing key is the fixed "converter" RSA key that ships identically with the KNX tooling (it is
not per-installation or secret), so any folder can be re-signed offline. Folders whose file names
use a character outside the embedded NLS table cannot have their order reproduced offline; those are
surfaced by :func:`audit_and_sign_folders` (regenerate the table via ``.references/nls_sortkeys.ps1``
to extend coverage).
"""

from __future__ import annotations

import base64
import hashlib
from collections.abc import Mapping, MutableMapping
from dataclasses import dataclass, field

from xknxmono.project.core._nls_sortkeys import CHAR_SORTKEYS

# The converter RSA key (1024 bit, public exponent 65537). Public knowledge - the
# same key ships with the KNX tooling; kept here so folders can be re-signed.
_MODULUS_B64 = (
    "zSjrmVmM+ULXdrFHiSZZo7PEHo/sXBIkjxHkqQbxEI2YE1SBq0dbEfqW3eDSdjLlpMy5Yx9hcMS"
    "nrmVUWh3PgBBQmzMBZpr/yJRny8UzB1pqTPyisWyfg7+NiAd1Ize4r/bQxKE4BaJ2wqEDwH8ggg"
    "2faxJ2/WReGVrrzJL2u00="
)
_PRIVATE_EXPONENT_B64 = (
    "p1DgE8h8uCxTHHGoLaohIOjS4TnvQYdqWWP2YANRRnazt9ALkGw5UYhU0c8w1UTdFHICH1zQUu+"
    "O8SOij3wQZKMGcw4GgsJH8jUtlbSkHCtJVOBe817tNcuVUC1qfSt59uCyR6jKV2pm2+Hy8MCcsZ"
    "kRXqDRcdgcYsiTpIwKcuE="
)

_MODULUS = int.from_bytes(base64.b64decode(_MODULUS_B64), "big")
_PRIVATE_EXPONENT = int.from_bytes(base64.b64decode(_PRIVATE_EXPONENT_B64), "big")
_PUBLIC_EXPONENT = 65537
_KEY_SIZE = (_MODULUS.bit_length() + 7) // 8
# ASN.1 DigestInfo prefix for a SHA-1 hash (RFC 3447).
_SHA1_DIGEST_INFO_PREFIX = bytes.fromhex("3021300906052b0e03021a05000414")

# Per-character Windows NLS sort-key sections, parsed from the embedded table. A .NET NLS sort key
# is ``P 01 D 01 C 01 X 01 S 00`` (primary/diacritic/case/.../special sections separated by 0x01);
# a string's key concatenates each section across its characters. Reproducing ETS 6's
# InvariantCulture (= Windows NLS) ordering this way was verified to yield byte-identical folder
# digests for real manufacturer folders (flat and nested/baggage). See _nls_sortkeys.py.
_CHAR_SECTIONS: dict[int, list[bytes]] = {
    cp: bytes.fromhex(hx).rstrip(b"\x00").split(b"\x01")
    for cp, hx in CHAR_SORTKEYS.items()
}


def _nls_sort_key(text: str) -> bytes | None:
    """Return the reconstructed Windows-NLS sort key for ``text``, or ``None`` if unrepresentable.

    ``None`` means a character is outside the embedded table (regenerate it via
    ``.references/nls_sortkeys.ps1`` to extend coverage); the caller then cannot reproduce ETS's
    order offline for that folder.
    """
    per_char: list[list[bytes]] = []
    for ch in text:
        sections = _CHAR_SECTIONS.get(ord(ch))
        if sections is None:
            return None
        per_char.append(sections)
    width = max((len(s) for s in per_char), default=0)
    merged = [b"".join(s[i] for s in per_char if i < len(s)) for i in range(width)]
    return b"\x01".join(merged) + b"\x00"


def directory_digest(files: Mapping[str, bytes]) -> bytes:
    """Return the SHA-1 folder digest for ``files`` (relative path -> content).

    Files are ordered the way ETS does it: by the Windows-NLS sort key of the relative path (ETS 6
    is .NET Framework, whose ``StringComparer.InvariantCulture`` uses NLS collation). Relative paths
    are normalised to backslash separators to match ETS. If any path contains a character outside
    the embedded NLS table the order cannot be reproduced and this raises ``KeyError`` - callers
    that must tolerate that use :func:`nls_directory_digest`.
    """
    digest = nls_directory_digest(files)
    if digest is None:
        raise KeyError(
            "path contains a character outside the embedded NLS sort-key table"
        )
    return digest


def nls_directory_digest(files: Mapping[str, bytes]) -> bytes | None:
    """Like :func:`directory_digest` but returns ``None`` when the NLS order is unrepresentable."""
    entries: dict[str, str] = {}
    keys: dict[str, bytes] = {}
    for path, content in files.items():
        rel = path.replace("/", "\\")
        sort_key = _nls_sort_key(rel)
        if sort_key is None:
            return None
        entries[rel] = base64.b64encode(hashlib.sha1(content).digest()).decode("ascii")
        keys[rel] = sort_key
    ordered = sorted(entries, key=lambda p: keys[p])
    joined = ",".join(f"{p}:{entries[p]}" for p in ordered)
    return hashlib.sha1(joined.encode("utf-8")).digest()


def _signature_from_digest(digest: bytes) -> bytes:
    block = _SHA1_DIGEST_INFO_PREFIX + digest
    padding = b"\xff" * (_KEY_SIZE - 3 - len(block))
    encoded = b"\x00\x01" + padding + b"\x00" + block
    signature = pow(int.from_bytes(encoded, "big"), _PRIVATE_EXPONENT, _MODULUS)
    return base64.b64encode(signature.to_bytes(_KEY_SIZE, "big"))


def directory_signature(files: Mapping[str, bytes]) -> bytes:
    """Return the base64 ``.signature`` bytes for a folder's ``files``.

    ``files`` maps each file's path (relative to the folder, ``/`` separated) to
    its content. Suitable directly as the body of the folder's ``.signature`` file. Raises
    ``KeyError`` if a path uses a character outside the embedded NLS table (see
    :func:`directory_digest`); use :func:`nls_directory_signature` to get ``None`` instead.
    """
    return _signature_from_digest(directory_digest(files))


def nls_directory_signature(files: Mapping[str, bytes]) -> bytes | None:
    """Like :func:`directory_signature` but returns ``None`` when the NLS order is unrepresentable."""
    digest = nls_directory_digest(files)
    return None if digest is None else _signature_from_digest(digest)


def verify_directory_signature(files: Mapping[str, bytes], signature: bytes) -> bool:
    """Return whether ``signature`` (a ``.signature`` file body) matches ``files``.

    Recomputes the folder digest (Windows-NLS order, backslash separators) and checks the
    RSA-PKCS#1 v1.5 block. Conclusive for both flat and nested/baggage folders as long as every
    path is covered by the embedded NLS table; if a path uses an uncovered character the order
    cannot be reproduced and this returns ``False`` (not proof of an invalid signature).
    """
    try:
        sig = base64.b64decode(signature.lstrip(b"\xef\xbb\xbf").strip())
    except (ValueError, TypeError):
        return False
    if len(sig) != _KEY_SIZE:
        return False
    digest = nls_directory_digest(files)
    if digest is None:
        return False
    recovered = pow(int.from_bytes(sig, "big"), _PUBLIC_EXPONENT, _MODULUS).to_bytes(
        _KEY_SIZE, "big"
    )
    block = _SHA1_DIGEST_INFO_PREFIX + digest
    expected = b"\x00\x01" + b"\xff" * (_KEY_SIZE - 3 - len(block)) + b"\x00" + block
    return recovered == expected


def _best_effort_digest(files: Mapping[str, bytes]) -> bytes:
    """Ordinal digest (backslash separators) used only when the NLS order is unrepresentable."""
    entries = {
        path.replace("/", "\\"): base64.b64encode(hashlib.sha1(c).digest()).decode(
            "ascii"
        )
        for path, c in files.items()
    }
    joined = ",".join(f"{p}:{h}" for p, h in sorted(entries.items()))
    return hashlib.sha1(joined.encode("utf-8")).digest()


@dataclass
class SignatureAudit:
    """Outcome of :func:`audit_and_sign_folders`.

    ``signed``: folders we (re)signed with a signature we can reproduce and verify (flat, or nested
    whose file names are all covered by the embedded NLS table).
    ``unverifiable``: folders that had no signature and use a character outside the NLS table, so we
    wrote a best-effort one that cannot be verified offline - the caller should surface these.
    """

    signed: list[str] = field(default_factory=list[str])
    unverifiable: list[str] = field(default_factory=list[str])


def audit_and_sign_folders(members: MutableMapping[str, bytes]) -> SignatureAudit:
    """Ensure every folder in a ``.knxproj`` member map carries a valid signature; sign what we can.

    ``members`` maps archive paths to bytes (``P-XXXX/project.xml``, ``M-XXXX/...``,
    ``M-XXXX.signature``, ``knx_master.xml``, ...). Mutated in place:

    - A folder whose existing signature already verifies is left untouched (the normal case -
      manufacturer data copied verbatim from a real, ETS-signed ``.knxprod`` stays quiet).
    - A folder with a missing or invalid signature is (re)signed, as long as its file names are all
      covered by the embedded NLS table (so we can reproduce ETS's Windows-NLS order). Reported in
      ``signed``.
    - A folder with no signature and an uncovered character gets a best-effort signature and is
      reported in ``unverifiable`` (the caller should surface it; regenerate the NLS table via
      ``.references/nls_sortkeys.ps1`` to extend coverage).
    """
    folders: dict[str, dict[str, bytes]] = {}
    for path, data in members.items():
        if "/" not in path:
            continue  # root-level file (knx_master.xml, <folder>.signature/.certificate/.info)
        top, rel = path.split("/", 1)
        folders.setdefault(top, {})[rel] = data

    audit = SignatureAudit()
    for folder, files in folders.items():
        sig_key = f"{folder}.signature"
        existing = members.get(sig_key)
        if existing is not None and verify_directory_signature(files, existing):
            continue  # already valid - never clobber
        nls_sig = nls_directory_signature(files)
        if nls_sig is not None:
            members[sig_key] = nls_sig
            audit.signed.append(folder)
        elif existing is None:
            members[sig_key] = _signature_from_digest(_best_effort_digest(files))
            audit.unverifiable.append(folder)
        # else: uncovered characters AND an existing (unverifiable) signature -> keep verbatim.
    audit.signed.sort()
    audit.unverifiable.sort()
    return audit
