from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v20.parameter_type_t_type_color_space import (
    ParameterTypeTypeColorSpace,
)

__NAMESPACE__ = "http://knx.org/xml/project/20"


@dataclass(slots=True, kw_only=True)
class ParameterTypeTypeColor:
    """
    :ivar space: registration-relevant
    """

    class Meta:
        global_type = False

    space: ParameterTypeTypeColorSpace = field(
        metadata={
            "name": "Space",
            "type": "Attribute",
        }
    )
