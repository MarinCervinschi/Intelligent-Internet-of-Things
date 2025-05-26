from abc import ABC
from dataclasses import dataclass, field
from typing import Dict, Any
import time
import json


@dataclass
class GenericMessage(ABC):
    type: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: int = field(default_factory=lambda: int(time.time() * 1000))

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)