from __future__ import annotations

from xknxmono.models.intermediate.parameter_calculation_t import ParameterCalculation
from xknxmono.models.intermediate.parameter_calculation_t_language import (
    ParameterCalculationLanguage,
)

from ._js import eval_inline, eval_named_func


def evaluate_lr(
    calc: ParameterCalculation, l_values: dict[str, str], script: str | None = None
) -> dict[str, str]:
    """Evaluate L→R transformation. l_values: {alias_name: value}. Returns {alias_name: value} for R-params."""
    if calc.language == ParameterCalculationLanguage.VBSCRIPT:
        raise NotImplementedError(f"VBScript calculation {calc.id!r}")
    r_names = [pr.alias_name or pr.ref_id for pr in calc.rparameters.parameter_ref_ref]
    if calc.lrtransformation_func:
        assert script is not None, (
            f"calc {calc.id!r} has LRTransformationFunc but no Script block"
        )
        return eval_named_func(
            script,
            calc.lrtransformation_func,
            calc.lrtransformation_parameters,
            l_values,
            r_names,
        )
    if calc.lrtransformation:
        return eval_inline(calc.lrtransformation, l_values, r_names)
    return {}


def evaluate_rl(
    calc: ParameterCalculation, r_values: dict[str, str], script: str | None = None
) -> dict[str, str]:
    """Evaluate R→L transformation. r_values: {alias_name: value}. Returns {alias_name: value} for L-params."""
    if calc.language == ParameterCalculationLanguage.VBSCRIPT:
        raise NotImplementedError(f"VBScript calculation {calc.id!r}")
    l_names = [pr.alias_name or pr.ref_id for pr in calc.lparameters.parameter_ref_ref]
    if calc.rltransformation_func:
        assert script is not None, (
            f"calc {calc.id!r} has RLTransformationFunc but no Script block"
        )
        return eval_named_func(
            script,
            calc.rltransformation_func,
            calc.rltransformation_parameters,
            r_values,
            l_names,
        )
    if calc.rltransformation:
        return eval_inline(calc.rltransformation, r_values, l_names)
    return {}
