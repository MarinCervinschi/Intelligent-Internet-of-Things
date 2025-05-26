from dataclasses import dataclass
from typing import Dict, Any
from .generic_message import GenericMessage


@dataclass
class ControlMessage(GenericMessage):
    def __repr__(self):
        return super().__repr__()
