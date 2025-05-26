from dataclasses import dataclass, asdict
from typing import Generic, TypeVar, Any
import time
import json

T = TypeVar("T")


@dataclass
class TelemetryMessage(Generic[T]):
    type: str
    data_value: T
    timestamp: int = None

    def __post_init__(self):
        self.timestamp = self.timestamp or int(time.time() * 1000)
        if not self.type:
            raise ValueError("Il tipo non può essere vuoto")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
    
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)
    
