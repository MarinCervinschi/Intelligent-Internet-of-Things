import json
from dataclasses import dataclass
from typing import Optional


@dataclass
class GpsLocationDescriptor:
    FILE_LOCATION_PROVIDER = "location_provider_file"
    GPS_LOCATION_PROVIDER = "location_provider_gps"
    NETWORK_LOCATION_PROVIDER = "location_provider_network"

    latitude: float = 0.0
    longitude: float = 0.0
    elevation: Optional[float] = None
    provider: Optional[str] = None

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

