"""xknxeditor-proj: an editable KNX project backed by one relational SQLite file.

Each project is a single on-disk database. All edits run through the command-based
:class:`~xknxeditor.proj.core.service.ProjectService`, which logs every command to an ``events``
table so undo/redo works. Topology and group-address models (:mod:`xknxeditor.proj.models`) are
the package's own, a slice of the KNX IR rather than the IR. See :mod:`xknxeditor.proj.core`.

Ref-only by design: a device keeps a ``product_ref_id`` and ``hardware2program_ref_id`` but nothing
here touches the catalog to resolve the application. The caller (the GUI, which holds the catalog)
expands it and hands the parameters and com-object refs to :meth:`ProjectService.add_device`.
"""

__version__ = "0.1.0"

from xknxeditor.proj.core import (
    DLL_NAME,
    ExportResult,
    KeyExtractionError,
    MyKnxError,
    ProjectService,
    current_signing_key,
    default_dll_path,
    export_knxproj,
    extract_converter_key,
    extraction_backend,
    fetch_master_xml,
    fetch_myknx_products,
    import_knxproj,
    myknx_certificate_signer,
    read_master_xml,
    reset_signing_key,
    set_signing_key,
    sign_exported_knxproj,
    signing_key_is_placeholder,
)

__all__ = [
    "DLL_NAME",
    "ExportResult",
    "KeyExtractionError",
    "MyKnxError",
    "ProjectService",
    "current_signing_key",
    "default_dll_path",
    "export_knxproj",
    "extract_converter_key",
    "extraction_backend",
    "fetch_master_xml",
    "fetch_myknx_products",
    "import_knxproj",
    "myknx_certificate_signer",
    "read_master_xml",
    "reset_signing_key",
    "set_signing_key",
    "sign_exported_knxproj",
    "signing_key_is_placeholder",
]
