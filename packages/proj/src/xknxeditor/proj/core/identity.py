"""Instance-identity resolution for persisted com-objects.

A com-object instance has two stored, individually lossy forms per row (see
:class:`xknxeditor.proj.models.ComObject`): ``ref_id`` is the application-program definition id
(app-prefixed but module-instance stripped, so every instance of the same module collapses onto one
string), and ``instance_ref_id`` is the raw ETS ``@RefId`` (per-instance, but with no app prefix).

The parser/dynamic UI keys every object by ``ctx.qualify(local_ref)`` — the app program id followed
by the raw ``@RefId``. That qualified form is what the live device, the parameter-driven active set,
and reconciliation targets all speak. Neither stored form equals it on its own, so any layer that
matches identity (display, reconcile, undo, application upgrade) must go through this one function or
it silently collapses distinct module instances onto one another.
"""


def qualified_com_object_ref(
    ref_id: str, instance_ref_id: str, app_program_id: str
) -> str:
    """Reconstruct the app-prefixed, per-instance qualified ref the dynamic UI emits.

    Uses ``instance_ref_id`` (the per-instance raw ``@RefId``), prefixing the app program id when it
    is not already present. Falls back to ``ref_id`` when ``instance_ref_id`` is empty — the case for
    objects created in the editor rather than imported, whose ``ref_id`` is already the qualified id —
    and when ``app_program_id`` is empty: without it the qualified form cannot be reconstructed, so we
    match on the stored ``ref_id`` exactly as the pre-resolver code did. Empty ``app_program_id`` is
    the legacy/non-module case (events serialized before the id was threaded deserialize to ``""``);
    prefixing a bare ``"_"`` there would match nothing and silently delete the surviving rows.
    """
    if not instance_ref_id or not app_program_id:
        return ref_id
    prefix = f"{app_program_id}_"
    return (
        instance_ref_id
        if instance_ref_id.startswith(prefix)
        else f"{prefix}{instance_ref_id}"
    )
