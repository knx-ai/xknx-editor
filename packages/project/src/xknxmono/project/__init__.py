"""xknx-project: an editable KNX project stored as a relational SQLite document.

A project is one on-disk SQLite database; edits go through a command-based
:class:`~xknxmono.project.core.service.ProjectService` that records each command in an ``events``
history for undo/redo. The package defines its own topology/group-address models
(:mod:`xknxmono.project.models`) — a subset of the KNX IR, not the IR itself. See
:mod:`xknxmono.project.core`.

The package is **ref-only**: a device stores a ``product_ref_id`` and a
``hardware2program_ref_id`` but the package never reads the catalog to resolve the application.
Callers (e.g. the GUI, which has the catalog) expand the application and pass its parameters and
com-object refs into :meth:`ProjectService.add_device`.
"""

__version__ = "0.1.0"

from xknxmono.project.core import (
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
