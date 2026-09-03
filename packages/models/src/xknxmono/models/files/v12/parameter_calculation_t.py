from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v12.parameter_calculation_t_language import (
    ParameterCalculationLanguage,
)
from xknxmono.models.files.v12.parameter_calculation_t_lparameters import (
    ParameterCalculationLparameters,
)
from xknxmono.models.files.v12.parameter_calculation_t_rparameters import (
    ParameterCalculationRparameters,
)

__NAMESPACE__ = "http://knx.org/xml/project/12"


@dataclass(slots=True, kw_only=True)
class ParameterCalculation:
    """
    :ivar rltransformation: registration-relevant
    :ivar lrtransformation: registration-relevant
    :ivar lparameters:
    :ivar rparameters:
    :ivar id: registration-relevant
    :ivar language: registration-relevant
    :ivar name:
    :ivar internal_description:
    """

    class Meta:
        name = "ParameterCalculation_t"

    rltransformation: str = field(
        metadata={
            "name": "RLTransformation",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
        }
    )
    lrtransformation: str = field(
        metadata={
            "name": "LRTransformation",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
        }
    )
    lparameters: ParameterCalculationLparameters = field(
        metadata={
            "name": "LParameters",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
        }
    )
    rparameters: ParameterCalculationRparameters = field(
        metadata={
            "name": "RParameters",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
        }
    )
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    language: ParameterCalculationLanguage = field(
        metadata={
            "name": "Language",
            "type": "Attribute",
        }
    )
    name: str = field(
        metadata={
            "name": "Name",
            "type": "Attribute",
            "max_length": 50,
        }
    )
    internal_description: None | str = field(
        default=None,
        metadata={
            "name": "InternalDescription",
            "type": "Attribute",
        },
    )
