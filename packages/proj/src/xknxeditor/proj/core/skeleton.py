"""Lay down a new project's baseline, matching a fresh project's starting state.

The baseline is not undoable, so it goes in directly (no event): a ``Project`` row (``ThreeLevel``
style) plus installation 0 with a default *backbone* topology (Area 0 / Line 0 / IP-medium segment)
and an empty group-address tree.
"""

from uuid import uuid4

from sqlalchemy.orm import Session

from xknxeditor.proj.core.addressing import GroupAddressStyle
from xknxeditor.proj.models import Area, Installation, Line, Project, Segment

MEDIUM_IP = "MT-5"
MEDIUM_TP = "MT-0"

DEFAULT_INSTALLATION = 0


def seed_new_project(
    session: Session,
    project_id: str,
    name: str,
    group_address_style: GroupAddressStyle = GroupAddressStyle.THREE_LEVEL,
) -> None:
    """Add the baseline project plus installation 0 and its backbone (Area 0 / Line 0 / IP segment)."""
    # A stable Guid identifies the project across (re-)exports; the importer expects every project
    # to have one, and rejects a project without it. Generate it once at creation.
    session.add(
        Project(
            id=project_id,
            name=name,
            group_address_style=group_address_style,
            guid=str(uuid4()),
        )
    )
    installation = Installation(index=DEFAULT_INSTALLATION, name="")
    installation.areas.append(
        Area(
            address=0,
            lines=[
                Line(
                    address=0,
                    segments=[Segment(number=0, medium_type=MEDIUM_IP)],
                )
            ],
        )
    )
    session.add(installation)
    session.commit()
