"""Extract the converter RSA key from a user's KNX signing assembly.

The genuine signing key is deliberately not shipped. A user who has ETS installed can extract it from
their own ``Knx.Ets.XmlSigning.dll`` and feed it to :func:`knxproj_signing.set_signing_key`, so
exports are signed ETS-valid without the key ever living in this source tree. The key is the same
across ETS 5.7 / 6.x, so any installed version works.

Extraction runs the assembly's converter-key accessor by reflection (see ``_extract.cs``) on a
.NET runtime that provides ``RSACryptoServiceProvider``:

- **.NET / CoreCLR** (``dotnet`` CLI) — preferred: loads obfuscated ETS assemblies (5.7, 6.3) that
  Mono's stricter metadata loader rejects.
- **Mono** (``mono`` + ``mcs``) — works for unobfuscated builds (e.g. ETS 6.4).
- **pythonnet** in-process on Windows (native .NET Framework).

If no runtime is available a :class:`KeyExtractionError` explains how to enable one. Nothing here is
bundled; extraction is entirely optional and the caller falls back to the placeholder key.

This builds on the approach of OpenKNXproducer (https://github.com/OpenKNX/OpenKNXproducer), which
drives the same ``Knx.Ets.XmlSigning`` assembly for KNX product signing.
"""

from __future__ import annotations

import base64
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

_EXTRACT_CS = Path(__file__).with_name("_extract.cs")
_TIMEOUT = 120.0

#: The assembly file that carries the signing key.
DLL_NAME = "Knx.Ets.XmlSigning.dll"


class KeyExtractionError(RuntimeError):
    """Raised when the converter key cannot be extracted from the assembly."""


def default_dll_path() -> str:
    """Return the ``Knx.Ets.XmlSigning.dll`` in the first detected ETS install, or ``""``.

    Used to point the file picker at the right place when ETS is installed locally.
    """
    from xknxeditor.proj.core._dll_signer import ETS_ROOTS

    for root in ETS_ROOTS:
        candidate = Path(root) / DLL_NAME
        if candidate.is_file():
            return str(candidate)
    return ""


def dotnet_available() -> bool:
    """Whether the ``dotnet`` CLI (SDK) is on PATH."""
    return shutil.which("dotnet") is not None


def mono_available() -> bool:
    """Whether a Mono toolchain (``mono`` + ``mcs``) is on PATH."""
    return shutil.which("mono") is not None and shutil.which("mcs") is not None


def pythonnet_available() -> bool:
    """Whether in-process .NET (pythonnet) is usable on this platform (Windows)."""
    if sys.platform != "win32":
        return False
    try:
        import pythonnet  # type: ignore[import-not-found]  # noqa: F401
    except ImportError:
        return False
    return True


def extraction_backend() -> str | None:
    """Return the backend that would be used, or ``None`` if none is available.

    Order: ``"dotnet"`` (widest coverage) > ``"mono"`` > ``"pythonnet"``.
    """
    if dotnet_available():
        return "dotnet"
    if mono_available():
        return "mono"
    if pythonnet_available():
        return "pythonnet"
    return None


def _parse_output(text: str) -> tuple[int, int, int]:
    """Parse the ``MOD=``/``EXP=``/``D=`` base64 lines into ``(modulus, private_exp, public_exp)``."""
    fields: dict[str, int] = {}
    for key in ("MOD", "EXP", "D"):
        m = re.search(rf"^{key}=(\S+)$", text, re.MULTILINE)
        if not m:
            raise KeyExtractionError(f"extractor output missing {key}:\n{text}")
        fields[key] = int.from_bytes(base64.b64decode(m.group(1)), "big")
    return fields["MOD"], fields["D"], fields["EXP"]


def _run(cmd: list[str], cwd: str | None = None) -> subprocess.CompletedProcess[str]:
    env = {"DOTNET_CLI_TELEMETRY_OPTOUT": "1", "DOTNET_NOLOGO": "1"}
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=_TIMEOUT,
        cwd=cwd,
        env={**os.environ, **env},
    )


def _dotnet_tfm() -> str:
    """Target framework matching the installed SDK major version (e.g. ``net10.0``)."""
    try:
        out = _run(["dotnet", "--version"]).stdout.strip()
        major = int(out.split(".", 1)[0])
        return f"net{major}.0"
    except (ValueError, OSError, subprocess.SubprocessError):
        return "net8.0"


def _extract_via_dotnet(dll: Path) -> tuple[int, int, int]:
    tfm = _dotnet_tfm()
    proj_dir = Path(tempfile.gettempdir()) / "xknx_keyextract_dotnet"
    proj_dir.mkdir(exist_ok=True)
    csproj = proj_dir / "xknxkeyx.csproj"
    csproj.write_text(
        '<Project Sdk="Microsoft.NET.Sdk">\n'
        "  <PropertyGroup>\n"
        "    <OutputType>Exe</OutputType>\n"
        f"    <TargetFramework>{tfm}</TargetFramework>\n"
        "    <Nullable>disable</Nullable>\n"
        "    <ImplicitUsings>disable</ImplicitUsings>\n"
        "    <AssemblyName>xknxkeyx</AssemblyName>\n"
        "    <EnableDefaultCompileItems>false</EnableDefaultCompileItems>\n"
        "  </PropertyGroup>\n"
        "  <ItemGroup>\n"
        f'    <Compile Include="{_EXTRACT_CS}" />\n'
        "  </ItemGroup>\n"
        "</Project>\n",
        encoding="utf-8",
    )
    build = _run(
        ["dotnet", "build", "-c", "Release", "-v", "q", "-nologo", str(csproj)]
    )
    if build.returncode != 0:
        raise KeyExtractionError(
            f"dotnet build failed:\n{build.stdout or build.stderr}"
        )
    app = proj_dir / "bin" / "Release" / tfm / "xknxkeyx.dll"
    # Run from the DLL's directory so its sibling assemblies resolve.
    proc = _run(["dotnet", str(app), str(dll)], cwd=str(dll.parent))
    if proc.returncode != 0:
        raise KeyExtractionError(f"extractor failed:\n{proc.stderr or proc.stdout}")
    return _parse_output(proc.stdout)


def _extract_via_mono(dll: Path) -> tuple[int, int, int]:
    exe = Path(tempfile.gettempdir()) / "xknx_keyextract.exe"
    build = _run(["mcs", f"-out:{exe}", str(_EXTRACT_CS)])
    if build.returncode != 0:
        raise KeyExtractionError(
            f"mcs failed to compile the extractor:\n{build.stderr}"
        )
    proc = _run(["mono", str(exe), str(dll)], cwd=str(dll.parent))
    if proc.returncode != 0:
        # Mono can abort with a native crash dump on obfuscated ETS builds (5.7, 6.3). Keep the
        # message short and steer the user to install the .NET SDK, which loads those.
        detail = "\n".join((proc.stderr or proc.stdout or "").strip().splitlines()[:3])
        raise KeyExtractionError(
            "Mono could not load this assembly (obfuscated ETS builds need the .NET SDK — "
            f"install `dotnet`).\n{detail}"
        )
    return _parse_output(proc.stdout)


def _extract_via_pythonnet(dll: Path) -> tuple[int, int, int]:
    # Everything from the CLR is dynamically typed; bind each symbol to Any so member access is allowed.
    import clr as _clr_mod  # type: ignore[import-not-found]
    import System as _system  # type: ignore[import-not-found]
    import System.Reflection as _reflection  # type: ignore[import-not-found]

    clr: Any = _clr_mod
    system: Any = _system
    reflection: Any = _reflection

    clr.AddReference(str(dll))
    asm: Any = reflection.Assembly.LoadFrom(str(dll))
    t: Any = asm.GetType("Knx.Ets.XmlSigning.XmlSigning")
    if t is None:
        raise KeyExtractionError("type Knx.Ets.XmlSigning.XmlSigning not found")
    bf: Any = reflection.BindingFlags
    flags = bf.NonPublic | bf.Public | bf.Static
    m: Any = t.GetMethod("GetConverterRsaKey", flags)
    if m is None:
        # Obfuscated builds rename it: first static, zero-arg method returning an RSA key.
        for mm in t.GetMethods(flags):
            try:
                if mm.GetParameters().Length == 0 and str(
                    mm.ReturnType.Name
                ).startswith("RSA"):
                    m = mm
                    break
            except Exception:
                continue
    if m is None:
        raise KeyExtractionError("no converter-key accessor found")
    rsa: Any = m.Invoke(None, system.Array[system.Object](0))
    p: Any = rsa.ExportParameters(True)

    def _to_int(b: Any) -> int:
        return int.from_bytes(bytes(b), "big")

    return _to_int(p.Modulus), _to_int(p.D), _to_int(p.Exponent)


def extract_converter_key(dll_path: str | Path) -> tuple[int, int, int]:
    """Extract ``(modulus, private_exponent, public_exponent)`` from ``dll_path``.

    Uses .NET (``dotnet``) if available, else Mono, else in-process pythonnet on Windows. Raises
    :class:`KeyExtractionError` if the file is missing or no .NET runtime is available.
    """
    dll = Path(dll_path)
    if not dll.is_file():
        raise KeyExtractionError(f"assembly not found: {dll}")
    backend = extraction_backend()
    if backend == "dotnet":
        return _extract_via_dotnet(dll)
    if backend == "mono":
        return _extract_via_mono(dll)
    if backend == "pythonnet":
        return _extract_via_pythonnet(dll)
    raise KeyExtractionError(
        "no .NET runtime available to read the assembly. Install the .NET SDK "
        "(`brew install dotnet-sdk` on macOS, your package manager on Linux) or run on Windows "
        "with pythonnet installed."
    )
