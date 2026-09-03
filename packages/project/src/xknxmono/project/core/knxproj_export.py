"""Export a project SQLite document to a simple ETS ``.knxproj`` archive.

This is a *simple* export: it writes the project structure (topology, devices with their
com-object → group-address links, the group-address tree, and the locations tree of spaces with
their device/function assignments) plus project metadata, in the ETS project XML shape so it
round-trips back through :func:`import_knxproj`.

The target schema is selectable: ``schema="20"`` (the default, ETS 5 / ``project/20``), ``"23"``
(current ETS 6 / ``project/23``), ``"22"`` (older ETS 6) or ``"14"`` (ETS 4). They share this
subset's element shape; only the XML namespace, the tool identity (``CreatedBy``/``ToolVersion``)
and the master-data source URL differ, so the same builder emits any of them by swapping the
namespace.

Manufacturer/application data (Hardware/Catalog/application program XMLs) is **not** read from a
catalog here — this package is catalog-free. Callers that have the catalog can pass those raw
archive members via ``extra_files`` (and a merged ``knx_master.xml`` via ``master_xml``) so the
resulting archive is self-contained and applications resolve.

Signature state of the exported archive:

- The **project folder** ``{pid}.signature`` is generated with a valid signature (see
  :mod:`knxproj_signing`); manufacturer ``M-XXXX.signature`` files, when needed, come from the
  catalog via ``extra_files``. The project **certificate** (``{pid}.certificate``, the licensing
  proof for projects above the free device limit) is server-signed and bound to the folder
  signature: pass a ``certificate_signer`` (e.g. :func:`myknx_cert.myknx_certificate_signer`) to
  request and embed it during export, or pass an existing one through via ``extra_files``.
- The **MasterData signature** in ``knx_master.xml`` is *not* generated here (``Signature=""``);
  its signing key is not part of this project. A fully signed archive can be built by reusing a
  signed ``knx_master.xml`` from an existing project via :func:`read_master_xml` (the signature
  covers the master content, not the project folders, so it stays valid) or by fetching the
  current signed master with :func:`fetch_master_xml`.
"""

from __future__ import annotations

import datetime
import logging
import re
import xml.etree.ElementTree as ET
import zipfile
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from pathlib import Path
from urllib.request import Request, urlopen
from uuid import uuid4

from sqlalchemy.orm import Session

from xknxmono.project.core.knxproj_signing import (
    SignatureAudit,
    audit_and_sign_folders,
    directory_signature,
)
from xknxmono.project.db import make_engine, url_for
from xknxmono.project.models import (
    Device,
    GroupRange,
    Installation,
    Project,
    Space,
)

logger = logging.getLogger(__name__)

# A certificate signer turns the freshly computed folder signature into a project certificate.
# Args: (pid, folder_signature_b64_bytes, project_name); returns the ``{pid}.certificate`` bytes,
# or None to skip embedding a certificate. ``folder_signature_b64_bytes`` is the raw content of the
# ``{pid}.signature`` file (base64, no BOM) that the certificate cryptographically binds to.
# The concrete MyKnx implementation lives in :mod:`myknx_cert` (kept out of this module so the
# export itself performs no network I/O unless a signer is passed in).
CertificateSigner = Callable[[str, bytes, str], bytes | None]


@dataclass
class ExportResult:
    """What :func:`export_knxproj` produced.

    ``schema``: the project schema actually written (may differ from the requested one; see
    :func:`export_knxproj`). ``unverifiable_folders``: nested/baggage folders that had no signature
    and got a best-effort one we cannot verify offline (needs ETS on Windows). ``missing_references``:
    application-program or hardware-to-program ids the installation references that are absent from
    the bundled manufacturer data - ETS's import converter looks these up in a dictionary and aborts
    with "The given key was not present in the dictionary" when one is missing. The caller should
    surface both to the user. Both empty on a normal, self-contained export.
    """

    schema: str
    unverifiable_folders: list[str] = field(default_factory=list[str])
    missing_references: list[str] = field(default_factory=list[str])

    def __str__(
        self,
    ) -> str:  # keep backwards-compatible with callers that used the schema string
        return self.schema


def _audit_installation_refs(members: Mapping[str, bytes]) -> list[str]:
    """Return references in the installation that point outside the bundled manufacturer data.

    Mirrors the two dictionaries ETS's import converter builds (``InstallationIdPatcher``): every
    application-program id (``M-XXXX_A-...``) an instance ref names must have its program XML in the
    bundle, and every ``Hardware2ProgramRefId`` must be declared in that manufacturer's
    ``Hardware.xml``. A miss is what makes ETS abort with "The given key was not present in the
    dictionary", so we flag it here instead of letting the import fail opaquely.
    """
    installations = [data for path, data in members.items() if path.endswith("/0.xml")]
    if not installations:
        return []
    hardware_xml: dict[str, str] = {
        path.split("/", 1)[0]: data.decode("utf-8", "replace")
        for path, data in members.items()
        if path.endswith("/Hardware.xml")
    }
    missing: set[str] = set()
    for data in installations:
        text = data.decode("utf-8", "replace")
        for value in re.findall(r'="([^"]+)"', text):
            parts = value.split("_")
            if (
                len(parts) >= 2
                and parts[0].startswith("M-")
                and parts[1].startswith("A-")
            ):
                app_id = f"{parts[0]}_{parts[1]}"
                if f"{parts[0]}/{app_id}.xml" not in members:
                    missing.add(f"application program {app_id}")
        for ref in re.findall(r'Hardware2ProgramRefId="([^"]+)"', text):
            mfr = ref.split("_", 1)[0]
            hardware = hardware_xml.get(mfr)
            if hardware is None or f'Id="{ref}"' not in hardware:
                missing.add(f"hardware2program {ref}")
    return sorted(missing)


# Supported target schemas mapped to (CreatedBy, ToolVersion) — the tool identity ETS validates on
# import. Verified against genuine exports + the decompiled ETS: ETS5 (5.7) writes project/20;
# ETS6 6.3 and 6.4 both use project/23 natively. We stamp the ETS 6.3 tool version (6.3.7959.0) for
# schema 23 so the export imports into ETS 6.3 as well as 6.4+ (a newer build number would be
# refused by an older ETS as "from a newer version"). project/22 is an older ETS6, project/14 ETS4.
_SCHEMA_TOOLS: dict[str, tuple[str, str]] = {
    "14": ("ETS4", "4.2.1287.32739"),
    "20": ("ETS5", "5.7.1428.39779"),
    "22": ("ETS6", "6.2.0.0"),
    "23": ("ETS6", "6.3.7959.0"),
}
DEFAULT_SCHEMA = "20"  # ETS5 shape: read by both ETS5 and ETS6


def _ns_for(schema: str) -> str:
    if schema not in _SCHEMA_TOOLS:
        raise ValueError(
            f"unsupported export schema {schema!r}; expected one of {sorted(_SCHEMA_TOOLS)}"
        )
    return f"http://knx.org/xml/project/{schema}"


def _schema_from_knx_xml(xml_bytes: bytes) -> str | None:
    """Return the ``project/<NN>`` schema number from a KNX XML root namespace, or ``None``."""
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError:
        return None
    if not root.tag.startswith("{"):
        return None
    uri = root.tag[1:].split("}", 1)[0]
    match = re.fullmatch(r"http://knx\.org/xml/project/(\d+)", uri)
    return match.group(1) if match else None


def _master_url(schema: str) -> str:
    return f"https://update.knx.org/data/XML/project-{schema}/knx_master.xml"


def _check_master(master: bytes, source: str, ns: str) -> bytes:
    root = ET.fromstring(master)
    if root.tag != f"{{{ns}}}KNX":
        raise ValueError(
            f"master from {source} uses namespace {root.tag}, expected {ns} — it would "
            "not verify against this export's project folders"
        )
    master_data = root.find(f"{{{ns}}}MasterData")
    if master_data is None or not master_data.get("Signature"):
        raise ValueError(
            f"knx_master.xml from {source} carries no MasterData signature"
        )
    return master


def read_master_xml(knxproj: Path | str, schema: str = DEFAULT_SCHEMA) -> bytes:
    """Read ``knx_master.xml`` from a (signed) ``.knxproj`` archive for reuse.

    Returns the master XML bytes as stored (so its ETS signature stays valid). The master is a
    catalog snapshot (datapoint types, medium types, manufacturers) that does not embed
    project-specific data, so it can be shared across exports. Raises ``ValueError`` when the
    master is missing, unsigned, or its schema namespace does not match ``schema``.
    """
    with zipfile.ZipFile(knxproj) as zf:
        return _check_master(zf.read("knx_master.xml"), str(knxproj), _ns_for(schema))


def fetch_master_xml(
    knxproj: Path | str | None = None,
    timeout: float = 15.0,
    schema: str = DEFAULT_SCHEMA,
) -> bytes:
    """Return a signed master XML for ``schema``, preferring the current KNX release.

    Tries the official master data for the schema (the same source ETS updates from), then falls
    back to the ``knx_master.xml`` from ``knxproj``. Raises ``OSError``/``ValueError`` when the
    download fails and no fallback archive was given. The returned bytes are always the untouched,
    signed master, so ``export_knxproj`` can pass them via ``master_xml`` directly.
    """
    ns = _ns_for(schema)
    url = _master_url(schema)
    try:
        with urlopen(Request(url), timeout=timeout) as response:
            return _check_master(response.read(), url, ns)
    except Exception as exc:
        if knxproj is None:
            raise
        logger.warning(
            "fetching current knx_master.xml failed (%s); using %s", exc, knxproj
        )
    return read_master_xml(knxproj, schema)


def export_knxproj(
    source: Path | str,
    dest: Path | str,
    *,
    schema: str = DEFAULT_SCHEMA,
    extra_files: Mapping[str, bytes] | None = None,
    master_xml: bytes | None = None,
    master_source: Path | str | None = None,
    fetch_master: bool = False,
    master_version: int = 1,
    certificate_signer: CertificateSigner | None = None,
    project_name: str | None = None,
) -> ExportResult:
    """Read the project at ``source`` (a ``.xknx``) and write a ``.knxproj`` archive to ``dest``.

    Returns an :class:`ExportResult`: the project schema actually written (``.schema`` — can differ
    from the requested ``schema`` because the export aligns to the bundled manufacturer/master data;
    ``str(result)`` yields it for backwards compatibility) plus ``.unverifiable_folders`` (nested
    folders that got a best-effort, offline-unverifiable signature — empty on a normal export).

    Args:
      source: Path to the ``.xknx`` project document.
      dest: Path to write the ``.knxproj`` archive to.
      schema: Target ETS project schema — ``"20"`` (ETS 5, default), ``"23"`` (current ETS 6),
        ``"22"`` (older ETS 6) or ``"14"`` (ETS 4). Controls the XML namespace, the tool identity
        stamped on the root and the master-data URL used by ``fetch_master``.
      extra_files: Optional raw archive members to add verbatim (e.g. manufacturer ``M-XXXX/``
        trees and their ``M-XXXX.signature`` files, supplied by a caller that has the catalog).
        Keys colliding with the export's own paths are ignored.
      master_xml: Optional ``knx_master.xml`` bytes to write instead of the generated one. Takes
        precedence over ``fetch_master``/``master_source``.
      master_source: Optional signed ``.knxproj`` whose (signed) master data is reused. Used as the
        fallback source when ``fetch_master`` is set and the download fails.
      fetch_master: When true (and ``master_xml`` is not given), download the current signed master
        for ``schema`` (:func:`fetch_master_xml`), falling back to ``master_source`` and then to the
        generated unsigned master. Off by default so the export performs no network I/O unless asked.
      master_version: ``MasterData`` ``Version`` attribute for the generated master (informational;
        only meaningful when the ``knx_master.xml`` is subsequently signed by an external master-data
        signer). Ignored when a signed master is supplied/fetched/reused.
      certificate_signer: Optional callback that turns the exported folder signature into a project
        certificate. When given, it is called after the folder signature is computed and, if it
        returns bytes, they are written as ``{pid}.certificate`` into the archive (the licensing
        proof ETS checks for projects above the free device limit). Use
        :func:`myknx_cert.myknx_certificate_signer` for the MyKnx cloud signer. Off by default so
        the export performs no network I/O and needs no MyKnx account.
      project_name: Optional name for the exported ProjectInformation (what ETS shows in its
        project list). When ``None`` the project's stored name is used. Does not persist to
        the source ``.xknx``.
    """
    ns = _ns_for(schema)
    logger.debug(
        "export_knxproj: source=%s dest=%s schema=%s signer=%s extra_files=%d",
        source,
        dest,
        schema,
        certificate_signer is not None,
        len(extra_files) if extra_files else 0,
    )
    if master_xml is None and (fetch_master or master_source is not None):
        try:
            if fetch_master:
                master_xml = fetch_master_xml(master_source, schema=schema)
            else:
                assert (
                    master_source is not None
                )  # implied by the branch condition above
                master_xml = read_master_xml(master_source, schema)
        except Exception as exc:
            logger.warning(
                "no signed master data available (%s); using generated unsigned master",
                exc,
            )
    # The whole .knxproj must use ONE schema. The bundled manufacturer data and knx_master.xml come
    # from .knxprod files at a fixed schema (often project/20); ETS rejects the import with
    # "Unreleased tool version" when the project files use a different schema than that master.
    # Align the project files to the supplied master's schema (ETS then converts up on import if it
    # runs a newer schema natively, e.g. project/20 -> /23 in ETS 6).
    if master_xml is not None:
        detected = _schema_from_knx_xml(master_xml)
        if detected is not None and detected != schema:
            if detected in _SCHEMA_TOOLS:
                logger.warning(
                    "aligning export schema %s -> %s to match bundled master data",
                    schema,
                    detected,
                )
                schema = detected
                ns = _ns_for(schema)
            else:
                logger.warning(
                    "bundled master uses unsupported schema %s; keeping %s (import may fail)",
                    detected,
                    schema,
                )
    # The bundled manufacturer data (M-XXXX trees) must use the SAME schema as the project files,
    # or ETS rejects the whole import with "Invalid import data". Fail fast on a mismatch — e.g. a
    # project/23 export with project/20 catalog product data (a native ETS6 export needs ETS6-era
    # .knxprod), or a catalog that mixes project/20 and project/23 manufacturers.
    if extra_files:
        mfr_schemas = {
            _schema_from_knx_xml(data)
            for name, data in extra_files.items()
            if name.endswith("/Hardware.xml")
        }
        mismatch = sorted(s for s in mfr_schemas if s is not None and s != schema)
        if mismatch:
            raise ValueError(
                f"cannot export as project/{schema}: bundled manufacturer data uses "
                f"project/{', project/'.join(mismatch)}. All device product data must match the "
                f"project schema — import ETS6-era .knxprod for a native project/23 export."
            )
    engine = make_engine(url_for(Path(source)))
    try:
        with Session(engine) as session:
            project = session.query(Project).first()
            if project is None:
                raise ValueError(f"{source} is not a project (no project row)")
            if project_name:
                # Override the exported ProjectInformation Name (transient: this session is never
                # committed, so the source .xknx is untouched).
                project.name = project_name
            installation = (
                session.query(Installation).order_by(Installation.index).first()
            )
            created_by, tool_version = _SCHEMA_TOOLS[schema]
            audit, missing_refs = _Writer(ns, created_by, tool_version).write_archive(
                Path(dest),
                project,
                installation,
                extra_files,
                master_xml,
                master_version,
                certificate_signer,
            )
    finally:
        engine.dispose()
    for folder in audit.signed:
        logger.info("signed folder %s (missing or invalid signature)", folder)
    for folder in audit.unverifiable:
        # A folder without a signature whose file names contain a character outside the embedded
        # NLS sort-key table: we cannot reproduce ETS's ordering, so the best-effort signature may
        # be rejected. Surface as an error so the GUI can alert the user.
        logger.error(
            "folder %s has no signature and uses characters outside the NLS table; the best-effort "
            "signature may be rejected by ETS (regenerate the NLS table via nls_sortkeys.ps1)",
            folder,
        )
    for ref in missing_refs:
        # The installation references manufacturer data missing from the bundle; ETS's import
        # converter aborts with "The given key was not present in the dictionary" on such a ref.
        logger.error(
            "export references %s, which is not in the bundled manufacturer data; ETS will reject "
            "the import (the device's product data is missing from the catalog bundle)",
            ref,
        )
    logger.debug(
        "export_knxproj done: %s (signed=%d unverifiable=%d missing_refs=%d)",
        dest,
        len(audit.signed),
        len(audit.unverifiable),
        len(missing_refs),
    )
    return ExportResult(
        schema=schema,
        unverifiable_folders=audit.unverifiable,
        missing_references=missing_refs,
    )


def _enable(value: bool | None) -> str | None:
    """A ``knx:Enable_t`` com-object flag attribute value, or ``None`` to omit it (inherit the
    application default). ``True`` -> ``"Enabled"``, ``False`` -> ``"Disabled"``."""
    return None if value is None else ("Enabled" if value else "Disabled")


def _relidref(ref_id: str) -> str:
    """Strip an instance ref id to the RELIDREF form ETS resolves against the application program.

    ETS stores ``ComObjectInstanceRef``/``ParameterInstanceRef`` ``@RefId`` as a "relative" id: the
    parent application-program part removed, leaving e.g. ``O-<n>_R-<m>`` for com-objects or
    ``UP-<n>_R-<m>`` / ``P-<n>_R-<m>`` for parameters (spec: ``knx:RELIDREF``). Our stored ref id
    keeps the full ``M-XXXX_A-XXXX-XX-XXXX_<local>`` form, so drop the two leading tokens of the
    application-program id (``M-XXXX`` and ``A-...``, which themselves contain no ``_``). Already
    relative ids are returned unchanged. Emitting the full id makes ETS unable to resolve the ref,
    so it drops the whole device on import.
    """
    parts = ref_id.split("_")
    if len(parts) >= 3 and parts[0].startswith("M-") and parts[1].startswith("A-"):
        return "_".join(parts[2:])
    return ref_id


def _assign_ids(
    pid: str, installation: Installation | None
) -> tuple[dict[int, str], dict[int, str]]:
    """Assign the stable element ids ETS uses: GA link tokens (``GA-n``) and device ids."""
    ga_link_id: dict[int, str] = {}
    di_id: dict[int, str] = {}
    if installation is None:
        return ga_link_id, di_id
    ga_seq = 0
    for group_range in installation.group_ranges:
        for ga in group_range.group_addresses:
            ga_seq += 1
            ga_link_id[ga.id] = f"GA-{ga_seq}"
    di_seq = 0
    for area in installation.areas:
        for line in area.lines:
            for segment in line.segments:
                for device in segment.devices:
                    di_seq += 1
                    di_id[device.id] = f"{pid}-0_DI-{di_seq}"
    return ga_link_id, di_id


class _Writer:
    """Builds the ``.knxproj`` XML for one target namespace (schema 14, 20, 22 or 23)."""

    def __init__(self, ns: str, created_by: str, tool_version: str) -> None:
        self._ns = ns
        self._created_by = created_by
        self._tool_version = tool_version
        self._puid = 0  # per-document unique element id ETS stamps on topology/GA nodes
        self._default_line_id: str | None = (
            None  # Installation DefaultLine (line holding devices)
        )
        # Topology shape differs by schema: ETS6 (project/22, /23) nests devices under a
        # <Segment> that carries MediumTypeRefId; ETS4/5 (project/14, /20) put devices directly
        # under <Line> with MediumTypeRefId on the line. Emitting the wrong shape makes ETS reject
        # the topology and import no devices.
        schema = ns.rsplit("/", 1)[-1]
        self._uses_segments = schema in {"22", "23"}

    def _next_puid(self) -> int:
        self._puid += 1
        return self._puid

    def _el(self, parent: ET.Element, tag: str, **attrs: object) -> ET.Element:
        child = ET.SubElement(parent, f"{{{self._ns}}}{tag}")
        for key, value in attrs.items():
            if value is not None:
                child.set(key, str(value))
        return child

    def _root(self) -> ET.Element:
        # ETS validates the tool identity on import, so mirror a genuine export's root: the two
        # extra schema namespaces plus CreatedBy/ToolVersion (a project/14 file with only the
        # default namespace is rejected as "Invalid import data").
        root = ET.Element(f"{{{self._ns}}}KNX")
        root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        root.set("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")
        root.set("CreatedBy", self._created_by)
        root.set("ToolVersion", self._tool_version)
        return root

    def _serialize(self, root: ET.Element) -> bytes:
        ET.register_namespace("", self._ns)
        # Genuine ETS writes every project XML as UTF-8 *with* a BOM; match it byte-for-byte so
        # ETS parses the installation files (without the BOM ETS can silently import nothing). The
        # folder signature is computed over exactly these bytes, so it stays self-consistent.
        return (
            b"\xef\xbb\xbf"
            + b'<?xml version="1.0" encoding="utf-8"?>\n'
            + ET.tostring(root, encoding="unicode").encode("utf-8")
        )

    def write_archive(
        self,
        dest: Path,
        project: Project,
        installation: Installation | None,
        extra_files: Mapping[str, bytes] | None,
        master_xml: bytes | None,
        master_version: int,
        certificate_signer: CertificateSigner | None = None,
    ) -> tuple[SignatureAudit, list[str]]:
        pid = project.id
        ga_link_id, di_id = _assign_ids(pid, installation)

        if master_xml is None:
            master = self._root()
            self._el(
                master, "MasterData", Id="MD-1", Version=master_version, Signature=""
            )
            master_xml = self._serialize(master)

        # Build the installation (0.xml) first: it stamps the Puids and picks the DefaultLine, both
        # of which the project.xml metadata references (LastUsedPuid must cover every Puid used).
        zero_xml = self._build_project_xml(
            pid, project, installation, ga_link_id, di_id
        )

        proj_xml = self._root()
        p = self._el(proj_xml, "Project", Id=pid)
        # ETS expects every project to carry a Guid and a LastModified timestamp; a project created
        # from scratch here has neither, and ETS then rejects the import ("Project file has no valid
        # signature"). Fall back to a fresh Guid + the current time so a from-scratch export imports.
        now = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%S.%f0Z")
        self._el(
            p,
            "ProjectInformation",
            Name=project.name,
            GroupAddressStyle=project.group_address_style,
            Comment="",
            LastUsedPuid=self._puid,
            Guid=project.guid or str(uuid4()),
            LastModified=project.last_modified or now,
        )

        own_paths = {
            "knx_master.xml",
            f"{pid}.signature",
            f"{pid}.certificate",
            f"{pid}/project.xml",
            f"{pid}/0.xml",
        }
        project_xml = self._serialize(proj_xml)
        zero = self._serialize(zero_xml)
        # Sign the project folder so a strict import accepts it (see knxproj_signing).
        folder_signature = directory_signature(
            {"project.xml": project_xml, "0.xml": zero}
        )
        logger.debug(
            "export: project folder signed (pid=%s project.xml=%d 0.xml=%d bytes)",
            pid,
            len(project_xml),
            len(zero),
        )
        # ETS writes the .signature file as raw base64 with NO BOM (verified against genuine ETS
        # archives, e.g. P-01D2.signature / M-0002.signature). A prepended UTF-8 BOM corrupts the
        # base64 and ETS rejects the project with "Project file has no valid signature".
        project_signature = folder_signature

        # Optionally obtain the project certificate (licensing proof), which binds to the folder
        # signature just computed. Done before opening the archive so a signer failure aborts cleanly.
        certificate: bytes | None = None
        if certificate_signer is not None:
            logger.debug("export: requesting project certificate for %s", pid)
            certificate = certificate_signer(pid, folder_signature, project.name)
            logger.debug(
                "export: certificate %s",
                f"{len(certificate)} bytes" if certificate else "skipped",
            )

        # Assemble every archive member first, then run the signature audit over the whole set so
        # each folder ends up with a signature: our own flat project folder is signed above and
        # verified here; manufacturer folders keep their (valid) catalog signatures verbatim; any
        # folder still missing a signature is signed best-effort and reported (see audit docs).
        members: dict[str, bytes] = {
            "knx_master.xml": master_xml,
            f"{pid}.signature": project_signature,
            f"{pid}/project.xml": project_xml,
            f"{pid}/0.xml": zero,
        }
        if certificate:
            members[f"{pid}.certificate"] = certificate
        for path, data in (extra_files or {}).items():
            if path not in own_paths:
                members[path] = data

        audit = audit_and_sign_folders(members)
        missing_refs = _audit_installation_refs(members)

        dest.unlink(missing_ok=True)
        with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as zf:
            for path, data in members.items():
                zf.writestr(path, data)
        return audit, missing_refs

    def _build_project_xml(
        self,
        pid: str,
        project: Project,
        installation: Installation | None,
        ga_link_id: dict[int, str],
        di_id: dict[int, str],
    ) -> ET.Element:
        root = self._root()
        p = self._el(root, "Project", Id=pid)
        insts = self._el(p, "Installations")
        if installation is None:
            return root
        # A genuine ETS installation carries these; ETS expects them on import.
        inst = self._el(
            insts,
            "Installation",
            Name=installation.name,
            BCUKey="4294967295",
            IPRoutingLatencyTolerance="2000",
        )

        topo = self._el(inst, "Topology")
        l_seq = 0
        s_seq = 0
        for a_seq, area in enumerate(
            sorted(installation.areas, key=lambda x: x.address), start=1
        ):
            area_el = self._el(
                topo,
                "Area",
                Id=f"{pid}-0_A-{a_seq}",
                Address=area.address,
                Name=area.name,
                Puid=self._next_puid(),
            )
            for line in sorted(area.lines, key=lambda x: x.address):
                l_seq += 1
                line_id = f"{pid}-0_L-{l_seq}"
                medium = line.segments[0].medium_type if line.segments else "MT-0"
                # ETS6 (segments) keeps MediumTypeRefId on the Segment; ETS4/5 on the Line.
                line_el = self._el(
                    area_el,
                    "Line",
                    Id=line_id,
                    Address=line.address,
                    Name=line.name,
                    MediumTypeRefId=None if self._uses_segments else medium,
                    Puid=self._next_puid(),
                )
                for segment in line.segments:
                    if self._uses_segments:
                        s_seq += 1
                        container = self._el(
                            line_el,
                            "Segment",
                            Id=f"{pid}-0_S-{s_seq}",
                            Number=segment.number,
                            MediumTypeRefId=segment.medium_type,
                            Puid=self._next_puid(),
                        )
                    else:
                        container = line_el
                    for device in segment.devices:
                        # ETS points DefaultLine at a line that actually holds devices.
                        if self._default_line_id is None:
                            self._default_line_id = line_id
                        self._build_device(
                            container, device, di_id[device.id], ga_link_id
                        )
                # Coupler "route regardless" pass-through addresses (KNX PR #651). Emitted on the
                # Line (ETS4/5 shape); newer schemas may also carry them on the Segment.
                extra = [
                    a for a in line.additional_group_addresses.split(",") if a.strip()
                ]
                if extra:
                    agas = self._el(line_el, "AdditionalGroupAddresses")
                    for addr in extra:
                        self._el(agas, "GroupAddress", Address=int(addr))

        if self._default_line_id is not None:
            inst.set("DefaultLine", self._default_line_id)

        self._build_locations(inst, installation, pid, di_id, ga_link_id)

        gas = self._el(inst, "GroupAddresses")
        ranges = self._el(gas, "GroupRanges")
        gr_seq = 0
        roots = [gr for gr in installation.group_ranges if gr.parent_id is None]
        for group_range in sorted(roots, key=lambda x: x.range_start):
            gr_seq = self._build_range(ranges, group_range, pid, gr_seq, ga_link_id)
        return root

    def _build_locations(
        self,
        inst_el: ET.Element,
        installation: Installation,
        pid: str,
        di_id: dict[int, str],
        ga_link_id: dict[int, str],
    ) -> None:
        roots = [s for s in installation.spaces if s.parent_id is None]
        if not roots:
            return
        locs = self._el(inst_el, "Locations")
        counters = {"sp": 0, "f": 0, "gar": 0}
        for space in sorted(roots, key=lambda s: (s.order, s.id)):
            self._build_space(locs, space, pid, di_id, ga_link_id, counters)

    def _build_space(
        self,
        parent: ET.Element,
        space: Space,
        pid: str,
        di_id: dict[int, str],
        ga_link_id: dict[int, str],
        counters: dict[str, int],
    ) -> None:
        counters["sp"] += 1
        sp = self._el(
            parent,
            "Space",
            Type=space.space_type or "Room",
            Id=f"{pid}-0_BP-{counters['sp']}",
            Name=space.name,
            Number=space.number or None,
            Description=space.description or None,
            Puid=self._next_puid(),
        )
        # The Space content model is a strict sequence: nested Space* first, then DeviceInstanceRef*,
        # then Function*. Emitting DeviceInstanceRef/Function before child spaces violates the schema.
        for child in sorted(space.children, key=lambda s: (s.order, s.id)):
            self._build_space(sp, child, pid, di_id, ga_link_id, counters)
        for device in space.devices:
            if device.id in di_id:
                self._el(sp, "DeviceInstanceRef", RefId=di_id[device.id])
        for fn in sorted(space.functions, key=lambda f: (f.order, f.id)):
            counters["f"] += 1
            fn_el = self._el(
                sp,
                "Function",
                Id=f"{pid}-0_F-{counters['f']}",
                Name=fn.name,
                Type=fn.function_type or None,
                Puid=self._next_puid(),
            )
            gf = 0
            for fga in fn.group_addresses:
                if fga.group_address_id not in ga_link_id:
                    continue
                # GroupAddressRef_t requires Name and Puid (schema); ETS crashes building the
                # buildings tree when they are missing. The Id is scoped under the function
                # (``_F-n_GF-m``) as ETS itself writes it.
                self._el(
                    fn_el,
                    "GroupAddressRef",
                    Id=f"{pid}-0_F-{counters['f']}_GF-{gf}",
                    Name="",
                    RefId=f"{pid}-0_{ga_link_id[fga.group_address_id]}",
                    Role=fga.role or None,
                    Puid=self._next_puid(),
                )
                gf += 1

    def _build_device(
        self,
        line_el: ET.Element,
        device: Device,
        device_id: str,
        ga_link_id: dict[int, str],
    ) -> None:
        di = self._el(
            line_el,
            "DeviceInstance",
            Id=device_id,
            Address=device.address,
            Name=device.name,
            ProductRefId=device.product_ref_id,
            Hardware2ProgramRefId=device.hardware2program_ref_id,
            Description=device.description or None,
            # Commissioning state (ETS's "loaded" ticks + serial / last download). Emit the flags
            # only when set; an absent attribute means "not loaded" (matches ETS and round-trips).
            SerialNumber=device.serial_number or None,
            LastDownload=device.last_download or None,
            IndividualAddressLoaded="true"
            if device.individual_address_loaded
            else None,
            ApplicationProgramLoaded="true"
            if device.application_program_loaded
            else None,
            CommunicationPartLoaded="true"
            if device.communication_part_loaded
            else None,
            MediumConfigLoaded="true" if device.medium_config_loaded else None,
            ParametersLoaded="true" if device.parameters_loaded else None,
            Puid=self._next_puid(),
        )
        # ETS orders the device's children ParameterInstanceRefs, then ComObjectInstanceRefs.
        # NOTE: unlike ComObjectInstanceRef (a RELIDREF), ParameterInstanceRef/@RefId is the FULL
        # id ("M-XXXX_A-..._P-n_R-m"); ETS reconstructs it via its parameter-id parser and crashes
        # (IndexOutOfRange in ParameterRefId.GetLongId) on a stripped id, dropping every device.
        if device.parameters:
            params = self._el(di, "ParameterInstanceRefs")
            for param in device.parameters:
                self._el(
                    params,
                    "ParameterInstanceRef",
                    RefId=param.ref_id,
                    Value=param.value,
                )
        # Emit a ComObjectInstanceRef for EVERY instantiated com-object (not only linked ones): the
        # device's object set — including objects a function/mode activated but that are not yet linked
        # to a group address (e.g. an active but unwired Channel D) — must survive export/re-import.
        # xknxproject keeps unlinked refs on read, and ETS resolves them fine. An empty container would
        # violate the schema, so only emit it when the device has at least one com-object.
        cos = list(device.com_objects)
        if cos:
            refs = self._el(di, "ComObjectInstanceRefs")
            for co in cos:
                # ETS orders the sending link first; our ComObjectLink.is_sending marks it.
                ordered = sorted(co.links, key=lambda link: not link.is_sending)
                links = " ".join(
                    ga_link_id[link.group_address_id]
                    for link in ordered
                    if link.group_address_id in ga_link_id
                )
                # RefId is a RELIDREF (app-program parent stripped); the full id would make ETS
                # unable to resolve the com-object and drop the whole device on import. ChannelId
                # (``CH-n``, already relative) places the object in its application channel. Links is
                # omitted when the object is not linked. Each flag is emitted only when set (non-None):
                # our stored flags are the effective flags (import resolves inherit→default), so a user
                # override survives export/re-import; a reconcile-added object with all-None (default)
                # flags emits none and inherits the application default, as ETS does.
                self._el(
                    refs,
                    "ComObjectInstanceRef",
                    RefId=_relidref(co.ref_id),
                    ChannelId=co.channel_id,
                    Links=links or None,
                    ReadFlag=_enable(co.read_flag),
                    WriteFlag=_enable(co.write_flag),
                    CommunicationFlag=_enable(co.communication_flag),
                    TransmitFlag=_enable(co.transmit_flag),
                    UpdateFlag=_enable(co.update_flag),
                    ReadOnInitFlag=_enable(co.read_on_init_flag),
                )

    def _build_range(
        self,
        parent: ET.Element,
        group_range: GroupRange,
        pid: str,
        seq: int,
        ga_link_id: dict[int, str],
    ) -> int:
        seq += 1
        gr_el = self._el(
            parent,
            "GroupRange",
            Id=f"{pid}-0_GR-{seq}",
            RangeStart=group_range.range_start,
            RangeEnd=group_range.range_end,
            Name=group_range.name,
            # Coupler pass-through flag; emit only when set (absent means filtered).
            Unfiltered="true" if group_range.unfiltered else None,
            Puid=self._next_puid(),
        )
        for ga in sorted(group_range.group_addresses, key=lambda x: x.address):
            self._el(
                gr_el,
                "GroupAddress",
                Id=f"{pid}-0_{ga_link_id[ga.id]}",
                Address=ga.address,
                Name=ga.name,
                Description=ga.description or None,
                Comment=ga.comment or None,
                DatapointType=ga.datapoint_type,
                Unfiltered="true" if ga.unfiltered else None,
                Puid=self._next_puid(),
            )
        for child in sorted(group_range.children, key=lambda x: x.range_start):
            seq = self._build_range(gr_el, child, pid, seq, ga_link_id)
        return seq
