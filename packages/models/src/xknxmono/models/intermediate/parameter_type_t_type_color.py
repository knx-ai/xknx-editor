from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.parameter_type_t_type_color_space import (
    ParameterTypeTypeColorSpace,
)


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
