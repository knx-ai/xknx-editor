from __future__ import annotations

import json

import dukpy


def _coerce(s: str) -> int | float | str:
    try:
        return int(s)
    except ValueError:
        pass
    try:
        return float(s)
    except ValueError:
        pass
    return s


def _to_js_literal(s: str) -> str:
    return json.dumps(_coerce(s))


def _read_js_var(interp: dukpy.JSInterpreter, expr: str) -> str | None:
    try:
        v = interp.evaljs(expr)  # type: ignore[union-attr]
    except Exception:
        return None
    if v is None:
        return None
    # dukpy returns JS numbers as Python floats; convert whole numbers to int strings
    if isinstance(v, (int, float)):
        fv = float(v)
        return str(int(fv)) if fv == int(fv) else str(fv)
    return str(v)


def eval_inline(
    code: str, inputs: dict[str, str], output_names: list[str]
) -> dict[str, str]:
    interp = dukpy.JSInterpreter()
    for name, val in inputs.items():
        interp.evaljs(f"var {name} = {_to_js_literal(val)};")  # type: ignore[union-attr]
    for name in output_names:
        if name not in inputs:
            interp.evaljs(f"var {name};")  # type: ignore[union-attr]
    interp.evaljs(code)  # type: ignore[union-attr]
    return {n: v for n in output_names if (v := _read_js_var(interp, n)) is not None}


def eval_named_func(
    app_script: str,
    func_name: str,
    func_params: str | None,
    inputs: dict[str, str],
    output_names: list[str],
) -> dict[str, str]:
    interp = dukpy.JSInterpreter()
    interp.evaljs(app_script)  # type: ignore[union-attr]
    input_obj = json.dumps({k: _coerce(v) for k, v in inputs.items()})
    output_obj = json.dumps({k: None for k in output_names})
    context_obj = func_params or "{}"
    interp.evaljs(  # type: ignore[union-attr]
        f"var __i={input_obj};var __o={output_obj};var __c={context_obj};{func_name}(__i,__o,__c);"
    )
    return {
        n: v
        for n in output_names
        if (v := _read_js_var(interp, f"__o.{n}")) is not None
    }
