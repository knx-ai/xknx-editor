"""Resolve the effective Load Procedure to execute for a download.

An application declares one of three load procedure styles:

- ``ProductProcedure``: the application ships the complete procedure; use it as is.
- ``DefaultProcedure``: the application ships no procedure; use the mask version's
  default procedure from the master data.
- ``MergedProcedure``: the application ships fragments identified by a merge id;
  splice them into the mask version's default procedure at the matching
  ``LdCtrlMerge`` placeholders.

The default procedures live per mask version in the master data
(``MaskVersion`` -> configuration data -> ``Procedures``), keyed by procedure
type (``Load`` for a download, ``Unload`` for removal).
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from xknxmono.models.intermediate.ld_ctrl_merge_t import LdCtrlMerge
from xknxmono.models.intermediate.load_procedure_style_t import LoadProcedureStyle
from xknxmono.models.intermediate.procedure_type_t import ProcedureType

from .errors import UnsupportedProcedureError

if TYPE_CHECKING:
    from xknxmono.models.intermediate.load_procedure_t import LoadProcedure
    from xknxmono.models.intermediate.load_procedures_t import LoadProcedures
    from xknxmono.models.intermediate.master_data_t import MasterData
    from xknxmono.product import Application


def resolve_download_controls(
    application: Application,
    master_data: MasterData | None = None,
    *,
    procedure_type: ProcedureType = ProcedureType.LOAD,
) -> list[object]:
    """Return the flat, ordered list of Load Controls to run for a download.

    ``master_data`` is required for default and merged procedures; without it (or
    without a matching default) the application's own procedure is used.
    """
    style = application.load_procedure_style
    load_procedures = application.load_procedures

    # An application ships only its Load procedure (ProductProcedure) or Load
    # fragments (MergedProcedure). The Unload procedure always comes from the
    # mask version's default in the master data, so never take the application's
    # own procedure for a non-Load request.
    if (
        procedure_type is ProcedureType.LOAD
        and style == LoadProcedureStyle.PRODUCT_PROCEDURE
    ):
        return _flatten(load_procedures)

    default = _default_procedure(
        master_data, application.program.mask_version, procedure_type
    )
    if default is None:
        if procedure_type is not ProcedureType.LOAD:
            raise UnsupportedProcedureError(
                f"no {procedure_type.value} procedure available for mask "
                f"{application.program.mask_version}; master data is required"
            )
        # No default available: fall back to the application's own procedure.
        return _flatten(load_procedures)

    return _splice(default.choice, _fragments_by_merge_id(load_procedures))


def _flatten(load_procedures: LoadProcedures | None) -> list[object]:
    """Concatenate the controls of every application load procedure."""
    if load_procedures is None:
        raise UnsupportedProcedureError("application has no load procedure")
    controls: list[object] = []
    for procedure in load_procedures.load_procedure:
        controls.extend(procedure.choice)
    return controls


def _fragments_by_merge_id(
    load_procedures: LoadProcedures | None,
) -> dict[int, list[object]]:
    """Group application procedure fragments by their merge id."""
    fragments: dict[int, list[object]] = {}
    if load_procedures is None:
        return fragments
    for procedure in load_procedures.load_procedure:
        if procedure.merge_id is None:
            continue
        fragments.setdefault(procedure.merge_id, []).extend(procedure.choice)
    return fragments


def _splice(
    controls: Sequence[object], fragments: dict[int, list[object]]
) -> list[object]:
    """Replace each merge placeholder with the fragment of matching merge id."""
    result: list[object] = []
    for control in controls:
        if isinstance(control, LdCtrlMerge):
            result.extend(fragments.get(control.merge_id, []))
        else:
            result.append(control)
    return result


def _default_procedure(
    master_data: MasterData | None,
    mask_version_id: str,
    procedure_type: ProcedureType,
) -> LoadProcedure | None:
    """Find the mask version's default procedure of the given type.

    Returns the first procedure of ``procedure_type`` (Load), regardless of its
    ProcedureSubType (ap1/all/grp/par/par,grp). ETS/Falcon pick a subtype-specific
    procedure per requested scope; this engine instead resolves one Load procedure
    and applies the download scope afterwards by the interface object each control
    targets (see :mod:`xknxmono.download.scope`). That object-based filtering was
    validated byte-perfect against real hardware (memory-mapped and System B),
    whereas ProcedureSubType/AppliesTo selection was not, so it is deliberately
    the single point that decides full vs partial here.
    """
    if master_data is None or master_data.mask_versions is None:
        return None
    for mask_version in master_data.mask_versions.mask_version:
        if mask_version.id != mask_version_id:
            continue
        for configuration in mask_version.hawk_configuration_data:
            if configuration.procedures is None:
                continue
            for procedure in configuration.procedures.procedure:
                if procedure.procedure_type == procedure_type:
                    return procedure
    return None
