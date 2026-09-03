from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v20.parameter_calculation_t_language import (
    ParameterCalculationLanguage,
)
from xknxmono.models.files.v20.parameter_calculation_t_lparameters import (
    ParameterCalculationLparameters,
)
from xknxmono.models.files.v20.parameter_calculation_t_rparameters import (
    ParameterCalculationRparameters,
)

__NAMESPACE__ = "http://knx.org/xml/project/20"


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
    :ivar rltransformation_func: registration-relevant
    :ivar rltransformation_parameters: registration-relevant
    :ivar lrtransformation_func: registration-relevant
    :ivar lrtransformation_parameters: registration-relevant
    """

    class Meta:
        name = "ParameterCalculation_t"

    rltransformation: None | str = field(
        default=None,
        metadata={
            "name": "RLTransformation",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/20",
        },
    )
    lrtransformation: None | str = field(
        default=None,
        metadata={
            "name": "LRTransformation",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/20",
        },
    )
    lparameters: ParameterCalculationLparameters = field(
        metadata={
            "name": "LParameters",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/20",
        }
    )
    rparameters: ParameterCalculationRparameters = field(
        metadata={
            "name": "RParameters",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/20",
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
    rltransformation_func: None | str = field(
        default=None,
        metadata={
            "name": "RLTransformationFunc",
            "type": "Attribute",
        },
    )
    rltransformation_parameters: None | str = field(
        default=None,
        metadata={
            "name": "RLTransformationParameters",
            "type": "Attribute",
        },
    )
    lrtransformation_func: None | str = field(
        default=None,
        metadata={
            "name": "LRTransformationFunc",
            "type": "Attribute",
        },
    )
    lrtransformation_parameters: None | str = field(
        default=None,
        metadata={
            "name": "LRTransformationParameters",
            "type": "Attribute",
        },
    )
