"""Pydantic response schemas for the catalog HTTP API endpoints.

All schemas that map to ORM models use ``model_config = {"from_attributes": True}``
so FastAPI can call ``model_validate`` automatically when a ``response_model`` is set.
"""

from __future__ import annotations

import datetime

from pydantic import BaseModel, field_validator

from xknxmono.catalog.models import HardwareProgramMediumType


class ManufacturerResponse(BaseModel):
    """API response schema for a KNX manufacturer."""

    id: str
    name: str | None
    model_config = {"from_attributes": True}


class HardwareProgramResponse(BaseModel):
    """API response schema for a hardware program, including its medium types and linked application."""

    model_config = {"from_attributes": True}

    class Application(BaseModel):
        """API response schema for an ETS application program."""

        model_config = {"from_attributes": True}
        id: str
        name: str
        application_number: int | None
        application_version: int | None
        mask_version: str | None
        is_secure_enabled: bool | None

    id: str
    hardware_id: str
    medium_types: list[str]
    registration_status: str | None
    registration_number: str | None
    registration_date: datetime.date | None
    application: HardwareProgramResponse.Application | None

    @field_validator("medium_types", mode="before")
    @classmethod
    def _flatten_medium_types(cls, v: list[HardwareProgramMediumType]) -> list[str]:
        """Flatten the ORM ``HardwareProgramMediumType`` relationship into a list of strings."""
        return [item.medium_type for item in v]


HardwareProgramResponse.model_rebuild()


class HardwareResponse(BaseModel):
    """API response schema for a hardware item, including all its associated programs."""

    id: str
    manufacturer_id: str
    name: str | None
    order_number: str | None
    description: str | None
    is_rail_mounted: bool | None
    width_mm: float | None
    serial_number: str | None
    version_number: int | None
    bus_current: float | None
    has_application_program: bool | None
    is_coupler: bool | None
    is_power_supply: bool | None
    is_ip_enabled: bool | None
    no_download_without_plugin: bool | None
    default_language: str | None
    programs: list[HardwareProgramResponse]
    model_config = {"from_attributes": True}


class CatalogSectionResponse(BaseModel):
    """API response schema for a catalog section node, with nested children."""

    id: str
    name: str
    number: str | None
    manufacturer_id: str
    parent_id: str | None
    children: list[CatalogSectionResponse] = []
