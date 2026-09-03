from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.device_certificate_t import DeviceCertificate

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class ProjectProjectInformationDeviceCertificates:
    class Meta:
        global_type = False

    device_certificate: list[DeviceCertificate] = field(
        default_factory=list,
        metadata={
            "name": "DeviceCertificate",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/23",
            "min_occurs": 1,
        },
    )
