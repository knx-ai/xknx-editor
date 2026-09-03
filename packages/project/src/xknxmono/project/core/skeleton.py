"""Seed a new project's baseline state, mirroring what ETS6 creates for a fresh project.

The baseline is *not* undoable, so it's inserted directly (no event): a ``Project`` row
(``ThreeLevel`` group-address style) and installation 0 with a default *backbone* topology
(Area 0 / Line 0 / Segment on the IP medium) and an empty group-address tree.
"""

from uuid import uuid4

from sqlalchemy.orm import Session

from xknxmono.project.core.addressing import GroupAddressStyle
from xknxmono.project.models import Area, Installation, Line, Project, Segment

MEDIUM_IP = "MT-5"
MEDIUM_TP = "MT-0"

DEFAULT_INSTALLATION = 0


def seed_new_project(
    session: Session,
    project_id: str,
    name: str,
    group_address_style: GroupAddressStyle = GroupAddressStyle.THREE_LEVEL,
) -> None:
    """Insert the baseline project + installation 0 with its backbone (Area 0 / Line 0 / IP Segment)."""
    # A stable Guid identifies the project across (re-)exports; ETS expects every project to have
    # one, and rejects the import of a project without it. Generate it once at creation.
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
