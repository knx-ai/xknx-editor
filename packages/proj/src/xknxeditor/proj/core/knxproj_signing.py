"""Sign a ``.knxproj`` directory the way the KNX tooling expects on import.

Each folder in a ``.knxproj`` archive (the project folder ``P-XXXX`` and each
manufacturer folder ``M-XXXX``) is accompanied by a ``<folder>.signature`` file
at the archive root. The signature is an RSA-PKCS#1 v1.5 signature over a SHA-1
digest of the folder's contents:

1. for every file in the folder (recursively), compute ``base64(sha1(content))``;
2. build the string ``"relpath:hash,relpath:hash,..."`` with the entries sorted by relative path
   and joined by commas. The .knxproj signer orders paths with ``StringComparer.InvariantCulture``;
   .NET Framework is used, so that is the **Windows NLS collation** (not ICU/UCA). We reproduce it
   with an embedded per-character NLS sort-key table (:mod:`_nls_sortkeys`), which was verified to
   yield byte-identical folder digests for real manufacturer folders. Relative paths use ``\\`` (the
   Windows separator the signer runs with);
3. the digest is ``sha1(utf-8(that string))``;
4. the signature is ``RSA-PKCS#1v1.5(sha1)`` of that digest, base64 encoded.

Mirrors the vendor ``Knx.Ets.XmlSigning`` assembly (reference: OpenKNXproducer
https://github.com/OpenKNX/OpenKNXproducer, ``Signing/XmlSigner.cs``, wrapped by :mod:`_dll_signer`).
Signs every folder offline (see :func:`set_signing_key`). Folders with a file name
outside the embedded NLS table cannot be ordered offline and are surfaced by
:func:`audit_and_sign_folders` (extend the table via ``nls_sortkeys.ps1``).
"""

from __future__ import annotations

import base64
import hashlib
from collections.abc import Mapping, MutableMapping
from dataclasses import dataclass, field

from xknxeditor.proj.core._nls_sortkeys import CHAR_SORTKEYS

# Throwaway 1024-bit RSA key so folders get a well-formed .signature (all an import needs). Stored as
# lowercase hex — the same format the Signing window shows/edits. Replaced at runtime via
# set_signing_key() with the genuine key extracted from the user's ETS DLL (see key_extract).
_PLACEHOLDER_MODULUS = "9878171fc16318fd7295e0cb2442d0bedb5435013a55e4806515f60b874d9b8415b18e5f508fa9758bdc443f4e1d2af3e198213fd4bc4e2dd172d9d80364cdd2d59c05b85fc69b9035d37b9e4542c7ab848b5930cbc5040915dd3ce39ad10c9cc96883fda6f165fce665fcd4a4fca8cdfe3c0da5e58f6e1de020b82404d8952f"
_PLACEHOLDER_PRIVATE_EXPONENT = "c7bd8b8dae6b8471838b95d28ace7d698b2be5c49607b032043ba0f9b967923497b6e42d39fcfaa363764c72228353a1ec08c0863ecbf21f542481fedb7353aeb9271f334780282a57213afbb405ee85916f18ec4435e3cac0a76297ccad31e2031c8681b9af1121450330aa63ef5059524e91f1f6cdd84bb495e9f3d309fb1"
_MODULUS = int(_PLACEHOLDER_MODULUS, 16)
_PRIVATE_EXPONENT = int(_PLACEHOLDER_PRIVATE_EXPONENT, 16)
_default_params = (_MODULUS, _PRIVATE_EXPONENT, 65537, (_MODULUS.bit_length() + 7) // 8)
_params = _default_params


def set_signing_key(
    modulus: int, private_exponent: int, public_exponent: int = 65537
) -> None:
    """Replace the signing key used by :func:`directory_signature`/:func:`verify_directory_signature`.

    Call with the genuine key (e.g. extracted from an ETS DLL) so exports are signed ETS-valid.
    """
    global _params
    _params = (
        modulus,
        private_exponent,
        public_exponent,
        (modulus.bit_length() + 7) // 8,
    )


def reset_signing_key() -> None:
    """Restore the built-in placeholder key."""
    global _params
    _params = _default_params


def current_signing_key() -> tuple[int, int, int]:
    """Return the active ``(modulus, private_exponent, public_exponent)``."""
    return (_params[0], _params[1], _params[2])


def signing_key_is_placeholder() -> bool:
    """Whether the active key is the built-in placeholder (signatures not ETS-valid)."""
    return _params == _default_params


# ASN.1 DigestInfo prefix for a SHA-1 hash (RFC 3447).
_SHA1_DIGEST_INFO_PREFIX = bytes.fromhex("3021300906052b0e03021a05000414")

# Per-character Windows NLS sort-key sections, parsed from the embedded table. A .NET NLS sort key
# is ``P 01 D 01 C 01 X 01 S 00`` (primary/diacritic/case/.../special sections separated by 0x01);
# a string's key concatenates each section across its characters. Reproducing the .knxproj signer's
# InvariantCulture (= Windows NLS) ordering this way was verified to yield byte-identical folder
# digests for real manufacturer folders (flat and nested/baggage). See _nls_sortkeys.py.
_CHAR_SECTIONS: dict[int, list[bytes]] = {
    cp: bytes.fromhex(hx).rstrip(b"\x00").split(b"\x01")
    for cp, hx in CHAR_SORTKEYS.items()
}


def _nls_sort_key(text: str) -> bytes | None:
    """Return the reconstructed Windows-NLS sort key for ``text``, or ``None`` if unrepresentable.

    ``None`` means a character is outside the embedded table (regenerate it via
    ``nls_sortkeys.ps1`` to extend coverage); the caller then cannot reproduce the
    genuine ordering offline for that folder.
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

    Files are ordered by the Windows-NLS sort key of the relative path (.NET Framework's
    ``StringComparer.InvariantCulture`` uses NLS collation, matching genuine exports). Relative paths
    are normalised to backslash separators to match genuine exports. If any path contains a character
    outside the embedded NLS table the order cannot be reproduced and this raises ``KeyError`` -
    callers that must tolerate that use :func:`nls_directory_digest`.
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
    padding = b"\xff" * (_params[3] - 3 - len(block))
    encoded = b"\x00\x01" + padding + b"\x00" + block
    signature = pow(int.from_bytes(encoded, "big"), _params[1], _params[0])
    return base64.b64encode(signature.to_bytes(_params[3], "big"))


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
    if len(sig) != _params[3]:
        return False
    digest = nls_directory_digest(files)
    if digest is None:
        return False
    recovered = pow(int.from_bytes(sig, "big"), _params[2], _params[0]).to_bytes(
        _params[3], "big"
    )
    block = _SHA1_DIGEST_INFO_PREFIX + digest
    expected = b"\x00\x01" + b"\xff" * (_params[3] - 3 - len(block)) + b"\x00" + block
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
      manufacturer data copied verbatim from a real, signed ``.knxprod`` stays quiet).
    - A folder with a missing or invalid signature is (re)signed, as long as its file names are all
      covered by the embedded NLS table (so we can reproduce the genuine Windows-NLS order). Reported in
      ``signed``.
    - A folder with no signature and an uncovered character gets a best-effort signature and is
      reported in ``unverifiable`` (the caller should surface it; regenerate the NLS table via
      ``nls_sortkeys.ps1`` to extend coverage).
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
