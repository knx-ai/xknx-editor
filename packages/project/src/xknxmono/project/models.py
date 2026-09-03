"""SQLAlchemy ORM models for a project's SQLite document — one database is one project.

These are the project package's *own* models (no IR import), shaped as a subset of the KNX IR
(`xknxmono.models.intermediate`) so a later `.knxproj` import/export converter is a plain field
mapping. Identity is internal autoincrement integers; ETS `id`/`puid` strings are a boundary
concern, not stored here.

Tree: ``Installation → Area → Line → Segment → Device``; group addresses live in a separate
recursive ``GroupRange`` tree. ``Event`` is the undo/redo history (see :mod:`.core.event_store`);
the live state is the other tables.
"""

import datetime
from typing import Any

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    LargeBinary,
    String,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """SQLAlchemy declarative base for all project ORM models."""


class Project(Base):
    """The single project metadata row for this database."""

    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False, default="")
    group_address_style: Mapped[str] = mapped_column(
        String, nullable=False, default="ThreeLevel"
    )
    # Descriptive metadata carried over from the imported .knxproj (ETS project information).
    guid: Mapped[str] = mapped_column(String, nullable=False, default="")
    created_by: Mapped[str] = mapped_column(Text, nullable=False, default="")
    last_modified: Mapped[str] = mapped_column(String, nullable=False, default="")
    schema_version: Mapped[str] = mapped_column(String, nullable=False, default="")
    tool_version: Mapped[str] = mapped_column(String, nullable=False, default="")
    # ETS protection artifacts carried over verbatim from the imported .knxproj so an export is a
    # loadable project again: the signed knx_master.xml, the project's ".validation" file and its
    # "<pid>.certificate". Empty when the source project had none (e.g. a freshly created one).
    knx_master_xml: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    knx_validation: Mapped[str] = mapped_column(Text, nullable=False, default="")
    knx_certificate: Mapped[str] = mapped_column(Text, nullable=False, default="")
    # The project id (P-XXXX) in the source .knxproj. The certificate/.validation are bound to it,
    # so an export of a protected project must reuse this id.
    original_project_id: Mapped[str] = mapped_column(String, nullable=False, default="")


class Installation(Base):
    """One installation (= IR ``installation_id``, maps to ETS ``N.xml``). ``index`` is user-facing."""

    __tablename__ = "installations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    index: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(Text, nullable=False, default="")

    areas: Mapped[list["Area"]] = relationship(
        back_populates="installation", cascade="all, delete-orphan"
    )
    group_ranges: Mapped[list["GroupRange"]] = relationship(
        back_populates="installation", cascade="all, delete-orphan"
    )
    spaces: Mapped[list["Space"]] = relationship(
        back_populates="installation", cascade="all, delete-orphan"
    )


class Area(Base):
    """A topology area (KNX address bits 12-15)."""

    __tablename__ = "areas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    installation_id: Mapped[int] = mapped_column(
        ForeignKey("installations.id"), nullable=False, index=True
    )
    address: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False, default="")

    installation: Mapped["Installation"] = relationship(back_populates="areas")
    lines: Mapped[list["Line"]] = relationship(
        back_populates="area", cascade="all, delete-orphan"
    )


class Line(Base):
    """A topology line (KNX address bits 8-11). Individual addresses are unique within a line."""

    __tablename__ = "lines"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    area_id: Mapped[int] = mapped_column(
        ForeignKey("areas.id"), nullable=False, index=True
    )
    address: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False, default="")
    # Coupler "route regardless" pass-through addresses (ETS ``AdditionalGroupAddresses``), stored as
    # comma-separated raw integer addresses. Empty when none. (KNX PR #651 project-side field.)
    additional_group_addresses: Mapped[str] = mapped_column(
        Text, nullable=False, default=""
    )

    area: Mapped["Area"] = relationship(back_populates="lines")
    segments: Mapped[list["Segment"]] = relationship(
        back_populates="line", cascade="all, delete-orphan"
    )


class Segment(Base):
    """A media segment within a line (carries the medium type, e.g. ``MT-0`` TP / ``MT-5`` IP)."""

    __tablename__ = "segments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    line_id: Mapped[int] = mapped_column(
        ForeignKey("lines.id"), nullable=False, index=True
    )
    number: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    medium_type: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False, default="")

    line: Mapped["Line"] = relationship(back_populates="segments")
    devices: Mapped[list["Device"]] = relationship(
        back_populates="segment", cascade="all, delete-orphan"
    )


class Device(Base):
    """A device instance. ``address`` is the 0-255 individual-address octet (unique within its line).

    ``product_ref_id`` is the catalog product (what was bought); ``hardware2program_ref_id`` is the
    loaded ``HP-…`` program (= catalog ``HardwareProgram.id``), through which the application —
    and thus parameter/com-object definitions — is resolved.
    """

    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    segment_id: Mapped[int] = mapped_column(
        ForeignKey("segments.id"), nullable=False, index=True
    )
    address: Mapped[int | None] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(Text, nullable=False, default="")
    product_ref_id: Mapped[str] = mapped_column(String, nullable=False)
    hardware2program_ref_id: Mapped[str | None] = mapped_column(String)
    # The building/room (Space) the device is placed in, if any.
    space_id: Mapped[int | None] = mapped_column(ForeignKey("spaces.id"), index=True)
    # Descriptive metadata carried over from the imported .knxproj (for display without a catalog).
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    order_number: Mapped[str] = mapped_column(String, nullable=False, default="")
    hardware_name: Mapped[str] = mapped_column(Text, nullable=False, default="")
    product_name: Mapped[str] = mapped_column(Text, nullable=False, default="")
    manufacturer_name: Mapped[str] = mapped_column(Text, nullable=False, default="")
    # Commissioning state (ETS's per-device "loaded" ticks + serial / last download), carried on the
    # DeviceInstance in a .knxproj. Round-tripped on import/export and updated after programming.
    serial_number: Mapped[str] = mapped_column(String, nullable=False, default="")
    last_download: Mapped[str | None] = mapped_column(String)
    individual_address_loaded: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    application_program_loaded: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    communication_part_loaded: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    medium_config_loaded: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    parameters_loaded: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )

    segment: Mapped["Segment"] = relationship(back_populates="devices")
    space: Mapped["Space | None"] = relationship(back_populates="devices")
    module_instances: Mapped[list["ModuleInstance"]] = relationship(
        back_populates="device", cascade="all, delete-orphan"
    )
    parameters: Mapped[list["Parameter"]] = relationship(
        back_populates="device", cascade="all, delete-orphan"
    )
    com_objects: Mapped[list["ComObject"]] = relationship(
        back_populates="device", cascade="all, delete-orphan"
    )


class ModuleInstance(Base):
    """A module instance: ``instance_id`` is the key used during eval (e.g. ``M-100_MI-1``);
    ``ref_id`` is the module definition ref (e.g. ``M-100``). Only top-level instances are stored."""

    __tablename__ = "module_instances"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    device_id: Mapped[int] = mapped_column(
        ForeignKey("devices.id"), nullable=False, index=True
    )
    instance_id: Mapped[str] = mapped_column(String, nullable=False)
    ref_id: Mapped[str] = mapped_column(String, nullable=False)

    device: Mapped["Device"] = relationship(back_populates="module_instances")


class Parameter(Base):
    """A parameter instance: ``ref_id`` points into the application's parameter refs; ``value`` is set."""

    __tablename__ = "parameters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    device_id: Mapped[int] = mapped_column(
        ForeignKey("devices.id"), nullable=False, index=True
    )
    ref_id: Mapped[str] = mapped_column(String, nullable=False)
    value: Mapped[str] = mapped_column(String, nullable=False, default="")

    device: Mapped["Device"] = relationship(back_populates="parameters")


class ComObject(Base):
    """A com-object instance ref: ``ref_id`` points into the application's com-object refs.

    ``channel_id`` references the ApplicationProgramChannel the instance lives in (``None`` when it
    is in the channel-independent block). The flags are *overrides* (``None`` = inherit from the
    product/application definition; a value forces ``Enabled``/``Disabled``). Defaults and lock state
    live on the product, not here.
    """

    __tablename__ = "com_objects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    device_id: Mapped[int] = mapped_column(
        ForeignKey("devices.id"), nullable=False, index=True
    )
    ref_id: Mapped[str] = mapped_column(String, nullable=False)
    channel_id: Mapped[str | None] = mapped_column(String)

    read_flag: Mapped[bool | None] = mapped_column(Boolean)
    write_flag: Mapped[bool | None] = mapped_column(Boolean)
    communication_flag: Mapped[bool | None] = mapped_column(Boolean)
    transmit_flag: Mapped[bool | None] = mapped_column(Boolean)
    update_flag: Mapped[bool | None] = mapped_column(Boolean)
    read_on_init_flag: Mapped[bool | None] = mapped_column(Boolean)

    device: Mapped["Device"] = relationship(back_populates="com_objects")
    links: Mapped[list["ComObjectLink"]] = relationship(
        back_populates="com_object", cascade="all, delete-orphan"
    )


class GroupRange(Base):
    """A node in the group-address range tree (recursive: main → middle in ThreeLevel)."""

    __tablename__ = "group_ranges"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    installation_id: Mapped[int] = mapped_column(
        ForeignKey("installations.id"), nullable=False, index=True
    )
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("group_ranges.id"), index=True
    )
    range_start: Mapped[int] = mapped_column(Integer, nullable=False)
    range_end: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False, default="")
    # Pass through line/backbone couplers unconditionally (ETS ``Unfiltered``). (KNX PR #651.)
    unfiltered: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    installation: Mapped["Installation"] = relationship(back_populates="group_ranges")
    parent: Mapped["GroupRange | None"] = relationship(
        back_populates="children", remote_side="GroupRange.id"
    )
    children: Mapped[list["GroupRange"]] = relationship(
        back_populates="parent", cascade="all, delete-orphan"
    )
    group_addresses: Mapped[list["GroupAddress"]] = relationship(
        back_populates="group_range", cascade="all, delete-orphan"
    )


class GroupAddress(Base):
    """A group address inside a (leaf) group range."""

    __tablename__ = "group_addresses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    group_range_id: Mapped[int] = mapped_column(
        ForeignKey("group_ranges.id"), nullable=False, index=True
    )
    address: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False, default="")
    datapoint_type: Mapped[str | None] = mapped_column(String)
    # Descriptive metadata carried over from the imported .knxproj.
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    comment: Mapped[str] = mapped_column(Text, nullable=False, default="")
    data_secure: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    # Pass through line/backbone couplers unconditionally (ETS ``Unfiltered``). (KNX PR #651.)
    unfiltered: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    group_range: Mapped["GroupRange"] = relationship(back_populates="group_addresses")
    links: Mapped[list["ComObjectLink"]] = relationship(
        back_populates="group_address", cascade="all, delete-orphan"
    )
    function_links: Mapped[list["FunctionGroupAddress"]] = relationship(
        back_populates="group_address", cascade="all, delete-orphan"
    )


class ComObjectLink(Base):
    """A link between a com-object instance and a group address. ``is_sending`` marks the (single)
    group address this object transmits to; the rest are receive-only. (The IR encodes this
    positionally as the first entry of its ``Links`` list; we store the bit directly.)"""

    __tablename__ = "com_object_links"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    com_object_id: Mapped[int] = mapped_column(
        ForeignKey("com_objects.id"), nullable=False, index=True
    )
    group_address_id: Mapped[int] = mapped_column(
        ForeignKey("group_addresses.id"), nullable=False, index=True
    )
    is_sending: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    com_object: Mapped["ComObject"] = relationship(back_populates="links")
    group_address: Mapped["GroupAddress"] = relationship(back_populates="links")


class Space(Base):
    """A node in the building/location tree (recursive: building → floor → room → …), imported
    from the ETS project's locations. ``space_type`` is the ETS type string (e.g. ``Building``,
    ``Floor``, ``Room``). ``order`` preserves the project's original sibling order."""

    __tablename__ = "spaces"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    installation_id: Mapped[int] = mapped_column(
        ForeignKey("installations.id"), nullable=False, index=True
    )
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("spaces.id"), index=True)
    space_type: Mapped[str] = mapped_column(String, nullable=False, default="")
    name: Mapped[str] = mapped_column(Text, nullable=False, default="")
    number: Mapped[str] = mapped_column(String, nullable=False, default="")
    usage_text: Mapped[str] = mapped_column(Text, nullable=False, default="")
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    installation: Mapped["Installation"] = relationship(back_populates="spaces")
    parent: Mapped["Space | None"] = relationship(
        back_populates="children", remote_side="Space.id"
    )
    children: Mapped[list["Space"]] = relationship(
        back_populates="parent", cascade="all, delete-orphan"
    )
    devices: Mapped[list["Device"]] = relationship(back_populates="space")
    functions: Mapped[list["Function"]] = relationship(
        back_populates="space", cascade="all, delete-orphan"
    )


class Function(Base):
    """A function assigned to a space (ETS ``Function``): a named grouping of group addresses by
    role (e.g. a light's switch/status/dimming addresses)."""

    __tablename__ = "functions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    space_id: Mapped[int] = mapped_column(
        ForeignKey("spaces.id"), nullable=False, index=True
    )
    function_type: Mapped[str] = mapped_column(String, nullable=False, default="")
    name: Mapped[str] = mapped_column(Text, nullable=False, default="")
    usage_text: Mapped[str] = mapped_column(Text, nullable=False, default="")
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    space: Mapped["Space"] = relationship(back_populates="functions")
    group_addresses: Mapped[list["FunctionGroupAddress"]] = relationship(
        back_populates="function", cascade="all, delete-orphan"
    )


class FunctionGroupAddress(Base):
    """A group address referenced by a function, with its ``role`` within that function."""

    __tablename__ = "function_group_addresses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    function_id: Mapped[int] = mapped_column(
        ForeignKey("functions.id"), nullable=False, index=True
    )
    group_address_id: Mapped[int] = mapped_column(
        ForeignKey("group_addresses.id"), nullable=False, index=True
    )
    role: Mapped[str] = mapped_column(String, nullable=False, default="")

    function: Mapped["Function"] = relationship(back_populates="group_addresses")
    group_address: Mapped["GroupAddress"] = relationship(
        back_populates="function_links"
    )


class Event(Base):
    """The undo/redo history. ``data`` is the serialized command payload (incl. before-values)."""

    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(String, nullable=False)
    data: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    reverted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
