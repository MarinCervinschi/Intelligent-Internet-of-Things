from dataclasses import dataclass

@dataclass
class TrafficEventDescriptor:
    JAM_TRAFFIC_EVENT = "jam_traffic_event"

    type: str = None
    latitude: float = 0.0
    longitude: float = 0.0
    timestamp: int = None

