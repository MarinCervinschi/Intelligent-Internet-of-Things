from dataclasses import dataclass
from typing import Dict, Any
import time
from .generic_message import GenericMessage


@dataclass
class EventMessage(GenericMessage):
    def __repr__(self):
        return super().__repr__()
