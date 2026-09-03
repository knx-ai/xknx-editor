"""Download scope: full download versus a partial parameter/group download.

A partial download runs only the Load Controls that target a given category of
loadable part (KNX Standard v3.0.0, Chapter 3/5/3 "Configuration Procedures",
section 3.5.3 "Load procedure for partial download"), classifying a control by
the interface object it addresses:

- the Address Table, Association Table and Group Object Table objects hold the
  group communication;
- the Application Program object holds the parameters;
- the Device Object and connection/restart controls are framing and always run.

The applies_to marker (``LdCtrlProcType``) is uniform on many products, so the
object a control targets - not applies_to - is what distinguishes a partial
parameter download from a partial group communication download.

This is a deliberate deviation from ETS/Falcon, which evaluate ``AppliesTo`` (and
select a subtype-specific procedure). Object-based scoping was validated
byte-perfect on real hardware (e.g. a partial parameter download on 1.1.74),
whereas an ``AppliesTo``-driven scope was observed to be wrong on that device, so
the object a control addresses is the authoritative signal here.

The classification looks at the object *type* for controls that carry one
(``obj_type``, e.g. the synthesized group-communication table writes use types
1/2/9) and at the interface object *index* otherwise (``obj_idx``/``lsm_idx``).
For our control set these do not collide - group-communication controls always
carry ``obj_type`` and parameter controls carry the Application Program index -
but a hand-built procedure that group-addressed the System B group object at
*index* 3 (rather than type 9) would need an index-to-type map to classify.
"""

from __future__ import annotations

from enum import Enum

# Interface object types (and their conventional indices) that hold group
# communication: address table (1), association table (2), group object
# table (9), group object responder table (also object type 9).
_GROUP_COMMUNICATION_OBJECTS = frozenset({1, 2, 9})
# The addressing tables (address table 1, association table 2) hold the group
# address links. They are group communication but NOT part of the application
# program - programming only the application program leaves them untouched.
_ADDRESSING_OBJECTS = frozenset({1, 2})
# The device object is framing (fingerprint compare) and always runs.
_DEVICE_OBJECT = 0
# The Router object (a line/backbone coupler's filter table) is group-address
# routing: it belongs to GROUP_COMMUNICATION, and the untargeted
# ``LdCtrlClearLCFilterTable`` clears it, so both must scope together (never clear
# without the following write, nor write without the clear).
_ROUTER_OBJECT = 6


class DownloadScope(Enum):
    """Which part of a Load Procedure to execute.

    ``UNLOAD`` is not a partial load: it selects the Unload procedure instead of
    the Load procedure (it removes the application program / resets the Load
    State Machines to Unloaded). The download entry point routes it to the
    ``Unload`` procedure and runs all of its controls.
    """

    FULL = "full"
    PARAMETERS = "par"
    GROUP_COMMUNICATION = "grp"
    APPLICATION = "ap1"
    UNLOAD = "unload"


def control_in_scope(control: object, scope: DownloadScope) -> bool:
    """Return whether a control runs in ``scope``.

    Controls that do not target a loadable part (Connect/Disconnect/Restart/
    Delay and Device Object compares) are framing and always run. Targeted
    controls run only when the object they address belongs to the requested
    category; a full download runs everything.

    - ``GROUP_COMMUNICATION`` runs the address, association and group object
      tables (objects 1/2/9).
    - ``PARAMETERS`` runs only the application program's parameter part (nothing
      that belongs to group communication).
    - ``APPLICATION`` runs the application program: the parameters, the
      application object and the group object (com object descriptor) table, but
      not the address/association tables (the group address links). It is the
      ETS "application program" (``ap1``) download.
    """
    if scope is DownloadScope.FULL or scope is DownloadScope.UNLOAD:
        # UNLOAD runs the Unload procedure's controls in full (they are resolved
        # separately by the download entry point, not filtered by object).
        return True
    target = _target_object(control)
    if target is None or target == _DEVICE_OBJECT:
        return True
    if scope is DownloadScope.GROUP_COMMUNICATION:
        return target in _GROUP_COMMUNICATION_OBJECTS or target == _ROUTER_OBJECT
    if scope is DownloadScope.APPLICATION:
        # Everything except the group address link tables (address/association) and the
        # coupler filter table (group routing, not the application program).
        return target not in _ADDRESSING_OBJECTS and target != _ROUTER_OBJECT
    # PARAMETERS: nothing that belongs to group communication (incl. the filter table).
    return target not in _GROUP_COMMUNICATION_OBJECTS and target != _ROUTER_OBJECT


def _target_object(control: object) -> int | None:
    """The interface object type/index a control addresses, or None if framing.

    ``LdCtrlClearLCFilterTable`` carries no object reference but operates on the coupler's
    Router object (its filter table), so it is classified as that object for scoping - it must
    never run in a scope where the following filter-table write does not, or vice versa."""
    if type(control).__name__ == "LdCtrlClearLcfilterTable":
        return _ROUTER_OBJECT
    obj_type = getattr(control, "obj_type", None)
    if obj_type is not None:
        return obj_type
    lsm_idx = getattr(control, "lsm_idx", None)
    if lsm_idx is not None:
        return lsm_idx
    obj_idx = getattr(control, "obj_idx", None)
    return obj_idx
