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
    ExportResult,
    MyKnxError,
    ProjectService,
    export_knxproj,
    fetch_master_xml,
    fetch_myknx_products,
    import_knxproj,
    myknx_certificate_signer,
    read_master_xml,
    sign_exported_knxproj,
)

__all__ = [
    "ExportResult",
    "MyKnxError",
    "ProjectService",
    "export_knxproj",
    "fetch_master_xml",
    "fetch_myknx_products",
    "import_knxproj",
    "myknx_certificate_signer",
    "read_master_xml",
    "sign_exported_knxproj",
]
