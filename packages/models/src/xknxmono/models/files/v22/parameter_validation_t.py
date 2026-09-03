from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v22.parameter_validation_t_parameters import (
    ParameterValidationParameters,
)

__NAMESPACE__ = "http://knx.org/xml/project/22"


@dataclass(slots=True, kw_only=True)
class ParameterValidation:
    """
    :ivar parameters:
    :ivar id: registration-relevant
    :ivar name:
    :ivar internal_description:
    :ivar validation_func: registration-relevant
    :ivar validation_parameters: registration-relevant
    """

    class Meta:
        name = "ParameterValidation_t"

    parameters: ParameterValidationParameters = field(
        metadata={
            "name": "Parameters",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/22",
        }
    )
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    name: str = field(
        metadata={
            "name": "Name",
            "type": "Attribute",
            "max_length": 255,
        }
    )
    internal_description: None | str = field(
        default=None,
        metadata={
            "name": "InternalDescription",
            "type": "Attribute",
        },
    )
    validation_func: str = field(
        metadata={
            "name": "ValidationFunc",
            "type": "Attribute",
        }
    )
    validation_parameters: None | str = field(
        default=None,
        metadata={
            "name": "ValidationParameters",
            "type": "Attribute",
        },
    )
