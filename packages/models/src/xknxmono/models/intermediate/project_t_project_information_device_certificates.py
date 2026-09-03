from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.device_certificate_t import DeviceCertificate


@dataclass(slots=True, kw_only=True)
class ProjectProjectInformationDeviceCertificates:
    class Meta:
        global_type = False

    device_certificate: list[DeviceCertificate] = field(
        default_factory=list,
        metadata={
            "name": "DeviceCertificate",
            "type": "Element",
        },
    )
