from dataclasses import dataclass
from datetime import datetime


@dataclass
class Fz44Tender:
    number: str
    publish_in_eis: datetime | None  # publishDTInEIS


@dataclass
class Fz44tenderWithUrl(Fz44Tender):
    xml_url: str

    def dict(self):
        return dict(
            number=self.number,
            publish_in_eis=self.publish_in_eis.isoformat() if self.publish_in_eis else None,
            xml_url=self.xml_url,
        )
