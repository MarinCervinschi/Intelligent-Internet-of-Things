from dataclasses import dataclass
from typing import Dict, Any
from .generic_message import GenericMessage
import time

@dataclass
class CommandMessage(GenericMessage):
    def __repr__(self):
        return super().__repr__()
