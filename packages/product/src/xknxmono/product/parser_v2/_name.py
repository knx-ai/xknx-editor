from __future__ import annotations

import re

_NAME_PLACEHOLDER = re.compile(r"\{\{0(?::[^}]*)?\}\}")


def apply_text_args(text: str, text_args: dict[str, str]) -> str:
    """Substitute {{ArgName}} and {{ArgName:fmt}} placeholders from module text args."""
    for name, value in text_args.items():
        text = re.sub(r"\{\{" + re.escape(name) + r"(?::[^}]*)?\}\}", value, text)
    return text


def fill_name(template: str, name_value: str) -> str:
    """Fill {{0}} / {{0:fallback}} with name_value or the fallback, strip remaining {{...}}."""

    def replace(m: re.Match[str]) -> str:
        if name_value:
            return name_value
        s = m.group(0)
        colon = s.find(":")
        return s[colon + 1 : -2] if colon != -1 else ""

    text = _NAME_PLACEHOLDER.sub(replace, template)
    text = re.sub(r"\{\{[^}]+\}\}", "", text)
    return re.sub(r"\s+", " ", text).strip()
